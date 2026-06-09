## Архитектура конвейера
Система построена как линейный трехэтапный конвейер:
- Этап 1: Сбор данных. Выполняется через asyncio и aiohttp.
- Этап 2: CPU-bound обработка. Асинхронный диспетчер забирает данные и передает их на расчеты в ProcessPoolExecutor, реззультаты кладутся в multiprocessing.Queue.
- Этап 3: Сохранение. Данные из multiprocessing.Queue читаются в отдельном потоке (ThreadPoolExecutor) и безопасно пишутся в SQLite синхронной библиотекой sqlite3.

## Benchmark
- Время последовательного выполнения: 47.16592979431152s
- Время гибридного выполнения: 7.993s
- Итоговое ускорение: в 44 секунд.

## Пример логов
```
2026-06-09 18:14:52,716 [MainProcess] [MainThread] [FX-USD-EUR] Fetching
2026-06-09 18:14:52,717 [MainProcess] [MainThread] [FX-USD-GBP] Fetching
2026-06-09 18:14:52,718 [MainProcess] [MainThread] [FX-USD-JPY] Fetching
2026-06-09 18:14:52,718 [MainProcess] [MainThread] [FX-USD-CHF] Fetching
2026-06-09 18:14:52,718 [MainProcess] [MainThread] [FX-EUR-USD] Fetching
2026-06-09 18:14:52,719 [MainProcess] [MainThread] [FX-EUR-GBP] Fetching
...
2026-06-09 18:14:59,623 [MainProcess] [ThreadPoolExecutor-0_0] [FX-USD-EUR] Saved
2026-06-09 18:14:59,634 [MainProcess] [ThreadPoolExecutor-0_0] [FX-USD-GBP] Saved
2026-06-09 18:14:59,649 [MainProcess] [ThreadPoolExecutor-0_0] [FX-USD-JPY] Saved
2026-06-09 18:14:59,663 [MainProcess] [ThreadPoolExecutor-0_0] [FX-USD-CHF] Saved
2026-06-09 18:14:59,677 [MainProcess] [ThreadPoolExecutor-0_0] [FX-EUR-USD] Saved
2026-06-09 18:14:59,691 [MainProcess] [ThreadPoolExecutor-0_0] [FX-EUR-GBP] Saved
```
## Данные в БД

```
╭───────────────┬─────────────────────┬────────────────────────╮
│ currency_pair │    average_rate     │        std_dev         │
╞═══════════════╪═════════════════════╪════════════════════════╡
│ USD/EUR       │ 0.86407999999999974 │ 2.2204460492503131e-16 │
│ USD/GBP       │ 0.74605000000000021 │ 2.2204460492503131e-16 │
│ USD/JPY       │              160.16 │                    0.0 │
│ USD/CHF       │             0.79547 │                    0.0 │
│ EUR/USD       │  1.1572999999999996 │ 4.4408920985006262e-16 │
│ EUR/GBP       │ 0.86340000000000028 │ 3.3306690738754696e-16 │
│ EUR/JPY       │  185.34999999999997 │ 2.8421709430404007e-14 │
│ EUR/CHF       │  0.9206000000000002 │ 2.2204460492503131e-16 │
│ GBP/USD       │              1.3404 │                    0.0 │
│ GBP/EUR       │              1.1582 │                    0.0 │
╰───────────────┴─────────────────────┴────────────────────────╯
```

## Профилирование

```
        401650 function calls (394432 primitive calls) in 7.993 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  477/476    0.017    0.000   16.456    0.035 base_events.py:1970(_run_once)
      4/3    0.000    0.000    9.411    3.137 base_events.py:689(run_until_complete)
      4/3    0.000    0.000    9.257    3.086 base_events.py:678(run_forever)
    288/1    0.002    0.000    7.635    7.635 {built-in method builtins.exec}
      2/1    0.000    0.000    7.635    7.635 main.py:1(<module>)
      2/1    0.000    0.000    7.632    7.632 runners.py:160(run)
        1    0.000    0.000    7.632    7.632 runners.py:61(__exit__)
        1    0.000    0.000    7.632    7.632 runners.py:64(close)
        4    0.000    0.000    7.631    1.908 util.py:272(__call__)
...
```
