import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(
    page_title="オールインワン旅行アプリ",
    page_icon="✈️",
    layout="wide"
)

# --- スタイル調整 ---
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.2rem; color: #4B5563; }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<p class="main-header">✈️ オールインワン旅行総合アプリ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">プランニング、ガチャによるひらめき、そしてコスパ分析をこれ一つで。</p>', unsafe_allow_html=True)
st.markdown("---")

# メインのナビゲーション（タブ構成）
tab1, tab2, tab3 = st.tabs(["🤖 AI 旅程プランナー", "🎰 旅先ガチャ＆お出かけ", "📊 観光地・コスパ分析"])

# ==========================================
# Tab 1: AI 旅程プランナー
# ==========================================
with tab1:
    st.subheader("🤖 AI 自動しおり＆ルートプランナー")
    st.write("行き先や好みの条件を入力すると、あなただけのオリジナル旅行プランを自動生成します。")

    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("行きたいエリア・都市", "金沢・能登")
        days = st.number_input("日数", min_value=1, max_value=7, value=2)
    with col2:
        budget_level = st.selectbox("予算感", ["エコノミー（〜3万円）", "スタンダード（3万〜7万円）", "ラグジュアリー（7万円〜）"])
        theme = st.multiselect("旅のテーマ・目的", ["グルメ", "温泉・リラックス", "歴史・文化", "絶景・自然", "ショッピング"], default=["グルメ", "温泉・リラックス"])

    if st.button("✨ 旅程プランを生成する", type="primary"):
        with st.spinner("AIが最適なスケジュールとルートを計算中..."):
            # 擬似的な生成ディレイ
            import time
            time.sleep(1.5)
            
            st.success("🎉 旅行プランが完成しました！")
            
            for d in range(1, days + 1):
                with st.expander(f"📅 第 {d} 日目：{destination} 満喫コース", expanded=(d==1)):
                    st.markdown(f"""
                    * **09:00** — 現地到着 ＆ ホテルに荷物を預ける
                    * **10:30** — 【観光】**{destination}の主要シンボル・歴史地区を散策**
                    * **12:30** — 【ランチ】地元で評判の海鮮・名物料理店で舌鼓
                    * **15:00** — 【体験】テーマ「{', '.join(theme)}」に合わせたアクティビティ
                    * **18:30** — 【ディナー】隠れ家風の郷土料理居酒屋で一杯
                    * **20:30** — 温泉宿・ホテルにチェックイン、リラックスタイム
                    """)

# ==========================================
# Tab 2: 旅先ガチャ
# ==========================================
with tab2:
    st.subheader("🎰 ランダム旅先ガチャ")
    st.write("「どこに行こうか迷う…」そんな時はガチャを回して運命の旅先を決めましょう！")

    # サンプルデータベース
    gacha_spots = [
        {"spot": "北海道・函館", "theme": "グルメ・夜景", "cost": "約45,000円", "weather": "晴れ 18°C", "desc": "絶品の海鮮朝市と函館山の夜景を満喫する旅"},
        {"spot": "長野・松本＆上高地", "theme": "絶景・自然", "cost": "約25,000円", "weather": "曇り空 14°C", "desc": "国宝松本城と神降地と呼ばれる美しき大自然"},
        {"spot": "石川・金沢", "theme": "歴史・文化", "cost": "約35,000円", "weather": "小雨 16°C", "desc": "兼六園の趣ある景色と近江町市場の食べ歩き"},
        {"spot": "沖縄・石垣島", "theme": "リゾート・海", "cost": "約60,000円", "weather": "快晴 27°C", "desc": "日本屈指の透明度を誇る海と島グルメの楽園"},
        {"spot": "福岡・博多", "theme": "グルメ・屋台", "cost": "約30,000円", "weather": "晴れ 21°C", "desc": "豚骨ラーメン、もつ鍋、中洲屋台のはしご酒"}
    ]

    gacha_theme = st.selectbox("ガチャのフィルター（テーマ）", ["すべて", "グルメ・夜景", "絶景・自然", "歴史・文化", "リゾート・海", "グルメ・屋台"])

    if st.button("🎲 運命の旅先をガチャる！", type="primary"):
        filtered_spots = gacha_spots if gacha_theme == "all" or gacha_theme == "すべて" else [s for s in gacha_spots if s["theme"] == gacha_theme]
        if not filtered_spots:
            filtered_spots = gacha_spots
            
        selected = random.choice(filtered_spots)
        
        st.balloons()
        st.markdown(f"""
        ### 🎯 当たった旅先： **{selected['spot']}**
        * **テーマ:** {selected['theme']}
        * **目安予算:** {selected['cost']}
        * **現地の天気:** 🌤️ {selected['weather']}
        * **魅力:** {selected['desc']}
        """)

# ==========================================
# Tab 3: 観光地・コスパ分析ダッシュボード
# ==========================================
with tab3:
    st.subheader("📊 観光地・宿泊施設のコスパ分析ダッシュボード")
    st.write("エリア内のホテルや観光スポットを「評価（満足度）」と「価格」でマッピングし、コスパの良い穴場を発見します。")

    # サンプルデータの作成
    np.random.seed(42)
    n_items = 30
    df_spots = pd.DataFrame({
        "SpotName": [f"スポット・ホテル {i+1}" for i in range(n_items)],
        "Category": np.random.choice(["ホテル・旅館", "温泉施設", "観光スポット", "飲食店"], n_items),
        "Price (JPY)": np.random.randint(3000, 35000, n_items),
        "Rating (1-5)": np.round(np.random.uniform(3.2, 4.9, n_items), 1),
        "ReviewCount": np.random.randint(20, 800, n_items)
    })

    # フィルター
    f_cat = st.selectbox("カテゴリ絞り込み", ["すべて"] + list(df_spots["Category"].unique()))
    if f_cat != "すべて":
        df_display = df_spots[df_spots["Category"] == f_cat]
    else:
        df_display = df_spots

    # 散布図の表示
    st.markdown("##### 💡 評価 vs 価格 分布図（右上にいくほど高評価・高価格）")
    st.scatter_chart(df_display, x="Price (JPY)", y="Rating (1-5)", color="Category", size="ReviewCount")

    st.markdown("##### 📋 該当スポット一覧データ")
    st.dataframe(df_display.sort_values(by="Rating (1-5)", ascending=False), use_container_width=True)
