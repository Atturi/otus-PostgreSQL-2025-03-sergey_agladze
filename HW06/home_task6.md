## Домашнее задание #6

### Окружение

Операционная система: **Linux Fedora 41**

Способ развёртывания **PostgreSQL**: **Docker**

Версия **PostgreSQL**: 15.12

### Задания

> Создать инстанс ВМ с 2 ядрами и 4 Гб ОЗУ и SSD 10 ГБ

**Fedora** стоит на железе, а не на виртуалке. Ограничить размер ssd можно только для контейнера.

- dd if=/dev/zero of=/mnt/hw6_docker_volume.img bs=1M 10240
- mkfs.ext4 /mnt/hw6_docker_volume.img
- mkdir /mnt/limited_volume
- mount -o loop /mnt/hw6_docker_volume.img /mnt/limited_volume
- sudo docker run --name pg15_restricted --memory=4GB --cpuset-cpus="1,2" -v /mnt/limited_volume:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres pg15

