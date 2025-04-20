## Домашнее задание #4

### Среда выполнения

Операционная система:  **Linux Fedora 41**
Способ развёртывания **PostgreSQL**: **Docker**

### Задания 

> 2. Зайдите в созданный кластер под пользователем postgres

psql -U postgres -d postgres

> 3. Создайте новую базу данных testdb

create database testdb;

> 4. Зайдите в созданную базу данных под пользователем postgres

\connect testdb

> 5. Создайте новую схему testnm

create schema testnm;

> 6. Создайте новую таблицу t1 с одной колонкой c1 типа integer

create table testnm.t1(c1 integer);

> 7. Вставьте строку со значением c1=1

insert into testnm.t1(c1) values(1);

> 8. Создайте новую роль readonly

create role readonly;

> 9. Дайте новой роли право на подключение к базе данных testdb

grant connect on database testdb to readonly;

> 10. Дайте новой роли право на использование схемы testnm

grant usage on schema testsnm to readonly;

> 11. Дайте новой роли право на select для всех таблиц схемы testnm

grant select on all tables in schema testnm to readonly;

> 12. Создайте пользователя testread с паролем test123

create user testread password 'test123';

> 13. Дайте роль readonly пользователю testread

grant readonly to testread;

> 14. Зайдите под пользователем testread в базу testdb

psql -U testread -d testdb

> 16. Получилось?

Да.

> 17. Напишите, что именно произошло

При выполнении select * from t1 вышло сообщение "relation t1 does not exists". Если перед именем таблицы поставить имя схемы testnm, ошибки не будет, и чтение пройдёт успешно. Объясняется это тем, что схема testnm не входит в путь поиска.

> 30. Как сделать так, чтобы такое больше не повторялось?

alter role testread set search_path to testnm, public;

> 37. Попробовать создать таблицу t2

Ошибка. У пользователя testread нет прав на создание объектов.

