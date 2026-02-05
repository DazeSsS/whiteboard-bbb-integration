resource "yandex_compute_disk" "boot-disk" {
  name     = "boot-disk-bbb"
  type     = "network-hdd"
  zone     = var.zone
  size     = var.disk_size
  image_id = var.image_id
}

data "yandex_vpc_address" "my-addr" {
  address_id = var.address_id
}

resource "yandex_compute_instance" "bbb-vm" {
  name                      = "bbb-vm"
  hostname                  = "bbb-vm"
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = var.zone

  resources {
    cores         = var.vm_cores
    memory        = var.vm_memory
    core_fraction = var.vm_core_fraction  
  }

  boot_disk {
    auto_delete = true
    disk_id     = yandex_compute_disk.boot-disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.bbb-subnet.id
    nat       = true
    nat_ip_address = data.yandex_vpc_address.my-addr.external_ipv4_address[0].address
  }

  scheduling_policy {
    preemptible = var.vm_preemptible
  }

  metadata = {
    user-data = templatefile("${path.module}/cloud-init-native.yml", {
      username            = var.username
      ssh_key             = var.ssh_key
      email               = var.email
      domain              = var.domain
      whiteboard_base_url = var.whiteboard_base_url
      api_prefix          = var.api_prefix
    })
  }
}

resource "yandex_vpc_network" "bbb-network" {
  name = "bbb-network"
}

resource "yandex_vpc_subnet" "bbb-subnet" {
  name           = "bbb-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.bbb-network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "internal_ip_address" {
  value = yandex_compute_instance.bbb-vm.network_interface.0.ip_address
}

output "external_ip_address" {
  value = yandex_compute_instance.bbb-vm.network_interface.0.nat_ip_address
}
