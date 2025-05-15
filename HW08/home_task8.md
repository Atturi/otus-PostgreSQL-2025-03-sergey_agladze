## Домашнее задание #8

### Среда выполнения

Операционная система: **Linux Fedora 41**
Способ развёртывания БД: **Docker**
Версия **PostgreSQL**: 15.12

### Задания

> Настройте сервер так, чтобы в журнал сообщений сбрасывалась информация о блокировках, удерживаемых более 200 миллисекунд. Воспроизведите ситуацию, при которой в журнале появятся такие сообщения.

**Настройка сервера**:
- alter system set log_lock_waits = on;
- alter system set log_min_message = 'info';
- alter system set deadlock_timeout = '200ms';
- alter system set lock_timeout = '1s';
- alter system set logging_collector = on;

**Воспроизведение блокировки**:
- create table lock_test(id serial, name test);
- insert into lock_test(name) values('name1');
- (Сессия 1) begin; update lock_test set name = 'NAME' where id = 1;
- (Сессия 2) begin; update lock_test set name = 'NAME' where id = 1;

**Сообщения в журнале**:
2025-05-15 17:43:41.524 GMT [50] LOG:  process 50 still waiting for ShareLock on transaction 3188777 after 200.165 ms
2025-05-15 17:43:41.524 GMT [50] DETAIL:  Process holding the lock: 42. Wait queue: 50.
2025-05-15 17:43:41.524 GMT [50] CONTEXT:  while updating tuple (0,1) in relation "lock_test"
2025-05-15 17:43:41.524 GMT [50] STATEMENT:  update lock_test set name = 'NAME' where id = 1;

