
## Домашнее задание #14

### Среда выполнения 

Операционная система: **Linux Fedora 42**

Способ развёртывания **PostgreSQL**: **Docker**

Версия **PostgreSQL**: 17.0

### Задания

> Создать 3 ВМ

- Создать 3 контейнера с **PostgreSQL 17**;
- Создать единую сеть для контейнеров: docker network create replication_network;
- Подключить контейнеры к сети: docker network connect replication_network *имя контейнера*;

> Создать объекты в двух контейнерах

- create database replication_base;
- create schema replication;
- create table replication.test(id serial, name text);
- create table replication.test2(id serial, name text);
- create role repluser with login nosuperuser nocreatedb nocreaterole inherit replication nobypassrls connection limit -1 password 'Labyrinth';
- grant usage on schema replication to repluser;
- grant select on table replication.test to repluser;
- Аналогичные команды для сервера 2.

> Создать публикацию таблицы test на первом сервере и подписаться на неё на втором.

- create publication for table replication.test; --первый сервер
- create subscription subscription01 connection 'host=172.18.0.2 user=repluser password=Labyrinth dbname=replication_base' publication publication_test; --второй сервер

> Создать публикацию таблицы test2 на втором сервере и подписать на неё на первом.

- create publication for table replication.test2; --второй сервер
- create subscription subscription02 connection 'host=pg17_host2 user=repluser password=Labyrinth dbname=replication_base' publication publication_test2; --первый сервер

> Третий контейнер использовать как реплику для чтения и бэкапов

- Создать публикацию таблицы test для третьего сервера: create publication publication_host3 for table replication.test; --первый контейнер
- Создать публикацию таблицы test2 для третьего контейнера: create publication publication_host3 for table replication.test2; --второй контейнер
- Создать базу replication_base, схему replication и таблицы test, test2 в контейнере 3;
- Создать подписку на публикаю с первых двух контейнеров: create subscription subscription_main connection 'host=pg17 user=repluser password=Labyrinth dbname=replication_base' publication publication_host3; create subscription subscription_host2 connection 'host=pg17_host2 user=repluser password=Labyrinth dbname=replication_base' publication publication_host3; --третий контейнер

Проблемы: После настройки публикации и подписки на принимающей стороне не появились данные с главного сервера. В таблице pg_subscription_rel у подписки был статус "d". Логи докера показали ошибку прав доступа при попытке чтения схемы на главном сервере. У пользователя repluser не было прав. Решилось путём выдачи прав пользователю на схему и таблицу.



