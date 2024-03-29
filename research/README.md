### Запуск тестов

* `docker-compose -f research/clickhouse/docker-compose-clickhouse.yml up -d --build`
* `docker-compose -f research/mongodb/docker-compose-mongo.yml up -d --build`

Если нужны тесты с нагрузкой, то перед запуском самих тестов:

* `python -m research.clickhouse.run_load`
* `python -m research.mongodb.run_load`

Запуск самих тестов
* `python -m research.clickhouse.run_tests`
* `python -m research.mongodb.run_tests`

Результаты будут выведены в терминале

Что бы удалить контейнеры

* `docker-compose -f research/clickhouse/docker-compose-clickhouse.yml  down --rmi all --volumes`
* `docker-compose -f research/mongodb/docker-compose-mongo.yml down --rmi all --volumes`

### Данные по итогам 20 подряд проведенных тестов


#### Тестируем clickhouse:  

Схема данных: 2 шарда по 2 реплики

В дб 4,5 млн объектов из которых около 40% попадают в выборку при запросах

Без нагрузки

| Тест                                     |        min - max, s:ms        | median, s:ms  |
|------------------------------------------|:-----------------------------:|:-------------:|
| get_users_favorite_movies_from_full_db   | 0: 10 432 449 - 0: 13 003 330 | 0: 10 987 058 |
| get_users_bookmark_from_full_db          | 0: 24 177 367 - 0: 30 678 830 | 0: 27 335 502 |



С нагрузкой (запущен параллельно процесс записывающий по 100 записей в 0,01 сек)

| Тест                                   |        min - max, s:ms        | median, s:ms  |
|----------------------------------------|:-----------------------------:|:-------------:|
| get_users_favorite_movies_from_full_db | 0: 18 444 464 - 0: 22 775 328 | 0: 20 816 724 |
| get_users_bookmark_from_full_db        | 0: 41 548 123 - 0: 58 652 139 | 0: 50 952 352 |


#### Тестируем mongodb:  

Схема данных: 4 node (2 реплики, 2 партиции)

Без нагрузки

| Тест                                   |        min - max, s:ms        | median, s:ms  |
|----------------------------------------|:-----------------------------:|:-------------:|
| get_users_favorite_movies_from_full_db | 0: 00 000 087 - 0: 00 000 506 | 0: 00 000 332 |
| get_users_bookmark_from_full_db        | 0: 00 000 085 - 0: 00 000 092 | 0: 00 000 092 |


С нагрузкой (запущен параллельно процесс записывающий по 100 записей в 0,01 сек)

| Тест                                   |        min - max, s:ms        | median, s:ms  |
|----------------------------------------|:-----------------------------:|:-------------:|
| get_users_favorite_movies_from_full_db | 0: 00 000 093 - 0: 00 000 172 | 0: 00 000 094 |
| get_users_bookmark_from_full_db        | 0: 00 000 090 - 0: 00 000 111 | 0: 00 000 091 |



### Итоги. Принятие решение по реализации сервиса

Было принято решение реализовать хранение данных спринта в отдельном сервисе  
В данном случаем нам важна скорость чтения данных, по итогам исследование 
выигрывает mongodb. Тем не менее у данного решения есть свои минусы: сложнее 
поддерживать консистентность данных.

По итогам тестирования по скорости чтения и с нагрузкой и без сильно 
выигрывает по времени mongodb. Но хотелось бы отметить, что легче и быстрее 
происходила запись в clickhouse (замеры не производила, но это было сильно 
заметно. При продолжительной записи контейнеры с mongodb постоянно 
падали, возможно из-за неоптимальной настройки или же из-за 
недостаточной производительность оборудования)

Так же изучив информацию об этих двух СУБД стало очевидно, что clickhouse 
все таки больше подходит для хранения аналитической информации, которая имеет 
ценность как совокупность данных. В то время как mongodb больше подходит для 
хранения контента и пользовательских данных. 




