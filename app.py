#!/usr/bin/env python3
"""
Wordstat Analytics - Сервис анализа поискового спроса
"""
from flask import Flask, render_template_string, request, jsonify
import requests
import threading

import database as db
import collector

app = Flask(__name__)

TOKEN = "y0__xCHu4rZARjd0Dogyfj_7RQJLwxI8zao8Pru2PA2l5w2HjR6dA"
BASE_URL = "https://api.wordstat.yandex.net"
HEADERS = {"Content-Type": "application/json;charset=utf-8", "Authorization": f"Bearer {TOKEN}"}
REGIONS = {0: "Все регионы", 225: "Россия", 213: "Москва", 1: "Московская область", 2: "Санкт-Петербург", 54: "Екатеринбург", 65: "Новосибирск", 43: "Казань", 35: "Краснодар"}

# ==================== СТРАНИЦА АНАЛИЗА НИШИ ====================

ANALYZE_HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Поиск ниш — Wordstat Analytics</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);min-height:100vh;padding:20px;color:#fff}
.container{max-width:1200px;margin:0 auto}
h1{text-align:center;margin-bottom:10px;font-size:2.2em;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.subtitle{text-align:center;color:#888;margin-bottom:30px}
.card{background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-radius:16px;padding:30px;border:1px solid rgba(255,255,255,0.1);margin-bottom:20px}
.search-box{display:flex;gap:15px;margin-bottom:20px}
.search-box input{flex:1;padding:16px 20px;border:2px solid rgba(255,255,255,0.1);border-radius:12px;font-size:18px;background:rgba(255,255,255,0.05);color:#fff}
.search-box input:focus{outline:none;border-color:#667eea}
.search-box input::placeholder{color:#666}
.search-box select{padding:16px;border-radius:12px;background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);color:#fff;font-size:16px}
.btn{padding:16px 32px;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;transition:transform 0.2s,box-shadow 0.2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(102,126,234,0.3)}
.btn:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.progress-container{display:none;margin:20px 0}
.progress-bar{height:8px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(135deg,#667eea,#764ba2);width:0%;transition:width 0.3s}
.progress-text{text-align:center;margin-top:10px;color:#888;font-size:14px}
.results{display:none}
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}
.stat-card{background:linear-gradient(135deg,rgba(102,126,234,0.2),rgba(118,75,162,0.2));border-radius:12px;padding:20px;text-align:center;border:1px solid rgba(255,255,255,0.1)}
.stat-value{font-size:2em;font-weight:bold;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{color:#888;margin-top:5px;font-size:14px}
.section-title{font-size:1.3em;margin:30px 0 15px;color:#fff;display:flex;align-items:center;gap:10px}
.section-title span{font-size:1.2em}
table{width:100%;border-collapse:collapse}
th,td{padding:12px 15px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.1)}
th{color:#888;font-weight:500;font-size:14px}
td{color:#fff}
tr:hover{background:rgba(255,255,255,0.03)}
.count{color:#667eea;font-weight:600}
.depth-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:12px;background:rgba(102,126,234,0.2);color:#667eea}
.chart-container{background:rgba(255,255,255,0.03);border-radius:12px;padding:20px;margin:20px 0}
.empty-state{text-align:center;padding:60px 20px;color:#666}
.empty-state h3{margin-bottom:10px;color:#888}
.nav{display:flex;gap:20px;margin-bottom:30px;justify-content:center}
.nav a{color:#888;text-decoration:none;padding:10px 20px;border-radius:8px;transition:all 0.2s}
.nav a:hover,.nav a.active{color:#fff;background:rgba(255,255,255,0.1)}
</style>
</head>
<body>
<div class="container">
<nav class="nav">
<a href="/">Простой режим</a>
<a href="/analyze" class="active">Поиск ниш</a>
</nav>

<h1>🔍 Поиск ниш</h1>
<p class="subtitle">Глубокий анализ поискового спроса</p>

<div class="card">
<div class="search-box">
<input type="text" id="phrase" placeholder="Введите нишу, например: купить телефон" value="">
<select id="region">
{% for c,n in regions.items() %}<option value="{{c}}"{% if c==225 %} selected{% endif %}>{{n}}</option>{% endfor %}
</select>
<button class="btn" id="analyzeBtn" onclick="startAnalysis()">Анализировать</button>
</div>

<div class="progress-container" id="progress">
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
<div class="progress-text" id="progressText">Подготовка...</div>
</div>
</div>

<div class="results" id="results">
<div class="stat-grid">
<div class="stat-card">
<div class="stat-value" id="totalQueries">0</div>
<div class="stat-label">Запросов собрано</div>
</div>
<div class="stat-card">
<div class="stat-value" id="totalVolume">0</div>
<div class="stat-label">Общий объём</div>
</div>
<div class="stat-card">
<div class="stat-value" id="apiCalls">0</div>
<div class="stat-label">API запросов</div>
</div>
<div class="stat-card">
<div class="stat-value" id="elapsed">0s</div>
<div class="stat-label">Время сбора</div>
</div>
</div>

<div class="card">
<div class="section-title"><span>📊</span> Топ запросов ниши</div>
<table>
<thead><tr><th>#</th><th>Запрос</th><th>Частотность</th><th>Уровень</th></tr></thead>
<tbody id="queriesTable"></tbody>
</table>
</div>
</div>

<div class="empty-state" id="emptyState">
<h3>Введите нишу для анализа</h3>
<p>Сервис соберёт все связанные запросы и покажет структуру спроса</p>
</div>
</div>

<script>
var projectId = null;
var pollInterval = null;

function fmt(n) {
    if (n === null || n === undefined) return '0';
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

async function startAnalysis() {
    var phrase = document.getElementById('phrase').value.trim();
    var region = parseInt(document.getElementById('region').value);
    
    if (!phrase) {
        alert('Введите поисковую фразу');
        return;
    }
    
    // UI: показываем прогресс
    document.getElementById('analyzeBtn').disabled = true;
    document.getElementById('progress').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('progressFill').style.width = '10%';
    document.getElementById('progressText').innerText = 'Запуск сбора...';
    
    try {
        // Запускаем сбор
        var r = await fetch('/api/collect/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({phrase: phrase, region: region})
        });
        var data = await r.json();
        
        if (data.error) {
            alert('Ошибка: ' + data.error);
            resetUI();
            return;
        }
        
        projectId = data.project_id;
        
        // Начинаем опрос статуса
        pollInterval = setInterval(pollStatus, 1000);
        
    } catch(e) {
        alert('Ошибка: ' + e);
        resetUI();
    }
}

async function pollStatus() {
    if (!projectId) return;
    
    try {
        var r = await fetch('/api/collect/status/' + projectId);
        var data = await r.json();
        
        // Обновляем прогресс
        var progress = Math.min(90, 10 + (data.total_queries_found || 0) / 5);
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressText').innerText = 
            'Собрано ' + data.total_queries_found + ' запросов (API: ' + data.total_api_calls + ')';
        
        if (data.status === 'completed') {
            clearInterval(pollInterval);
            document.getElementById('progressFill').style.width = '100%';
            document.getElementById('progressText').innerText = 'Готово!';
            setTimeout(loadResults, 500);
        } else if (data.status === 'error') {
            clearInterval(pollInterval);
            alert('Ошибка сбора: ' + (data.error || 'Unknown'));
            resetUI();
        }
        
    } catch(e) {
        console.error('Poll error:', e);
    }
}

async function loadResults() {
    try {
        var r = await fetch('/api/collect/results/' + projectId);
        var data = await r.json();
        
        // Заполняем статистику
        document.getElementById('totalQueries').innerText = fmt(data.stats.total_queries);
        document.getElementById('totalVolume').innerText = fmt(data.stats.total_volume);
        document.getElementById('apiCalls').innerText = data.state ? data.state.total_api_calls : '-';
        document.getElementById('elapsed').innerText = (data.state ? data.state.elapsed_seconds : 0) + 's';
        
        // Заполняем таблицу
        var html = '';
        var queries = data.queries || [];
        for (var i = 0; i < Math.min(queries.length, 100); i++) {
            var q = queries[i];
            html += '<tr><td>' + (i+1) + '</td><td>' + q.phrase + '</td><td class="count">' + fmt(q.count) + '</td><td><span class="depth-badge">L' + q.depth + '</span></td></tr>';
        }
        document.getElementById('queriesTable').innerHTML = html;
        
        // Показываем результаты
        document.getElementById('progress').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        document.getElementById('analyzeBtn').disabled = false;
        
    } catch(e) {
        alert('Ошибка загрузки результатов: ' + e);
        resetUI();
    }
}

function resetUI() {
    document.getElementById('analyzeBtn').disabled = false;
    document.getElementById('progress').style.display = 'none';
    document.getElementById('emptyState').style.display = 'block';
    if (pollInterval) clearInterval(pollInterval);
}
</script>
</body>
</html>'''


# ==================== ПРОСТОЙ РЕЖИМ (старый интерфейс) ====================

HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wordstat API</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
.container{max-width:1000px;margin:0 auto}
h1{color:white;text-align:center;margin-bottom:30px;font-size:2.5em}
.nav{display:flex;gap:20px;margin-bottom:30px;justify-content:center}
.nav a{color:rgba(255,255,255,0.8);text-decoration:none;padding:10px 20px;border-radius:8px;transition:all 0.2s}
.nav a:hover,.nav a.active{color:#fff;background:rgba(255,255,255,0.2)}
.card{background:white;border-radius:16px;padding:30px;box-shadow:0 10px 40px rgba(0,0,0,0.2)}
.form-group{margin-bottom:20px}
label{display:block;margin-bottom:8px;font-weight:600;color:#333}
input[type="text"],select{width:100%;padding:14px;border:2px solid #e0e0e0;border-radius:10px;font-size:16px}
input:focus,select:focus{outline:none;border-color:#667eea}
.btn-group{display:flex;gap:10px;flex-wrap:wrap}
button{flex:1;min-width:140px;padding:14px;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;color:white}
.btn-primary{background:linear-gradient(135deg,#667eea,#764ba2)}
.btn-secondary{background:linear-gradient(135deg,#11998e,#38ef7d)}
.btn-info{background:linear-gradient(135deg,#fc4a1a,#f7b733)}
.btn-dark{background:linear-gradient(135deg,#434343,#000)}
#res{margin-top:30px;min-height:100px;background:#fafafa;border-radius:10px;padding:20px}
#res h3{color:#333;margin-bottom:15px;padding-bottom:10px;border-bottom:2px solid #667eea}
.stat-box{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:20px;border-radius:12px;text-align:center;margin-bottom:20px}
.stat-box .value{font-size:2em;font-weight:bold}
.chart-container{background:white;border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
table{width:100%;border-collapse:collapse;margin-top:15px}
th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd}
th{background:#f0f0f0;font-weight:600}
tr:hover{background:#f5f5f5}
.count{font-weight:600;color:#667eea}
.loading{text-align:center;padding:40px;color:#666}
.error{background:#fee;color:#c00;padding:15px;border-radius:10px}
.quota-info{background:#f0f7ff;padding:15px;border-radius:10px;margin-bottom:20px;display:flex;justify-content:space-around}
.quota-item{text-align:center}
.quota-item .value{font-size:1.5em;font-weight:bold;color:#667eea}
.debug-panel{background:#1e1e1e;border-radius:10px;padding:15px;margin-top:20px;font-family:monospace;font-size:12px;max-height:200px;overflow-y:auto}
.debug-panel h4{color:#888;margin-bottom:10px;display:flex;justify-content:space-between}
.debug-panel h4 button{background:#333;border:none;color:#888;padding:5px 10px;border-radius:5px;cursor:pointer;font-size:11px;min-width:auto;flex:none;margin-left:5px}
.debug-log{margin:3px 0;padding:3px}
.log-info{color:#4fc3f7}
.log-ok{color:#81c784}
.log-err{color:#e57373}
.log-time{color:#666;margin-right:8px}
</style>
</head>
<body>
<div class="container">
<nav class="nav">
<a href="/" class="active">Простой режим</a>
<a href="/analyze">Поиск ниш</a>
</nav>
<h1>Wordstat API</h1>
<div class="card">
<div class="quota-info">
<div class="quota-item"><div class="value" id="qr">-</div><div>Осталось</div></div>
<div class="quota-item"><div class="value" id="ql">-</div><div>Лимит</div></div>
</div>
<div class="form-group"><label>Поисковая фраза</label><input type="text" id="phrase" value="купить телефон"></div>
<div class="form-group"><label>Регион</label><select id="region">{% for c,n in regions.items() %}<option value="{{c}}"{% if c==213 %} selected{% endif %}>{{n}}</option>{% endfor %}</select></div>
<div class="btn-group">
<button class="btn-primary" onclick="doTop()">Топ запросов</button>
<button class="btn-secondary" onclick="doDyn()">Динамика</button>
<button class="btn-info" onclick="doReg()">Регионы</button>
<button class="btn-dark" onclick="doQuota()">Квота</button>
</div>
<div id="res">Нажмите кнопку для загрузки данных</div>
<div class="debug-panel"><h4><span>Console</span><span><button onclick="copyLog()">Копировать</button><button onclick="clrLog()">Очистить</button></span></h4><div id="logs"></div></div>
</div>
</div>
<script>
var L=document.getElementById('logs');var R=document.getElementById('res');var chart=null;
var REGION_NAMES={1:'Москва и область',2:'Санкт-Петербург',35:'Краснодар',43:'Казань',54:'Екатеринбург',65:'Новосибирск',213:'Москва',225:'Россия'};
function t(){return new Date().toLocaleTimeString('ru-RU')}
function log(m,c){var d=document.createElement('div');d.className='debug-log log-'+c;d.innerHTML='<span class="log-time">['+t()+']</span>'+m;L.appendChild(d);L.parentElement.scrollTop=9999}
function clrLog(){L.innerHTML='';log('Очищено','info')}
function copyLog(){var a=document.createElement('textarea');a.value=L.innerText;document.body.appendChild(a);a.select();document.execCommand('copy');document.body.removeChild(a);log('Скопировано','ok')}
function fmt(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,' ')}
function render(html){R.innerHTML=html;log('Rendered '+html.length+' chars','ok')}
function getRegionName(id){return REGION_NAMES[id]||('ID:'+id)}
async function updateQuota(){try{var r=await fetch('/api/userInfo',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});var j=await r.json();var i=j.userInfo||{};document.getElementById('qr').innerText=i.dailyLimitRemaining||'-';document.getElementById('ql').innerText=i.dailyLimit||'-';log('Quota: '+i.dailyLimitRemaining+'/'+i.dailyLimit,'ok');}catch(e){log('Quota error: '+e,'err')}}
async function doQuota(){render('<div class="loading">Загрузка...</div>');log('POST /api/userInfo','info');try{var r=await fetch('/api/userInfo',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});var j=await r.json();log('Status: '+r.status,'ok');var i=j.userInfo||{};document.getElementById('qr').innerText=i.dailyLimitRemaining||'-';document.getElementById('ql').innerText=i.dailyLimit||'-';render('<h3>Квота</h3><p>Логин: '+i.login+'</p><p>Осталось: '+i.dailyLimitRemaining+' из '+i.dailyLimit+'</p>');}catch(e){render('<div class="error">'+e+'</div>')}}
async function doTop(){var p=document.getElementById('phrase').value;var reg=parseInt(document.getElementById('region').value);render('<div class="loading">Загрузка...</div>');log('POST /api/topRequests','info');try{var r=await fetch('/api/topRequests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phrase:p,region:reg})});var d=await r.json();log('Status: '+r.status+', Keys: '+Object.keys(d).join(','),'ok');if(d.error){render('<div class="error">'+d.error+'</div>');return}var items=d.topRequests||[];var assoc=d.associations||[];log('Items: '+items.length+', Assoc: '+assoc.length,'ok');var h='<h3>Топ запросов: "'+p+'"</h3>';h+='<div class="stat-box"><div class="value">'+fmt(d.totalCount||0)+'</div><div>Всего запросов</div></div>';h+='<table><thead><tr><th>#</th><th>Запрос</th><th>Частота</th></tr></thead><tbody>';for(var i=0;i<Math.min(items.length,20);i++){h+='<tr><td>'+(i+1)+'</td><td>'+items[i].phrase+'</td><td class="count">'+fmt(items[i].count)+'</td></tr>';}h+='</tbody></table>';if(assoc.length>0){h+='<h3 style="margin-top:25px">Похожие запросы</h3><table><thead><tr><th>#</th><th>Запрос</th><th>Частота</th></tr></thead><tbody>';for(var i=0;i<Math.min(assoc.length,10);i++){h+='<tr><td>'+(i+1)+'</td><td>'+assoc[i].phrase+'</td><td class="count">'+fmt(assoc[i].count)+'</td></tr>';}h+='</tbody></table>';}render(h);updateQuota();}catch(e){render('<div class="error">'+e+'</div>')}}
async function doDyn(){var p=document.getElementById('phrase').value;var reg=parseInt(document.getElementById('region').value);render('<div class="loading">Загрузка...</div>');log('POST /api/dynamics','info');try{var r=await fetch('/api/dynamics',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phrase:p,region:reg})});var d=await r.json();log('Status: '+r.status,'ok');if(d.error){render('<div class="error">'+d.error+'</div>');return}var items=d.dynamics||[];log('Dynamics: '+items.length+' items','ok');var labels=[];var data=[];var months=['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек'];for(var i=0;i<items.length;i++){var dt=items[i].date;var m=parseInt(dt.slice(5,7))-1;labels.push(months[m]+' '+dt.slice(0,4));data.push(items[i].count);}var h='<h3>Динамика: "'+p+'"</h3><div class="chart-container"><canvas id="dynChart"></canvas></div><table><thead><tr><th>Месяц</th><th>Запросов</th><th>Доля</th></tr></thead><tbody>';for(var i=0;i<items.length;i++){h+='<tr><td>'+items[i].date.slice(0,7)+'</td><td class="count">'+fmt(items[i].count)+'</td><td>'+(items[i].share*100).toFixed(2)+'%</td></tr>';}h+='</tbody></table>';render(h);if(chart)chart.destroy();var ctx=document.getElementById('dynChart').getContext('2d');chart=new Chart(ctx,{type:'line',data:{labels:labels,datasets:[{label:'Запросов',data:data,borderColor:'#667eea',backgroundColor:'rgba(102,126,234,0.1)',borderWidth:3,fill:true,tension:0.3,pointBackgroundColor:'#667eea',pointBorderColor:'#fff',pointBorderWidth:2,pointRadius:5,pointHoverRadius:7}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:{backgroundColor:'#333',titleFont:{size:14},bodyFont:{size:13},padding:12,callbacks:{label:function(ctx){return fmt(ctx.raw)+' запросов'}}}},scales:{y:{beginAtZero:false,ticks:{callback:function(v){return fmt(v)}},grid:{color:'rgba(0,0,0,0.05)'}},x:{grid:{display:false}}}}});log('Chart rendered','ok');updateQuota();}catch(e){render('<div class="error">'+e+'</div>')}}
async function doReg(){var p=document.getElementById('phrase').value;render('<div class="loading">Загрузка...</div>');log('POST /api/regions','info');try{var r=await fetch('/api/regions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phrase:p})});var d=await r.json();log('Status: '+r.status,'ok');if(d.error){render('<div class="error">'+d.error+'</div>');return}var items=d.regions||[];log('Regions: '+items.length+' items','ok');var h='<h3>Регионы: "'+p+'"</h3><table><thead><tr><th>#</th><th>Регион</th><th>Запросов</th><th>Доля</th></tr></thead><tbody>';for(var i=0;i<Math.min(items.length,20);i++){var name=getRegionName(items[i].regionId);h+='<tr><td>'+(i+1)+'</td><td>'+name+'</td><td class="count">'+fmt(items[i].count)+'</td><td>'+(items[i].share*100).toFixed(2)+'%</td></tr>';}h+='</tbody></table>';render(h);updateQuota();}catch(e){render('<div class="error">'+e+'</div>')}}
window.onerror=function(m,u,l){log('JS: '+m+' line '+l,'err')};log('Ready','ok');updateQuota();
</script>
</body>
</html>'''


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template_string(HTML, regions=REGIONS)


@app.route('/analyze')
def analyze():
    return render_template_string(ANALYZE_HTML, regions=REGIONS)


# ==================== API: Простой режим ====================

@app.route('/api/userInfo', methods=['POST'])
def api_user_info():
    try:
        r = requests.post(f"{BASE_URL}/v1/userInfo", headers=HEADERS, json={}, timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/topRequests', methods=['POST'])
def api_top_requests():
    try:
        data = request.json or {}
        payload = {"phrase": data.get("phrase", "")}
        region = data.get("region", 0)
        if region and region != 0:
            payload["regions"] = [region]
        r = requests.post(f"{BASE_URL}/v1/topRequests", headers=HEADERS, json=payload, timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/dynamics', methods=['POST'])
def api_dynamics():
    try:
        data = request.json or {}
        payload = {"phrase": data.get("phrase", ""), "period": "monthly", "fromDate": "2025-01-01", "toDate": "2025-12-31"}
        region = data.get("region", 0)
        if region and region != 0:
            payload["regions"] = [region]
        r = requests.post(f"{BASE_URL}/v1/dynamics", headers=HEADERS, json=payload, timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/regions', methods=['POST'])
def api_regions():
    try:
        data = request.json or {}
        payload = {"phrase": data.get("phrase", "")}
        r = requests.post(f"{BASE_URL}/v1/regions", headers=HEADERS, json=payload, timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


# ==================== API: Глубокий сбор ====================

@app.route('/api/collect/start', methods=['POST'])
def api_collect_start():
    """Запустить глубокий сбор"""
    try:
        data = request.json or {}
        phrase = data.get("phrase", "").strip()
        region = data.get("region", 225)
        
        if not phrase:
            return jsonify({"error": "Phrase is required"})
        
        # Запускаем сбор в отдельном потоке
        def run_collector():
            collector.collect_deep(phrase, region_id=region, max_depth=2)
        
        # Создаём проект сразу, чтобы вернуть ID
        project_id = db.create_project(phrase, region)
        
        # Запускаем сбор
        thread = threading.Thread(target=lambda: collector.collect_deep(phrase, region_id=region, max_depth=2))
        thread.daemon = True
        thread.start()
        
        return jsonify({"project_id": project_id, "status": "started"})
        
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/collect/status/<int:project_id>')
def api_collect_status(project_id):
    """Получить статус сбора"""
    state = collector.get_collector_state(project_id)
    if state:
        return jsonify(state)
    return jsonify({"error": "Project not found"}), 404


@app.route('/api/collect/results/<int:project_id>')
def api_collect_results(project_id):
    """Получить результаты сбора"""
    project = db.get_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    queries = db.get_all_queries(project_id)
    stats = db.get_project_stats(project_id)
    state = collector.get_collector_state(project_id)
    
    return jsonify({
        "project": project,
        "queries": queries,
        "stats": stats,
        "state": state
    })




# ==================== НОВЫЕ ENDPOINTS ДЛЯ ГЛУБОКОГО СБОРА ====================

@app.route('/api/deepCollect', methods=['POST'])
def api_deep_collect():
    """Запустить глубокий сбор запросов"""
    try:
        data = request.json or {}
        phrase = data.get("phrase", "").strip()
        region = data.get("region", 225)
        max_depth = data.get("max_depth", 2)
        
        if not phrase:
            return jsonify({"error": "Phrase is required"})
        
        # Запускаем сбор в отдельном потоке
        def run_collection():
            from collector import deep_collect
            deep_collect(phrase, region_id=region, max_depth=max_depth)
        
        thread = threading.Thread(target=run_collection)
        thread.daemon = True
        thread.start()
        
        return jsonify({"status": "started", "phrase": phrase, "region": region})
        
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/collectStatus')
def api_collect_status_simple():
    """Получить статус текущего сбора"""
    from collector import get_collect_status
    return jsonify(get_collect_status())


@app.route('/api/collectedQueries')
def api_collected_queries():
    """Получить собранные запросы"""
    from database import get_all_queries, get_query_count
    
    region = request.args.get("region", 225, type=int)
    queries = get_all_queries(region)
    count = get_query_count(region)
    
    return jsonify({
        "total": count,
        "queries": queries[:500]
    })



@app.route('/api/clusters')
def api_clusters():
    """Получить кластеры запросов"""
    from database import get_all_queries
    from clusterer import clusterize
    
    region = request.args.get("region", 225, type=int)
    root_phrase = request.args.get("phrase", "")
    
    queries = get_all_queries(region)
    
    if not queries:
        return jsonify({"error": "No data. Run deepCollect first."})
    
    result = clusterize(queries, root_phrase)
    return jsonify(result)



@app.route('/niche')
def niche_page():
    """Страница анализа ниши"""
    from templates_analyze import ANALYZE_HTML
    return ANALYZE_HTML



@app.route('/api/analyze')
def api_analyze():
    """Полный анализ ниши с выводами"""
    from database import get_all_queries
    from clusterer import clusterize
    from analyzer import analyze_niche
    
    region = request.args.get("region", 225, type=int)
    phrase = request.args.get("phrase", "")
    
    queries = get_all_queries(region)
    if not queries:
        return jsonify({"error": "No data"})
    
    clusters = clusterize(queries, phrase)
    analysis = analyze_niche(queries, clusters, phrase)
    
    return jsonify({
        "phrase": phrase,
        "total_count": clusters["total_count"],
        "total_queries": clusters["total_queries"],
        "clusters": clusters["clusters"],
        "clusters_count": clusters["clusters_count"],
        "metrics": analysis["metrics"],
        "insights": analysis["insights"],
        "recommendations": analysis["recommendations"],
        "summary": analysis["summary"]
    })



@app.route('/api/ai-analyze')
def api_ai_analyze():
    """ИИ-анализ ниши v2.0"""
    from analyzer_v2 import analyze_niche_v2
    from ai_analyzer import generate_ai_analysis
    
    region = request.args.get("region", 225, type=int)
    phrase = request.args.get("phrase", "")
    
    # Получаем данные v2
    data = analyze_niche_v2(phrase, region)
    if "error" in data:
        return jsonify({"error": data["error"]})
    
    # Формируем метрики для ИИ (v3 — на основе YoY)
    seasonality = data.get("seasonality", {})
    metrics_for_ai = {
        # Главные метрики YoY
        "now_count": seasonality.get("now_count", 0),
        "year_ago_count": seasonality.get("year_ago_count", 0),
        "yoy_percent": seasonality.get("yoy_percent", 0),
        "current_month_label": seasonality.get("current_month_label", ""),
        "year_ago_month_label": seasonality.get("year_ago_month_label", ""),
        
        # Вердикт
        "verdict": data.get("verdict", {}).get("verdict", "conditional"),
        "verdict_label": data.get("verdict", {}).get("verdict_label", ""),
    }
    
    # Генерируем ИИ-анализ
    ai_result = generate_ai_analysis(phrase, metrics_for_ai, data.get("clusters", []))
    
    return jsonify({
        "phrase": phrase,
        "ai_summary": ai_result.get("summary", ""),
        "ai_scenarios": ai_result.get("scenarios", []),
        "ai_suitable_for": ai_result.get("suitable_for", []),
        "ai_not_suitable_for": ai_result.get("not_suitable_for", []),
        "ai_risks": ai_result.get("risks", []),
        "_tokens": ai_result.get("_tokens", 0)
    })



@app.route('/api/analyze-v2')
def api_analyze_v2():
    """Полный анализ ниши v2.0 с новыми метриками"""
    from analyzer_v2 import analyze_niche_v2
    
    region = request.args.get("region", 225, type=int)
    phrase = request.args.get("phrase", "")
    
    result = analyze_niche_v2(phrase, region)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
