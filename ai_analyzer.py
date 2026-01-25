"""
Модуль ИИ-анализа ниши через OpenAI Proxy (NL сервер)
Интерпретирует данные, не генерирует цифры
"""

import requests
import logging
import json

# Прокси на сервере в Нидерландах
PROXY_URL = "http://91.132.59.183:5050/analyze"
SECRET_KEY = "wordstat-proxy-2026"


def generate_ai_analysis(phrase: str, metrics: dict, clusters: list) -> dict:
    """
    Генерирует ИИ-анализ ниши через прокси
    
    Returns:
        {
            "summary": str,      # Главный вывод о нише
            "scenarios": list,   # Сценарии входа
            "risks": list        # Риски
        }
    """
    
    try:
        response = requests.post(
            PROXY_URL,
            json={
                "phrase": phrase,
                "metrics": metrics,
                "clusters": clusters
            },
            headers={"X-Api-Key": SECRET_KEY},
            timeout=90
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"AI Proxy HTTP error {response.status_code} for phrase: {phrase}")
            return {
                "summary": "Ошибка при обращении к ИИ.",
                "scenarios": [],
                "risks": [],
                "_error": f"HTTP {response.status_code}"
            }
            
    except requests.Timeout:
        logging.error(f"AI Proxy timeout for phrase: {phrase}")
        return {
            "summary": "Превышено время ожидания ответа от ИИ.",
            "scenarios": [],
            "risks": [],
            "_error": "Timeout"
        }
    except Exception as e:
        logging.error(f"AI Proxy error for phrase '{phrase}': {type(e).__name__}: {str(e)}")
        return {
            "summary": "Ошибка соединения с ИИ-сервисом.",
            "scenarios": [],
            "risks": [],
            "_error": f"{type(e).__name__}: {str(e)}"
        }


if __name__ == "__main__":
    # Тест
    test_metrics = {
        "total_count": 140000,
        "total_queries": 374,
        "niche_size": "средняя",
        "top3_share": 28.0,
        "geo_share": 5.2,
        "mp_share": 0.8
    }
    
    test_clusters = [
        {"name": "кровли", "share": 20.1, "count": 28264},
        {"name": "мягкая", "share": 4.5, "count": 6384},
        {"name": "плоская", "share": 3.4, "count": 4861},
        {"name": "ремонт", "share": 3.1, "count": 4381},
    ]
    
    result = generate_ai_analysis("кровля", test_metrics, test_clusters)
    print(json.dumps(result, ensure_ascii=False, indent=2))
