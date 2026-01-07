"""
HTML шаблон страницы анализа ниши v2
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

.card{background:white;border-radius:12px;padding:25px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.card h3{margin-bottom:20px;color:#333;font-size:1.1em}

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

/* Recommendations */
.recs-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;padding:25px;color:white;margin-bottom:20px}
.recs-card h3{color:white;margin-bottom:15px}
.rec-item{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.2)}
.rec-item:last-child{border-bottom:none}
.rec-icon{font-size:1.3em}
.rec-text{font-size:14px;line-height:1.5}
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

<div class="stats-row">
<div class="stat-card">
<div class="stat-value" id="statTotal">0</div>
<div class="stat-label">Запросов/мес</div>
</div>
<div class="stat-card">
<div class="stat-value" id="statQueries">0</div>
<div class="stat-label">Уникальных фраз</div>
</div>
<div class="stat-card">
<div class="stat-value" id="statClusters">0</div>
<div class="stat-label">Направлений</div>
</div>
<div class="stat-card">
<div class="stat-value" id="statSize">—</div>
<div class="stat-label">Размер ниши</div>
</div>
<div class="stat-card">
<div class="stat-value" id="statCompetition">—</div>
<div class="stat-label">Конкуренция</div>
</div>
</div>

<div class="insights-grid" id="insightsGrid"></div>

<div class="recs-card" id="recsCard" style="display:none">
<h3>💡 Рекомендации</h3>
<div id="recsList"></div>
</div>

<div class="grid-2">
<div class="card">
<h3>📊 Структура спроса</h3>
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
        var resp = await fetch('/api/analyze?phrase=' + encodeURIComponent(phrase) + '&region=' + region);
        var data = await resp.json();
        
        // Stats
        document.getElementById('statTotal').textContent = fmt(data.total_count);
        document.getElementById('statQueries').textContent = fmt(data.total_queries);
        document.getElementById('statClusters').textContent = data.clusters_count;
        document.getElementById('statSize').innerHTML = data.metrics.niche_size_icon + ' ' + data.metrics.niche_size;
        document.getElementById('statCompetition').innerHTML = data.metrics.competition_icon + ' ' + data.metrics.competition;
        
        // Insights
        renderInsights(data.insights);
        
        // Recommendations
        renderRecs(data.recommendations);
        
        // Chart
        renderPieChart(data.clusters);
        
        // Clusters
        renderClusterList(data.clusters);
        
        document.getElementById('progressBar').classList.remove('active');
        document.getElementById('results').classList.add('active');
    } catch(e) { alert('Ошибка: ' + e); }
    resetUI();
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
    clusters.forEach(function(c, i) {
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
</script>
</body>
</html>'''
