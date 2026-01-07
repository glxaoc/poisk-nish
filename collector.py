"""
Модуль глубокого сбора запросов из Wordstat API
Рекурсивно собирает вложенные запросы
"""

import requests
import time
from typing import List, Dict, Set, Optional
from database import save_queries_batch, clear_queries

# Настройки API
TOKEN = "y0__xCHu4rZARjd0Dogyfj_7RQJLwxI8zao8Pru2PA2l5w2HjR6dA"
BASE_URL = "https://api.wordstat.yandex.net"
HEADERS = {
    "Content-Type": "application/json;charset=utf-8",
    "Authorization": f"Bearer {TOKEN}"
}

# Лимиты
RATE_LIMIT_DELAY = 0.15  # 10 запросов в секунду = 0.1с, берём с запасом


class Collector:
    """Сборщик запросов из Wordstat"""
    
    def __init__(self):
        self.collected_phrases: Set[str] = set()  # Уже собранные фразы
        self.all_queries: List[Dict] = []  # Все собранные запросы
        self.api_calls = 0  # Счётчик вызовов API
        self.status = "idle"  # idle, running, done, error
        self.progress = 0  # Прогресс 0-100
        self.current_phrase = ""  # Текущая обрабатываемая фраза
        
    def _api_request(self, phrase: str, region_id: int = 225) -> Optional[Dict]:
        """Запрос к API с учётом лимитов"""
        time.sleep(RATE_LIMIT_DELAY)
        
        payload = {"phrase": phrase}
        if region_id and region_id != 0:
            payload["regions"] = [region_id]
            
        try:
            response = requests.post(
                f"{BASE_URL}/v1/topRequests",
                headers=HEADERS,
                json=payload,
                timeout=30
            )
            self.api_calls += 1
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    def collect(self, phrase: str, region_id: int = 225, max_depth: int = 2, 
                max_queries: int = 500) -> Dict:
        """
        Глубокий сбор запросов
        
        Args:
            phrase: Исходная фраза
            region_id: ID региона (225 = Россия)
            max_depth: Максимальная глубина (2 = ~400 запросов к API)
            max_queries: Максимум запросов для сбора
        
        Returns:
            Статистика сбора
        """
        self.status = "running"
        self.collected_phrases = set()
        self.all_queries = []
        self.api_calls = 0
        self.progress = 0
        
        # Очищаем старые данные
        clear_queries(region_id)
        
        # Очередь на обработку: (фраза, родитель, глубина)
        queue = [(phrase, None, 0)]
        
        while queue and len(self.all_queries) < max_queries:
            current_phrase, parent, depth = queue.pop(0)
            
            # Пропускаем уже собранные
            if current_phrase.lower() in self.collected_phrases:
                continue
                
            self.current_phrase = current_phrase
            self.collected_phrases.add(current_phrase.lower())
            
            # Запрос к API
            data = self._api_request(current_phrase, region_id)
            if not data:
                continue
            
            # Сохраняем топ запросы
            top_requests = data.get("topRequests", [])
            for item in top_requests:
                query = {
                    "phrase": item["phrase"],
                    "count": item["count"],
                    "parent_phrase": current_phrase,
                    "depth": depth,
                    "region_id": region_id
                }
                self.all_queries.append(query)
                
                # Добавляем в очередь если не достигли максимальной глубины
                if depth < max_depth and item["phrase"].lower() not in self.collected_phrases:
                    queue.append((item["phrase"], current_phrase, depth + 1))
            
            # Обновляем прогресс
            self.progress = min(95, int(len(self.all_queries) / max_queries * 100))
            
            # Лог каждые 10 запросов
            if self.api_calls % 10 == 0:
                print(f"Collected: {len(self.all_queries)} queries, API calls: {self.api_calls}")
        
        # Сохраняем в базу
        saved = save_queries_batch(self.all_queries)
        
        self.status = "done"
        self.progress = 100
        
        return {
            "status": "done",
            "total_queries": len(self.all_queries),
            "unique_phrases": len(self.collected_phrases),
            "api_calls": self.api_calls,
            "saved_to_db": saved
        }
    
    def get_status(self) -> Dict:
        """Текущий статус сбора"""
        return {
            "status": self.status,
            "progress": self.progress,
            "collected": len(self.all_queries),
            "api_calls": self.api_calls,
            "current_phrase": self.current_phrase
        }


# Глобальный экземпляр
collector = Collector()


def deep_collect(phrase: str, region_id: int = 225, max_depth: int = 2) -> Dict:
    """Функция для вызова из app.py"""
    return collector.collect(phrase, region_id, max_depth)


def get_collect_status() -> Dict:
    """Получить статус сбора"""
    return collector.get_status()
