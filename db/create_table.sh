#!/bin/bash

DB_FILE="finance.db"

SQL_CREATE_TABLE="
CREATE TABLE IF NOT EXISTS account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_user_id INTEGER NOT NULL UNIQUE,
  telegram_username TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);
"
sqlite3 "$DB_FILE" "$SQL_CREATE_TABLE"
echo "Таблица 'account' создана (если не существовала) в БД '$DB_FILE'"

SQL_CREATE_TABLE="
CREATE TABLE IF NOT EXISTS category (
  name TEXT CHECK (LENGTH(name) >= 3),
  name_detail TEXT CHECK (LENGTH(name) >= 3),
  account_id INTEGER,
  created_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES account(id),
  PRIMARY KEY (name, name_detail, account_id)
);
"
sqlite3 "$DB_FILE" "$SQL_CREATE_TABLE"
echo "Таблица 'category' создана (если не существовала) в БД '$DB_FILE'"

SQL_CREATE_TABLE="
CREATE TABLE IF NOT EXISTS wallet (
  name TEXT NOT NULL CHECK (LENGTH(name) > 5),
  amount REAL DEFAULT 0.0,
  account_id INTEGER,
  created_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES account(id),
  PRIMARY KEY (name, account_id)
);
"
sqlite3 "$DB_FILE" "$SQL_CREATE_TABLE"
echo "Таблица 'wallet' создана (если не существовала) в БД '$DB_FILE'"

SQL_CREATE_TABLE="
CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER,
  category_name TEXT NOT NULL,
  wallet_name TEXT NOT NULL,
  amount REAL NOT NULL,
  created_at TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (account_id) REFERENCES account(id),
  FOREIGN KEY (category_name, account_id) REFERENCES category(name_detail, account_id),
  FOREIGN KEY (wallet_name, account_id) REFERENCES wallet(name, account_id)
);
"
sqlite3 "$DB_FILE" "$SQL_CREATE_TABLE"
echo "Таблица 'transactions' создана (если не существовала) в БД '$DB_FILE'"
