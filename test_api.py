#!/usr/bin/env python3
"""
Тест Wordstat API - все методы
"""

import requests
import json
import sys
from datetime import datetime

TOKEN = "y0__xCHu4rZARjd0Dogyfj_7RQJLwxI8zao8Pru2PA2l5w2HjR6dA"
BASE_URL = "https://api.wordstat.yandex.net"

headers = {
    "Content-Type": "application/json;charset=utf-8",
    "Authorization": f"Bearer {TOKEN}"
}

def test_user_info():
    print("\n" + "=" * 60)
    print("ТЕСТ 1: Проверка авторизации (userInfo)")
    print("=" * 60)
    
    response = requests.post(f"{BASE_URL}/v1/userInfo", headers=headers, json={}, timeout=30)
    
    if response.status_code == 200:
        print("✅ Авторизация успешна!")
        data = response.json()
        info = data.get("userInfo", {})
        print(f"   Логин: {info.get('login')}")
        print(f"   Лимит/сек: {info.get('limitPerSecond')}")
        print(f"   Лимит/день: {info.get('dailyLimit')}")
        print(f"   Осталось: {info.get('dailyLimitRemaining')}")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

def test_top_requests():
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Топ запросов 'купить телефон' (Москва)")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/v1/topRequests",
        headers=headers,
        json={"phrase": "купить телефон", "regions": [213]},
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Запрос успешен!")
        data = response.json()
        print(f"\n   Всего запросов: {data.get('totalCount', 0):,}")
        print("\n   Топ-5 запросов:")
        for i, item in enumerate(data.get('topRequests', [])[:5], 1):
            print(f"     {i}. {item['phrase']}: {item['count']:,}")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

def test_dynamics():
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Динамика 'iphone' за 2025 год")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/v1/dynamics",
        headers=headers,
        json={
            "phrase": "iphone",
            "period": "monthly",
            "fromDate": "2025-01-01",
            "toDate": "2025-11-30"
        },
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Запрос успешен!")
        data = response.json()
        print("\n   Динамика по месяцам:")
        for point in data.get('dynamics', []):
            month = point['date'][:7]
            print(f"     {month}: {point['count']:,} ({point['share']:.2%})")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

def test_regions():
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Регионы 'доставка еды'")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/v1/regions",
        headers=headers,
        json={"phrase": "доставка еды"},
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Запрос успешен!")
        data = response.json()
        regions = data.get('regions', [])[:5]
        print("\n   Топ-5 регионов:")
        for i, r in enumerate(regions, 1):
            print(f"     {i}. ID {r['regionId']}: {r['count']:,} ({r['share']:.2%})")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🔍 WORDSTAT API - ПОЛНОЕ ТЕСТИРОВАНИЕ")
    print("=" * 60)
    print(f"   Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Токен: {TOKEN[:15]}...")
    
    tests = [
        ("userInfo", test_user_info),
        ("topRequests", test_top_requests),
        ("dynamics", test_dynamics),
        ("regions", test_regions),
    ]
    
    results = []
    for name, func in tests:
        try:
            results.append((name, func()))
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 ИТОГИ")
    print("=" * 60)
    
    for name, ok in results:
        print(f"   {'✅' if ok else '❌'} {name}")
    
    passed = sum(1 for _, ok in results if ok)
    print(f"\n   Пройдено: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")

if __name__ == "__main__":
    main()
