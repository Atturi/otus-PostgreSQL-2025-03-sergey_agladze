## Домашнее задание #5

### Среда выполнения

#### Hardware

- CPU: intel core i5 220H
- SSD:  ymtc pc411 1tb(nvme)
- RAM: sk hynix lpddr5 32gb 6400mt/s

#### Software

- OS: Linux Fedora 41
- Способ развёртывания PostgreSQL: Docker
- Версия PostgreSQL: 15.12

### Задание

#### Инициализация pgbench

- quite
- scale 4000 - Объём базы 55gb
- foreign-keys

#### Запуск pgbench

- client 80
- connect
- vacuum-all
- T 600
- jobs 4

#### Описание и результаты

Максимальный средний tps, которого удалось добиться - 640(в пике - 849). Этих показателей удалось добиться при дефолтной конфигурации. Любые попытки изменить postgresql.conf либо не изменяли производительность, либо ухудшали её.

На сайте cybertec был сгенерирован следующий конфиг:

Connectivity max_connections = 80 

superuser_reserved_connections = 3 

shared_buffers = '8192 MB' 

work_mem = '32 MB' 

maintenance_work_mem = '420 MB' 

huge_pages = try 

effective_cache_size = '22 GB' 

effective_io_concurrency = 100 

random_page_cost = 1.25  

shared_preload_libraries = 'pg_stat_statements' 

stats track_io_timing=on 

track_functions=pl 

wal_level = replica 

max_wal_senders = 0 

synchronous_commit = on 

checkpoint_timeout = '15 min' 

checkpoint_completion_target = 0.9 

max_wal_size = '1024 MB' 

min_wal_size = '512 MB' 

wal_compression = on 

wal_buffers = -1 

wal_writer_delay = 200ms 

wal_writer_flush_after = 1MB 

bgwriter_delay = 200ms 

bgwriter_lru_maxpages = 100 

bgwriter_lru_multiplier = 2.0 

bgwriter_flush_after = 0 

max_worker_processes = 16 

max_parallel_workers_per_gather = 8 

max_parallel_maintenance_workers = 8 

max_parallel_workers = 16 

parallel_leader_participation = on 

enable_partitionwise_join = on 

enable_partitionwise_aggregate = on 

jit = on 

max_slot_wal_keep_size = '1000 MB' 

track_wal_io_timing = on 

maintenance_io_concurrency = 100 

wal_recycle = on

Изменение дефолтных параметров на указанные не привело к изменениям ни в однопоточном режиме(tps ~ 300 при обеих конфигурациях), ни при jobs 4.

Команда top показывает, что ядра процессора нагружены равномерно, но только на 20-25%.
Команда iostat показывает, что диск используется на 20-25%.

Chatgpt сказал, что проблема в большом количестве грязных страниц, которые часто сбрасываются на диск. Значения buffers_checkpoint и buffers_backend оказались большими. 

По предложению нейросети параметр max_wal_size был увеличен до 4gb, чтобы уменьшить количество записей на диск. После этого значение buffers_backend снизилось в несколько раз, tps вырос примерно на 7%.

Тем не менее, даже увеличение shared_buffers и work_mem при сохранении прочих дефолтных настроек прироста не даёт. Уповаю на синтетичность тестов. Буду экспериментировать на проде :) 


