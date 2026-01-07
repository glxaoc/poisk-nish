"""
Модуль аналитики и генерации выводов
"""

from typing import List, Dict


def analyze_niche(queries: List[Dict], clusters: Dict, phrase: str) -> Dict:
    """
    Полный анализ ниши с выводами
    """
    total_count = clusters["total_count"]
    total_queries = clusters["total_queries"]
    cluster_list = clusters["clusters"]
    
    # Метрики
    metrics = calculate_metrics(total_count, total_queries, cluster_list)
    
    # Инсайты
    insights = generate_insights(phrase, metrics, cluster_list)
    
    # Рекомендации
    recommendations = generate_recommendations(metrics, cluster_list)
    
    # Текстовый вывод
    summary = generate_summary(phrase, metrics, cluster_list)
    
    return {
        "metrics": metrics,
        "insights": insights,
        "recommendations": recommendations,
        "summary": summary
    }


def calculate_metrics(total_count: int, total_queries: int, clusters: List[Dict]) -> Dict:
    """Расчёт ключевых метрик"""
    
    # Средняя частотность
    avg_freq = total_count // total_queries if total_queries > 0 else 0
    
    # Концентрация (топ-3)
    top3_share = sum(c["share"] for c in clusters[:3]) if len(clusters) >= 3 else 100
    
    # Специальные кластеры
    geo = next((c for c in clusters if "География" in c["name"]), None)
    mp = next((c for c in clusters if "Маркетплейс" in c["name"]), None)
    
    # Размер ниши
    if total_count >= 500000:
        size, size_icon = "крупная", "🔥"
    elif total_count >= 100000:
        size, size_icon = "средняя", "📈"
    elif total_count >= 10000:
        size, size_icon = "небольшая", "📊"
    else:
        size, size_icon = "микро", "🔍"
    
    # Конкуренция
    if top3_share >= 60:
        competition, comp_icon = "высокая", "🔴"
    elif top3_share >= 40:
        competition, comp_icon = "средняя", "🟡"
    else:
        competition, comp_icon = "низкая", "🟢"
    
    return {
        "total_count": total_count,
        "total_queries": total_queries,
        "avg_frequency": avg_freq,
        "clusters_count": len(clusters),
        "top3_share": round(top3_share, 1),
        "geo_share": geo["share"] if geo else 0,
        "mp_share": mp["share"] if mp else 0,
        "niche_size": size,
        "niche_size_icon": size_icon,
        "competition": competition,
        "competition_icon": comp_icon
    }


def generate_insights(phrase: str, metrics: Dict, clusters: List[Dict]) -> List[Dict]:
    """Генерация инсайтов"""
    
    insights = []
    
    # Размер ниши
    insights.append({
        "icon": metrics["niche_size_icon"],
        "type": "size",
        "title": f"{metrics['niche_size'].capitalize()} ниша",
        "text": f"{metrics['total_count']:,} запросов/мес — это {metrics['niche_size']} объём для рынка."
    })
    
    # Структура
    if len(clusters) >= 3:
        top3 = ", ".join(c["name"] for c in clusters[:3])
        insights.append({
            "icon": "📊",
            "type": "structure", 
            "title": "Топ направления",
            "text": f"{top3}. На них приходится {metrics['top3_share']}% спроса."
        })
    
    # География
    if metrics["geo_share"] > 5:
        insights.append({
            "icon": "🌍",
            "type": "geo",
            "title": "Локальный спрос",
            "text": f"{metrics['geo_share']}% ищут с указанием города. Работает геотаргетинг."
        })
    
    # Маркетплейсы
    if metrics["mp_share"] > 2:
        insights.append({
            "icon": "🛒",
            "type": "marketplace",
            "title": "Маркетплейсы",
            "text": f"{metrics['mp_share']}% ищут на WB, Ozon и других площадках."
        })
    
    # Конкуренция
    insights.append({
        "icon": metrics["competition_icon"],
        "type": "competition",
        "title": f"Конкуренция: {metrics['competition']}",
        "text": f"Концентрация спроса в топ-3: {metrics['top3_share']}%."
    })
    
    return insights


def generate_recommendations(metrics: Dict, clusters: List[Dict]) -> List[Dict]:
    """Генерация рекомендаций"""
    
    recs = []
    
    # По размеру
    if metrics["niche_size"] == "крупная":
        recs.append({
            "icon": "🎯",
            "text": "Большая ниша — выберите узкую специализацию для старта"
        })
    elif metrics["niche_size"] == "микро":
        recs.append({
            "icon": "🔎",
            "text": "Малый спрос — проверьте смежные ниши или расширьте запрос"
        })
    
    # По конкуренции
    if metrics["top3_share"] >= 50 and len(clusters) > 5:
        small = [c["name"] for c in clusters[3:6] if c["share"] >= 1.5]
        if small:
            recs.append({
                "icon": "💡",
                "text": f"Менее конкурентные направления: {', '.join(small)}"
            })
    
    # По географии
    if metrics["geo_share"] > 5:
        recs.append({
            "icon": "📍",
            "text": "Используйте геотаргетинг — есть локальный спрос"
        })
    
    # По маркетплейсам
    if metrics["mp_share"] > 3:
        recs.append({
            "icon": "🛒",
            "text": "Выходите на Wildberries и Ozon — там ищут ваш товар"
        })
    elif metrics["mp_share"] < 1 and metrics["total_count"] > 50000:
        recs.append({
            "icon": "🏪",
            "text": "Мало ищут на МП — возможность для своего магазина"
        })
    
    # Общая
    if len(clusters) >= 8:
        recs.append({
            "icon": "📋",
            "text": "Много подниш — выберите 2-3 для фокусировки"
        })
    
    return recs


def generate_summary(phrase: str, metrics: Dict, clusters: List[Dict]) -> str:
    """Текстовый вывод"""
    
    lines = [
        f"📊 **Ниша:** {phrase}",
        f"",
        f"**Объём:** {metrics['total_count']:,} запросов/мес ({metrics['niche_size']})",
        f"**Фраз:** {metrics['total_queries']:,} уникальных",
        f"**Направлений:** {metrics['clusters_count']}",
        f"**Концентрация:** {metrics['top3_share']}% в топ-3",
        f"",
        f"**Топ-5 направлений:**"
    ]
    
    for i, c in enumerate(clusters[:5], 1):
        lines.append(f"{i}. {c['name']} — {c['share']}%")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("analyzer.py loaded OK")
