## Домашнее задание #7

### Окружение

Операционная система: **Linux Fedora 41**
Способ развёртывания СУБД: **Docker**
Версия **PostgreSQL**: 15.12

### Задания

> Настройте выполнение контрольной точки раз в 30 секунд

alter system set checkpoint_timeout = '30s';

> 10 минут с помощью утилиты pgbench подавайте нагрузку

pgbench --client=80 --connect --progress=20 --vacuum-all -T 600 -U postgres postgres

> Измерьте, какой объём журнальных файлов был сгенерирован за это время. Оцените, какой объём приходится в среднем на одну контрольную точку.

select pg_current_wal_lsn(); --23/940DA528 - до запуска **pgbench**

select pg_current_wal_lsn(); --24/38356C58 --после запуска **pgbench**

select pg_size_pretty('24/38356C58'::pg_lsn - '23/940DA528'::pg_lsn) as generated_wal_size; --2626MB - Объём сгенерированных wal-файлов

Данные из pg_stat_bgwriter до запуска **pgbench**:

checkpoints_timed    2064

checkpoints_req        20

Данные из pg_stat_bgwriter после запуска **pgbench**:

checkpoints_timed    2091
checkpoints_req        20

select 2626 / 27; --Объём сгенерированных файлов / количество контрольных точек, 97 MB в среднем на одну точку.
Все контрольные точки выполнились по расписанию.

> Сравните tps в синхронном/асинхронном режимах утилитой pgbench. Объясните полученный результат

Настройка **pgbench**: 
- initialize
- quite
- scale = 600
- foreign-keys

Запуск **pgbench**:
- client = 80
- connect
- vacuum-all
- T 600

При synchronous_commit = on tps = 278, при synchronous_commit = off tps = 265.

В ходе тестирования было проанализировано представление pg_stat_bgwriter. Значение в поле buffers_backend_fsync = 0 в обоих случаях, buffers_backend различаются менее чем на процент, checkpoint_sync_time отличаются на 3 процента. Предположительно, отсутствие разницы объясняется достаточно мощным железом и неоптимальной нагрузкой pgbench.

> Создайте новый кластер с включённой контрольной суммой страниц. Создайте таблицу. Вставьте несколько значений. Выключите кластер. Измените пару байт в таблице. Включите кластер и сделайте выборку из таблицы. Что и почему произошло?  Как проигнорировать ошибку и продолжить работу?

Создание кластера:
- В Dockerfile добавить строку "ENV POSTGRES_INITDB_ARGS="--data-checksums""
- Создание образа на основе Dockerfile: docker build -t pg15checksums .

Создание таблицы и наполнение её данными:
- create table test_checksum(id serial primary key, insert_date date not null default now(), name text);
- insert into test_checksum(name) values('name1'), ('name2');

Изменение таблицы: dd if=/dev/zero of=/var/lib/postgresql/data/base/5/16389 oflag=dsync conv=notrunc bs=1 count=8

Перезагрузка кластера: docker restart pg15chsm

Результат выборки из повреждённой таблицы: WARNING:  page verification failed, calculated checksum 47551 but expected 3548
ERROR:  invalid page in block 0 of relation base/5/16389

Игнорирование ошибки:
- alter system set ignore_checksum_failure = 'on';
- select pg_reload_conf();

Новый вывод после выборки:

WARNING:  page verification failed, calculated checksum 47551 but expected 3548
 id | insert_date | name  
----+-------------+-------
  1 | 2025-06-01  | name1
  2 | 2025-06-01  | name2
(2 rows)


