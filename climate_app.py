import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="مناخي - اكتشف عالم المناخ")

# ==========================================
# 1. Mock Data - البيانات التجريبية
# ==========================================
CITIES_DATA = {
    "دمياط": {
        "temperature": 31,
        "humidity": 72,
        "wind": 18,
        "rain": 10,
        "coastal_risk": "مرتفع 🌊",
        "heat_index": 34,
        "trend": [28, 29, 29, 30, 31, 31, 32]
    },
    "القاهرة": {
        "temperature": 37,
        "humidity": 40,
        "wind": 12,
        "rain": 0,
        "coastal_risk": "منخفض 🏙️",
        "heat_index": 39,
        "trend": [34, 35, 36, 36, 37, 37, 38]
    },
    "الإسكندرية": {
        "temperature": 30,
        "humidity": 75,
        "wind": 22,
        "rain": 20,
        "coastal_risk": "مرتفع 🌊",
        "heat_index": 33,
        "trend": [27, 28, 28, 29, 30, 29, 31]
    },
    "بورسعيد": {
        "temperature": 31,
        "humidity": 70,
        "wind": 20,
        "rain": 15,
        "coastal_risk": "متوسط 🌊",
        "heat_index": 33,
        "trend": [28, 28, 29, 30, 31, 31, 31]
    },
    "المنصورة": {
        "temperature": 34,
        "humidity": 55,
        "wind": 14,
        "rain": 5,
        "coastal_risk": "منخفض 🌳",
        "heat_index": 36,
        "trend": [31, 32, 33, 33, 34, 35, 35]
    },
    "أسوان": {
        "temperature": 42,
        "humidity": 15,
        "wind": 10,
        "rain": 0,
        "coastal_risk": "منعدم ☀️",
        "heat_index": 42,
        "trend": [40, 41, 41, 42, 42, 43, 43]
    }
}

def analyze_climate(city_data):
    """تحليل البيانات لتوليد مؤشر المناخ التعليمي"""
    score = 100
    reasons = []
    
    t = city_data["temperature"]
    h = city_data["humidity"]
    
    # تحليل الحرارة
    if t > 35:
        score -= 20
        reasons.append("الحرارة مرتفعة وتحتاج لشرب الكثير من الماء 💧")
    elif t < 15:
        score -= 10
        reasons.append("الجو بارد، ارتدِ ملابس ثقيلة 🧥")
    else:
        reasons.append("درجة الحرارة معتدلة وجميلة ☀️")
        
    # تحليل الرطوبة
    if h > 60:
        score -= 10
        reasons.append("الرطوبة مرتفعة قليلاً، قد تشعر بالحر أكثر 💦")
    else:
        reasons.append("مستوى الرطوبة مريح ☁️")
        
    # تحليل الرياح والمطر
    if city_data["wind"] > 20:
        score -= 5
        reasons.append("الرياح نشطة اليوم 🌬️")
    if city_data["rain"] > 0:
        reasons.append("هناك احتمال لتساقط الأمطار 🌧️")
        
    # تحديد التقييم
    if score >= 85:
        label = "ممتاز 🌟"
    elif score >= 70:
        label = "جيد 😊"
    elif score >= 50:
        label = "متوسط 🙂"
    else:
        label = "يحتاج انتباه 🌱"
        
    return score, label, reasons

# ==========================================
# 2. API Endpoints - مسارات واجهة برمجة التطبيقات
# ==========================================
@app.get("/api/climate")
def get_climate(city: str = "دمياط"):
    data = CITIES_DATA.get(city, CITIES_DATA["دمياط"])
    score, label, reasons = analyze_climate(data)
    
    return {
        "city": city,
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind": data["wind"],
        "rain": data["rain"],
        "coastal_risk": data["coastal_risk"],
        "heat_index": data["heat_index"],
        "trend": data["trend"],
        "climate_score": score,
        "label": label,
        "reasons": reasons
    }

