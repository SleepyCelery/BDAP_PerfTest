#!/bin/bash

# 定义数据库连接信息
DB_DRIVER="pgsql"
DB_HOST=""
DB_PORT="5432"
DB_USER=""
DB_PASSWORD=""
DB_NAME=""

# 定义测试参数
TABLE_SIZE_LIST=(10000 20000 50000 100000)
TABLES=3
EVENTS=0
TIME=300
THREADS=10

# 开始测试
for TABLE_SIZE in "${TABLE_SIZE_LIST[@]}"; do
    echo "开始对 ${TABLE_SIZE} 用户进行OLTP混合读写测试..."

    # 准备阶段
    echo "准备测试数据..."
    sysbench --db-driver=$DB_DRIVER --pgsql-host=$DB_HOST --pgsql-port=$DB_PORT --pgsql-user=$DB_USER --pgsql-password="$DB_PASSWORD" --pgsql-db=$DB_NAME --table_size=$TABLE_SIZE --tables=$TABLES --events=$EVENTS --time=$TIME --threads=$THREADS oltp_read_write prepare

    # 运行阶段
    echo "开始测试..."
    sysbench --db-driver=$DB_DRIVER --pgsql-host=$DB_HOST --pgsql-port=$DB_PORT --pgsql-user=$DB_USER --pgsql-password="$DB_PASSWORD" --pgsql-db=$DB_NAME --table_size=$TABLE_SIZE --tables=$TABLES --events=$EVENTS --time=$TIME --threads=$THREADS --report-interval=1 oltp_read_write run &> "${TABLE_SIZE}user_${THREADS}threads.log"

    # 清理阶段
    echo "清理测试数据..."
    sysbench --db-driver=$DB_DRIVER --pgsql-host=$DB_HOST --pgsql-port=$DB_PORT --pgsql-user=$DB_USER --pgsql-password="$DB_PASSWORD" --pgsql-db=$DB_NAME --table_size=$TABLE_SIZE --tables=$TABLES --events=$EVENTS --time=$TIME --threads=$THREADS oltp_read_write cleanup

    echo "${TABLE_SIZE} 用户的测试完成."
    echo "--------------------------------"
done

echo "所有测试完成。"
