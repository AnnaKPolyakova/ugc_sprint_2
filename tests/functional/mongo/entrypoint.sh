#!/bin/bash

echo "start creation mongodb db"
# Для начала настроим серверы конфигурации.
docker exec mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongosh'
# Далее, соберём набор реплик первого шарда.
docker exec mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}]})" | mongosh'
# Познакомим шард с маршрутизаторами
docker exec mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
## Второй шард добавим по аналогии. Сначала инициализируем реплики.
docker exec mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}]})" | mongosh'
# Затем добавим их в кластер.
docker exec mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
