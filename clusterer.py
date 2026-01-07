"""
Модуль кластеризации запросов
Группирует запросы по смыслу на основе ключевых слов
"""

from typing import List, Dict, Set
from collections import defaultdict
import re

# Стоп-слова — убираем из анализа
STOP_WORDS = {
    # Коммерческие
    'купить', 'куплю', 'покупка', 'заказать', 'заказ',
    'цена', 'цены', 'ценой', 'стоимость', 'стоит',
    'недорого', 'дешево', 'дёшево', 'дешевый', 'дешёвый',
    'скидка', 'скидки', 'акция', 'распродажа',
    'доставка', 'доставкой',
    
    # Где купить
    'магазин', 'магазине', 'интернет',
    'онлайн', 'сайт', 'официальный',
    
    # Предлоги и союзы
    'в', 'на', 'с', 'со', 'из', 'от', 'до', 'для', 'по', 'за', 'к', 'у',
    'и', 'или', 'а', 'но', 'что', 'как', 'где', 'когда', 'какой', 'какая', 'какие',
    
    # Местоимения
    'мне', 'мой', 'моя', 'мои', 'свой', 'своя', 'свои',
    
    # Прочее
    'можно', 'нужно', 'лучше', 'лучший', 'лучшие', 'хороший', 'хорошая', 'хорошие',
    'новый', 'новая', 'новые', '2024', '2025', '2026',
    'год', 'года', 'году',
}

# Города — выделяем в отдельный кластер "География"
CITIES = {
    'москва', 'москве', 'московский', 'мск',
    'спб', 'питер', 'петербург', 'санкт',
    'новосибирск', 'екатеринбург', 'казань', 'краснодар',
    'нижний', 'самара', 'омск', 'ростов', 'воронеж', 'пермь',
    'волгоград', 'красноярск', 'уфа', 'челябинск', 'тюмень',
}

# Маркетплейсы — отдельный кластер "Площадки"
MARKETPLACES = {
    'wildberries', 'вайлдберриз', 'вб', 'wb',
    'ozon', 'озон',
    'яндекс', 'маркет', 'yandex',
    'авито', 'avito',
    'aliexpress', 'алиэкспресс', 'али',
}


def extract_keywords(phrase: str) -> List[str]:
    """Извлечь значимые слова из фразы"""
    # Приводим к нижнему регистру и разбиваем
    words = re.findall(r'[а-яёa-z0-9]+', phrase.lower())
    
    # Фильтруем стоп-слова и короткие слова
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    
    return keywords


def detect_category(phrase: str) -> str:
    """Определить категорию фразы"""
    phrase_lower = phrase.lower()
    
    # Проверяем на города
    for city in CITIES:
        if city in phrase_lower:
            return "geo"
    
    # Проверяем на маркетплейсы
    for mp in MARKETPLACES:
        if mp in phrase_lower:
            return "marketplace"
    
    return "other"


def clusterize(queries: List[Dict], root_phrase: str = "") -> Dict:
    """
    Кластеризация запросов по ключевым словам
    
    Args:
        queries: Список запросов [{"phrase": "...", "count": N}, ...]
        root_phrase: Корневая фраза (её слова тоже исключаем)
    
    Returns:
        Структура кластеров с метриками
    """
    # Добавляем слова корневой фразы в стоп-слова
    root_words = set(extract_keywords(root_phrase))
    local_stop_words = STOP_WORDS | root_words
    
    # Собираем статистику по словам
    word_stats = defaultdict(lambda: {"count": 0, "phrases": []})
    
    # Отдельные кластеры для гео и маркетплейсов
    geo_cluster = {"count": 0, "phrases": []}
    marketplace_cluster = {"count": 0, "phrases": []}
    
    total_count = 0
    
    for q in queries:
        phrase = q.get("phrase", "")
        count = q.get("count", 0)
        total_count += count
        
        # Определяем категорию
        category = detect_category(phrase)
        
        if category == "geo":
            geo_cluster["count"] += count
            geo_cluster["phrases"].append({"phrase": phrase, "count": count})
            continue
        
        if category == "marketplace":
            marketplace_cluster["count"] += count
            marketplace_cluster["phrases"].append({"phrase": phrase, "count": count})
            continue
        
        # Извлекаем ключевые слова
        words = re.findall(r'[а-яёa-z0-9]+', phrase.lower())
        keywords = [w for w in words if w not in local_stop_words and len(w) > 2]
        
        # Считаем статистику для каждого слова
        for word in keywords:
            word_stats[word]["count"] += count
            word_stats[word]["phrases"].append({"phrase": phrase, "count": count})
    
    # Формируем кластеры из топ слов
    clusters = []
    used_phrases = set()
    
    # Сортируем слова по суммарной частотности
    sorted_words = sorted(word_stats.items(), key=lambda x: x[1]["count"], reverse=True)
    
    for word, data in sorted_words[:20]:  # Топ-20 кластеров
        # Фильтруем уже использованные фразы
        unique_phrases = [p for p in data["phrases"] if p["phrase"] not in used_phrases]
        
        if not unique_phrases:
            continue
        
        cluster_count = sum(p["count"] for p in unique_phrases)
        
        if cluster_count < total_count * 0.01:  # Минимум 1% от общего
            continue
        
        clusters.append({
            "name": word,
            "count": cluster_count,
            "share": round(cluster_count / total_count * 100, 1) if total_count > 0 else 0,
            "phrases": sorted(unique_phrases, key=lambda x: x["count"], reverse=True)[:10]
        })
        
        # Помечаем фразы как использованные
        for p in unique_phrases:
            used_phrases.add(p["phrase"])
    
    # Добавляем гео-кластер если есть
    if geo_cluster["count"] > 0:
        geo_cluster["name"] = "🌍 География"
        geo_cluster["share"] = round(geo_cluster["count"] / total_count * 100, 1) if total_count > 0 else 0
        geo_cluster["phrases"] = sorted(geo_cluster["phrases"], key=lambda x: x["count"], reverse=True)[:10]
        clusters.append(geo_cluster)
    
    # Добавляем маркетплейс-кластер если есть
    if marketplace_cluster["count"] > 0:
        marketplace_cluster["name"] = "🛒 Маркетплейсы"
        marketplace_cluster["share"] = round(marketplace_cluster["count"] / total_count * 100, 1) if total_count > 0 else 0
        marketplace_cluster["phrases"] = sorted(marketplace_cluster["phrases"], key=lambda x: x["count"], reverse=True)[:10]
        clusters.append(marketplace_cluster)
    
    # Сортируем кластеры по доле
    clusters = sorted(clusters, key=lambda x: x["count"], reverse=True)
    
    return {
        "total_count": total_count,
        "total_queries": len(queries),
        "clusters": clusters,
        "clusters_count": len(clusters)
    }


if __name__ == "__main__":
    # Тест
    test_queries = [
        {"phrase": "купить самокат", "count": 28897},
        {"phrase": "купить самокат электрический", "count": 5000},
        {"phrase": "купить самокат детский", "count": 3000},
        {"phrase": "купить самокат в москве", "count": 2000},
        {"phrase": "купить самокат на wildberries", "count": 1500},
    ]
    
    result = clusterize(test_queries, "купить самокат")
    print(f"Всего: {result['total_count']:,} запросов")
    print(f"Кластеров: {result['clusters_count']}")
    for c in result["clusters"]:
        print(f"  {c['name']}: {c['count']:,} ({c['share']}%)")
