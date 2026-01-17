"""
Конфигурация расчётов v2.0
Все пороги и веса вынесены сюда для удобного тюнинга
"""

# ═══════════════════════════════════════════════════════════════
# РАЗМЕР НИШИ
# ═══════════════════════════════════════════════════════════════

# Пороги размера (применяются к нормализованному значению)
SIZE_THRESHOLDS = {
    "micro": 10_000,      # < 10k — микрониша
    "small": 30_000,      # 10k-30k — маленькая
    "medium": 150_000,    # 30k-150k — средняя
    "large": 300_000,     # 150k-300k — крупная
    # > 300k — очень крупная
}

SIZE_LABELS = {
    "micro": ("Микрониша", "🔹"),
    "small": ("Небольшая", "🔸"),
    "medium": ("Средняя", "📊"),
    "large": ("Крупная", "🔥"),
    "huge": ("Очень крупная", "💎"),
}

# Максимум для расчёта индекса 0-100
SIZE_INDEX_MAX = 500_000


# ═══════════════════════════════════════════════════════════════
# КОНКУРЕНЦИЯ
# ═══════════════════════════════════════════════════════════════

# Веса факторов конкуренции
COMPETITION_WEIGHTS = {
    "top3_concentration": 0.50,  # Концентрация в топ-3
    "brand_share": 0.30,         # Доля брендов
    "mp_share": 0.20,            # Доля маркетплейсов
}

# Пороги конкуренции (индекс 0-100)
COMPETITION_THRESHOLDS = {
    "low": 30,        # < 30 — низкая
    "medium": 50,     # 30-50 — средняя
    "high": 70,       # 50-70 — высокая
    # > 70 — очень высокая
}

COMPETITION_LABELS = {
    "low": ("Низкая", "🟢"),
    "medium": ("Средняя", "🟡"),
    "high": ("Высокая", "🟠"),
    "very_high": ("Очень высокая", "🔴"),
}


# ═══════════════════════════════════════════════════════════════
# БРЕНДЫ
# ═══════════════════════════════════════════════════════════════

# Популярные бренды по категориям
BRAND_PATTERNS = {
    # Обувь/одежда
    "nike", "adidas", "puma", "reebok", "new balance", "asics",
    "fila", "converse", "vans", "skechers", "salomon", "ecco",
    "timberland", "dr martens", "crocs", "geox", "columbia",
    
    # Электроника
    "apple", "samsung", "xiaomi", "huawei", "honor", "realme",
    "oppo", "vivo", "oneplus", "sony", "lg", "philips", "bosch",
    "dyson", "tefal", "braun", "panasonic", "jbl", "bose",
    
    # Авто
    "toyota", "volkswagen", "bmw", "mercedes", "audi", "kia",
    "hyundai", "skoda", "ford", "renault", "nissan", "mazda",
    
    # Общие
    "ikea", "zara", "h&m", "uniqlo", "mango", "lego",
}


# ═══════════════════════════════════════════════════════════════
# ВЕРДИКТЫ AI
# ═══════════════════════════════════════════════════════════════

VERDICT_RULES = {
    # (size_index, competition_index) → verdict
    "recommended": {
        "min_size": 20,
        "max_competition": 50,
    },
    "conditional": {
        "min_size": 10,
        "max_competition": 70,
    },
    "not_recommended": {
        "max_size": 10,
        "min_competition": 70,
    },
}

VERDICT_LABELS = {
    "recommended": ("Подходит для входа", "✅"),
    "conditional": ("Подходит с ограничениями", "⚠️"),
    "not_recommended": ("Не рекомендуется", "❌"),
    "uncertain": ("Неопределённо", "❓"),
}
