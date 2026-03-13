#!/bin/bash

DB_FILE="finance.db"

SQL_DROP_TABLE="
DROP TABLE IF EXISTS account;
"
sqlite3 "$DB_FILE" "$SQL_DROP_TABLE"
echo "Таблица 'account' удалена (если существовала) из БД '$DB_FILE'"

SQL_DROP_TABLE="
DROP TABLE IF EXISTS category;
"
sqlite3 "$DB_FILE" "$SQL_DROP_TABLE"
echo "Таблица 'category' удалена (если существовала) из БД '$DB_FILE'"

SQL_DROP_TABLE="
DROP TABLE IF EXISTS wallet;
"
sqlite3 "$DB_FILE" "$SQL_DROP_TABLE"
echo "Таблица 'wallet' удалена (если существовала) из БД '$DB_FILE'"

SQL_DROP_TABLE="
DROP TABLE IF EXISTS transactions;
"
sqlite3 "$DB_FILE" "$SQL_DROP_TABLE"
echo "Таблица 'transactions' удалена (если существовала) из БД '$DB_FILE'"
