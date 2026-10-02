# -*- coding: utf-8 -*-
"""
database.py - SQLite 数据库操作模块
===================================
负责计算历史记录的持久化存储：
  - 插入一条计算记录
  - 查询全部计算记录
  - 按 id 删除指定记录
  - 清空全部记录

使用 Python 自带的 SQLite，无需额外安装数据库服务。
数据保存在项目目录下的 calculator.db 文件中，因此前端刷新、
重启都不会导致历史记录丢失。
"""

import os
import sqlite3
from datetime import datetime

# 数据库文件路径：与当前文件同目录
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculator.db")


class Database:
    """封装 SQLite 的常用操作。"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def _connect(self):
        """建立连接，返回带 row_factory 的连接对象。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """初始化数据表（如果表不存在则创建）。"""
        conn = self._connect()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                expression  TEXT    NOT NULL,
                result      TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def insert_history(self, expression, result):
        """
        插入一条计算记录，返回新记录的自增 id。

        参数:
            expression: 原始表达式字符串，如 "(1+2)*3"
            result:     计算结果，如 9
        """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cursor = conn.execute(
            "INSERT INTO calculation_history (expression, result, created_at) "
            "VALUES (?, ?, ?)",
            (expression, str(result), created_at),
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    def get_all_history(self):
        """
        查询全部计算记录，按 id 倒序返回（最新的在最前面）。

        返回:
            [{id, expression, result, created_at}, ...]
        """
        conn = self._connect()
        rows = conn.execute(
            "SELECT id, expression, result, created_at "
            "FROM calculation_history ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def delete_history(self, record_id):
        """
        按 id 删除一条记录。

        返回:
            True 表示删除成功；False 表示该记录不存在
        """
        conn = self._connect()
        cursor = conn.execute(
            "DELETE FROM calculation_history WHERE id = ?", (record_id,)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def clear_history(self):
        """清空全部计算记录。"""
        conn = self._connect()
        conn.execute("DELETE FROM calculation_history")
        conn.commit()
        conn.close()