# ==========================================
# 3. Frontend HTML/CSS/JS (All in one string)
# ==========================================
HTML_CONTENT = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مناخي | اكتشف عالم المناخ 🌍</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --sky-blue: #70C1B3;
            --light-blue: #B2EBF2;
            --mint-green: #A3E4D7;
            --soft-green: #D5F5E3;
            --yellow: #FDEBD0;
            --white: #FFFFFF;
            --light-orange: #FAD7A1;
            --text-dark: #2C3E50;
            --bg-color: #F4FAFC;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Cairo', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-dark);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* --- Header & Hero --- */
        .hero {
            background: linear-gradient(135deg, var(--light-blue), var(--mint-green));
            padding: 60px 20px;
            text-align: center;
            border-bottom-left-radius: 50px;
            border-bottom-right-radius: 50px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            margin-bottom: 40px;
        }

        .hero h1 {
            font-size: 3rem;
            color: var(--text-dark);
            margin-bottom: 10px;
        }

        .hero p {
            font-size: 1.2rem;
            max-width: 600px;
            margin: 0 auto 20px auto;
            color: #34495E;
        }

        .city-selector {
            background: var(--white);
            padding: 15px 30px;
            border-radius: 30px;
            display: inline-flex;
            gap: 15px;
            align-items: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        select {
            padding: 10px 20px;
            border: 2px solid var(--sky-blue);
            border-radius: 20px;
            font-size: 1.1rem;
            font-family: inherit;
            outline: none;
            background: var(--white);
            cursor: pointer;
        }

        .btn {
            background: var(--sky-blue);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 20px;
            font-size: 1.1rem;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s, background 0.2s;
        }

        .btn:hover {
            transform: scale(1.05);
            background: #5FB4A5;
        }

        /* --- Container --- */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .section-title {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 30px;
            position: relative;
            display: inline-block;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .section-title::after {
            content: "";
            display: block;
            width: 50%;
            height: 4px;
            background: var(--light-orange);
            margin: 5px auto 0 auto;
            border-radius: 2px;
        }

        /* --- Grid Layouts --- */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 50px; }
        .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 50px;}

        /* --- Cards --- */
        .card {
            background: var(--white);
            border-radius: 30px;
            padding: 25px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
            transition: transform 0.3s;
            text-align: center;
            border: 2px solid transparent;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: var(--soft-green);
        }

        .card-emoji { font-size: 3rem; margin-bottom: 10px; }
        .card-value { font-size: 2rem; font-weight: 900; color: var(--sky-blue); }
        .card-title { font-size: 1.2rem; color: #7F8C8D; }

        /* --- Climate Score --- */
        .score-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--soft-green), var(--white));
            border-radius: 40px;
            padding: 30px;
        }

        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: var(--white);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border: 5px solid var(--sky-blue);
            margin-bottom: 20px;
        }

        .score-number { font-size: 2.5rem; font-weight: 900; }
        .score-label { font-size: 1.5rem; font-weight: bold; color: var(--sky-blue); }
        .reasons-list { text-align: right; width: 100%; list-style: none; padding-right: 20px;}
        .reasons-list li { margin-bottom: 10px; font-size: 1.1rem; position: relative;}
        .reasons-list li::before { content: "✨"; position: absolute; right: -25px; }

        /* --- Trend Chart --- */
        .chart-card {
            background: var(--white);
            border-radius: 30px;
            padding: 30px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        }
        
        .chart-container {
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            height: 200px;
            margin-top: 20px;
            padding-bottom: 20px;
            border-bottom: 2px dashed #BDC3C7;
        }

        .bar-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 12%;
        }

        .bar {
            width: 100%;
            background: linear-gradient(to top, var(--sky-blue), var(--light-blue));
            border-radius: 10px 10px 0 0;
            transition: height 1s ease-out;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding-top: 5px;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .bar-label { margin-top: 10px; font-size: 0.9rem; color: #7F8C8D; }
        .chart-note { margin-top: 20px; padding: 15px; background: var(--yellow); border-radius: 15px; font-size: 0.95rem; }

        /* --- Carbon Footprint --- */
        .footprint-section {
            background: var(--white);
            border-radius: 40px;
            padding: 40px;
            margin-bottom: 50px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        }

        .fp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .fp-item label { display: block; margin-bottom: 10px; font-weight: bold; }
        .fp-item input { width: 100%; padding: 10px; border-radius: 15px; border: 2px solid var(--soft-green); outline: none; font-family: inherit;}
        
        .fp-result {
            text-align: center;
            padding: 20px;
            background: var(--soft-green);
            border-radius: 20px;
            font-size: 1.5rem;
            font-weight: bold;
            display: none;
        }

        /* --- Challenges --- */
        .challenges-section { margin-bottom: 50px; }
        .challenge-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--white);
            padding: 15px 25px;
            border-radius: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            border-right: 5px solid var(--mint-green);
            transition: 0.3s;
        }

        .challenge-item.completed {
            opacity: 0.7;
            background: #F8F9F9;
            border-right-color: #BDC3C7;
        }

        .challenge-text { font-size: 1.1rem; }
        .challenge-points { color: #F39C12; font-weight: bold; margin-right: 15px; }
        
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--white);
            padding: 15px 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }

        .progress-bar-container {
            flex-grow: 1;
            margin: 0 20px;
            background: #ECF0F1;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--mint-green), var(--sky-blue));
            width: 0%;
            transition: width 0.5s;
        }

        /* --- Education --- */
        .edu-card {
            background: var(--white);
            padding: 20px;
            border-radius: 20px;
            cursor: pointer;
            border: 2px solid var(--light-blue);
            transition: 0.3s;
        }
        .edu-card:hover { background: var(--light-blue); }
        .edu-answer {
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed #BDC3C7;
            color: #34495E;
            font-size: 0.95rem;
        }
        .edu-card.active .edu-answer { display: block; animation: fadeIn 0.5s; }

        /* --- Map --- */
        .map-section {
            background: var(--white);
            border-radius: 40px;
            padding: 40px;
            margin-bottom: 50px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        }

        .map-container {
            position: relative;
            width: 100%;
            max-width: 400px;
            height: 500px;
            margin: 0 auto;
            background: var(--yellow);
            border-radius: 30px;
            overflow: hidden;
            border: 4px solid var(--light-orange);
        }

        .map-sea {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 120px;
            background: var(--light-blue);
            border-bottom: 5px solid var(--sky-blue);
        }

        .map-nile {
            position: absolute;
            top: 120px;
            left: 50%;
            transform: translateX(-50%);
            width: 20px;
            height: 380px;
            background: var(--sky-blue);
            border-radius: 10px;
        }
        
        .map-nile-delta {
            position: absolute;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            width: 120px;
            height: 100px;
            background: var(--sky-blue);
            clip-path: polygon(50% 100%, 0 0, 100% 0);
        }

        .map-city {
            position: absolute;
            width: 20px;
            height: 20px;
            background: #E74C3C;
            border-radius: 50%;
            border: 3px solid white;
            cursor: pointer;
            transition: 0.3s;
            z-index: 10;
        }
        
        .map-city:hover { transform: scale(1.5); }
        .map-city-label {
            position: absolute;
            background: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: bold;
            pointer-events: none;
            z-index: 10;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            white-space: nowrap;
        }

        /* City Positions */
        #city-alex { top: 100px; left: 20%; } #label-alex { top: 125px; left: 15%; }
        #city-damietta { top: 90px; left: 65%; } #label-damietta { top: 65px; left: 60%; }
        #city-portsaid { top: 95px; left: 80%; } #label-portsaid { top: 70px; left: 75%; }
        #city-mansoura { top: 130px; left: 55%; } #label-mansoura { top: 155px; left: 50%; }
        #city-cairo { top: 190px; left: 48%; } #label-cairo { top: 190px; left: 55%; }
        #city-aswan { top: 430px; left: 48%; } #label-aswan { top: 430px; left: 55%; }

        @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }

        /* Responsive */
        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
            .hero h1 { font-size: 2rem; }
            .top-bar { flex-direction: column; gap: 15px; }
            .city-selector { flex-direction: column; width: 100%; }
        }
    </style>
