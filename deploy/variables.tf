# Disk
variable "disk_size" {
  description = "Размер диска"
  type        = number
  default     = 30
}

variable "image_id" {
  description = "Идентификатор образа"
  type        = string
  default     = "fd8gm9cegc39t4nsm8cv"
}


# Address
variable "address_id" {
  description = "Идентификатор публичного IP-адреса"
  type        = string
}


# VM
variable "zone" {
  description = "Зона доступности"
  type        = string
  default     = "ru-central1-d"
}

variable "vm_cores" {
  description = "Количество vCPU"
  type        = number
  default     = 4
}

variable "vm_memory" {
  description = "Количество RAM"
  type        = number
  default     = 8
}

variable "vm_core_fraction" {
  description = "Гарантированная доля vCPU"
  type        = number
  default     = 50
}

variable "vm_preemptible" {
  description = "Прерываемая ВМ"
  type        = bool
  default     = true
}


# User settings
variable "username" {
  description = "Имя пользователя на сервере"
  type        = string
  default     = "bbbuser"
}

variable "ssh_key" {
  description = "Публичный ssh-ключ"
  type        = string
}

variable "email" {
  description = "Email для автоматической настройки сертификата Let's Encrypt"
  type        = string
}


# BBB settings
variable "domain" {
  description = "Доменное имя сервера"
  type        = string
  default     = "example.com"
}


# Whiteboard settings
variable "whiteboard_base_url" {
  description = "Адрес вайтборда"
  type        = string
  default     = "http://example.com"
}


# API settings
variable "api_base_url" {
  description = "Адрес API"
  type        = string
  default     = "http://example.com"
}
