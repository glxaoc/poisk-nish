"""
HTML шаблон страницы анализа ниши v3.0 — YoY-центричный UI
"""

ANALYZE_HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Поиск ниш — Анализ спроса</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;min-height:100vh}
.header{background:#0f172a;color:white;padding:20px 40px}
.header h1{font-size:1.8em;font-weight:600}
.container{max-width:1200px;margin:0 auto;padding:20px}
.search-card{background:white;border-radius:16px;padding:30px;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin-bottom:20px}
.search-form{display:flex;gap:15px;align-items:end;flex-wrap:wrap}
.form-group{flex:1;min-width:200px}
.form-group label{display:block;margin-bottom:8px;font-weight:600;color:#333;font-size:14px}
.form-group input,.form-group select{width:100%;padding:14px 16px;border:2px solid #e0e0e0;border-radius:10px;font-size:16px}
.form-group input:focus{outline:none;border-color:#1a56db}
.btn{background:#1a56db;color:white;border:none;padding:14px 40px;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 15px rgba(102,126,234,0.4)}
.btn:disabled{opacity:0.6;cursor:not-allowed;transform:none}

.progress-bar{display:none;margin-top:20px}
.progress-bar.active{display:block}
.progress-track{background:#e0e0e0;border-radius:10px;height:8px;overflow:hidden}
.progress-fill{background:#1a56db;height:100%;width:0%;transition:width 0.3s}
.progress-text{text-align:center;margin-top:10px;color:#666;font-size:14px}

.results{display:none}
.results.active{display:block}

/* Verdict block */
.verdict-card{border-radius:8px;padding:28px 24px;margin-bottom:24px;text-align:center}
.verdict-card.recommended{background:#f0fdf4;color:#166534;border:2px solid #22c55e}
.verdict-card.conditional{background:#fefce8;color:#854d0e;border:2px solid #eab308}
.verdict-card.not_recommended{background:#fef2f2;color:#991b1b;border:2px solid #ef4444}
.verdict-card.uncertain{background:#f9fafb;color:#374151;border:2px solid #6b7280}
.verdict-icon{font-size:3em;margin-bottom:10px}
.verdict-label{font-size:1.5em;font-weight:700;margin-bottom:10px}
.verdict-reason{font-size:14px;opacity:0.9}

/* YoY metrics row */
.yoy-row{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px}
@media(max-width:700px){.yoy-row{grid-template-columns:1fr}}
.yoy-card{background:white;border-radius:8px;padding:24px 20px;text-align:center;border:1px solid #e2e8f0}
.yoy-value{font-size:26px;font-weight:600;color:#1e293b}
.yoy-value.positive{color:#166534}
.yoy-value.negative{color:#991b1b}
.yoy-label{color:#64748b;font-size:12px;margin-top:8px;text-transform:uppercase;letter-spacing:0.5px}
.yoy-month{font-size:12px;color:#aaa;margin-top:4px}

/* Dynamics chart */
.dynamics-card{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:20px}
.dynamics-card h3{margin-bottom:15px;color:#333;font-size:1em}
.dynamics-chart{height:200px}
.yoy-hint{font-size:12px;color:#888;margin-top:10px;text-align:center}

/* AI Block */
.ai-card{background:#f8fafc;border-radius:16px;padding:30px;color:#1e293b;margin-bottom:20px;border:1px solid #e2e8f0}
.ai-card h3{color:#fff;margin-bottom:20px;font-size:1.3em}
.ai-block{margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid #e2e8f0}
.ai-block:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.ai-block-title{font-weight:600;margin-bottom:12px;color:#1e293b;font-size:14px;letter-spacing:0}
.ai-fact{font-size:17px;line-height:1.6;color:#fff;font-weight:500}
.ai-fact-context{font-size:14px;color:#a0c4ff;margin-top:8px}
.ai-phase{font-size:15px;line-height:1.7;color:#e0e0e0}
.ai-tension{font-size:14px;color:#ffd700;font-style:italic;margin-top:10px}
.ai-pattern{background:rgba(255,255,255,0.03);padding:12px 15px;border-radius:8px;margin-bottom:10px}
.ai-pattern-name{font-size:15px;font-weight:600;color:#b0ffb0;margin-bottom:5px}
.ai-pattern-desc{font-size:13px;color:#d0d0d0;line-height:1.5;margin-bottom:8px}
.ai-pattern-note{font-size:11px;color:#808080;font-style:italic}
.ai-list{margin:0;padding-left:20px;color:#d0d0d0;font-size:14px;line-height:1.8}
.ai-list li{margin-bottom:6px}
.ai-difficulties li{color:#ffb0b0}
.ai-thinking li{color:#b0d4ff}
.ai-recommendations li{color:#90eec0}
.ai-verdict{padding:16px;border-radius:8px;margin-bottom:16px}
.verdict-green{background:rgba(76,175,80,0.15);border-left:4px solid #4caf50}
.verdict-yellow{background:rgba(255,193,7,0.15);border-left:4px solid #ffc107}
.verdict-red{background:rgba(244,67,54,0.15);border-left:4px solid #f44336}
.verdict-header{font-size:18px;font-weight:600;margin-bottom:8px}
.verdict-reason{font-size:14px;color:#ccc}
.ai-text{font-size:14px;line-height:1.6;color:#ddd}
.segment-group{padding:10px 14px;margin:8px 0;border-radius:4px;background:#fff;border-left:3px solid #94a3b8}
.segment-growth{background:rgba(76,175,80,0.1)}
.segment-stable{background:rgba(255,193,7,0.1)}
.segment-risk{background:rgba(244,67,54,0.1)}
.segment-label{font-weight:600;margin-right:8px}
.model-type{font-size:14px;padding:8px 0;color:#ddd}
.model-scale{font-size:13px;color:#90caf9;padding:4px 0}
.ai-risks li{color:#ff8a80}
.ai-mistakes li{color:#ffab91}
.ai-notfor li{color:#ce93d8}
.subniche{background:rgba(100,100,100,0.2);padding:10px 12px;margin:8px 0;border-radius:6px}
.subniche-idea{font-size:14px;font-weight:500;color:#81d4fa}
.subniche-why{font-size:12px;color:#aaa;margin-top:4px}
.strategy{padding:10px 12px;margin:6px 0;border-radius:4px;font-size:13px}
.strategy-cautious{background:rgba(156,39,176,0.1)}
.strategy-aggressive{background:rgba(255,152,0,0.1)}
.strategy-label{font-weight:600}
.ai-conclusion{background:rgba(33,150,243,0.1);padding:16px;border-radius:8px;border-left:4px solid #2196f3}
.conclusion-header{font-size:16px;font-weight:600}
.conclusion-answer{margin-left:10px}
.conclusion-condition{font-size:13px;color:#ffc107;margin:8px 0}
.conclusion-summary{font-size:14px;color:#ddd;margin-top:8px}
.ai-limits-block{background:rgba(255,255,255,0.02);padding:15px;border-radius:8px;margin-top:15px}
.ai-limits li{color:#909090;font-size:13px}
.ai-loading{text-align:center;padding:40px;color:#888}
.ai-loading .spinner{width:40px;height:40px;border:3px solid #333;border-top-color:#1a56db;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 15px}
@keyframes spin{to{transform:rotate(360deg)}}
.scenario-card{background:#f8fafc;border-radius:12px;padding:15px;margin:10px 0;border-left:4px solid #1a56db}
.scenario-name{font-weight:600;font-size:15px;color:#1e293b;margin-bottom:8px}
.scenario-action{font-size:14px;color:#475569;margin-bottom:6px}
.scenario-risk{font-size:13px;color:#dc2626;background:#fef2f2;padding:6px 10px;border-radius:6px;margin-top:8px}

/* Details section */
.details-section{margin-top:40px;padding-top:28px;border-top:1px solid #e2e8f0}
.details-title{font-size:14px;color:#666;margin-bottom:15px;text-transform:uppercase;letter-spacing:1px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
@media(max-width:900px){.grid-2{grid-template-columns:1fr}}
.card{background:white;border-radius:12px;padding:25px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.card h3{margin-bottom:15px;color:#333;font-size:1.1em;display:flex;align-items:center;gap:10px}
.chart-container{position:relative;height:250px}

/* Extra metrics */
.extra-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:28px}
@media(max-width:800px){.extra-metrics{grid-template-columns:repeat(2,1fr)}}
.extra-card{background:white;border-radius:8px;padding:18px;text-align:center;border:1px solid #e2e8f0}
.extra-value{font-size:20px;font-weight:700;color:#1a56db}
.extra-label{font-size:11px;color:#888;margin-top:4px}

/* Clusters */
.cluster-list{max-height:350px;overflow-y:auto}
.cluster-item{border:1px solid #e2e8f0;border-radius:8px;margin-bottom:10px;overflow:hidden;background:white}
.cluster-header{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;cursor:pointer;background:white}
.cluster-header:hover{background:#f8fafc}
.cluster-name{font-weight:600;color:#333;font-size:14px}
.cluster-stats{display:flex;gap:10px;align-items:center}
.cluster-count{color:#1a56db;font-weight:600;font-size:13px}
.cluster-share{background:#f1f5f9;color:#475569;padding:4px 10px;border-radius:4px;font-size:12px;font-weight:500}
.cluster-phrases{display:none;padding:12px 15px;border-top:1px solid #eee;background:white}
.cluster-phrases.open{display:block}
.phrase-item{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f5f5f5;font-size:13px}
.phrase-item:last-child{border-bottom:none}
.phrase-text{color:#555}
.phrase-count{color:#1a56db;font-weight:500}

/* AI Button */
.ai-button-container{text-align:center;padding:40px 20px}
.ai-launch-btn{background:#0f172a;color:white;border:none;padding:16px 32px;font-size:16px;font-weight:600;border-radius:12px;cursor:pointer;transition:all 0.3s ease;box-shadow:0 4px 15px rgba(102,126,234,0.4)}
.ai-launch-btn:hover{background:#1e40af}
.ai-cost{margin-top:12px;color:#888;font-size:13px}
</style>
</head>
<body>
<div class="header">
<h1>Поиск ниш</h1>
</div>

<div class="container">
<div class="search-card">
<div class="search-form">
<div class="form-group" style="flex:2">
<label>Поисковая фраза</label>
<input type="text" id="phrase" placeholder="Например: купить кофемашину">
</div>
<div class="form-group" style="flex:1">
<label>Регион</label>
<select id="region">
<option value="225" selected>Россия</option>
<option value="213">Москва</option>
<option value="22">Калининград</option>
<option value="2">Санкт-Петербург</option>
</select>
</div>
<button class="btn" id="btnAnalyze" onclick="startAnalysis()">Показать данные</button>
</div>
<div class="progress-bar" id="progressBar">
<div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
<div class="progress-text" id="progressText">Подготовка...</div>
</div>
</div>

<div class="results" id="results">

<!-- Verdict -->
<div class="verdict-card" id="verdictCard" style="display:none">
<div class="verdict-icon" id="verdictIcon"></div>
<div class="verdict-label" id="verdictLabel"></div>
<div class="verdict-reason" id="verdictReason"></div>
</div>

<!-- YoY metrics: NOW / YEAR_AGO / YoY -->
<div class="yoy-row">
<div class="yoy-card">
<div class="yoy-value" id="nowValue">—</div>
<div class="yoy-label">Сейчас</div>
<div class="yoy-month" id="nowMonth"></div>
</div>
<div class="yoy-card">
<div class="yoy-value" id="yearAgoValue">—</div>
<div class="yoy-label">Год назад</div>
<div class="yoy-month" id="yearAgoMonth"></div>
</div>
<div class="yoy-card">
<div class="yoy-value" id="yoyValue">—</div>
<div class="yoy-label">Изменение YoY</div>
<div class="yoy-month">год к году</div>
</div>
</div>

<!-- Dynamics chart -->
<div class="dynamics-card">
<h3>Динамика за 12 месяцев</h3>
<div class="dynamics-chart">
<canvas id="dynamicsChart"></canvas>
</div>
<div class="yoy-hint">YoY = сравнение одного календарного месяца с тем же месяцем год назад</div>
</div>

<!-- AI Analysis Block -->
<div class="ai-card" id="aiCard">
<h3>Анализ спроса</h3>
<div id="aiContent">
<div class="ai-loading">
<div class="spinner"></div>
<div>Генерируем анализ...</div>
</div>
</div>
</div>

<div class="card">
<h3>Кластеры запросов</h3>
<div class="cluster-list" id="clusterList"></div>
</div>


</div>
</div>

<script>
var dynamicsChart = null;
var currentPhrase = '';
var currentRegion = 225;
var pollInterval = null;

function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

function formatMonth(label) {
    var months = {'01':'янв','02':'фев','03':'мар','04':'апр','05':'май','06':'июн','07':'июл','08':'авг','09':'сен','10':'окт','11':'ноя','12':'дек'};
    var parts = label.split('-');
    return months[parts[1]] + ' ' + parts[0];
}

async function startAnalysis() {
    var phrase = document.getElementById('phrase').value.trim();
    var region = parseInt(document.getElementById('region').value);
    if (!phrase) { alert('Введите поисковую фразу'); return; }
    
    document.getElementById('btnAnalyze').disabled = true;
    document.getElementById('progressBar').classList.add('active');
    document.getElementById('results').classList.remove('active');
    updateProgress(5, 'Запуск сбора...');
    
    try {
        await fetch('/api/deepCollect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({phrase: phrase, region: region, max_depth: 1})
        });
        pollInterval = setInterval(checkStatus, 1000);
    } catch(e) { alert('Ошибка: ' + e); resetUI(); }
}

async function checkStatus() {
    try {
        var resp = await fetch('/api/collectStatus');
        var data = await resp.json();
        updateProgress(data.progress, 'Собрано ' + data.collected + ' запросов...');
        if (data.status === 'done') {
            clearInterval(pollInterval);
            updateProgress(100, 'Анализ данных...');
            setTimeout(loadResults, 500);
        }
    } catch(e) { console.error(e); }
}

async function loadResults() {
    var phrase = document.getElementById('phrase').value.trim();
    var region = parseInt(document.getElementById('region').value);
    
    try {
        var resp = await fetch('/api/analyze-v2?phrase=' + encodeURIComponent(phrase) + '&region=' + region);
        var data = await resp.json();
        
        // Verdict
        if (data.verdict) {
            var vc = document.getElementById('verdictCard');
            vc.className = 'verdict-card ' + data.verdict.verdict;
            vc.style.display = 'block';
            document.getElementById('verdictIcon').textContent = data.verdict.verdict_icon;
            document.getElementById('verdictLabel').textContent = data.verdict.verdict_label;
            document.getElementById('verdictReason').textContent = data.verdict.reason;
        }
        
        // YoY metrics
        if (data.seasonality) {
            var s = data.seasonality;
            
            // NOW
            document.getElementById('nowValue').textContent = fmt(s.now_count || 0);
            document.getElementById('nowMonth').textContent = s.current_month_label ? formatMonth(s.current_month_label) : '';
            
            // YEAR_AGO
            document.getElementById('yearAgoValue').textContent = fmt(s.year_ago_count || 0);
            document.getElementById('yearAgoMonth').textContent = s.year_ago_month_label ? formatMonth(s.year_ago_month_label) : '';
            
            // YoY
            var yoy = s.yoy_percent || 0;
            var yoyEl = document.getElementById('yoyValue');
            var prefix = yoy >= 0 ? '+' : '';
            yoyEl.textContent = prefix + yoy.toFixed(0) + '%';
            yoyEl.classList.remove('positive', 'negative');
            yoyEl.classList.add(yoy >= 0 ? 'positive' : 'negative');
            
            // Dynamics chart
            if (s.monthly_labels && s.monthly_series) {
                renderDynamicsChart(s.monthly_labels, s.monthly_series);
            }
        }
        
        if (data.clusters) { renderClusterList(data.clusters); }
        
        document.getElementById('progressBar').classList.remove('active');
        document.getElementById('results').classList.add('active');
        
        // Store for AI button
        currentPhrase = phrase;
        currentRegion = region;
        showAIButton();
        
    } catch(e) { alert('Ошибка: ' + e); }
    resetUI();
}

function renderDynamicsChart(labels, values) {
    var ctx = document.getElementById('dynamicsChart').getContext('2d');
    if (dynamicsChart) dynamicsChart.destroy();
    
    var formattedLabels = labels.map(formatMonth);
    
    dynamicsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: formattedLabels,
            datasets: [{
                label: 'Запросов',
                data: values,
                borderColor: '#1a56db',
                backgroundColor: 'rgba(102,126,234,0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#1a56db'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) { return fmt(ctx.raw) + ' запросов'; }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(v) { return v >= 1000 ? (v/1000) + 'k' : v; }
                    }
                }
            }
        }
    });
}

function showAIButton() {
    document.getElementById("aiContent").innerHTML = '<div class="ai-button-container"><button class="ai-launch-btn" onclick="launchAIAnalysis()">Получить анализ</button><div class="ai-cost">Около 5 секунд</div></div>';
}

function launchAIAnalysis() {
    loadAIAnalysis(currentPhrase, currentRegion);
}

async function loadAIAnalysis(phrase, region) {
    document.getElementById("aiContent").innerHTML = '<div class="ai-loading"><div class="spinner"></div><div>Анализ данных...</div></div>';
    
    try {
        var resp = await fetch("/api/ai-analyze?phrase=" + encodeURIComponent(phrase) + "&region=" + region);
        var data = await resp.json();
        
        var html = "";
        
        // 1. Verdict
        if (data.verdict && data.verdict.status) {
            var statusClass = data.verdict.status.includes("✅") ? "verdict-green" : (data.verdict.status.includes("⚠️") ? "verdict-yellow" : "verdict-red");
            html += '<div class="ai-block ai-verdict ' + statusClass + '">';
            html += '<div class="verdict-header">' + data.verdict.status + ' ' + (data.verdict.title || "") + '</div>';
            html += '<div class="verdict-reason">' + (data.verdict.reason || "") + '</div>';
            html += '</div>';
        }
        
        // 2. Market Reality
        if (data.market_reality) {
            html += '<div class="ai-block"><div class="ai-block-title">Что происходит с рынком</div>';
            html += '<div class="ai-text">' + data.market_reality + '</div></div>';
        }
        
        // 3. Demand Map
        if (data.demand_map) {
            html += '<div class="ai-block"><div class="ai-block-title">Карта спроса</div>';
            if (data.demand_map.growth && data.demand_map.growth.length > 0) {
                html += '<div class="segment-group segment-growth"><span class="segment-label">Рост:</span> ' + data.demand_map.growth.join(", ") + '</div>';
            }
            if (data.demand_map.stable && data.demand_map.stable.length > 0) {
                html += '<div class="segment-group segment-stable"><span class="segment-label">Стабильно:</span> ' + data.demand_map.stable.join(", ") + '</div>';
            }
            if (data.demand_map.risk && data.demand_map.risk.length > 0) {
                html += '<div class="segment-group segment-risk"><span class="segment-label">Риск:</span> ' + data.demand_map.risk.join(", ") + '</div>';
            }
            html += '</div>';
        }
        
        // 4. Business Model
        if (data.business_model_type && data.business_model_type.type) {
            var modelIcon = data.business_model_type.type.includes("капитал") ? "💰" : (data.business_model_type.type.includes("систем") ? "⚙️" : "👤");
            html += '<div class="ai-block"><div class="ai-block-title">Тип бизнес-модели</div>';
            html += '<div class="model-type">' + modelIcon + ' <b>' + data.business_model_type.type + '</b>: ' + data.business_model_type.explanation + '</div>';
            html += '<div class="model-scale">' + data.business_model_type.scalability + '</div></div>';
        }
        
        // 5. Entry Risks
        if (data.entry_risks && data.entry_risks.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">Риски входа</div><ul class="ai-list ai-risks">';
            data.entry_risks.forEach(function(item) { html += '<li>' + item + '</li>'; });
            html += '</ul></div>';
        }
        
        // 6. Beginner Mistakes
        if (data.beginner_mistakes && data.beginner_mistakes.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">Типичные ошибки новичков</div><ul class="ai-list ai-mistakes">';
            data.beginner_mistakes.forEach(function(item) { html += '<li>' + item + '</li>'; });
            html += '</ul></div>';
        }
        
        // 7. Not Suitable For
        if (data.not_for && data.not_for.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">Кому не подходит</div><ul class="ai-list ai-notfor">';
            data.not_for.forEach(function(item) { html += '<li>' + item + '</li>'; });
            html += '</ul></div>';
        }
        
        // 8. Sub-niches
        if (data.sub_niches && data.sub_niches.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">Потенциальные подниши</div>';
            data.sub_niches.forEach(function(n) {
                html += '<div class="subniche"><div class="subniche-idea">→ ' + n.idea + '</div>';
                html += '<div class="subniche-why">' + n.why + '</div></div>';
            });
            html += '</div>';
        }
        
        // 9. Entry Strategy
        if (data.entry_strategy) {
            html += '<div class="ai-block"><div class="ai-block-title">Стратегия входа</div>';
            if (data.entry_strategy.cautious) {
                html += '<div class="strategy strategy-cautious"><span class="strategy-label">Осторожный:</span> ' + data.entry_strategy.cautious + '</div>';
            }
            if (data.entry_strategy.aggressive) {
                html += '<div class="strategy strategy-aggressive"><span class="strategy-label">Агрессивный:</span> ' + data.entry_strategy.aggressive + '</div>';
            }
            html += '</div>';
        }
        
        // 10. Final Verdict
        if (data.final_verdict && data.final_verdict.answer) {
            var answerClass = data.final_verdict.answer.toLowerCase().includes("да") ? "answer-yes" : (data.final_verdict.answer.toLowerCase().includes("нет") ? "answer-no" : "answer-conditional");
            html += '<div class="ai-block ai-conclusion">';
            html += '<div class="conclusion-header">Стоит ли заходить? <span class="conclusion-answer">' + data.final_verdict.answer + '</span></div>';
            html += '<div class="conclusion-summary">' + data.final_verdict.summary + '</div></div>';
        }
        
        document.getElementById("aiContent").innerHTML = html || '<div style="color:#888">Не удалось получить анализ</div>';
        
    } catch(e) {
        document.getElementById("aiContent").innerHTML = '<div style="color:#888">Ошибка загрузки анализа</div>';
    }
}

function updateProgress(pct, text) {
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = text;
}

function resetUI() { document.getElementById('btnAnalyze').disabled = false; }


function renderClusterList(clusters) {
    var html = '';
    var top5 = clusters.slice(0, 5);
    top5.forEach(function(c, i) {
        html += '<div class="cluster-item">';
        html += '<div class="cluster-header" onclick="toggleCluster(' + i + ')">';
        html += '<span class="cluster-name">' + c.name + '</span>';
        html += '<div class="cluster-stats"><span class="cluster-count">' + fmt(c.count) + '</span>';
        html += '<span class="cluster-share">' + c.share + '%</span></div></div>';
        html += '<div class="cluster-phrases" id="cluster-' + i + '">';
        if (c.phrases) {
            c.phrases.forEach(function(p) {
                html += '<div class="phrase-item"><span class="phrase-text">' + p.phrase + '</span>';
                html += '<span class="phrase-count">' + fmt(p.count) + '</span></div>';
            });
        }
        html += '</div></div>';
    });
    document.getElementById('clusterList').innerHTML = html;
}

function toggleCluster(i) { document.getElementById('cluster-' + i).classList.toggle('open'); }

</script>
</body>
</html>'''
