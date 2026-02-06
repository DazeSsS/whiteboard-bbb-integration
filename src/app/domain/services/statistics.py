import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import xmltodict
from lxml import html
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import StatsModule
from app.data.repositories import MeetingRepository, StatsModuleRepository
from app.domain.exceptions import NotFoundException
from config import settings

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(
        self,
        session: AsyncSession,
        meeting_repo: MeetingRepository,
        stats_module_repo: StatsModuleRepository,
    ):
        self.session = session
        self.meeting_repo = meeting_repo
        self.stats_module_repo = stats_module_repo

    async def create_stats_module(
        self,
        name: str,
    ):
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                url=f'{settings.WHITEBOARD_BASE_URL}/api/stats/module/create',
                json={'moduleName': name},
            )
            data = response.json()

        async with self.session.begin():
            new_module = StatsModule(
                id=data.get('moduleId'),
                name=data.get('moduleName'),
                token=data.get('token'),
            )
            self.stats_module_repo.add(new_module)
            return new_module

    async def get_current_metrics(
        self,
    ):
        stats_module = await self.stats_module_repo.get_first_module()
        if stats_module is None:
            logger.warning('Stats Module does not exist')
            raise NotFoundException(entity_name='StatsModule')

        token = stats_module.token

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(
                    url=f'{settings.WHITEBOARD_BASE_URL}/api/stats/module/metrics',
                    headers={'X-Module-Token': token},
                )
                response.raise_for_status()
                return response.json()
            except Exception:
                logger.exception('Error while getting current metrics')

    async def update_metrics(
        self,
        metrics: dict,
    ):
        stats_module = await self.stats_module_repo.get_first_module()
        if stats_module is None:
            logger.warning('Stats Module does not exist')
            raise NotFoundException(entity_name='StatsModule')

        token = stats_module.token

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.put(
                url=f'{settings.WHITEBOARD_BASE_URL}/api/stats/module/metrics',
                json=metrics,
                headers={'X-Module-Token': token},
            )

            return response.json()

    async def process_stats(
        self,
        internal_meeting_id: str,
    ) -> dict:
        stats_module = await self.stats_module_repo.get_first_module()
        if stats_module is None:
            logger.warning('Stats Module does not exist')
            raise NotFoundException(entity_name='StatsModule')

        events_path = await self._get_events_path(
            internal_meeting_id=internal_meeting_id,
        )
        if events_path is None:
            logger.warning(
                'Events file for meeting %r does not exist',
                internal_meeting_id,
            )
            return

        with open(events_path, encoding='utf-8') as file:
            events_xml = file.read()

        events_dict = xmltodict.parse(events_xml)
        meeting_data = await self._parse_events(events_dict=events_dict)
        meeting_stats = await self._get_meeting_stats(meeting_data=meeting_data)

        async with self.session.begin():
            await self.meeting_repo.update_meeting_stats(
                internal_id=internal_meeting_id,
                stats=meeting_stats,
            )

        metrics = await self.get_current_metrics()

        meeting_ID = meeting_stats.get('meetingID')
        whiteboard_id = meeting_stats.get('whiteboardId')
        start_time = meeting_stats.get('startTime')

        boards = metrics.get('boards')
        if boards is None:
            metrics['boards'] = {
                whiteboard_id: {meeting_ID: {start_time: meeting_stats}}
            }
        else:
            if whiteboard_id not in boards:
                boards[whiteboard_id] = {meeting_ID: {start_time: meeting_stats}}
            else:
                rooms = boards[whiteboard_id]
                if meeting_ID not in rooms:
                    rooms[meeting_ID] = {start_time: meeting_stats}
                else:
                    rooms[meeting_ID][start_time] = meeting_stats

        await self.update_metrics(metrics=metrics)

        return metrics

    async def _get_events_path(
        self,
        internal_meeting_id: str,
    ) -> str:
        root = Path(settings.APP_RECORDINGS_PATH)

        events_path = None
        for _ in range(3):
            target_dir = list(root.rglob(internal_meeting_id))
            if target_dir:
                events_file = list(target_dir[0].rglob('events.xml'))
                if events_file:
                    events_path = events_file[0]
                else:
                    logger.info('Ожидание генерации файла с эвентами')
                    await asyncio.sleep(5)
            else:
                logger.info('Ожидание генерации папки с эвентами')
                await asyncio.sleep(5)

        return events_path

    async def _parse_events(
        self,
        events_dict: dict,
    ) -> dict:
        recording = events_dict['recording']

        meeting_data = recording['meeting']
        metadata = recording['metadata']
        events = recording['event']

        self.meeting = {
            'internalID': meeting_data['@id'],
            'meetingID': meeting_data['@externalId'],
            'name': meeting_data['@name'],
            'whiteboardId': metadata['@whiteboard'],
        }

        self.users = {}
        self.meeting['users'] = self.users

        for event in events:
            event_type = (event['@eventname'], event['@module'])

            handlers = {
                (
                    'MeetingConfigurationEvent',
                    'CONFIG',
                ): self._handle_configuration_event,
                (
                    'ParticipantJoinEvent',
                    'PARTICIPANT',
                ): self._handle_participant_join_meeting_event,
                (
                    'ParticipantJoinedEvent',
                    'VOICE',
                ): self._handle_participant_join_voice_event,
                (
                    'ParticipantMutedEvent',
                    'VOICE',
                ): self._handle_participant_muted_event,
                (
                    'ParticipantTalkingEvent',
                    'VOICE',
                ): self._handle_participant_talking_event,
                (
                    'ParticipantLeftEvent',
                    'PARTICIPANT',
                ): self._handle_participant_left_meeting_event,
                (
                    'ParticipantLeftEvent',
                    'VOICE',
                ): self._handle_participant_left_voice_event,
                (
                    'PublicChatEvent',
                    'CHAT',
                ): self._handle_public_chat_event,
                (
                    'EndAndKickAllEvent',
                    'PARTICIPANT',
                ): self._handle_end_and_kick_all_event,
            }

            handler = handlers.get(event_type)
            if handler:
                await handler(event)

        grouped_users = {}
        for user_id in self.users:
            user = self.users.get(user_id)

            extId = user.get('extId')
            if grouped_users.get(extId):
                grouped_users[extId].append(user.copy())
            else:
                grouped_users[extId] = [user.copy()]

        self.meeting['users'] = grouped_users

        return self.meeting

    async def _get_meeting_stats(
        self,
        meeting_data: dict,
    ):
        grouped_users = meeting_data.get('users')

        users_info = {}
        for user_id in grouped_users:
            user_names = []
            user_role = None

            user_talking = timedelta(hours=0, minutes=0, seconds=0)
            user_muted = timedelta(hours=0, minutes=0, seconds=0)
            user_unmuted = timedelta(hours=0, minutes=0, seconds=0)

            user_sessions = grouped_users.get(user_id)
            for session in user_sessions:
                name = session.get('name')
                if name not in user_names:
                    user_names.append(name)

                user_role = session.get('role')

                talking = session.get('talking')
                if talking:
                    last_update = None
                    for update in talking:
                        if last_update is None:
                            last_update = update
                            continue

                        last_value = last_update.get('value')
                        current_value = update.get('value')
                        if last_value == 'true' and current_value == 'false':
                            last_time = last_update.get('date')
                            current_time = update.get('date')
                            user_talking += current_time - last_time

                        last_update = update

                muted = session.get('muted')
                if muted:
                    last_update = None
                    for update in muted:
                        if last_update is None:
                            last_update = update
                            if len(muted) != 1:
                                continue

                        last_value = last_update.get('value')
                        last_time = last_update.get('date')

                        current_value = update.get('value')
                        current_time = update.get('date')

                        if last_value == 'true' and current_value == 'false':
                            user_muted += current_time - last_time
                        elif last_value == 'false' and current_value == 'true':
                            user_unmuted += current_time - last_time
                        elif last_value == 'true' and current_value == 'true':
                            user_muted += current_time - last_time

                        last_update = update

            users_info[user_id] = {
                'name': user_names,
                'role': user_role,
                'stats': {
                    'talking': str(user_talking).split('.')[0],
                    'muted': str(user_muted).split('.')[0],
                    'unmuted': str(user_unmuted).split('.')[0],
                },
            }

        name = meeting_data.get('name')
        meeting_ID = meeting_data.get('meetingID')
        whiteboard_id = meeting_data.get('whiteboardId')

        start_time = (
            meeting_data.get('startTime')
            .isoformat()
            .replace('000', '')
            .replace('+00:00', 'Z')
        )
        end_time = (
            meeting_data.get('endTime')
            .isoformat()
            .replace('000', '')
            .replace('+00:00', 'Z')
        )

        duration = str(
            meeting_data.get('endTime') - meeting_data.get('startTime')
        ).split('.')[0]

        stats = {
            'name': name,
            'meetingID': meeting_ID,
            'whiteboardId': whiteboard_id,
            'startTime': start_time,
            'endTime': end_time,
            'duration': duration,
            'users_count': len(grouped_users.keys()),
            'users': users_info,
        }

        return stats

    async def _handle_configuration_event(
        self,
        event: dict,
    ):
        self.meeting['startTime'] = datetime.fromisoformat(event['date'])

    async def _handle_participant_join_meeting_event(
        self,
        event: dict,
    ):
        user = {
            'extId': event['externalUserId'],
            'intId': event['userId'],
            'name': event['name'],
            'role': event['role'],
            'joined': datetime.fromisoformat(event['date']),
        }
        self.users[event['userId']] = user

    async def _handle_participant_join_voice_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['participant'])

        muted = user.get('muted')
        if muted:
            if muted[-1]['value'] != event['muted']:
                user['muted'].append(
                    {
                        'date': datetime.fromisoformat(event['date']),
                        'value': event['muted'],
                    }
                )
        else:
            user.update(
                {
                    'muted': [
                        {
                            'date': datetime.fromisoformat(event['date']),
                            'value': event['muted'],
                        }
                    ]
                }
            )

    async def _handle_participant_muted_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['participant'])

        muted = user.get('muted')
        if muted:
            if muted[-1]['value'] != event['muted']:
                user['muted'].append(
                    {
                        'date': datetime.fromisoformat(event['date']),
                        'value': event['muted'],
                    }
                )
        else:
            user.update(
                {
                    'muted': [
                        {
                            'date': datetime.fromisoformat(event['date']),
                            'value': event['muted'],
                        }
                    ]
                }
            )

    async def _handle_participant_talking_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['participant'])

        talking = user.get('talking')
        if talking:
            if talking[-1]['value'] != event['talking']:
                user['talking'].append(
                    {
                        'date': datetime.fromisoformat(event['date']),
                        'value': event['talking'],
                    }
                )
        else:
            user.update(
                {
                    'talking': [
                        {
                            'date': datetime.fromisoformat(event['date']),
                            'value': event['talking'],
                        }
                    ]
                }
            )

    async def _handle_participant_left_meeting_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['userId'])
        user.update({'left': datetime.fromisoformat(event['date'])})

    async def _handle_participant_left_voice_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['participant'])

        muted = user.get('muted')
        if muted:
            user['muted'].append(
                {
                    'date': datetime.fromisoformat(event['date']),
                    'value': 'true',
                }
            )

        talking = user.get('talking')
        if talking:
            if talking[-1]['value'] == 'true':
                user['talking'].append(
                    {
                        'date': datetime.fromisoformat(event['date']),
                        'value': 'false',
                    }
                )

    async def _handle_public_chat_event(
        self,
        event: dict,
    ):
        user = self.users.get(event['senderId'])

        message = html.fromstring(event['message']).text_content()
        if user.get('messages'):
            user['messages'].append(message)
        else:
            user.update({'messages': [message]})

    async def _handle_end_and_kick_all_event(
        self,
        event: dict,
    ):
        self.meeting['endTime'] = datetime.fromisoformat(event['date'])

        for user_id in self.users:
            user = self.users.get(user_id)
            left = user.get('left')

            if not left:
                user.update({'left': datetime.fromisoformat(event['date'])})

                muted = user.get('muted')
                if muted:
                    user['muted'].append(
                        {
                            'date': datetime.fromisoformat(event['date']),
                            'value': 'true',
                        }
                    )

                talking = user.get('talking')
                if talking:
                    if talking[-1]['value'] == 'true':
                        user['talking'].append(
                            {
                                'date': datetime.fromisoformat(event['date']),
                                'value': 'false',
                            }
                        )
