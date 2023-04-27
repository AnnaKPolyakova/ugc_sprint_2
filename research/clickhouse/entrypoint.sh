#!/bin/bash

echo "start table creation"
docker exec -i node1 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS default;
    CREATE DATABASE IF NOT EXISTS shard;
    CREATE TABLE IF NOT EXISTS default.bookmark_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID
    ) ENGINE = Distributed ('company_cluster', '', bookmark_test, rand());
    CREATE TABLE IF NOT EXISTS default.movie_rating_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID,
    rating INTEGER
    ) ENGINE = Distributed ('company_cluster', '', movie_rating_test, rand());
    CREATE TABLE IF NOT EXISTS shard.bookmark_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/bookmark_test', 'bookmark_test_replica_1')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
    CREATE TABLE IF NOT EXISTS shard.movie_rating_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID,
    rating INTEGER
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/movie_rating_test', 'movie_rating_test_replica_1')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
EOSQL

docker exec -i node2 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE TABLE IF NOT EXISTS replica.bookmark_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/bookmark_test', 'bookmark_test_replica_2')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
    CREATE TABLE IF NOT EXISTS replica.movie_rating_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID,
    rating INTEGER
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/movie_rating_test', 'movie_rating_test_replica_2')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
EOSQL

docker exec -i node3 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS shard;
    CREATE TABLE IF NOT EXISTS shard.bookmark_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/bookmark_test', 'bookmark_test_replica_1')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
    CREATE TABLE IF NOT EXISTS shard.movie_rating_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID,
    rating INTEGER
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/movie_rating_test', 'movie_rating_test_replica_1')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
EOSQL

docker exec -i node4 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE TABLE IF NOT EXISTS replica.bookmark_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/bookmark_test', 'bookmark_test_replica_2')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
    CREATE TABLE IF NOT EXISTS replica.movie_rating_test (
    id UUID,
    create_at DateTime,
    user_id UUID,
    movie_id UUID,
    rating INTEGER
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/movie_rating_test', 'movie_rating_test_replica_2')
    PARTITION BY toYYYYMMDD(create_at) ORDER BY create_at;
EOSQL

echo "done"