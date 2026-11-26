import random
import re
from datetime import date, datetime
import streamlit as st

st.set_page_config(
    page_title="世界の文化遺産検定 4択マスター",
    page_icon="🏛️",
    layout="centered",
)

# --- CSSスタイル定義 ---
st.markdown("""
<style>
    .trivia-box {
        background-color: #f0f7ff;
        border-left: 5px solid #0d6efd;
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        color: #111827;
    }
    .correct-box {
        background-color: #d1e7dd;
        border-left: 5px solid #198754;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #0f5132;
    }
    .incorrect-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #842029;
    }
    .explanation-box {
        background-color: #e7f1ff;
        border-left: 5px solid #084298;
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        color: #052c65;
    }
    .pass-banner {
        background-color: #d1e7dd;
        border: 2px solid #198754;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        color: #0f5132;
        margin-bottom: 16px;
    }
    .fail-banner {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        color: #664d03;
        margin-bottom: 16px;
    }
    /* 選択肢ボタンの箱を大きくし、長文でも折り返して収まるように調整 */
    div.stButton > button {
        min-height: 64px;
        height: auto !important;
        padding: 14px 18px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.5 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
    div.stButton > button p {
        font-size: 1.05rem !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ここに問題を追加してください
QUIZ_DATA = [
  {
    "question": "世界遺産『カスビのブガンダ王国の王墓』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① ガンダ族 ／ ムジブ・アザーラ・ムバンガ",
      "② ドゴン族 ／ トグナ",
      "③ ショナ族 ／ アクロポリス",
      "④ 納西族 ／ 東巴文字"
    ],
    "answer": "① ガンダ族 ／ ムジブ・アザーラ・ムバンガ",
    "explanation": "正解は①です。『カスビのブガンダ王国の王墓』（ウガンダ共和国）は農耕民族のガンダ族を主体とする王国の歴代王の墓所で、4つの王墓があるドーム型の「ムジブ・アザーラ・ムバンガ」が傑作とされています。②は『バンディアガラの断崖』、③は『大ジンバブエ遺跡』、④は『麗江の旧市街』の語句です。",
    "tag": "ウガンダ共和国 / 登録年: 2001年 / 基準(i)(iii)(iv)(vi) / カスビのブガンダ王国の王墓",
    "trivia": "ムジブ・アザーラ・ムバンガは木材やわら、葦、土壁を用いた自然素材建築で、2010年に火災で焼失し危機遺産リストに記載されましたが、2023年に修復が完了し除外されました。"
  },
  {
    "question": "世界遺産『バンディアガラの断崖』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① ドゴン族 ／ アンマ",
      "② ガンダ族 ／ ムジブ・アザーラ・ムバンガ",
      "③ 長耳族 ／ 凝灰岩",
      "④ トルコ系クマン人 ／ パローツ様式"
    ],
    "answer": "① ドゴン族 ／ アンマ",
    "explanation": "正解は①です。『バンディアガラの断崖』（マリ共和国）は、西アフリカの奴隷狩りやイスラム化から逃れたドゴン族が移り住んだ地域で、「アンマ」という神を信仰する神話に由来して家屋が配置されています。②は『カスビのブガンダ王国の王墓』、③は『ラパ・ニュイ国立公園』、④は『ホローケーの伝統的集落』の語句です。",
    "tag": "マリ共和国 / 登録年: 1989年 / 基準(v)(vii) / バンディアガラの断崖",
    "trivia": "集落の北端には「トグナ」と呼ばれる集会所があり、断崖には円錐形の屋根をもつ穀物倉庫が立ち並んでいます。"
  },
  {
    "question": "世界遺産『マサダ国立公園』に関連する語句として、正しいものはどれか。",
    "options": [
      "① ユダヤ人の結束のシンボル",
      "② 国民統合の象徴",
      "③ 生命発祥の地",
      "④ 遊牧民の伝統"
    ],
    "answer": "① ユダヤ人の結束のシンボル",
    "explanation": "正解は①です。『マサダ国立公園』（イスラエル国）は、ローマ軍に抵抗し集団自決を遂げた悲劇のために「ユダヤ人の結束のシンボル」となっています。②は『シングヴェトリル国立公園』、③は『パパハナウモクアケア』、④は『オルホン渓谷の文化的景観』に関連する語句です。",
    "tag": "イスラエル国 / 登録年: 2001年 / 基準(iii)(iv)(vi) / マサダ国立公園",
    "trivia": "「マサダ」とはヘブライ語で「要塞」を意味し、紀元前1世紀にユダヤ王国のヘロデ王が築いた冬の離宮兼要塞の跡が残ります。"
  },
  {
    "question": "世界遺産『大ジンバブエ遺跡』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① ショナ族 ／ アクロポリス",
      "② ドゴン族 ／ トグナ",
      "③ ガンダ族 ／ ブガンダ王国",
      "④ 納西族 ／ 雲南省"
    ],
    "answer": "① ショナ族 ／ アクロポリス",
    "explanation": "正解は①です。『大ジンバブエ遺跡』（ジンバブエ共和国）はショナ族が11〜15世紀に築いた都市遺跡で、「アクロポリス」と「神殿」、「谷の遺跡」からなります。②は『バンディアガラの断崖』、③は『カスビのブガンダ王国の王墓』、④は『麗江の旧市街』の語句です。",
    "tag": "ジンバブエ共和国 / 登録年: 1986年 / 基準(i)(iii)(vi) / 大ジンバブエ遺跡",
    "trivia": "丘の上の「アクロポリス」は王の都市であったと考えられており、石壁で楕円形に囲まれた「神殿」は祭祀の空間と生活の空間に分けられていました。"
  },
  {
    "question": "世界遺産『パパハナウモクアケア』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① ニホア ／ マクマナマナ",
      "② ギャオ ／ ゲイシール",
      "③ アルシンの遺構 ／ レイキャヴィーク",
      "④ サウデルール朝 ／ ポンペイ島"
    ],
    "answer": "① ニホア ／ マクマナマナ",
    "explanation": "正解は①です。『パパハナウモクアケア』（アメリカ合衆国）は北西ハワイ諸島の島々と環礁の集合体で、「ニホア」と「マクマナマナ」という2つの島に考古学的に重要な西欧化以前の定住跡が残ります。②・③は『シングヴェトリル国立公園』、④は『ナン・マトール』の語句です。",
    "tag": "アメリカ合衆国 / 登録年: 2010年 / 基準(iii)(vi)(viii)(ix)(x) / パパハナウモクアケア",
    "trivia": "ハワイの先住民は、代々受け継いできたこの一帯を、生命発祥の地かつ死後には魂が帰る故郷と考えていました。"
  },
  {
    "question": "世界遺産『ティムリカ・オヒンガの考古遺跡』に関連する説明として、正しいものはどれか。",
    "options": [
      "① 集落の住民や家畜を守る砦の役割を果たす石垣に囲まれた集落跡",
      "② 海に浮かぶ100以上の人工島からなる石造りの儀礼の中心地",
      "③ 凝灰岩を削ってつくられたモアイ像約900体が残る孤島",
      "④ 泥とわらを混ぜた壁に石灰を塗った木造家屋が並ぶ集落"
    ],
    "answer": "① 集落の住民や家畜を守る砦の役割を果たす石垣に囲まれた集落跡",
    "explanation": "正解は①です。『ティムリカ・オヒンガの考古遺跡』（ケニア共和国）の「オヒンガ」は集落を意味し、集落の住民や家畜を守る砦の役割を果たすと同時に種族間の社会的なつながりを明らかにするものです。②は『ナン・マトール』、③は『ラパ・ニュイ国立公園』、④は『ホローケーの伝統的集落』の説明です。",
    "tag": "ケニア共和国 / 登録年: 2018年 / 基準(iii)(iv)(v) / ティムリカ・オヒンガの考古遺跡",
    "trivia": "ケニア西部のヴィクトリア湖に近い都市ミゴリの北西にあり、16世紀に築かれたと考えられています。"
  },
  {
    "question": "世界遺産『ナン・マトール：ミクロネシア東部の儀礼的中心地』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① サウデルール朝 ／ ポンペイ島",
      "② 長耳族 ／ 短耳族",
      "③ 首長ロイ・マタ ／ フェルス洞窟",
      "④ 突厥 ／ カラコルム"
    ],
    "answer": "① サウデルール朝 ／ ポンペイ島",
    "explanation": "正解は①です。『ナン・マトール』（ミクロネシア連邦）はポンペイ島南東岸に浮かぶ100以上の人工島からなり、サウデルール朝の儀礼の中心地として築かれました。②は『ラパ・ニュイ国立公園』、③は『首長ロイ・マタの旧所領』、④は『オルホン渓谷の文化的景観』の語句です。",
    "tag": "ミクロネシア連邦 / 登録年: 2016年・2016年危機遺産登録 / 基準(i)(iii)(iv)(vi) / ナン・マトール",
    "trivia": "マングローブの繁茂や構築物の損傷度合いの大きさなどから、世界遺産登録と同時に危機遺産リストにも記載されました。"
  },
  {
    "question": "世界遺産『ラパ・ニュイ国立公園』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① 長耳族 ／ 凝灰岩",
      "② サウデルール朝 ／ 人工島",
      "③ 首長ロイ・マタ ／ アルトク島",
      "④ ドゴン族 ／ アンマ"
    ],
    "answer": "① 長耳族 ／ 凝灰岩",
    "explanation": "正解は①です。『ラパ・ニュイ国立公園』（チリ共和国）では、凝灰岩を削ってつくられたモアイ像約900体が残り、ポリネシアに起源をもつ長耳族によって制作が始まったとされます。②は『ナン・マトール』、③は『首長ロイ・マタの旧所領』、④は『バンディアガラの断崖』の語句です。",
    "tag": "チリ共和国 / 登録年: 1995年 / 基準(i)(iii)(v) / ラパ・ニュイ国立公園",
    "trivia": "11世紀頃までのモアイはおおむね5〜7mの高さでしたが、南米から短耳族が移住してくると10mを超えるモアイがつくられるようになりました。"
  },
  {
    "question": "世界遺産『首長ロイ・マタの旧所領』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① 首長ロイ・マタ ／ バヌアツ共和国",
      "② サウデルール朝 ／ ミクロネシア連邦",
      "③ 長耳族 ／ チリ共和国",
      "④ ショナ族 ／ ジンバブエ共和国"
    ],
    "answer": "① 首長ロイ・マタ ／ バヌアツ共和国",
    "explanation": "正解は①です。『首長ロイ・マタの旧所領』（バヌアツ共和国）は、17世紀初頭の伝説的な首長ロイ・マタゆかりの史跡群（住居跡、フェルス洞窟、アルトク島など）とその伝説に結びついた景観です。②は『ナン・マトール』、③は『ラパ・ニュイ国立公園』、④は『大ジンバブエ遺跡』です。",
    "tag": "バヌアツ共和国 / 登録年: 2008年 / 基準(iii)(v)(vi) / 首長ロイ・マタの旧所領",
    "trivia": "ロイ・マタは諸部族を平和的に統一し社会変革を実行したとされ、今もバヌアツの人々の精神的な支柱です。"
  },
  {
    "question": "世界遺産『シングヴェトリル国立公園』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① アルシング（全島集会） ／ ギャオ ／ ゲイシール",
      "② トリ・ヒタ・カラナ ／ スバック ／ 棚田",
      "③ オルホン碑文 ／ カラコルム ／ 突厥",
      "④ 東巴文字 ／ 納西族 ／ 瓦屋根"
    ],
    "answer": "① アルシング（全島集会） ／ ギャオ ／ ゲイシール",
    "explanation": "正解は①です。『シングヴェトリル国立公園』（アイスランド共和国）には、「世界最古の議会」とされるアルシング（全島集会）の遺構や、大陸プレートの裂け目「ギャオ」、間欠泉「ゲイシール」が見られます。②は『バリの文化的景観』、③は『オルホン渓谷の文化的景観』、④は『麗江の旧市街』の語句です。",
    "tag": "アイスランド共和国 / 登録年: 2004年 / 基準(iii)(vi) / シングヴェトリル国立公園",
    "trivia": "ゲイシールはアイスランド語で間欠泉のことを指し、英語で間欠泉を意味する「ガイザー」の語源ともなりました。"
  },
  {
    "question": "世界遺産『麗江の旧市街』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① 納西族 ／ 東巴文字",
      "② トルコ系クマン人 ／ パローツ様式",
      "③ 突厥 ／ オルホン碑文",
      "④ ガンダ族 ／ ムジブ・アザーラ・ムバンガ"
    ],
    "answer": "① 納西族 ／ 東巴文字",
    "explanation": "正解は①です。『麗江の旧市街』（中華人民共和国）は、12世紀の宋代末に中国の少数民族である納西族によって築かれた都市で、現在も儀礼などで使われる象形文字「東巴文字」に代表される独自の文化を育みました。②は『ホローケーの伝統的集落』、③は『オルホン渓谷の文化的景観』、④は『カスビのブガンダ王国の王墓』の語句です。",
    "tag": "中華人民共和国 / 登録年: 1997年・2012年範囲変更 / 基準(ii)(iv)(v) / 麗江の旧市街",
    "trivia": "縦横に張り巡らされた水路や、街路沿いに2階建ての木造建築が隙間なく立ち並び瓦屋根が続く景観が特徴です。"
  },
  {
    "question": "世界遺産『ホローケーの伝統的集落』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① パローツ様式 ／ トルコ系クマン人",
      "② 納西族 ／ 東巴文字",
      "③ スバック ／ トリ・ヒタ・カラナ",
      "④ アルシング ／ 法律の岩"
    ],
    "answer": "① パローツ様式 ／ トルコ系クマン人",
    "explanation": "正解は①です。『ホローケーの伝統的集落』（ハンガリー）には、「パローツ様式」と呼ばれる独特の木造家屋が軒を連ねており、パローツとは中世にカスピ海沿岸から移住してきたトルコ系クマン人と関係があるともいわれます。②は『麗江の旧市街』、③は『バリの文化的景観』、④は『シングヴェトリル国立公園』の語句です。",
    "tag": "ハンガリー / 登録年: 1987年 / 基準(v) / ホローケーの伝統的集落",
    "trivia": "泥とわらを混ぜた壁に石灰を塗って仕上げられた木造家屋で、火災による焼失のたびに伝統的な景観のまま再建されてきました。"
  },
  {
    "question": "世界遺産『バリの文化的景観：バリ・ヒンドゥー哲学トリ・ヒタ・カラナを表す水利システム「スバック」』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① トリ・ヒタ・カラナ ／ スバック ／ タマン・アユン",
      "② オルホン碑文 ／ カラ・バルガスン遺跡 ／ カラコルム",
      "③ ギャオ ／ ゲイシール ／ グトルフォスの滝",
      "④ ニホア ／ マクマナマナ ／ 北西ハワイ諸島"
    ],
    "answer": "① トリ・ヒタ・カラナ ／ スバック ／ タマン・アユン",
    "explanation": "正解は①です。『バリの文化的景観』（インドネシア共和国）は、神と人、自然の調和をもたらす宇宙観「トリ・ヒタ・カラナ」に基づく5つの棚田や水利システム「スバック」を司る寺院（王立寺院タマン・アユンなど）が登録されています。②は『オルホン渓谷』、③は『シングヴェトリル国立公園』、④は『パパハナウモクアケア』の語句です。",
    "tag": "インドネシア共和国 / 登録年: 2012年 / 基準(iii)(v)(vi) / バリの文化的景観",
    "trivia": "「スバック」とは寺院に集められた水を分け合う水利システムで、9世紀頃から継承されてきました。"
  },
  {
    "question": "世界遺産『オルホン渓谷の文化的景観』に関連する語句として、正しい組み合わせはどれか。",
    "options": [
      "① 突厥 ／ カラコルム ／ オルホン碑文",
      "② 納西族 ／ 雲南省 ／ 東巴文字",
      "③ ドゴン族 ／ ニジェール川流域 ／ トグナ",
      "④ ショナ族 ／ 谷の遺跡 ／ 神殿"
    ],
    "answer": "① 突厥 ／ カラコルム ／ オルホン碑文",
    "explanation": "正解は①です。『オルホン渓谷の文化的景観』（モンゴル国）には、トルコ系民族とされる突厥の遺跡やモンゴル帝国の首都カラコルムなどの考古遺跡が点在し、ホショー・ツァイダム遺跡から「オルホン碑文」が発見されました。②は『麗江の旧市街』、③は『バンディアガラの断崖』、④は『大ジンバブエ遺跡』の語句です。",
    "tag": "モンゴル国 / 登録年: 2004年 / 基準(ii)(iii)(iv) / オルホン渓谷の文化的景観",
    "trivia": "オルホン碑文は古代テュルク語で歴史上の出来事や宗教的・呪術的な記述が彫られた碑文で、東アジアでは漢字を除いて日本の「かな」と並ぶ古い歴史をもちます。"
  }
]

# --- ヘルパー関数：選択肢のシャッフル ---
def prepare_quiz_session(questions_list):
    prepared = []
    for q in questions_list:
        q_copy = q.copy()
        clean_options = [re.sub(r'^[①②③④]\s*', '', opt) for opt in q_copy["options"]]
        clean_answer = re.sub(r'^[①②③④]\s*', '', q_copy["answer"])

        random.shuffle(clean_options)

        prefixes = ["①", "②", "③", "④"]
        new_options = []
        new_answer = ""
        for idx, text in enumerate(clean_options):
            labeled_opt = f"{prefixes[idx]} {text}"
            new_options.append(labeled_opt)
            if text == clean_answer:
                new_answer = labeled_opt

        q_copy["options"] = new_options
        q_copy["answer"] = new_answer
        prepared.append(q_copy)
    return prepared


def start_quiz(questions, mode_label, is_mock_exam=False):
    quiz_list = questions.copy()
    random.shuffle(quiz_list)
    st.session_state.shuffled_quiz = prepare_quiz_session(quiz_list)
    st.session_state.app_mode = "quiz"
    st.session_state.mode_label = mode_label
    st.session_state.is_mock_exam = is_mock_exam
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.wrong_questions = []
    st.session_state.quiz_results_log = []
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.history_recorded = False


# --- セッション状態の初期化 ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "home"
if "shuffled_quiz" not in st.session_state:
    st.session_state.shuffled_quiz = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []
if "history" not in st.session_state:
    st.session_state.history = []
if "mode_label" not in st.session_state:
    st.session_state.mode_label = ""
if "is_mock_exam" not in st.session_state:
    st.session_state.is_mock_exam = False
if "quiz_results_log" not in st.session_state:
    st.session_state.quiz_results_log = []
if "forgetting_curve_log" not in st.session_state:
    st.session_state.forgetting_curve_log = {}
if "study_dates" not in st.session_state:
    st.session_state.study_dates = {str(date.today())}

# タイトル
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 世界の文化遺産検定 4択マスター</h2>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 1. ホーム画面
# ==========================================
if st.session_state.app_mode == "home":
    if "daily_trivia" not in st.session_state:
        st.session_state.daily_trivia = random.choice(QUIZ_DATA)

    dt = st.session_state.daily_trivia
    st.markdown(f"""
        <div class="trivia-box">
            <b>💡 本日の世界遺産トリビア</b><br>
            {dt['trivia']}
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 学習メニューを選択")

    if st.button(f"🎓 本番模擬試験をスタート（全{len(QUIZ_DATA)}問）", type="primary", use_container_width=True):
        start_quiz(QUIZ_DATA, "🎓 本番模擬試験モード（合格ライン70%）", is_mock_exam=True)
        st.rerun()

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        wrong_count = len(st.session_state.wrong_questions)
        if st.button(f"❌ 間違い復習 ({wrong_count}問)", disabled=(wrong_count == 0), use_container_width=True):
            start_quiz(st.session_state.wrong_questions, "🔄 間違い復習モード", is_mock_exam=False)
            st.rerun()

    with col2:
        fc_due_list = [q for q in QUIZ_DATA if q["question"] in st.session_state.forgetting_curve_log]
        if st.button(f"🧠 忘却曲線復習 ({len(fc_due_list)}問)", disabled=(len(fc_due_list) == 0), use_container_width=True):
            start_quiz(fc_due_list, "🧠 忘却曲線・最適復習モード", is_mock_exam=False)
            st.rerun()

# ==========================================
# 2. クイズ・模擬試験プレイ画面
# ==========================================
elif st.session_state.app_mode == "quiz":
    active_quiz = st.session_state.shuffled_quiz
    st.caption(f"【{st.session_state.mode_label}】")

    if st.session_state.current_q < len(active_quiz):
        q = active_quiz[st.session_state.current_q]

        st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
        st.markdown(f"**{q['question']}**")
        st.write("")

        for i, option in enumerate(q["options"]):
            if st.button(option, key=f"opt_{i}_{st.session_state.current_q}", use_container_width=True, disabled=st.session_state.answered):
                st.session_state.answered = True
                st.session_state.selected_option = option

                is_correct = (option[:1] == q["answer"][:1])
                if is_correct:
                    st.session_state.score += 1
                    if q["question"] in st.session_state.forgetting_curve_log:
                        del st.session_state.forgetting_curve_log[q["question"]]
                else:
                    orig_q = next((item for item in QUIZ_DATA if item["question"] == q["question"]), q)
                    if orig_q not in st.session_state.wrong_questions:
                        st.session_state.wrong_questions.append(orig_q)
                    st.session_state.forgetting_curve_log[q["question"]] = str(datetime.now())

                st.session_state.quiz_results_log.append({
                    "question": q["question"],
                    "user_answer": option,
                    "correct_answer": q["answer"],
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                })
                st.rerun()

        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>'
                    f'正解は <b>{q["answer"]}</b> です。</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(f"""
                <div class="explanation-box">
                    <b>💡 解説:</b> {q['explanation']}<br><br>
                    <span style="font-size: 0.9em; background-color: #ffffff; padding: 3px 6px; border-radius: 4px; color: #084298;">📌 <b>検定ポイント:</b> {q['tag']}</span>
                </div>
            """, unsafe_allow_html=True)

            if st.button("次の問題へ ➡️", type="primary", use_container_width=True):
                st.session_state.current_q += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()

    # ==========================================
    # 3. 結果発表画面
    # ==========================================
    else:
        total_len = len(active_quiz)
        accuracy = round((st.session_state.score / total_len) * 100, 1) if total_len > 0 else 0

        if st.session_state.is_mock_exam:
            st.header("🎓 本番模擬試験 結果発表")
            if accuracy >= 70.0:
                st.balloons()
                st.markdown(f"""
                    <div class="pass-banner">
                        <h2>🎉 合格圏内クリア！おめでとうございます！</h2>
                        <p style="font-size: 1.2em;">得点率: <b>{accuracy}%</b>（合格基準 70%以上）</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="fail-banner">
                        <h2>💪 合格ラインまであと一歩！</h2>
                        <p style="font-size: 1.2em;">得点率: <b>{accuracy}%</b>（合格基準 70%以上）</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.balloons()
            st.header("🎊 お疲れ様でした！結果発表")

        st.metric(label="獲得スコア / 正答率", value=f"{st.session_state.score} / {total_len} 問正解 ({accuracy}%)")

        if not st.session_state.get("history_recorded", False):
            attempt_num = len(st.session_state.history) + 1
            st.session_state.history.append({"回数": f"{attempt_num}回目", "正答率(%)": accuracy})
            st.session_state.study_dates.add(str(date.today()))
            st.session_state.history_recorded = True

        st.markdown("---")
        st.subheader("📋 今回の全問レビュー（答え合わせ）")
        for idx, log in enumerate(st.session_state.quiz_results_log):
            status = "🟢 正解" if log["is_correct"] else "🔴 不正解"
            with st.expander(f"第{idx+1}問: {status} - {log['question'][:30]}..."):
                st.write(f"**問題:** {log['question']}")
                st.write(f"あなたの回答: {log['user_answer']}")
                st.write(f"正しい答え: **{log['correct_answer']}**")
                st.info(f"解説: {log['explanation']}")

        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 ホーム画面に戻る", type="primary", use_container_width=True):
                st.session_state.app_mode = "home"
                st.session_state.history_recorded = False
                st.rerun()
        with col2:
            wrong_cnt = len(st.session_state.wrong_questions)
            if st.button(f"❌ 間違い復習 ({wrong_cnt}問)", disabled=(wrong_cnt == 0), use_container_width=True):
                start_quiz(st.session_state.wrong_questions, "🔄 間違い復習モード", is_mock_exam=False)
                st.rerun()
