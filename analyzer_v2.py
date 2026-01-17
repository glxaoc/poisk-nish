"""
Анализатор ниши v2.0
Интегрирует метрики, кластеры и формирует полный анализ
"""

from typing import Dict, List
from metrics import MetricsCalculator
from database import get_all_queries
from clusterer import clusterize


def analyze_niche_v2(phrase: str, region: int = 225) -> Dict:
    """
    Полный анализ ниши v2.0
    
    Returns:
        {
            "phrase": str,
            "region": int,
            "metrics": {...},       # size, competition, etc.
            "seasonality": {...},   # динамика, тренд
            "clusters": [...],      # кластеры с долями
            "verdict": {...},       # предварительный вердикт
            "insights": [...],      # текстовые выводы
        }
    """
    calc = MetricsCalculator()
    
    # 1. Получаем собранные запросы из БД
    queries = get_all_queries(region)
    if not queries:
        return {"error": "no_data", "phrase": phrase}
    
    total_count = sum(q.get('count', 0) for q in queries)
    
    # 2. Кластеризация
    cluster_result = clusterize(queries, phrase)
    clusters = cluster_result.get('clusters', [])
    
    # Считаем доли гео и маркетплейсов из кластеров
    geo_share = 0
    mp_share = 0
    for c in clusters:
        if c.get('name') == 'География':
            geo_share = c.get('share', 0)
        elif c.get('name') == 'Маркетплейсы':
            mp_share = c.get('share', 0)
    
    # 3. Региональный коэффициент
    region_coef, region_details = calc.get_region_coefficient(phrase, region)
    
    # 4. Сезонный коэффициент
    season_coef, season_details = calc.get_seasonality_coefficient(phrase, region)
    
    # 5. Размер ниши
    size_metrics = calc.calculate_size_metrics(total_count, region_coef, season_coef)
    
    # 6. Конкуренция
    comp_metrics = calc.calculate_competition_metrics(
        queries, clusters, mp_share=mp_share, geo_share=geo_share
    )
    
    # 7. Предварительный вердикт
    verdict = calc.determine_verdict(
        size_metrics['size_index'],
        comp_metrics['competition_index'],
        len(queries)
    )
    
    # 8. Формируем инсайты
    insights = generate_insights_v2(
        size_metrics, comp_metrics, season_details, 
        clusters, geo_share, mp_share
    )
    
    return {
        "phrase": phrase,
        "region": region,
        "total_count": total_count,
        "total_queries": len(queries),
        "clusters_count": len(clusters),
        
        # Новые метрики v2
        "size": size_metrics,
        "competition": comp_metrics,
        "seasonality": {
            "coefficient": season_coef,
            "current_month": season_details.get('current_month', 0),
            "average_month": season_details.get('average_month', 0),
            "trend": season_details.get('trend', 'unknown'),
            "peak_month": season_details.get('peak_month', ''),
            "dynamics": season_details.get('dynamics', []),
            "yearly_growth": season_details.get('yearly_growth', 0)
        },
        "region_info": region_details,
        
        # Вердикт и выводы
        "verdict": verdict,
        "insights": insights,
        
        # Кластеры
        "clusters": clusters,
        
        # Старые метрики для совместимости
        "metrics": {
            "total_count": total_count,
            "niche_size": size_metrics['size_label'],
            "niche_size_icon": size_metrics['size_icon'],
            "competition": comp_metrics['competition_label'],
            "competition_icon": comp_metrics['competition_icon'],
            "top3_share": comp_metrics['factors'].get('top3_concentration', 0),
            "geo_share": geo_share,
            "mp_share": mp_share,
            "brand_share": comp_metrics['factors'].get('brand_share', 0),
        }
    }


