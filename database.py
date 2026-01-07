"""
Модуль работы с базой данных SQLite
Хранение собранных запросов из Wordstat
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "/root/wordstat-api/wordstat.db"


def init_db():
    """Создание таблиц если их нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            parent_phrase TEXT,
            depth INTEGER DEFAULT 0,
            region_id INTEGER DEFAULT 225,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(phrase, region_id)
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_phrase ON queries(phrase)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_parent ON queries(parent_phrase)
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")


def save_query(phrase: str, count: int, parent_phrase: Optional[str] = None, 
               depth: int = 0, region_id: int = 225) -> bool:
    """Сохранить один запрос"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO queries (phrase, count, parent_phrase, depth, region_id, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (phrase, count, parent_phrase, depth, region_id, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving query: {e}")
        return False
    finally:
        conn.close()


def save_queries_batch(queries: List[Dict]) -> int:
    """Сохранить пачку запросов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    saved = 0
    
    for q in queries:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO queries (phrase, count, parent_phrase, depth, region_id, collected_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                q.get('phrase'),
                q.get('count', 0),
                q.get('parent_phrase'),
                q.get('depth', 0),
                q.get('region_id', 225),
                datetime.now()
            ))
            saved += 1
        except Exception as e:
            print(f"Error saving {q.get('phrase')}: {e}")
    
    conn.commit()
    conn.close()
    return saved


def get_all_queries(region_id: int = 225) -> List[Dict]:
    """Получить все запросы"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT phrase, count, parent_phrase, depth 
        FROM queries 
        WHERE region_id = ?
        ORDER BY count DESC
    ''', (region_id,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_query_count(region_id: int = 225) -> int:
    """Количество запросов в базе"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM queries WHERE region_id = ?', (region_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def clear_queries(region_id: int = 225):
    """Очистить запросы"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM queries WHERE region_id = ?', (region_id,))
    conn.commit()
    conn.close()


# Инициализация при импорте
init_db()