</head>
<body>

    <!-- Hero Section -->
    <div class="hero">
        <h1>🌍 اكتشف عالم المناخ</h1>
        <p>تعلم عن المناخ، اكتشف ما يحدث حولك، واكتشف كيف يمكن لعاداتك اليومية أن تساعد كوكبنا بطريقة ممتعة!</p>
        <div class="city-selector">
            <select id="citySelect">
                <option value="دمياط">دمياط</option>
                <option value="القاهرة">القاهرة</option>
                <option value="الإسكندرية">الإسكندرية</option>
                <option value="بورسعيد">بورسعيد</option>
                <option value="المنصورة">المنصورة</option>
                <option value="أسوان">أسوان</option>
            </select>
            <button class="btn" onclick="loadCityData()">اكتشف مناخ مدينتي ✨</button>
        </div>
    </div>

    <div class="container">
        
        <!-- Progress Bar -->
        <div class="top-bar">
            <div>🏆 تقدمي: <span id="progressText">0 / 7 أيام</span></div>
            <div class="progress-bar-container">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div>⭐ النقاط: <span id="totalPoints">0</span></div>
        </div>

        <h2 class="section-title" id="dashboardTitle">لوحة المناخ - دمياط</h2>
        
        <div class="grid-2">
            <!-- Score -->
            <div class="score-container">
                <h3>🌱 مؤشر يومك المناخي</h3>
                <div class="score-circle">
                    <div class="score-number" id="scoreValue">--</div>
                </div>
                <div class="score-label" id="scoreLabel">جاري التحميل...</div>
                <p style="margin: 15px 0; color: #7F8C8D;">لماذا حصلنا على هذا المؤشر؟</p>
                <ul class="reasons-list" id="scoreReasons">
                    <!-- Reasons dynamically loaded -->
                </ul>
                <p style="margin-top: 20px; font-size: 0.8rem; color: #95A5A6; text-align: center;">
                    ⚠️ هذا المؤشر تعليمي فقط وليس مؤشرًا علميًا أو طبيًا.
                </p>
            </div>

            <!-- Trend Chart -->
            <div class="chart-card">
                <h3>📈 ماذا لو استمر هذا الاتجاه؟</h3>
                <div class="chart-container" id="trendChart">
                    <!-- Bars dynamically loaded -->
                </div>
                <p id="trendAnalysis" style="margin-top: 15px; font-weight: bold;"></p>
                <div class="chart-note">
                    ⚠️ هذه محاكاة تعليمية لبيانات افتراضية وليست توقعًا أرصاديًا دقيقًا. تهدف لتبسيط فكرة الاتجاه المناخي.
                </div>
            </div>
        </div>

        <!-- Dashboard Cards -->
        <div class="grid-3">
            <div class="card">
                <div class="card-emoji">🌡️</div>
                <div class="card-value" id="valTemp">--°C</div>
                <div class="card-title">درجة الحرارة</div>
            </div>
            <div class="card">
                <div class="card-emoji">💧</div>
                <div class="card-value" id="valHum">--%</div>
                <div class="card-title">الرطوبة</div>
            </div>
            <div class="card">
                <div class="card-emoji">🌬️</div>
                <div class="card-value" id="valWind">-- كم/س</div>
                <div class="card-title">سرعة الرياح</div>
            </div>
            <div class="card">
                <div class="card-emoji">🌧️</div>
                <div class="card-value" id="valRain">--%</div>
                <div class="card-title">احتمال المطر</div>
            </div>
            <div class="card">
                <div class="card-emoji">🌊</div>
                <div class="card-value" style="font-size: 1.5rem;" id="valRisk">--</div>
                <div class="card-title">عامل المخاطر الساحلية</div>
            </div>
            <div class="card">
                <div class="card-emoji">☀️</div>
                <div class="card-value" id="valHeat">--°C</div>
                <div class="card-title">مؤشر الحرارة</div>
            </div>
        </div>

        <!-- Map Section -->
        <div class="map-section">
            <h2 class="section-title">🗺️ خريطة المناخ في مصر</h2>
            <p>اضغط على المدينة للتعرف على مناخها!</p>
            <br>
            <div class="map-container">
                <div class="map-sea"></div>
                <div class="map-nile-delta"></div>
                <div class="map-nile"></div>
                
                <div class="map-city" id="city-alex" onclick="selectMapCity('الإسكندرية')"></div>
                <div class="map-city-label" id="label-alex">الإسكندرية</div>
                
                <div class="map-city" id="city-damietta" onclick="selectMapCity('دمياط')"></div>
                <div class="map-city-label" id="label-damietta">دمياط</div>
                
                <div class="map-city" id="city-portsaid" onclick="selectMapCity('بورسعيد')"></div>
                <div class="map-city-label" id="label-portsaid">بورسعيد</div>
                
                <div class="map-city" id="city-mansoura" onclick="selectMapCity('المنصورة')"></div>
                <div class="map-city-label" id="label-mansoura">المنصورة</div>
                
                <div class="map-city" id="city-cairo" onclick="selectMapCity('القاهرة')"></div>
                <div class="map-city-label" id="label-cairo">القاهرة</div>
                
                <div class="map-city" id="city-aswan" onclick="selectMapCity('أسوان')"></div>
                <div class="map-city-label" id="label-aswan">أسوان</div>
            </div>
        </div>

        <!-- Carbon Footprint -->
        <div class="footprint-section">
            <h2 class="section-title">🌱 بصمتي المناخية</h2>
            <p style="text-align: center; margin-bottom: 20px;">احسب تأثير عاداتك اليومية على البيئة (بصورة تقديرية)</p>
            
            <div class="fp-grid">
                <div class="fp-item">
                    <label>🚗 رحلات بالسيارة (أسبوعياً)</label>
                    <input type="number" id="fpCar" min="0" value="5">
                </div>
                <div class="fp-item">
                    <label>❄️ ساعات التكييف (يومياً)</label>
                    <input type="number" id="fpAc" min="0" value="4">
                </div>
                <div class="fp-item">
                    <label>⚡ أجهزة كهربائية (ساعات/يوم)</label>
                    <input type="number" id="fpElec" min="0" value="6">
                </div>
                <div class="fp-item">
                    <label>🍖 وجبات لحوم (أسبوعياً)</label>
                    <input type="number" id="fpMeat" min="0" value="4">
                </div>
            </div>
            <div style="text-align: center;">
                <button class="btn" onclick="calculateFootprint()">احسب بصمتي 🌍</button>
            </div>
            
            <div id="fpResult" class="fp-result" style="margin-top: 20px;">
                🌿 بصمتك التقديرية: <span id="fpValue">0</span> kg CO₂e
                <p style="font-size: 0.9rem; font-weight: normal; margin-top: 10px; color: #34495E;">
                    هذه قيمة تعليمية مبسطة وليست قياسًا شخصيًا دقيقًا للانبعاثات. حاول تقليلها بممارسة تحدياتنا!
                </p>
            </div>
        </div>

        <!-- Challenges -->
        <div class="challenges-section">
            <h2 class="section-title">🏆 تحدي 7 أيام 🌱</h2>
            <div id="challengesList">
                <!-- Challenges generated by JS -->
            </div>
        </div>

        <!-- Education -->
        <h2 class="section-title">📚 اكتشف وتعلم</h2>
        <div class="grid-3" style="margin-bottom: 80px;">
            <div class="edu-card" onclick="this.classList.toggle('active')">
                <h3>🌡️ ما هو تغير المناخ؟</h3>
                <div class="edu-answer">تغير المناخ يعني أن الطقس المعتاد للأرض يتغير لفترة طويلة. الأرض تسخن تدريجياً بسبب بعض الغازات التي تحبس حرارة الشمس.</div>
            </div>
            <div class="edu-card" onclick="this.classList.toggle('active')">
                <h3>🌳 لماذا الأشجار مهمة؟</h3>
                <div class="edu-answer">الأشجار تتنفس الغازات الضارة (مثل ثاني أكسيد الكربون) وتعطينا الأكسجين النظيف. إنها مثل الرئتين لكوكب الأرض!</div>
            </div>
            <div class="edu-card" onclick="this.classList.toggle('active')">
                <h3>🌊 لماذا نهتم بالمناطق الساحلية؟</h3>
                <div class="edu-answer">عندما تسخن الأرض، يذوب الجليد في القطبين ويرتفع مستوى سطح البحر، مما قد يهدد المدن الساحلية مثل دمياط والإسكندرية بالماء الزائد.</div>
            </div>
            <div class="edu-card" onclick="this.classList.toggle('active')">
                <h3>☁️ طقس أم مناخ؟</h3>
                <div class="edu-answer">الطقس هو حالة الجو اليوم (ممطر، مشمس). أما المناخ فهو حالة الجو لفترة طويلة جداً (سنوات عديدة).</div>
            </div>
        </div>

    </div>

    <!-- JavaScript -->
    <script>
        const challenges = [
            { id: 1, text: "☀️ استخدم الإضاءة الطبيعية لمدة ساعة بدل المصابيح.", points: 10 },
            { id: 2, text: "💡 أوقف تشغيل جهاز كهربائي غير ضروري.", points: 10 },
            { id: 3, text: "🚶 تحرك بطريقة صديقة للبيئة (مشي أو دراجة) إذا كان آمنًا.", points: 15 },
            { id: 4, text: "🌱 اعتنِ بنبات أو قم بري زرع في بيتك.", points: 15 },
            { id: 5, text: "💧 حاول توفير المياه أثناء غسل يديك أو أسنانك.", points: 10 },
            { id: 6, text: "♻️ أعد استخدام شيء قديم بدل التخلص منه.", points: 20 },
            { id: 7, text: "📚 اقرأ معلومة جديدة عن المناخ وشاركها مع عائلتك.", points: 20 }
        ];

        let state = {
            city: "دمياط",
            points: 0,
            completed: []
        };

        // Initialize Application
        function init() {
            // Load local storage
            const savedState = localStorage.getItem('climateAppState');
            if (savedState) {
                state = JSON.parse(savedState);
            }
            
            document.getElementById('citySelect').value = state.city;
            
            renderChallenges();
            updateProgress();
            loadCityData(state.city);
        }

        // Save state
        function saveState() {
            localStorage.setItem('climateAppState', JSON.stringify(state));
            updateProgress();
        }

        // Map Selection
        function selectMapCity(cityName) {
            document.getElementById('citySelect').value = cityName;
            loadCityData(cityName);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Load API Data
        async function loadCityData(cityOverride) {
            const city = cityOverride || document.getElementById('citySelect').value;
            state.city = city;
            saveState();

            document.getElementById('dashboardTitle').innerText = `لوحة المناخ - ${city}`;

            try {
                const response = await fetch(`/api/climate?city=${encodeURIComponent(city)}`);
                const data = await response.json();
                
                // Update Cards
                document.getElementById('valTemp').innerText = data.temperature + "°C";
                document.getElementById('valHum').innerText = data.humidity + "%";
                document.getElementById('valWind').innerText = data.wind + " كم/س";
                document.getElementById('valRain').innerText = data.rain + "%";
                document.getElementById('valRisk').innerText = data.coastal_risk;
                document.getElementById('valHeat').innerText = data.heat_index + "°C";

                // Update Score
                document.getElementById('scoreValue').innerText = data.climate_score;
                document.getElementById('scoreLabel').innerText = data.label;
                
                const reasonsList = document.getElementById('scoreReasons');
                reasonsList.innerHTML = '';
                data.reasons.forEach(r => {
                    const li = document.createElement('li');
                    li.innerText = r;
                    reasonsList.appendChild(li);
                });

                // Update Chart
                drawChart(data.trend);

            } catch (error) {
                console.error("Error fetching climate data:", error);
            }
        }

        // Draw Trend Chart
        function drawChart(trendData) {
            const chart = document.getElementById('trendChart');
            chart.innerHTML = '';
            
            const minTemp = Math.min(...trendData) - 2;
            const maxTemp = Math.max(...trendData) + 2;
            const range = maxTemp - minTemp;
            
            trendData.forEach((temp, index) => {
                const heightPercent = ((temp - minTemp) / range) * 100;
                
                const wrapper = document.createElement('div');
                wrapper.className = 'bar-wrapper';
                
                const bar = document.createElement('div');
                bar.className = 'bar';
                // Trigger animation
                setTimeout(() => { bar.style.height = `${heightPercent}%`; }, 100);
                bar.innerText = temp + "°";
                
                const label = document.createElement('div');
                label.className = 'bar-label';
                label.innerText = `يوم ${index + 1}`;
                
                wrapper.appendChild(bar);
                wrapper.appendChild(label);
                chart.appendChild(wrapper);
            });

            const analysis = document.getElementById('trendAnalysis');
            if (trendData[6] > trendData[0]) {
                analysis.innerText = "📈 ارتفعت درجة الحرارة تدريجيًا خلال البيانات التجريبية الأخيرة. إذا استمر نفس النمط، فقد يستمر الاتجاه الصاعد.";
                analysis.style.color = "#E74C3C";
            } else if (trendData[6] < trendData[0]) {
                analysis.innerText = "📉 انخفضت درجة الحرارة تدريجيًا. الطقس يميل للبرودة.";
                analysis.style.color = "#3498DB";
            } else {
                analysis.innerText = "➡️ درجات الحرارة مستقرة نسبياً في هذه المحاكاة.";
                analysis.style.color = "#2ECC71";
            }
        }

        // Carbon Footprint Calculator
        function calculateFootprint() {
            const car = parseFloat(document.getElementById('fpCar').value) || 0;
            const ac = parseFloat(document.getElementById('fpAc').value) || 0;
            const elec = parseFloat(document.getElementById('fpElec').value) || 0;
            const meat = parseFloat(document.getElementById('fpMeat').value) || 0;
            
            // Formula is purely educational/mock
            const total = (car * 2.5) + (ac * 1.5 * 7) + (elec * 0.5 * 7) + (meat * 3);
            
            const resDiv = document.getElementById('fpResult');
            const resVal = document.getElementById('fpValue');
            
            resVal.innerText = total.toFixed(1);
            resDiv.style.display = 'block';
            resDiv.style.animation = 'fadeIn 0.5s';
        }

        // Challenges Logic
        function renderChallenges() {
            const list = document.getElementById('challengesList');
            list.innerHTML = '';
            
            challenges.forEach(ch => {
                const isDone = state.completed.includes(ch.id);
                const div = document.createElement('div');
                div.className = `challenge-item ${isDone ? 'completed' : ''}`;
                
                let btnHtml = isDone ? 
                    `<button class="btn" style="background:#BDC3C7; cursor:default;">مكتمل ✓</button>` :
                    `<button class="btn" onclick="completeChallenge(${ch.id}, ${ch.points})">أنجزت التحدي ✓</button>`;

                div.innerHTML = `
                    <div>
                        <div class="challenge-text">يوم ${ch.id}: ${ch.text}</div>
                        <span class="challenge-points">⭐ +${ch.points} نقطة</span>
                    </div>
                    <div>${btnHtml}</div>
                `;
                list.appendChild(div);
            });
        }

        function completeChallenge(id, points) {
            if(!state.completed.includes(id)) {
                state.completed.push(id);
                state.points += points;
                saveState();
                renderChallenges();
                alert(`ممتاز! 🌟 اكتسبت ${points} نقطة!`);
            }
        }

        function updateProgress() {
            const count = state.completed.length;
            document.getElementById('progressText').innerText = `${count} / 7 أيام`;
            document.getElementById('totalPoints').innerText = state.points;
            
            const percent = (count / 7) * 100;
            document.getElementById('progressFill').style.width = `${percent}%`;
            
            if(count === 7 && !localStorage.getItem('wonAlready')) {
                setTimeout(() => {
                    alert("أحسنت! 🌱 لقد أكملت جميع التحديات وأصبحت صديقاً حقيقياً للبيئة!");
                    localStorage.setItem('wonAlready', 'true');
                }, 500);
            }
        }

        // Start
        window.onload = init;
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    """تقديم صفحة الويب الرئيسية"""
    return HTML_CONTENT

# ==========================================
# 4. Entry Point - نقطة التشغيل
# ==========================================
if __name__ == "__main__":
    print("🚀 بدء تشغيل تطبيق 'مناخي' التعليمي...")
    print("🌍 افتح المتصفح على الرابط: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)