def generate_insights_v2(
    size: Dict, 
    competition: Dict, 
    seasonality: Dict,
    clusters: List[Dict],
    geo_share: float,
    mp_share: float
) -> List[Dict]:
    """Генерирует текстовые инсайты на основе метрик"""
    
    insights = []
    
    # 1. Размер ниши
    size_text = f"{size['raw_count']:,} запросов/мес"
    if size['season_coefficient'] < 0.8:
        size_text += f" (сейчас низкий сезон, обычно ×{1/size['season_coefficient']:.1f})"
    elif size['season_coefficient'] > 1.2:
        size_text += f" (сейчас высокий сезон)"
        
    insights.append({
        "icon": size['size_icon'],
        "title": f"{size['size_label']} ниша",
        "text": size_text,
        "index": size['size_index'],
        "type": "size"
    })
    
    # 2. Конкуренция
    comp_factors = competition['factors']
    comp_details = []
    if comp_factors.get('top3_concentration', 0) > 40:
        comp_details.append(f"топ-3 кластера = {comp_factors['top3_concentration']:.0f}%")
    if comp_factors.get('brand_share', 0) > 10:
        comp_details.append(f"бренды = {comp_factors['brand_share']:.0f}%")
    if comp_factors.get('found_brands'):
        comp_details.append(f"найдены: {', '.join(comp_factors['found_brands'][:5])}")
    
    insights.append({
        "icon": competition['competition_icon'],
        "title": f"Конкуренция: {competition['competition_label'].lower()}",
        "text": "; ".join(comp_details) if comp_details else "Умеренная концентрация спроса",
        "index": competition['competition_index'],
        "type": "competition"
    })
    
    # 3. Сезонность
    trend_labels = {
        "growing": ("📈", "растёт"),
        "declining": ("📉", "падает"),
        "stable": ("➡️", "стабильный"),
        "unknown": ("❓", "неизвестен")
    }
    trend_icon, trend_text = trend_labels.get(seasonality.get('trend', 'unknown'), ("❓", "?"))
    
    season_coef = seasonality.get('coefficient', 1.0)
    if season_coef < 0.7:
        season_text = f"Низкий сезон (×{season_coef:.2f} от среднего). Тренд: {trend_text}"
    elif season_coef > 1.3:
        season_text = f"Высокий сезон (×{season_coef:.2f} от среднего). Тренд: {trend_text}"
    else:
        season_text = f"Нормальный сезон. Тренд: {trend_text}"
    
    insights.append({
        "icon": trend_icon,
        "title": "Сезонность",
        "text": season_text,
        "type": "seasonality"
    })
    
    # 4. Топ направления
    if clusters:
        top3 = clusters[:3]
        top_names = [f"{c['name']} ({c['share']}%)" for c in top3]
        insights.append({
            "icon": "🎯",
            "title": "Топ направления",
            "text": ", ".join(top_names),
            "type": "clusters"
        })
    
    # 5. Гео-запросы
    if geo_share > 5:
        insights.append({
            "icon": "🌍",
            "title": "Локальный спрос",
            "text": f"{geo_share:.1f}% запросов с указанием города. Геотаргетинг эффективен.",
            "type": "geo"
        })
    
    # 6. Маркетплейсы
    if mp_share > 2:
        insights.append({
            "icon": "🛒",
            "title": "Маркетплейсы",
            "text": f"{mp_share:.1f}% ищут на WB, Ozon и др. Канал продаж актуален.",
            "type": "marketplace"
        })
    
    return insights


# ═══════════════════════════════════════════════════════════════
# ТЕСТ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json
    
    result = analyze_niche_v2("купить кроссовки", region=213)
    
    print("=== АНАЛИЗ НИШИ v2.0 ===\n")
    print(f"Фраза: {result.get('phrase')}")
    print(f"Регион: {result.get('region')}")
    print(f"Всего запросов: {result.get('total_count', 0):,}")
    print(f"Уникальных фраз: {result.get('total_queries', 0)}")
    print(f"Кластеров: {result.get('clusters_count', 0)}")
    
    print(f"\n--- Размер ниши ---")
    size = result.get('size', {})
    print(f"  Индекс: {size.get('size_index', 0)}/100")
    print(f"  Категория: {size.get('size_icon', '')} {size.get('size_label', '')}")
    print(f"  Нормализовано: {size.get('normalized_count', 0):,}")
    
    print(f"\n--- Конкуренция ---")
    comp = result.get('competition', {})
    print(f"  Индекс: {comp.get('competition_index', 0)}/100")
    print(f"  Категория: {comp.get('competition_icon', '')} {comp.get('competition_label', '')}")
    print(f"  Бренды: {comp.get('factors', {}).get('found_brands', [])}")
    
    print(f"\n--- Вердикт ---")
    verdict = result.get('verdict', {})
    print(f"  {verdict.get('verdict_icon', '')} {verdict.get('verdict_label', '')}")
    print(f"  Причина: {verdict.get('reason', '')}")
    
    print(f"\n--- Инсайты ---")
    for ins in result.get('insights', []):
        print(f"  {ins['icon']} {ins['title']}: {ins['text']}")
