import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PREMIUM TASARIM & GİZLEME (CSS)
# ---------------------------------------------------------
st.set_page_config(page_title="Turkcell Executive Dashboard", layout="wide", page_icon="📶")

st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    .stApp { background-color: #0E1117 !important; }
    h1, h2, h3, h4 { color: #FFC900 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* KPI KARTLARI */
    div[data-testid="stMetric"] {
        background-color: #1A1C24 !important;
        border: 1px solid #333;
        border-left: 5px solid #FFC900 !important;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    div[data-testid="stMetricLabel"] { color: #A0A0A0 !important; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.8rem; font-weight: bold; }
    
    /* ANALİZ KUTUSU */
    .executive-card {
        background-color: #1E232F;
        border: 1px solid #2855AC;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* FİNANSAL RİSK KARTI */
    .financial-metric {
        color: #ff4d4d;
        font-size: 0.9rem;
        font-weight: bold;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KURUMSAL ZEKA (BUSINESS LOGIC - GÜÇLENDİRİLDİ 💪)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('turkcell_yorumlar_final.csv')
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        return df
    except: return None

@st.cache_resource
def load_model():
    try:
        model = joblib.load('turkcell_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        return model, vectorizer
    except: return None, None

# GELİŞMİŞ KATEGORİ ETİKETLEME (Kelime Dağarcığı Artırıldı)
def kurumsal_kategori(yorum):
    text = str(yorum).lower()
    
    # 1. ALTYAPI
    if any(x in text for x in ['internet', 'çekmiyor', 'yavaş', 'hız', 'donuyor', 'şebeke', '3g', '4.5g', 'çekim', 'kapsama', 'hat yok']):
        return "Altyapı & Bant Genişliği Performansı"
    
    # 2. FİNANS (Fiyat eklendi!)
    if any(x in text for x in ['fatura', 'tl', 'lira', 'pahalı', 'pahalo', 'zam', 'paket', 'ücret', 'tarife', 'fiyat', 'bakiye', 'borç']):
        return "Fiyatlandırma Stratejisi & ARPU"
    
    # 3. DİJİTAL SERVİSLER
    if any(x in text for x in ['salla kazan', 'uygulama', 'giriş', 'şifre', 'bip', 'paycell', 'tv+', 'gnç', 'hesabım']):
        return "Dijital Servisler & Kullanıcı Deneyimi (UX)"
    
    # 4. OPERASYON
    if any(x in text for x in ['müşteri hizmetleri', 'temsilci', 'ulaşamıyorum', 'cevap', 'bekletme', 'bağlan', 'robot']):
        return "Müşteri Hizmetleri Operasyonel Verimlilik"
        
    return "Diğer Operasyonel Geri Bildirimler"

# CHURN RİSKİ
def churn_analizi(yorum):
    text = str(yorum).lower()
    risk_keywords = ['iptal', 'kapat', 'vodafone', 'telekom', 'bimcell', 'geçiş', 'taahhüt', 'bırakıyorum', 'yeter', 'hat taşıma', 'başka operatör']
    return any(x in text for x in risk_keywords)

# 🔥 HİBRİT DUYGU ANALİZİ (YAPAY ZEKA + KURAL BAZLI KORUMA)
def hibrit_analiz(text, model_prediction):
    text = text.lower()
    # Eğer bu kelimeler varsa, model ne derse desin sonuç OLUMSUZ'dur.
    hard_negatives = [
        'pahalı', 'pahalo', 'pahali', 'yüksek', 'zam', 'kötü', 'berbat', 'iğrenç', 'rezalet', 
        'çekmiyor', 'yavaş', 'donuyor', 'hata', 'sorun', 'lanet', 'haram', 'yazık', 'pişman',
        'değilim', 'vermem', 'tavsiye etmem', 'yok', 'olmadı', 'açılmıyor', 'bıktım'
    ]
    
    # Model "Olumlu" (1) dediyse bile, içinde kötü kelime var mı diye bak
    if model_prediction == 1:
        for word in hard_negatives:
            if word in text:
                return 0 # Zorla Olumsuz Yap (Override)
    
    return model_prediction

# ---------------------------------------------------------
# 3. ANA EKRAN & FİLTRELER
# ---------------------------------------------------------
df = load_data()
model, vectorizer = load_model()

if df is None: st.stop()

# Kategorileri hesapla
df['Business_Category'] = df['Yorum'].apply(kurumsal_kategori)
df['Is_Churn_Risk'] = df['Yorum'].apply(churn_analizi)

# HEADER
c1, c2 = st.columns([1, 6])
with c1:
    try: st.image("turkcell logo2-Photoroom.png", width=140)
    except: st.warning("Logo?")
with c2:
    st.markdown("# TURKCELL | Uygulama İçi Müşteri Geri Bildirim Dashboard")
    st.markdown("<span style='color:#bbb'>Q1 2026 - Stratejik Müşteri İçgörü Raporu</span>", unsafe_allow_html=True)

st.divider()

# TARİH FİLTRESİ
min_date, max_date = df['Tarih'].min(), df['Tarih'].max()
dr = st.sidebar.date_input("Raporlama Dönemi:", value=(min_date, max_date), min_value=min_date, max_value=max_date, format="DD.MM.YYYY")

if len(dr) == 2:
    start, end = pd.to_datetime(dr[0]), pd.to_datetime(dr[1])
    filtered_df = df[(df['Tarih'] >= start) & (df['Tarih'] <= end)].copy()
else:
    filtered_df = df.copy()

# ---------------------------------------------------------
# 4. KPI KARTLARI
# ---------------------------------------------------------
total = len(filtered_df)
riskli_musteri = len(filtered_df[filtered_df['Is_Churn_Risk'] == True])
memnuniyet_orani = (len(filtered_df[filtered_df['Durum']==1]) / total * 100) if total > 0 else 0
finansal_risk = riskli_musteri * 350 # ARPU

k1, k2, k3, k4 = st.columns(4)
k1.metric("Toplam Veri Hacmi", f"{total:,}")
k2.metric("Müşteri Memnuniyet Endeksi (CSAT)", f"%{memnuniyet_orani:.1f}")
k3.metric("Kritik Şikayet Hacmi", len(filtered_df[filtered_df['Durum']==0]), delta_color="inverse")

with k4:
    st.metric("🚨 Yüksek Churn (Kayıp) Riski", f"{riskli_musteri} Kişi", "Acil Aksiyon", delta_color="inverse")
    st.markdown(f"<div class='financial-metric'>📉 Tahmini Kayıp: ₺{finansal_risk:,.0f}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. STRATEJİK ANALİZ (BAR GRAFİĞİ)
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
c_main, c_risk = st.columns([2, 1])

with c_main:
    st.subheader("📊 Stratejik Alan Bazlı Sorun Dağılımı")
    sikayet_df = filtered_df[filtered_df['Durum'] == 0]
    if not sikayet_df.empty:
        cat_counts = sikayet_df['Business_Category'].value_counts().reset_index()
        cat_counts.columns = ['Stratejik Alan', 'Hacim']
        fig = px.bar(cat_counts, x='Hacim', y='Stratejik Alan', orientation='h', text='Hacim', 
                     color='Hacim', color_continuous_scale=['#00205B', '#2855AC', '#FFC900'], template="plotly_dark")
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veri yok.")

with c_risk:
    st.subheader("⚠️ Yönetim Özeti")
    top_issue = cat_counts.iloc[0]['Stratejik Alan'] if not sikayet_df.empty else "Veri Yok"
    top_count = cat_counts.iloc[0]['Hacim'] if not sikayet_df.empty else 0
    st.markdown(f"""
    <div class="executive-card">
        <div style="color:#FFC900; font-weight:bold; border-bottom:1px solid #444; margin-bottom:10px;">📌 Kritik Bulgular</div>
        <div style="color:#E0E0E0;">
        • <b>Ana Darboğaz:</b> "{top_issue}" ({top_count} şikayet).<br><br>
        • <b>Finansal Etki:</b> Aylık <b>₺{finansal_risk:,.0f}</b> ciro riski.<br><br>
        • <b>Strateji:</b> Operasyonel verimlilik için Q2 bütçesi revize edilmelidir.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. DETAY GRAFİKLER
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
c_pie, c_trend = st.columns([1, 2])

with c_pie:
    st.subheader("☯️ Duygu Durum Dağılımı")
    durum_counts = filtered_df['Durum'].value_counts().reset_index()
    durum_counts.columns = ['Durum', 'Adet']
    durum_counts['Etiket'] = durum_counts['Durum'].map({1: 'Olumlu (Memnuniyet)', 0: 'Olumsuz (Şikayet)'})
    fig_pie = px.pie(durum_counts, values='Adet', names='Etiket', color='Etiket',
                     color_discrete_map={'Olumlu (Memnuniyet)': '#0057B7', 'Olumsuz (Şikayet)': '#FFC900'},
                     hole=0.4, template="plotly_dark")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with c_trend:
    st.subheader("📈 Operasyonel Performans Trendi")
    daily_vol = filtered_df.resample('D', on='Tarih')['Durum'].count()
    daily_sat = filtered_df.resample('D', on='Tarih')['Durum'].mean() * 100
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=daily_vol.index, y=daily_vol.values, name='Hacim', marker_color='#2855AC', opacity=0.6))
    fig_trend.add_trace(go.Scatter(x=daily_sat.index, y=daily_sat.values, name='Memnuniyet (%)', yaxis='y2', line=dict(color='#FFC900', width=3)))
    fig_trend.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            yaxis=dict(title='Hacim', showgrid=False),
                            yaxis2=dict(title='CSAT (%)', overlaying='y', side='right', range=[0, 110], showgrid=True, gridcolor='#333'),
                            legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------
# 7. CANLI SİMÜLASYON (HATASIZ KUL OLMAZ MODU 🤖)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🤖 Gerçek Zamanlı Simülasyon")

col_input, col_result = st.columns([1, 1])

with col_input:
    user_input = st.text_area("Müşteri Geri Bildirimi:", placeholder="Örn: Fiyatı çok pahalo...", height=100)
    analyze_btn = st.button("Analiz Et", type="primary")

with col_result:
    if analyze_btn and user_input:
        # 1. MODEL TAHMİNİ
        vector_input = vectorizer.transform([user_input.lower()])
        raw_prediction = model.predict(vector_input)[0]
        
        # 2. HİBRİT KONTROL (KURAL BAZLI DÜZELTME)
        final_prediction = hibrit_analiz(user_input, raw_prediction)
        
        # 3. KATEGORİ
        category = kurumsal_kategori(user_input)
        
        st.markdown("### 🔍 Analiz Sonucu")
        
        if final_prediction == 1:
            st.success("✅ **Duygu Durumu:** OLUMLU (Memnuniyet)")
        else:
            st.error("😡 **Duygu Durumu:** OLUMSUZ (Şikayet)")
            # Eğer AI pozitif demiş ama biz zorla negatif yaptıysak kullanıcıya çaktırmadan bilgi verebiliriz (Opsiyonel)
            
        st.info(f"📂 **Stratejik Kategori:** {category}")