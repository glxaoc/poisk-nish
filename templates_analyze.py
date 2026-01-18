"""
HTML шаблон страницы анализа ниши v3 - с ИИ
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

.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px;margin-bottom:20px}
.stat-card{background:white;border-radius:12px;padding:20px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.stat-value{font-size:1.8em;font-weight:700;color:#667eea}
.stat-label{color:#666;margin-top:5px;font-size:13px}

.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
@media(max-width:900px){.grid-2{grid-template-columns:1fr}}

.card{background:white;border-radius:12px;padding:25px;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:20px}
.card h3{margin-bottom:15px;color:#333;font-size:1.1em;display:flex;align-items:center;gap:10px}

.chart-container{position:relative;height:280px}

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

/* Insights */
.insights-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:15px;margin-bottom:20px}
.insight-card{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.05);border-left:4px solid #667eea}
.insight-header{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.insight-icon{font-size:1.5em}
.insight-title{font-weight:600;color:#333}
.insight-text{color:#666;font-size:14px;line-height:1.5}

/* AI Block */
.ai-card{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border-radius:16px;padding:30px;color:white;margin-bottom:20px}
.ai-card h3{color:#fff;margin-bottom:20px;font-size:1.3em}
.ai-summary{font-size:16px;line-height:1.7;margin-bottom:25px;color:#e0e0e0}
.ai-section{margin-bottom:20px}
.ai-section-title{font-weight:600;margin-bottom:12px;color:#a0a0ff;font-size:14px;text-transform:uppercase;letter-spacing:1px}
.ai-list{list-style:none}
.ai-list li{padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.1);display:flex;gap:12px;align-items:flex-start}
.ai-list li:last-child{border-bottom:none}
.ai-list .icon{font-size:1.2em}
.ai-list .text{color:#d0d0d0;font-size:14px;line-height:1.5}
.ai-loading{text-align:center;padding:40px;color:#888}
.ai-loading .spinner{width:40px;height:40px;border:3px solid #333;border-top-color:#667eea;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 15px}
@keyframes spin{to{transform:rotate(360deg)}}

/* Recommendations */
.recs-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;padding:25px;color:white;margin-bottom:20px}
.recs-card h3{color:white;margin-bottom:15px}
.rec-item{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.2)}
.rec-item:last-child{border-bottom:none}
.rec-icon{font-size:1.3em}
.rec-text{font-size:14px;line-height:1.5}
/* Progress bars for metrics */
.metric-bar{background:#e0e0e0;border-radius:10px;height:8px;overflow:hidden;margin-top:8px}
.metric-bar-fill{height:100%;border-radius:10px;transition:width 0.5s ease}
.metric-bar-fill.size{background:linear-gradient(90deg,#667eea,#764ba2)}
.metric-bar-fill.competition{background:linear-gradient(90deg,#22c55e,#eab308,#ef4444)}
.metric-index{font-size:24px;font-weight:700;color:#333}
.metric-label{font-size:12px;color:#888;margin-top:4px}
/* Verdict block */
.verdict-card{border-radius:16px;padding:25px;margin-bottom:20px;text-align:center}
.verdict-card.recommended{background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);color:white}
.verdict-card.conditional{background:linear-gradient(135deg,#eab308 0%,#ca8a04 100%);color:white}
.verdict-card.not_recommended{background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);color:white}
.verdict-card.uncertain{background:linear-gradient(135deg,#6b7280 0%,#4b5563 100%);color:white}
.verdict-icon{font-size:3em;margin-bottom:10px}
.verdict-label{font-size:1.5em;font-weight:700;margin-bottom:10px}
.verdict-reason{font-size:14px;opacity:0.9}
/* AI v2 styles */
.ai-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.ai-tag{padding:6px 12px;border-radius:20px;font-size:13px;font-weight:500}
.ai-tag.green{background:#dcfce7;color:#166534}
.ai-tag.red{background:#fee2e2;color:#991b1b}
.scenario-card{background:#f8fafc;border-radius:12px;padding:15px;margin:10px 0;border-left:4px solid #667eea}
.scenario-name{font-weight:600;font-size:15px;color:#1e293b;margin-bottom:8px}
.scenario-action{font-size:14px;color:#475569;margin-bottom:6px}
.scenario-risk{font-size:13px;color:#dc2626;background:#fef2f2;padding:6px 10px;border-radius:6px;margin-top:8px}
/* Summary block */
.summary-card{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border-radius:16px;padding:25px;color:white;margin-top:20px}
.summary-card h3{margin-bottom:20px;font-size:1.3em}
.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px}
.summary-item{background:rgba(255,255,255,0.1);border-radius:12px;padding:15px;text-align:center}
.summary-label{font-size:12px;color:#94a3b8;margin-bottom:5px}
.summary-value{font-size:18px;font-weight:700}
.summary-directions{margin-bottom:15px}
.summary-directions .summary-label{margin-bottom:10px}
.summary-direction-tag{display:inline-block;background:rgba(102,126,234,0.3);color:#a5b4fc;padding:6px 12px;border-radius:20px;margin:4px;font-size:13px}
.summary-verdict{background:rgba(255,255,255,0.1);border-radius:12px;padding:15px;text-align:center;font-size:16px;font-weight:600}
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

<!-- 4 ключевых метрики -->
<div class="stats-row">
<div class="stat-card">
<div class="metric-index" id="sizeIndex">0</div>
<div class="metric-label">Размер ниши</div>
<div class="metric-bar"><div class="metric-bar-fill size" id="sizeBar" style="width:0%"></div></div>
<div style="font-size:12px;color:#666;margin-top:5px" id="sizeLabel"></div>
</div>
<div class="stat-card">
<div class="metric-index" id="compIndex">0</div>
<div class="metric-label">Конкуренция</div>
<div class="metric-bar"><div class="metric-bar-fill competition" id="compBar" style="width:0%"></div></div>
<div style="font-size:12px;color:#666;margin-top:5px" id="compLabel"></div>
</div>
<div class="stat-card">
<div class="metric-index" id="seasonIndex">×1.0</div>
<div class="metric-label">Сезонность</div>
<div style="font-size:12px;color:#666;margin-top:8px" id="seasonLabel"></div>
</div>
<div class="stat-card">
<div class="metric-index" id="growthIndex" style="color:#22c55e">+0%</div>
<div class="metric-label">Рост за год</div>
<div style="font-size:12px;color:#666;margin-top:8px" id="growthLabel"></div>
</div>
</div>

<!-- AI Analysis Block -->
<div class="ai-card" id="aiCard">
<h3>🧠 Анализ от ИИ</h3>
<div id="aiContent">
<div class="ai-loading">
<div class="spinner"></div>
<div>Генерируем анализ...</div>
</div>
</div>
</div>



<div class="grid-2">
<div class="card">
<h3>📊 Структура спроса</h3>
<div id="chartHint" style="font-size:13px;color:#666;margin-bottom:10px;padding:8px;background:#f8fafc;border-radius:8px"></div>
<div class="chart-container">
<canvas id="pieChart"></canvas>
</div>
</div>
<div class="card">
<h3>📋 Кластеры запросов</h3>
<div class="cluster-list" id="clusterList"></div>
</div>
</div>



</div>
</div>

<script>
var pieChart = null;
var pollInterval = null;

function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

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
        
        // Stats
        document.getElementById('statTotal').textContent = fmt(data.total_count);
        document.getElementById('statQueries').textContent = fmt(data.total_queries);
        document.getElementById('statClusters').textContent = data.clusters_count;
        
        // Verdict
        if (data.verdict) {
            var vc = document.getElementById('verdictCard');
            vc.className = 'verdict-card ' + data.verdict.verdict;
            vc.style.display = 'block';
            document.getElementById('verdictIcon').textContent = data.verdict.verdict_icon;
            document.getElementById('verdictLabel').textContent = data.verdict.verdict_label;
            document.getElementById('verdictReason').textContent = data.verdict.reason;
        }
        
        // Size metric
        if (data.size) {
            document.getElementById('sizeIndex').textContent = Math.round(data.size.size_index);
            document.getElementById('sizeBar').style.width = data.size.size_index + '%';
            var sizeKey = data.size.size_key;
            var sizeHint = {
                'micro': 'узкая аудитория',
                'small': 'для теста идеи',
                'medium': 'хороший потенциал',
                'large': 'большой рынок',
                'huge': 'массовый спрос'
            };
            document.getElementById('sizeLabel').innerHTML = data.size.size_icon + ' ' + (sizeHint[sizeKey] || data.size.size_label);
        }
        
        // Competition metric
        if (data.competition) {
            document.getElementById('compIndex').textContent = Math.round(data.competition.competition_index);
            document.getElementById('compBar').style.width = data.competition.competition_index + '%';
            var compKey = data.competition.competition_key;
            var compHint = {
                'low': 'можно заходить без бренда',
                'medium': 'нужна стратегия',
                'high': 'дорогой вход',
                'very_high': 'только для крупных игроков'
            };
            document.getElementById('compLabel').innerHTML = data.competition.competition_icon + ' ' + (compHint[compKey] || data.competition.competition_label);
        }
        
        // Seasonality
        if (data.seasonality) {
            var coef = data.seasonality.coefficient;
            document.getElementById('seasonIndex').textContent = '×' + coef.toFixed(2);
            var trend = data.seasonality.trend;
            var trendIcon = trend === 'growing' ? '📈' : trend === 'declining' ? '📉' : '➡️';
            document.getElementById('seasonLabel').innerHTML = trendIcon + ' ' + (coef < 0.8 ? 'низкий сезон' : coef > 1.2 ? 'высокий сезон' : 'норма');
            
            // Yearly growth
            var growth = data.seasonality.yearly_growth || 0;
            var growthEl = document.getElementById('growthIndex');
            var growthLabel = document.getElementById('growthLabel');
            var prefix = growth >= 0 ? '+' : '';
            growthEl.textContent = prefix + growth.toFixed(0) + '%';
            growthEl.style.color = growth >= 0 ? '#22c55e' : '#ef4444';
            if (growth > 50) {
                growthLabel.innerHTML = '🚀 быстрый рост';
            } else if (growth > 10) {
                growthLabel.innerHTML = '📈 растёт';
            } else if (growth > -10) {
                growthLabel.innerHTML = '➡️ стабильно';
            } else {
                growthLabel.innerHTML = '📉 падает';
            }
        }
        
        // Insights
        renderInsights(data.insights);
        
        // Recommendations
        renderRecs(data.recommendations);
        
        // Chart hint
        if (data.clusters && data.clusters.length > 0) {
            var top = data.clusters[0];
            document.getElementById('chartHint').textContent = 'Основной спрос: ' + top.name + ' (' + top.share + '%)';
        }
        
        // Chart
        renderPieChart(data.clusters);
        
        // Clusters
        renderClusterList(data.clusters);
        

        
        document.getElementById('progressBar').classList.remove('active');
        document.getElementById('results').classList.add('active');
        
        // Load AI analysis async
        loadAIAnalysis(phrase, region);
        
    } catch(e) { alert('Ошибка: ' + e); }
    resetUI();
}

async function loadAIAnalysis(phrase, region) {
    document.getElementById('aiContent').innerHTML = '<div class="ai-loading"><div class="spinner"></div><div>Генерируем анализ...</div></div>';
    
    try {
        var resp = await fetch('/api/ai-analyze?phrase=' + encodeURIComponent(phrase) + '&region=' + region);
        var data = await resp.json();
        
        var html = '';
        
        // Summary
        if (data.ai_summary) {
            html += '<div class="ai-summary">' + data.ai_summary + '</div>';
        }
        
        // Suitable for
        if (data.ai_suitable_for && data.ai_suitable_for.length > 0) {
            html += '<div class="ai-section">';
            html += '<div class="ai-section-title">✅ Подходит для</div>';
            html += '<div class="ai-tags">';
            data.ai_suitable_for.forEach(function(s) {
                html += '<span class="ai-tag green">' + s + '</span>';
            });
            html += '</div></div>';
        }
        
        // Not suitable for
        if (data.ai_not_suitable_for && data.ai_not_suitable_for.length > 0) {
            html += '<div class="ai-section">';
            html += '<div class="ai-section-title">❌ Не подходит для</div>';
            html += '<div class="ai-tags">';
            data.ai_not_suitable_for.forEach(function(s) {
                html += '<span class="ai-tag red">' + s + '</span>';
            });
            html += '</div></div>';
        }
        
        // Scenarios v2.1 — компактный формат
        if (data.ai_scenarios && data.ai_scenarios.length > 0) {
            html += '<div class="ai-section">';
            html += '<div class="ai-section-title">🎯 Как заходить</div>';
            data.ai_scenarios.slice(0, 2).forEach(function(s, i) {
                if (typeof s === 'object') {
                    html += '<div class="scenario-card">';
                    html += '<div class="scenario-name">' + (s.name || '') + '</div>';
                    if (s.action) html += '<div class="scenario-action">' + s.action + '</div>';
                    if (s.risk) html += '<div class="scenario-risk">⚠️ ' + s.risk + '</div>';
                    html += '</div>';
                } else {
                    html += '<div class="scenario-card"><div class="scenario-name">' + s + '</div></div>';
                }
            });
            html += '</div>';
        }
        
        // Risks
        if (data.ai_risks && data.ai_risks.length > 0) {
            html += '<div class="ai-section">';
            html += '<div class="ai-section-title">⚠️ Риски</div>';
            html += '<ul class="ai-list">';
            data.ai_risks.forEach(function(r) {
                html += '<li><span class="icon">•</span><span class="text">' + r + '</span></li>';
            });
            html += '</ul></div>';
        }
        
        document.getElementById('aiContent').innerHTML = html || '<div style="color:#888">Не удалось получить анализ</div>';
        
    } catch(e) {
        document.getElementById('aiContent').innerHTML = '<div style="color:#888">Ошибка загрузки ИИ-анализа</div>';
    }
}

function updateProgress(pct, text) {
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = text;
}

function resetUI() { document.getElementById('btnAnalyze').disabled = false; }

function renderInsights(insights) {
    var html = '';
    insights.forEach(function(ins) {
        html += '<div class="insight-card">';
        html += '<div class="insight-header"><span class="insight-icon">' + ins.icon + '</span>';
        html += '<span class="insight-title">' + ins.title + '</span></div>';
        html += '<div class="insight-text">' + ins.text + '</div></div>';
    });
    document.getElementById('insightsGrid').innerHTML = html;
}

function renderRecs(recs) {
    if (!recs || recs.length === 0) {
        document.getElementById('recsCard').style.display = 'none';
        return;
    }
    var html = '';
    recs.forEach(function(r) {
        html += '<div class="rec-item"><span class="rec-icon">' + r.icon + '</span>';
        html += '<span class="rec-text">' + r.text + '</span></div>';
    });
    document.getElementById('recsList').innerHTML = html;
    document.getElementById('recsCard').style.display = 'block';
}

function renderPieChart(clusters) {
    var ctx = document.getElementById('pieChart').getContext('2d');
    if (pieChart) pieChart.destroy();
    
    var colors = ['#667eea','#764ba2','#f093fb','#f5576c','#4facfe','#00f2fe','#43e97b','#38f9d7','#fa709a','#fee140'];
    var top = clusters.slice(0, 8);
    var other = clusters.slice(8);
    var otherSum = other.reduce((a,c) => a + c.count, 0);
    
    var labels = top.map(c => c.name);
    var values = top.map(c => c.count);
    if (otherSum > 0) { labels.push('Другое'); values.push(otherSum); }
    
    pieChart = new Chart(ctx, {
        type: 'pie',
        data: { labels: labels, datasets: [{ data: values, backgroundColor: colors.slice(0, labels.length), borderWidth: 2, borderColor: '#fff' }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } } }
    });
}

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
        c.phrases.forEach(function(p) {
            html += '<div class="phrase-item"><span class="phrase-text">' + p.phrase + '</span>';
            html += '<span class="phrase-count">' + fmt(p.count) + '</span></div>';
        });
        html += '</div></div>';
    });
    document.getElementById('clusterList').innerHTML = html;
}

function toggleCluster(i) { document.getElementById('cluster-' + i).classList.toggle('open'); }

function renderSummary(data) {
    var card = document.getElementById('summaryCard');
    card.style.display = 'block';
    
    // Size
    if (data.size) {
        document.getElementById('sumSize').innerHTML = data.size.size_icon + ' ' + Math.round(data.size.size_index) + '/100';
    }
    
    // Competition
    if (data.competition) {
        document.getElementById('sumComp').innerHTML = data.competition.competition_icon + ' ' + Math.round(data.competition.competition_index) + '/100';
    }
    
    // Season
    if (data.seasonality) {
        var coef = data.seasonality.coefficient;
        var icon = coef < 0.8 ? '📉' : coef > 1.2 ? '📈' : '➡️';
        document.getElementById('sumSeason').innerHTML = icon + ' ×' + coef.toFixed(2);
    }
    
    // Top directions
    if (data.clusters && data.clusters.length > 0) {
        var html = '';
        data.clusters.slice(0, 3).forEach(function(c) {
            html += '<span class="summary-direction-tag">' + c.name + ' (' + c.share + '%)</span>';
        });
        document.getElementById('sumDirections').innerHTML = html;
    }
    
    // Verdict
    if (data.verdict) {
        document.getElementById('sumVerdict').innerHTML = data.verdict.verdict_icon + ' ' + data.verdict.verdict_label;
    }
}
</script>
</body>
</html>'''
