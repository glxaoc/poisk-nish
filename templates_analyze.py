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
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;min-height:100vh}
.header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px 40px}
.header h1{font-size:1.8em;font-weight:600}
.container{max-width:1200px;margin:0 auto;padding:20px}
.search-card{background:white;border-radius:16px;padding:30px;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin-bottom:20px}
.search-form{display:flex;gap:15px;align-items:end;flex-wrap:wrap}
.form-group{flex:1;min-width:200px}
.form-group label{display:block;margin-bottom:8px;font-weight:600;color:#333;font-size:14px}
.form-group input,.form-group select{width:100%;padding:14px 16px;border:2px solid #e0e0e0;border-radius:10px;font-size:16px}
.form-group input:focus{outline:none;border-color:#667eea}
.btn{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;padding:14px 40px;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 15px rgba(102,126,234,0.4)}
.btn:disabled{opacity:0.6;cursor:not-allowed;transform:none}

.progress-bar{display:none;margin-top:20px}
.progress-bar.active{display:block}
.progress-track{background:#e0e0e0;border-radius:10px;height:8px;overflow:hidden}
.progress-fill{background:linear-gradient(90deg,#667eea,#764ba2);height:100%;width:0%;transition:width 0.3s}
.progress-text{text-align:center;margin-top:10px;color:#666;font-size:14px}

.results{display:none}
.results.active{display:block}

/* Verdict block */
.verdict-card{border-radius:16px;padding:25px;margin-bottom:20px;text-align:center}
.verdict-card.recommended{background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);color:white}
.verdict-card.conditional{background:linear-gradient(135deg,#eab308 0%,#ca8a04 100%);color:white}
.verdict-card.not_recommended{background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);color:white}
.verdict-card.uncertain{background:linear-gradient(135deg,#6b7280 0%,#4b5563 100%);color:white}
.verdict-icon{font-size:3em;margin-bottom:10px}
.verdict-label{font-size:1.5em;font-weight:700;margin-bottom:10px}
.verdict-reason{font-size:14px;opacity:0.9}

/* YoY metrics row */
.yoy-row{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px}
@media(max-width:700px){.yoy-row{grid-template-columns:1fr}}
.yoy-card{background:white;border-radius:12px;padding:20px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.yoy-value{font-size:28px;font-weight:700;color:#333}
.yoy-value.positive{color:#22c55e}
.yoy-value.negative{color:#ef4444}
.yoy-label{color:#888;font-size:13px;margin-top:6px}
.yoy-month{font-size:12px;color:#aaa;margin-top:4px}

/* Dynamics chart */
.dynamics-card{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:20px}
.dynamics-card h3{margin-bottom:15px;color:#333;font-size:1em}
.dynamics-chart{height:200px}
.yoy-hint{font-size:12px;color:#888;margin-top:10px;text-align:center}

/* AI Block */
.ai-card{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border-radius:16px;padding:30px;color:white;margin-bottom:20px}
.ai-card h3{color:#fff;margin-bottom:20px;font-size:1.3em}
.ai-block{margin-bottom:20px;padding-bottom:18px;border-bottom:1px solid rgba(255,255,255,0.08)}
.ai-block:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.ai-block-title{font-weight:600;margin-bottom:12px;color:#a0a0ff;font-size:13px;text-transform:uppercase;letter-spacing:1px}
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
.ai-limits-block{background:rgba(255,255,255,0.02);padding:15px;border-radius:8px;margin-top:15px}
.ai-limits li{color:#909090;font-size:13px}
.ai-loading{text-align:center;padding:40px;color:#888}
.ai-loading .spinner{width:40px;height:40px;border:3px solid #333;border-top-color:#667eea;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 15px}
@keyframes spin{to{transform:rotate(360deg)}}
.scenario-card{background:#f8fafc;border-radius:12px;padding:15px;margin:10px 0;border-left:4px solid #667eea}
.scenario-name{font-weight:600;font-size:15px;color:#1e293b;margin-bottom:8px}
.scenario-action{font-size:14px;color:#475569;margin-bottom:6px}
.scenario-risk{font-size:13px;color:#dc2626;background:#fef2f2;padding:6px 10px;border-radius:6px;margin-top:8px}

/* Details section */
.details-section{margin-top:30px;padding-top:20px;border-top:2px solid #e5e7eb}
.details-title{font-size:14px;color:#666;margin-bottom:15px;text-transform:uppercase;letter-spacing:1px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
@media(max-width:900px){.grid-2{grid-template-columns:1fr}}
.card{background:white;border-radius:12px;padding:25px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.card h3{margin-bottom:15px;color:#333;font-size:1.1em;display:flex;align-items:center;gap:10px}
.chart-container{position:relative;height:250px}

/* Extra metrics */
.extra-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:20px}
@media(max-width:800px){.extra-metrics{grid-template-columns:repeat(2,1fr)}}
.extra-card{background:white;border-radius:10px;padding:15px;text-align:center}
.extra-value{font-size:20px;font-weight:700;color:#667eea}
.extra-label{font-size:11px;color:#888;margin-top:4px}

/* Clusters */
.cluster-list{max-height:350px;overflow-y:auto}
.cluster-item{border:1px solid #eee;border-radius:10px;margin-bottom:8px;overflow:hidden}
.cluster-header{display:flex;justify-content:space-between;align-items:center;padding:12px 15px;cursor:pointer;background:#fafafa}
.cluster-header:hover{background:#f0f0f0}
.cluster-name{font-weight:600;color:#333;font-size:14px}
.cluster-stats{display:flex;gap:10px;align-items:center}
.cluster-count{color:#667eea;font-weight:600;font-size:13px}
.cluster-share{background:#667eea;color:white;padding:3px 8px;border-radius:20px;font-size:11px;font-weight:600}
.cluster-phrases{display:none;padding:12px 15px;border-top:1px solid #eee;background:white}
.cluster-phrases.open{display:block}
.phrase-item{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f5f5f5;font-size:13px}
.phrase-item:last-child{border-bottom:none}
.phrase-text{color:#555}
.phrase-count{color:#667eea;font-weight:500}
</style>
</head>
<body>
<div class="header">
<h1>🔍 Поиск ниш</h1>
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
<button class="btn" id="btnAnalyze" onclick="startAnalysis()">Анализировать</button>
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
<h3>📈 Динамика за 12 месяцев</h3>
<div class="dynamics-chart">
<canvas id="dynamicsChart"></canvas>
</div>
<div class="yoy-hint">YoY = сравнение одного календарного месяца с тем же месяцем год назад</div>
</div>

<!-- AI Analysis Block -->
<div class="ai-card" id="aiCard">
<h3>🧠 Анализ спроса</h3>
<div id="aiContent">
<div class="ai-loading">
<div class="spinner"></div>
<div>Генерируем анализ...</div>
</div>
</div>
</div>

<div class="card">
<h3>📋 Кластеры запросов</h3>
<div class="cluster-list" id="clusterList"></div>
</div>


</div>
</div>

<script>
var dynamicsChart = null;
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
        
        // Load AI analysis async
        loadAIAnalysis(phrase, region);
        
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
                borderColor: '#667eea',
                backgroundColor: 'rgba(102,126,234,0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#667eea'
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

async function loadAIAnalysis(phrase, region) {
    document.getElementById("aiContent").innerHTML = '<div class="ai-loading"><div class="spinner"></div><div>Анализируем спрос...</div></div>';
    
    try {
        var resp = await fetch("/api/ai-analyze?phrase=" + encodeURIComponent(phrase) + "&region=" + region);
        var data = await resp.json();
        
        var html = "";
        
        // 1. Facts block
        if (data.facts_block) {
            html += '<div class="ai-block"><div class="ai-block-title">📊 Факты о спросе</div>';
            if (data.facts_block.demand_change) {
                html += '<div class="ai-fact">' + data.facts_block.demand_change + '</div>';
            }
            if (data.facts_block.absolute_context) {
                html += '<div class="ai-fact-context">' + data.facts_block.absolute_context + '</div>';
            }
            html += '</div>';
        }
        
        // 2. Demand interpretation
        if (data.demand_interpretation) {
            html += '<div class="ai-block"><div class="ai-block-title">📈 Как читать эту динамику</div>';
            if (data.demand_interpretation.market_phase) {
                html += '<div class="ai-phase">' + data.demand_interpretation.market_phase + '</div>';
            }
            if (data.demand_interpretation.key_tension) {
                html += '<div class="ai-tension">💥 ' + data.demand_interpretation.key_tension + '</div>';
            }
            html += '</div>';
        }
        
        // 3. Business patterns
        if (data.business_patterns && data.business_patterns.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">🏢 Типовые бизнес-паттерны</div>';
            data.business_patterns.forEach(function(p) {
                html += '<div class="ai-pattern">';
                html += '<div class="ai-pattern-name">' + p.pattern + '</div>';
                html += '<div class="ai-pattern-desc">' + p.description + '</div>';
                html += '<div class="ai-pattern-note">ℹ️ ' + p.note + '</div>';
                html += '</div>';
            });
            html += '</div>';
        }
        
        // 4. Structural difficulties
        if (data.structural_difficulties && data.structural_difficulties.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">⚠️ Структурные сложности</div><ul class="ai-list ai-difficulties">';
            data.structural_difficulties.forEach(function(item) {
                html += '<li>' + item + '</li>';
            });
            html += '</ul></div>';
        }
        
        // 5. Entrepreneur thinking
        if (data.entrepreneur_thinking && data.entrepreneur_thinking.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">💭 Вопросы предпринимателя</div><ul class="ai-list ai-thinking">';
            data.entrepreneur_thinking.forEach(function(item) {
                html += '<li>' + item + '</li>';
            });
            html += '</ul></div>';
        }
        
        // 6. Thinking recommendations
        if (data.thinking_recommendations && data.thinking_recommendations.length > 0) {
            html += '<div class="ai-block"><div class="ai-block-title">🔍 Направления для анализа</div><ul class="ai-list ai-recommendations">';
            data.thinking_recommendations.forEach(function(item) {
                html += '<li>' + item + '</li>';
            });
            html += '</ul></div>';
        }
        
        // 7. Analysis limits
        if (data.analysis_limits && data.analysis_limits.length > 0) {
            html += '<div class="ai-block ai-limits-block"><div class="ai-block-title">🚫 Ограничения анализа</div><ul class="ai-list ai-limits">';
            data.analysis_limits.forEach(function(item) {
                html += '<li>' + item + '</li>';
            });
            html += '</ul></div>';
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
