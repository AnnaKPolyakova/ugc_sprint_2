#!/bin/bash

echo "start drop tables"

docker exec -i node1 clickhouse-client -n <<-EOSQL
    DELETE * FROM default.bookmark_test;
    DELETE * FROM shard.bookmark_test;
    DELETE * FROM default.movie_rating_test;
    DELETE * FROM shard.movie_rating_test;
EOSQL

docker exec -i node2 clickhouse-client -n <<-EOSQL
    DELETE * FROM replica.bookmark_test;
    DELETE * FROM replica.movie_rating_test;
EOSQL

docker exec -i node3 clickhouse-client -n <<-EOSQL
    DELETE * FROM shard.bookmark_test;
    DELETE * FROM shard.movie_rating_test;
EOSQL

docker exec -i node4 clickhouse-client -n <<-EOSQL
    DELETE * FROM replica.bookmark_test;
    DELETE * FROM replica.movie_rating_test;
EOSQL

echo "done"