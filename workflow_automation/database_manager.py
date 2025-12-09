"""
数据库管理模块
本小姐为双库维护与自动化处理提供统一数据底座！(￣ω￣)ノ

功能：
- 初始化 SQLite 数据库与表结构
- 批量导入（CSV/JSON）政府库与行业库条目
- 队列化处理（pending/processing/completed/error）
- 结果与错误归档（JSON 文本）
"""

import os
import json
import csv
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional


class DatabaseManager:
    """数据库管理器类"""

    def __init__(self, db_path: str = "data/materials.db"):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """
        初始化数据库表结构
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                source TEXT,
                url TEXT,
                agency TEXT,
                doc_number TEXT,
                subject TEXT,
                event_type TEXT,
                key_data TEXT,
                date TEXT,
                status TEXT DEFAULT 'pending',
                result_json TEXT,
                error_msg TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )

        conn.commit()
        # 迁移：补齐缺失列
        c.execute("PRAGMA table_info(materials)")
        cols = {row[1] for row in c.fetchall()}
        desired = [
            ('type','TEXT'),('title','TEXT'),('content','TEXT'),('source','TEXT'),
            ('url','TEXT'),('agency','TEXT'),('doc_number','TEXT'),('subject','TEXT'),
            ('event_type','TEXT'),('key_data','TEXT'),('date','TEXT'),('status','TEXT'),
            ('result_json','TEXT'),('error_msg','TEXT'),('created_at','TEXT'),('updated_at','TEXT')
        ]
        for col, typ in desired:
            if col not in cols:
                c.execute(f"ALTER TABLE materials ADD COLUMN {col} {typ}")
        conn.commit()
        conn.close()

    def add_material(self, item: Dict[str, Any]) -> int:
        """
        新增材料条目

        Args:
            item: 字段字典（至少包含 type/title）

        Returns:
            新增记录的ID
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fields = [
            'type','title','content','source','url','agency','doc_number',
            'subject','event_type','key_data','date','status','result_json',
            'error_msg','created_at','updated_at'
        ]
        record = {k: item.get(k) for k in fields}
        record['status'] = record.get('status') or 'pending'
        record['created_at'] = record.get('created_at') or now
        record['updated_at'] = now
        record['content'] = record.get('content') or ''
        record['source'] = record.get('source') or ''
        record['title'] = record.get('title') or ''
        record['type'] = record.get('type') or ''

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO materials (
                type,title,content,source,url,agency,doc_number,
                subject,event_type,key_data,date,status,result_json,
                error_msg,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                record['type'], record['title'], record['content'], record['source'],
                record.get('url'), record.get('agency'), record.get('doc_number'),
                record.get('subject'), record.get('event_type'), record.get('key_data'),
                record.get('date'), record['status'], record.get('result_json'),
                record.get('error_msg'), record['created_at'], record['updated_at']
            )
        )
        new_id = c.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def add_bulk_from_csv(self, file_path: str, entry_type: str) -> int:
        """
        从 CSV 批量导入材料

        Args:
            file_path: CSV 文件路径
            entry_type: 条目类型（government/industry）

        Returns:
            成功导入的数量
        """
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = {
                    'type': entry_type,
                    'title': row.get('title') or row.get('标题') or '',
                    'content': row.get('content') or row.get('正文'),
                    'source': row.get('source') or row.get('来源'),
                    'url': row.get('url') or row.get('链接'),
                    'agency': row.get('agency') or row.get('发布机构'),
                    'doc_number': row.get('doc_number') or row.get('文号'),
                    'subject': row.get('subject') or row.get('主题'),
                    'event_type': row.get('event_type') or row.get('事件类型'),
                    'key_data': row.get('key_data') or row.get('关键数据'),
                    'date': row.get('date') or row.get('日期')
                }
                if item['title']:
                    self.add_material(item)
                    count += 1
        return count

    def add_bulk_from_json(self, file_path: str, entry_type: str) -> int:
        """
        从 JSON 批量导入材料

        Args:
            file_path: JSON 文件路径（列表或对象）
            entry_type: 条目类型（government/industry）

        Returns:
            成功导入的数量
        """
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        items = data if isinstance(data, list) else [data]
        for obj in items:
            item = {
                'type': entry_type,
                'title': obj.get('title', ''),
                'content': obj.get('content'),
                'source': obj.get('source'),
                'url': obj.get('url'),
                'agency': obj.get('agency'),
                'doc_number': obj.get('doc_number'),
                'subject': obj.get('subject'),
                'event_type': obj.get('event_type'),
                'key_data': obj.get('key_data'),
                'date': obj.get('date')
            }
            if item['title']:
                self.add_material(item)
                count += 1
        return count

    def get_pending(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取待处理队列

        Args:
            limit: 返回数量上限

        Returns:
            待处理材料列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM materials WHERE status='pending' ORDER BY id ASC LIMIT ?", (limit,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows

    def update_status(self, material_id: int, status: str,
                      result: Optional[Dict[str, Any]] = None,
                      error_msg: str = "") -> None:
        """
        更新材料处理状态

        Args:
            material_id: 记录ID
            status: 状态（pending/processing/completed/error）
            result: 结果字典（将序列化为 JSON 文本）
            error_msg: 错误信息
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_json = json.dumps(result, ensure_ascii=False) if result else None
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "UPDATE materials SET status=?, result_json=?, error_msg=?, updated_at=? WHERE id=?",
            (status, result_json, error_msg, now, material_id)
        )
        conn.commit()
        conn.close()

    def get_stats(self) -> Dict[str, Any]:
        """
        获取数据库统计信息

        Returns:
            统计字典
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        stats = {}
        for s in ['pending','processing','completed','error']:
            c.execute("SELECT COUNT(*) FROM materials WHERE status=?", (s,))
            stats[s] = c.fetchone()[0]
        conn.close()
        return stats
