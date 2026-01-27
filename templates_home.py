# templates_home.py
# v6.1.0 - Темный SaaS дизайн, три экрана

def render_home_page():
    """Рендерит главную страницу сервиса"""
    
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Поиск ниш | Аналитический SaaS</title>
    <style>
        :root {
            --bg-color: #0F1115;
            --surface-color: #1A1D24;
            --accent-primary: #3B82F6;
            --accent-secondary: #8B5CF6;
            --text-main: #FFFFFF;
            --text-secondary: #9CA3AF;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            overflow-x: hidden;
        }

        a { text-decoration: none; }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            height: 100%;
        }

        .btn {
            display: inline-block;
            padding: 16px 32px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            border: none;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        }

        section {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 60px 0;
        }

        .hero {
            text-align: center;
            background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
        }

        .hero-content {
            max-width: 800px;
            margin: 0 auto;
            z-index: 2;
            position: relative;
        }

        .tag {
            display: inline-block;
            padding: 6px 12px;
            background: rgba(59, 130, 246, 0.1);
            color: var(--accent-primary);
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 24px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        h1 {
            font-size: 4rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 24px;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #fff, #b0b0b0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-desc {
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .grid-bg {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: 1;
            mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
        }

        .result-section {
            background-color: #13161C;
        }

        .split-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }

        .text-block h2 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        .text-block p {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .dashboard-mockup {
            background: var(--surface-color);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            position: relative;
        }
        
        .mock-header {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }
        .mock-line { 
            height: 12px; 
            background: #2A2F3A; 
            border-radius: 4px; 
            width: 100%; 
        }
        .mock-line.short { width: 40%; }
        
        .mock-chart {
            display: flex;
            align-items: flex-end;
            gap: 8px;
            height: 150px;
            margin-top: 30px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2A2F3A;
        }
        .bar {
            flex: 1;
            background: var(--accent-primary);
            opacity: 0.8;
            border-radius: 4px 4px 0 0;
        }
        .bar:nth-child(even) { 
            background: var(--accent-secondary); 
            opacity: 0.6; 
        }

        .benefits-section {
            flex-direction: column;
            text-align: center;
        }

        .benefits-section h2 {
            font-size: 2.5rem;
            margin-bottom: 60px;
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            width: 100%;
            margin-bottom: 60px;
        }

        .card {
            background: var(--surface-color);
            padding: 30px;
            border-radius: 12px;
            text-align: left;
            border: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }

        .card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-5px);
        }

        .card-icon {
            font-size: 24px;
            margin-bottom: 20px;
            color: var(--accent-primary);
        }

        .card h3 {
            font-size: 1.2rem;
            margin-bottom: 10px;
        }

        .card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .footer {
            margin-top: 80px;
            padding: 40px 0;
            border-top: 1px solid rgba(255,255,255,0.05);
            text-align: center;
            font-size: 14px;
            color: var(--text-secondary);
        }

        .footer a {
            color: var(--accent-primary);
            text-decoration: none;
            transition: color 0.2s;
        }

        .footer a:hover {
            color: #fff;
        }

        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .split-layout { grid-template-columns: 1fr; }
            .hero-desc { font-size: 1rem; }
            section { padding: 40px 0; min-height: auto; }
            .text-block h2 { font-size: 2rem; }
            .benefits-section h2 { font-size: 2rem; }
        }
    </style>
</head>
<body>

    <section class="hero">
        <div class="grid-bg"></div>
        <div class="container">
            <div class="hero-content">
                <div class="tag">Wordstat Analytics</div>
                <h1>Видеть рынок до входа в бизнес</h1>
                <p class="hero-desc">
                    Аналитический SaaS инструмент для глубокого понимания ниш. 
                    Превращаем хаос поисковых запросов в четкую структуру рынка.
                </p>
                <a href="/niche" class="btn">Проанализировать нишу</a>
            </div>
        </div>
    </section>

    <section class="result-section">
        <div class="container">
            <div class="split-layout">
                <div class="dashboard-mockup">
                    <div class="mock-header">
                        <div class="mock-line short" style="background: #3B82F6;"></div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                        <div class="mock-line"></div>
                        <div class="mock-line"></div>
                        <div class="mock-line"></div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; opacity: 0.5;">
                        <div class="mock-line"></div>
                        <div class="mock-line"></div>
                        <div class="mock-line"></div>
                    </div>
                    <div class="mock-chart">
                        <div class="bar" style="height: 40%;"></div>
                        <div class="bar" style="height: 70%;"></div>
                        <div class="bar" style="height: 50%;"></div>
                        <div class="bar" style="height: 90%;"></div>
                        <div class="bar" style="height: 60%;"></div>
                    </div>
                </div>

                <div class="text-block">
                    <h2>Как выглядит ниша после анализа</h2>
                    <p>
                        Больше никаких догадок. Мы раскладываем рынок на понятные сегменты. 
                        Вы видите реальный спрос, сезонность и конкурентное поле в одном окне.
                        Это взгляд на бизнес через призму подтвержденных данных.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <section class="benefits-section">
        <div class="container">
            <h2>Что вы поймете о рынке</h2>
            
            <div class="cards-grid">
                <div class="card">
                    <div class="card-icon">📊</div>
                    <h3>Структура спроса</h3>
                    <p>Поймете, что именно ищут люди, и как они формулируют свои потребности.</p>
                </div>
                <div class="card">
                    <div class="card-icon">📈</div>
                    <h3>Динамика и тренды</h3>
                    <p>Увидите, растет рынок или падает, чтобы не заходить в угасающие ниши.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🎯</div>
                    <h3>Сегментация</h3>
                    <p>Найдете узкие и прибыльные сегменты внутри больших категорий.</p>
                </div>
                <div class="card">
                    <div class="card-icon">💰</div>
                    <h3>Объем рынка</h3>
                    <p>Оцените потенциал заработка в цифрах, опираясь на частотность запросов.</p>
                </div>
            </div>

            <div class="cta-block">
                <p style="color: #9CA3AF; margin-bottom: 20px;">Начните действовать, опираясь на факты</p>
                <a href="/niche" class="btn">Попробовать сервис бесплатно</a>
            </div>

            <div class="footer">
                Создано <a href="https://t.me/ivandrobitko" target="_blank">@ivandrobitko</a> • 2026
            </div>
        </div>
    </section>

</body>
</html>"""
    
    return html
