from datetime import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import mapped_column


ID = Annotated[int, mapped_column(primary_key=True)]

CreatedAt = Annotated[datetime, mapped_column(server_default=func.now())]
