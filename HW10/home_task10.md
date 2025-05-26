## Домашнее задание #10

### Среда выполнения

Операционная система: **Linux Fedora 41**
Способ развёртывания СУБД: **Docker**
Версия **PostgreSQL**: 15.12

### Задания

> Создать индекс какой-либо из таблиц вашей БД

create index idx_pgbench_tellers_tbalance on pgbench_tellers using btree(tbalance); --Индекс для поиска по сумме остатка на счёте.

> Прислать текстом  результат команды explain, в которой используется данный индекс

explain(analyze, costs off) select * from pgbench_tellers where tbalance = 2689;

 Index Scan using idx_pgbench_tellers_tbalance on pgbench_tellers (actual time=0.061..0.062 rows=1 loops=1)
   Index Cond: (tbalance = 2689)
 Planning Time: 0.423 ms
 Execution Time: 0.086 ms
(4 rows)

> Реализовать индекс для полнотекстового поиска

create table index_table(id serial, fio text, birth_year integer);

create index idx_index_table_fio on index_table using gin(to_tsvector('russian', fio)); --Индекс для поиска по имению

> Реализовать индекс на часть таблицы

create index idx_index_table_birth_year on index_table using btree(birth_year) where birth_year <= 1945; --Индекс для поиска малой группы наиболее пожилых людей.

> Создать индекс на несколько полей

create index idx_index_table_fio_birth_year on index_table using btree(fio, birth_year); --Индекс для наиболее точного поиска конкретного человека.


