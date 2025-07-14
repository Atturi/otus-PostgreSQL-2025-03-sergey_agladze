## Домашнее задание #13

### Среда выполнения

Операционная система: **Linux Fedora 42**

Способ развёртывания **PostgreSQL**: **Docker**

Версия **PostgreSQL**: 17.0

### Задания

>  Создать БД, схему и таблицу

- *create database backup_base;*
- *create schema backup_schema;*
- create table backup_schema.backup_table(id serial primary key, num text);

> Заполнить таблицу

*insert into backup_table(id, num) select v, 'num_'||v from generate_series(1, 100) v;*

> Сделать логический бэкап, используя утилиту copy

*psql -U postgres -d backup_base -c "\copy backup_table to 'backup_table.csv' csv header"*

> Восстановить данные во вторую таблицу

- *create table restore_table(id serial primary key, num text);* - создание второй таблицы
- *copy restore_table from '/var/lib/postgresql/data/backups/backup_table.csv' with delimiter ',' header;*

> Создать бэкап двух таблиц

*pg_dump -U postgres -Fc -d backup_base --schema backup_schema -f dump_schema.sql* - бэкап всей схемы, включая 2 таблицы

> Восстановить в новую БД только вторую таблицу

- *pg_restore -l dump_schema.sql > full.list* - сохранить список всех объектов бэкапа в файл full.list;
- С помощью тексторовго редактора оставить в *full.list* только объект, относящиеся в таблице *restore_table*. Конечное содержимое файла показано на скриншоте *full.png*.
- *pg_restore -U postgres -L full.list -d restore_base dump_schema.sql* - восстановить в базу *restore_base* только объекты, указанные в *full.list*.


