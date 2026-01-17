"""
Модуль расчёта метрик v2.0
Размер ниши, конкуренция, сезонность
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from wordstat_client import WordstatClient
from config import (
    SIZE_THRESHOLDS, SIZE_LABELS, SIZE_INDEX_MAX,
    COMPETITION_WEIGHTS, COMPETITION_THRESHOLDS, COMPETITION_LABELS,
    BRAND_PATTERNS, VERDICT_LABELS, VERDICT_RULES
)


TOKEN = "y0__xCHu4rZARjd0Dogyfj_7RQJLwxI8zao8Pru2PA2l5w2HjR6dA"


class MetricsCalculator:
    """Калькулятор метрик ниши"""
    
    def __init__(self):
        self.client = WordstatClient(TOKEN)
        self._regions_cache = None
    
    # ═══════════════════════════════════════════════════════════
    # РЕГИОНАЛЬНЫЙ КОЭФФИЦИЕНТ
    # ═══════════════════════════════════════════════════════════
    
    def get_region_coefficient(self, phrase: str, region_id: int) -> Tuple[float, Dict]:
        """
        Рассчитывает региональный коэффициент для фразы.
        
        Коэффициент показывает, насколько спрос в регионе выше/ниже 
        среднего по России.
        
        Returns:
            (coefficient, details)
            coefficient: 1.0 = средний, >1 = выше среднего, <1 = ниже
        """
        try:
            result = self.client.get_regions(phrase)
            regions = result.get('regions', [])
            
            if not regions:
                return 1.0, {"error": "no_data"}
            
            # Находим данные по запрошенному региону и по России (225)
            total_count = sum(r.get('count', 0) for r in regions)
            russia_data = None
            region_data = None
            
            for r in regions:
                if r.get('regionId') == 225:
                    russia_data = r
                if r.get('regionId') == region_id:
                    region_data = r
            
            # Если запрос по всей России — коэффициент 1.0
            if region_id == 225:
                return 1.0, {
                    "region_name": "Россия",
                    "region_count": russia_data.get('count', 0) if russia_data else total_count,
                    "total_count": total_count,
                    "coefficient": 1.0
                }
            
            if not region_data:
                return 1.0, {"error": "region_not_found", "region_id": region_id}
            
            # Рассчитываем коэффициент
            # Сравниваем долю региона с его "нормальной" долей в общем трафике
            region_share = region_data.get('share', 0)
            affinity_index = region_data.get('affinityIndex', 100)
            
            # affinityIndex показывает интерес к теме в регионе
            # 100 = средний, >100 = выше среднего
            coefficient = affinity_index / 100.0
            
            return coefficient, {
                "region_id": region_id,
                "region_count": region_data.get('count', 0),
                "region_share": round(region_share * 100, 2),
                "affinity_index": round(affinity_index, 1),
                "coefficient": round(coefficient, 2),
                "total_count": total_count
            }
            
        except Exception as e:
            return 1.0, {"error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # СЕЗОННЫЙ КОЭФФИЦИЕНТ
    # ═══════════════════════════════════════════════════════════
    
    def get_seasonality_coefficient(self, phrase: str, region_id: int = 225) -> Tuple[float, Dict]:
        """
        Рассчитывает сезонный коэффициент.
        
        Коэффициент = текущий месяц / среднее за год
        >1 = сейчас спрос выше среднего (хорошее время)
        <1 = сейчас спрос ниже среднего
        
        Returns:
            (coefficient, details)
        """
        try:
            # Период: последние 12 месяцев
            now = datetime.now()
            
            # to_date = последний день прошлого месяца
            to_dt = now.replace(day=1) - timedelta(days=1)
            to_date = to_dt.strftime("%Y-%m-%d")
            
            # from_date = первый день 12 месяцев назад
            from_dt = to_dt.replace(day=1)
            for _ in range(11):
                from_dt = (from_dt - timedelta(days=1)).replace(day=1)
            from_date = from_dt.strftime("%Y-%m-%d")
            
            result = self.client.get_dynamics(
                phrase,
                period="monthly",
                from_date=from_date,
                to_date=to_date,
                regions=[region_id] if region_id != 225 else None
            )
            
            dynamics = result.get('dynamics', [])
            
            if not dynamics:
                return 1.0, {"error": "no_data"}
            
            counts = [d.get('count', 0) for d in dynamics]
            average = sum(counts) / len(counts) if counts else 1
            current = counts[-1] if counts else 0
            
            # Находим пики и спады
            max_month = max(dynamics, key=lambda x: x.get('count', 0))
            min_month = min(dynamics, key=lambda x: x.get('count', 0))
            
            coefficient = current / average if average > 0 else 1.0
            
            # Определяем тренд (растёт/падает)
            if len(counts) >= 3:
                recent_avg = sum(counts[-3:]) / 3
                earlier_avg = sum(counts[:3]) / 3
                trend = "growing" if recent_avg > earlier_avg * 1.1 else \
                        "declining" if recent_avg < earlier_avg * 0.9 else "stable"
            else:
                trend = "unknown"
            
            # Рост за год (сравниваем последний месяц с первым)
            if len(counts) >= 2 and counts[0] > 0:
                yearly_growth = round(((counts[-1] / counts[0]) - 1) * 100, 1)
            else:
                yearly_growth = 0.0
            
            return round(coefficient, 2), {
                "current_month": current,
                "average_month": round(average),
                "coefficient": round(coefficient, 2),
                "peak_month": max_month.get('date', ''),
                "peak_count": max_month.get('count', 0),
                "low_month": min_month.get('date', ''),
                "low_count": min_month.get('count', 0),
                "trend": trend,
                "yearly_growth": yearly_growth,
                "dynamics": dynamics
            }
            
        except Exception as e:
            return 1.0, {"error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # РАЗМЕР НИШИ
    # ═══════════════════════════════════════════════════════════
    
    def calculate_size_metrics(
        self, 
        total_count: int,
        region_coef: float = 1.0,
        season_coef: float = 1.0
    ) -> Dict:
        """
        Рассчитывает метрики размера ниши.
        
        Args:
            total_count: сумма частотностей всех запросов
            region_coef: региональный коэффициент (из get_region_coefficient)
            season_coef: сезонный коэффициент (из get_seasonality_coefficient)
        
        Returns:
            {
                "raw_count": исходное значение,
                "normalized_count": нормализованное,
                "size_index": 0-100,
                "size_label": "Средняя",
                "size_icon": "📊"
            }
        """
        # Нормализация с учётом региона и сезона
        # Если регион < 1 (низкий affinity), увеличиваем оценку
        # Если сезон < 1 (низкий сезон), увеличиваем оценку
        normalized = total_count / region_coef / season_coef if region_coef > 0 and season_coef > 0 else total_count
        
        # Индекс 0-100
        size_index = min(100, (normalized / SIZE_INDEX_MAX) * 100)
        
        # Определяем категорию
        if normalized < SIZE_THRESHOLDS["micro"]:
            size_key = "micro"
        elif normalized < SIZE_THRESHOLDS["small"]:
            size_key = "small"
        elif normalized < SIZE_THRESHOLDS["medium"]:
            size_key = "medium"
        elif normalized < SIZE_THRESHOLDS["large"]:
            size_key = "large"
        else:
            size_key = "huge"
        
        label, icon = SIZE_LABELS[size_key]
        
        return {
            "raw_count": total_count,
            "normalized_count": round(normalized),
            "size_index": round(size_index, 1),
            "size_key": size_key,
            "size_label": label,
            "size_icon": icon,
            "region_coefficient": region_coef,
            "season_coefficient": season_coef
        }
    
    # ═══════════════════════════════════════════════════════════
    # КОНКУРЕНЦИЯ
    # ═══════════════════════════════════════════════════════════
    
    def calculate_brand_share(self, queries: List[Dict]) -> Tuple[float, List[str]]:
        """Рассчитывает долю брендовых запросов"""
        if not queries:
            return 0.0, []
        
        total_count = sum(q.get('count', 0) for q in queries)
        brand_count = 0
        found_brands = set()
        
        for q in queries:
            phrase_lower = q.get('phrase', '').lower()
            for brand in BRAND_PATTERNS:
                if brand in phrase_lower:
                    brand_count += q.get('count', 0)
                    found_brands.add(brand)
                    break
        
        share = (brand_count / total_count * 100) if total_count > 0 else 0
        return round(share, 1), list(found_brands)
    
    def calculate_competition_metrics(
        self,
        queries: List[Dict],
        clusters: List[Dict],
        mp_share: float = 0.0,
        geo_share: float = 0.0
    ) -> Dict:
        """
        Рассчитывает метрики конкуренции.
        
        Args:
            queries: список запросов с count
            clusters: список кластеров с share
            mp_share: доля маркетплейс-запросов (уже рассчитана)
            geo_share: доля гео-запросов
        """
        if not queries or not clusters:
            return {
                "competition_index": 50,
                "competition_label": "Средняя",
                "competition_icon": "🟡",
                "factors": {}
            }
        
        total_count = sum(q.get('count', 0) for q in queries)
        
        # 1. Концентрация в топ-3 кластерах
        top3_share = sum(c.get('share', 0) for c in clusters[:3])
        
        # 2. Доля брендов
        brand_share, found_brands = self.calculate_brand_share(queries)
        
        # 3. Плотность (запросов на кластер)
        density = total_count / len(clusters) if clusters else 0
        
        # Рассчитываем индекс конкуренции
        # top3_share уже в процентах (0-100)
        competition_index = (
            top3_share * COMPETITION_WEIGHTS["top3_concentration"] +
            brand_share * COMPETITION_WEIGHTS["brand_share"] +
            mp_share * COMPETITION_WEIGHTS["mp_share"]
        )
        
        # Определяем категорию
        if competition_index < COMPETITION_THRESHOLDS["low"]:
            comp_key = "low"
        elif competition_index < COMPETITION_THRESHOLDS["medium"]:
            comp_key = "medium"
        elif competition_index < COMPETITION_THRESHOLDS["high"]:
            comp_key = "high"
        else:
            comp_key = "very_high"
        
        label, icon = COMPETITION_LABELS[comp_key]
        
        return {
            "competition_index": round(competition_index, 1),
            "competition_key": comp_key,
            "competition_label": label,
            "competition_icon": icon,
            "factors": {
                "top3_concentration": round(top3_share, 1),
                "brand_share": brand_share,
                "mp_share": round(mp_share, 1),
                "density": round(density),
                "found_brands": found_brands[:10]  # топ-10 брендов
            }
        }
    
    # ═══════════════════════════════════════════════════════════
    # ВЕРДИКТ
    # ═══════════════════════════════════════════════════════════
    
    def determine_verdict(
        self,
        size_index: float,
        competition_index: float,
        queries_count: int
    ) -> Dict:
        """
        Определяет предварительный вердикт по нише.
        
        Returns:
            {"verdict": "conditional", "verdict_label": "...", "verdict_icon": "⚠️"}
        """
        # Мало данных
        if queries_count < 50:
            return {
                "verdict": "uncertain",
                "verdict_label": VERDICT_LABELS["uncertain"][0],
                "verdict_icon": VERDICT_LABELS["uncertain"][1],
                "reason": "Недостаточно данных для анализа"
            }
        
        rules = VERDICT_RULES
        
        # Рекомендуется
        if size_index >= rules["recommended"]["min_size"] and \
           competition_index <= rules["recommended"]["max_competition"]:
            return {
                "verdict": "recommended",
                "verdict_label": VERDICT_LABELS["recommended"][0],
                "verdict_icon": VERDICT_LABELS["recommended"][1],
                "reason": "Достаточный размер и умеренная конкуренция"
            }
        
        # Не рекомендуется
        if size_index <= rules["not_recommended"]["max_size"] or \
           competition_index >= rules["not_recommended"]["min_competition"]:
            return {
                "verdict": "not_recommended",
                "verdict_label": VERDICT_LABELS["not_recommended"][0],
                "verdict_icon": VERDICT_LABELS["not_recommended"][1],
                "reason": "Слишком маленький рынок или высокая конкуренция"
            }
        
        # С ограничениями (всё остальное)
        return {
            "verdict": "conditional",
            "verdict_label": VERDICT_LABELS["conditional"][0],
            "verdict_icon": VERDICT_LABELS["conditional"][1],
            "reason": "Есть возможности, но требуется стратегия"
        }


# ═══════════════════════════════════════════════════════════════
# ТЕСТ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json
    
    calc = MetricsCalculator()
    
    phrase = "купить кроссовки"
    region = 213  # Москва
    
    print(f"=== Метрики для '{phrase}' (регион {region}) ===\n")
    
    # 1. Региональный коэффициент
    region_coef, region_details = calc.get_region_coefficient(phrase, region)
    print(f"Региональный коэф: {region_coef}")
    print(f"  Детали: {json.dumps(region_details, ensure_ascii=False)}\n")
    
    # 2. Сезонный коэффициент
    season_coef, season_details = calc.get_seasonality_coefficient(phrase, region)
    print(f"Сезонный коэф: {season_coef}")
    print(f"  Текущий месяц: {season_details.get('current_month', 0):,}")
    print(f"  Среднее: {season_details.get('average_month', 0):,}")
    print(f"  Тренд: {season_details.get('trend', '?')}\n")
    
    # 3. Размер ниши (тестовые данные)
    test_total = 139_000
    size_metrics = calc.calculate_size_metrics(test_total, region_coef, season_coef)
    print(f"Размер ниши:")
    print(f"  Raw: {size_metrics['raw_count']:,}")
    print(f"  Normalized: {size_metrics['normalized_count']:,}")
    print(f"  Index: {size_metrics['size_index']}/100")
    print(f"  Label: {size_metrics['size_icon']} {size_metrics['size_label']}\n")
    
    # 4. Конкуренция (тестовые данные)
    test_queries = [{"phrase": "nike кроссовки", "count": 1000}, {"phrase": "кроссовки", "count": 5000}]
    test_clusters = [{"name": "test", "share": 40}]
    comp_metrics = calc.calculate_competition_metrics(test_queries, test_clusters, mp_share=3.0)
    print(f"Конкуренция:")
    print(f"  Index: {comp_metrics['competition_index']}/100")
    print(f"  Label: {comp_metrics['competition_icon']} {comp_metrics['competition_label']}")
    print(f"  Бренды: {comp_metrics['factors']['found_brands']}\n")
    
    # 5. Вердикт
    verdict = calc.determine_verdict(
        size_metrics['size_index'],
        comp_metrics['competition_index'],
        len(test_queries)
    )
    print(f"Вердикт: {verdict['verdict_icon']} {verdict['verdict_label']}")
    print(f"  Причина: {verdict['reason']}")
