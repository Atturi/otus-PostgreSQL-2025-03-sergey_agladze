## Домашнее задание #3

### Среда выполнения

Операционная система: **Linux Fedora 41** на **Virtual Box** 
Версия  **PostgreSQL**: 17
### Задания

>Проверить, что кластер запущен

systemctl status postgresql-17

>Остановить сервер БД

sudo systemctl stop postgresql-17

>Проинициализировать новый диск и добавить его в файловую систему

Разметка диска через fdisk:
sudo fdisk /dev/sdb
n - add new partition
p - primary partition type(mbr)
1 - partition number
first sector: default
last sector: default
w - write table to disk and exit
Создание файловое системы и монтирование согласно инструкции в задании.

>Запустить кластер после перемещения содержимого папки data

Запустить не получилось потому что папка data отсутствует в каталоге /var/lib/pgsql/17

>Найти конфигурационный параметр в файлах в /etc/postgresql и поменять его

Папка postgresql в /etc отсутствует.
Был найден параметр **data_directory** в файле postgresql.conf, но файл находится внутри перемещённой папки data, и его изменение не приводит к успеху.

Решено через изменение конфигурации сервиса **postgresql-17** в **systemctl**:

sudo systemctl edit postgresql-17
[Service]
Environment=PGDATA={новый путь до папки data}
>Задание со звёздочкой

- В **Virtual Box** в разделе **Носители** отсоединить ранее созданный диск;
- Добавить отсоединённый на прошлом шаге диск в новую виртуальную машину;
- На новой машине через убедиться в сохранении структуры диска при переносе: 
 lsblk /dev/sdb1 -f
- sudo mount /dev/sdb1 /var/lib/pgsql/
- sudo systemctl start postgersql-17

В итоге СУБД запустилась и правильно прочитал папку data. На новой машине удалось обратиться к перенесённым данным.

