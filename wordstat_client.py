"""
Wordstat API Client
====================
Клиент для работы с новым API Яндекс Вордстат (запущен июнь 2025)

Документация: https://yandex.ru/support2/wordstat/ru/content/api-structure

Лимиты API:
- 10 запросов в секунду
- 1000 запросов в сутки

Методы API:
- /v1/topRequests - топ запросов по фразе
- /v1/dynamics - динамика запросов по времени
- /v1/regions - распределение по регионам
- /v1/getRegionsTree - дерево регионов
- /v1/userInfo - информация о квоте
"""

import requests
import json
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class WordstatConfig:
    """Конфигурация клиента Wordstat API"""
    oauth_token: str
    base_url: str = "https://api.wordstat.yandex.net"
    requests_per_second: int = 10
    daily_limit: int = 1000


class WordstatAPIError(Exception):
    """Исключение для ошибок Wordstat API"""
    def __init__(self, message: str, response: Optional[requests.Response] = None):
        self.message = message
        self.response = response
        super().__init__(self.message)


class WordstatClient:
    """
    Клиент для работы с Wordstat API
    """
    
    def __init__(self, oauth_token: str, config: Optional[WordstatConfig] = None):
        self.config = config or WordstatConfig(oauth_token=oauth_token)
        self.config.oauth_token = oauth_token
        self._last_request_time = 0
        self._request_count = 0
        
    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": f"Bearer {self.config.oauth_token}"
        }
    
    def _rate_limit(self):
        current_time = time.time()
        time_diff = current_time - self._last_request_time
        if time_diff < 0.1:
            time.sleep(0.1 - time_diff)
        self._last_request_time = time.time()
        self._request_count += 1
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        self._rate_limit()
        url = f"{self.config.base_url}{endpoint}"
        
        try:
            response = requests.post(url, headers=self._headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise WordstatAPIError("Ошибка авторизации. Проверьте OAuth токен.", response)
            elif response.status_code == 429:
                raise WordstatAPIError("Превышен лимит запросов.", response)
            else:
                raise WordstatAPIError(f"Ошибка API: {response.status_code} - {response.text}", response)
                
        except requests.exceptions.Timeout:
            raise WordstatAPIError("Таймаут запроса")
        except requests.exceptions.ConnectionError:
            raise WordstatAPIError("Ошибка подключения к API")
    
    def get_user_info(self) -> Dict[str, Any]:
        return self._make_request("/v1/userInfo", {})
    
    def get_regions_tree(self) -> Dict[str, Any]:
        return self._make_request("/v1/getRegionsTree", {})
    
    def get_top_requests(self, phrase: str, regions: Optional[List[int]] = None, devices: Optional[List[str]] = None) -> Dict[str, Any]:
        data = {"phrase": phrase}
        if regions:
            data["regions"] = regions
        if devices:
            data["devices"] = devices
        return self._make_request("/v1/topRequests", data)
    
    def get_dynamics(self, phrase: str, period: str = "weekly", from_date: Optional[str] = None, to_date: Optional[str] = None, regions: Optional[List[int]] = None, devices: Optional[List[str]] = None) -> Dict[str, Any]:
        data = {"phrase": phrase, "period": period}
        if from_date:
            data["fromDate"] = from_date
        if to_date:
            data["toDate"] = to_date
        if regions:
            data["regions"] = regions
        if devices:
            data["devices"] = devices
        return self._make_request("/v1/dynamics", data)
    
    def get_regions(self, phrase: str, devices: Optional[List[str]] = None) -> Dict[str, Any]:
        data = {"phrase": phrase}
        if devices:
            data["devices"] = devices
        return self._make_request("/v1/regions", data)


REGIONS = {
    "russia": 225,
    "moscow": 213,
    "moscow_region": 1,
    "saint_petersburg": 2,
    "novosibirsk": 65,
    "yekaterinburg": 54,
    "kazan": 43,
    "krasnodar": 35,
}
