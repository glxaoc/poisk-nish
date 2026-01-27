# templates_home.py
# v6.0.6 - Hero-блок: короткий заголовок, уточнённый подзаголовок

def render_home_page():
    """Рендерит главную страницу сервиса"""
    
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Поиск ниш — Аналитика спроса на данных Wordstat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f8f9fa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            color: #1a1a1a;
        }
        
        .container {
            background: white;
            border-radius: 12px;
            padding: 56px 48px;
            max-width: 680px;
            width: 100%;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }
        
        h1 {
            font-size: 36px;
            color: #1a1a1a;
            margin-bottom: 20px;
            font-weight: 600;
            line-height: 1.3;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            font-size: 17px;
            color: #6b7280;
            margin-bottom: 32px;
            line-height: 1.5;
        }
        
        .cta-button {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 14px 32px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 16px;
            font-weight: 500;
            transition: background 0.2s ease;
            border: none;
            cursor: pointer;
        }
        
        .cta-button:hover {
            background: #1d4ed8;
        }
        
        .cta-hints {
            margin-top: 16px;
            font-size: 13px;
            color: #9ca3af;
            line-height: 1.6;
        }
        
        .cta-hints span {
            display: inline-block;
            margin-right: 12px;
        }
        
        .cta-hints span:before {
            content: "•";
            margin-right: 8px;
            color: #d1d5db;
        }
        
        .example-section {
            margin-top: 48px;
            padding-top: 40px;
            border-top: 1px solid #e5e7eb;
        }
        
        .example-title {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        .example-table {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .example-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 16px;
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
        }
        
        .example-row:last-child {
            border-bottom: none;
        }
        
        .example-row.header {
            background: #f3f4f6;
            font-weight: 500;
            color: #374151;
            font-size: 13px;
        }
        
        .example-cluster {
            flex: 1;
            color: #1f2937;
        }
        
        .example-count {
            color: #6b7280;
            text-align: right;
            min-width: 80px;
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid #e5e7eb;
            font-size: 13px;
            color: #9ca3af;
            text-align: center;
        }
        
        .footer a {
            color: #2563eb;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 640px) {
            .container {
                padding: 40px 28px;
            }
            
            h1 {
                font-size: 28px;
            }
            
            .subtitle {
                font-size: 16px;
            }
            
            .cta-hints span {
                display: block;
                margin-right: 0;
                margin-bottom: 4px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Видеть рынок до входа в бизнес</h1>
        
        <p class="subtitle">
            Анализ спроса, сегментов и динамики ниш на данных Яндекс Wordstat
        </p>
        
        <a href="/niche" class="cta-button">Проанализировать нишу</a>
        
        <div class="cta-hints">
            <span>Без регистрации</span>
            <span>Данные Wordstat</span>
            <span>Результат за 1–2 минуты</span>
        </div>
        
        <div class="example-section">
            <div class="example-title">Пример структуры ниши после анализа</div>
            
            <div class="example-table">
                <div class="example-row header">
                    <div class="example-cluster">Кластер</div>
                    <div class="example-count">Запросов</div>
                </div>
                <div class="example-row">
                    <div class="example-cluster">Корпоративные подарки</div>
                    <div class="example-count">127</div>
                </div>
                <div class="example-row">
                    <div class="example-cluster">Подарки сотрудникам</div>
                    <div class="example-count">89</div>
                </div>
                <div class="example-row">
                    <div class="example-cluster">Брендированные сувениры</div>
                    <div class="example-count">64</div>
                </div>
                <div class="example-row">
                    <div class="example-cluster">Новогодние наборы</div>
                    <div class="example-count">52</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Создано <a href="https://t.me/glxaoc" target="_blank">@glxaoc</a> • Санкт-Петербург, 2026
        </div>
    </div>
</body>
</html>"""
    
    return html
