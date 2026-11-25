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
    "question": "「イエローストーン国立公園」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 1872年に世界初の国立公園として設立され、1978年に自然遺産として登録された。",
      "② 公園中心部には、約200万年前の最初の噴火によって巨大なカルデラが形成された。",
      "③ 有名な間欠泉オールド・フェイスフル・ガイザーは、平均30分間隔で熱湯を噴出する。",
      "④ 山火事が発生した際は、生態系を守るため人間が迅速に消火活動を行う方針をとっている。"
    ],
    "answer": "① 1872年に世界初の国立公園として設立され、1978年に自然遺産として登録された。",
    "explanation": "正解は①です[cite: 34]。②は「最後の噴火時（約60万年前）」に巨大なカルデラが形成[cite: 34]、③は平均「70分間隔」[cite: 34]、④は「ウィルダネス（手つかずの自然）」の概念に基づき人間が消火をせずに「自然の回復機能に任せる」対応がとられます[cite: 34]。",
    "tag": "登録年: 1978年 / 基準(vii)(viii)(ix)(x) / イエローストーン国立公園",
    "trivia": "バクテリアの影響で青色をした温泉グランド・プリズマティック・スプリングがあり、先住民族のスー族は「霊気に満ちた場所」と恐れました[cite: 34]。"
  },
  {
    "question": "「ナハニ国立公園」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① カナダに位置し、1978年に自然遺産として登録された。",
      "② 高緯度のツンドラ地帯でありながら穏やかな気候で、ハッカやシオンといった植物が自生する。",
      "③ グリズリーやカリブー、シロイワヤギなどの野生動物の姿も見られる。",
      "④ サウス・ナハニ川の流れは上流が岩をも削る急流で、ヴァージニア滝を過ぎるとゆったりとした流れになる。"
    ],
    "answer": "④ サウス・ナハニ川の流れは上流が岩をも削る急流で、ヴァージニア滝を過ぎるとゆったりとした流れになる。",
    "explanation": "正解は④です。サウス・ナハニ川の流れは、上流はゆったりとしていますが、ヴァージニア滝を過ぎると岩をも削るほどの急流となります[cite: 35]。①〜③は紙面の記載どおり正しい内容です[cite: 35]。",
    "tag": "登録年: 1978年 / 基準(vii)(viii) / ナハニ国立公園",
    "trivia": "滝やオーロラなど美しい自然が広がり、場所によって大きく表情を変える独特の景観をつくり出しています[cite: 35]。"
  },
  {
    "question": "「シミエン国立公園」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 標高約4,500mを誇るアフリカ最高峰のラスダシャン山がそびえる山岳地帯に位置する。",
      "② ワリアアイベックスやゲラダヒヒなど貴重な動物が生息している。",
      "③ 一日の寒暖差が小さいため、多様な種類の動植物が生息できる。",
      "④ 密猟や新道路の建設計画による生態系の破壊が懸念され、現在も危機遺産リストに記載されている。"
    ],
    "answer": "② ワリアアイベックスやゲラダヒヒなど貴重な動物が生息している。",
    "explanation": "正解は②です[cite: 35]。①のラスダシャン山はアフリカ「第4の山」[cite: 35]、③は一日の寒暖差が「激しい」ため生息できる動植物の種類が限られており[cite: 35]、④は危機遺産リストに記載「されていた」（過去形）と記されています[cite: 35]。",
    "tag": "登録年: 1978年 / 基準(vii)(x) / シミエン国立公園",
    "trivia": "エチオピア連邦民主共和国に位置し、氷河がつくり出した渓谷や岩山が広がる厳しい環境です[cite: 35]。"
  },
  {
    "question": "「ガラパゴス諸島」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 大小19の島々と多くの岩礁からなり、チャールズ・ダーウィンが生物を観察し進化論の着想を得た。",
      "② 1978年に自然遺産に登録され、2001年に範囲が縮小された。",
      "③ 島々で見られる植物の半数、繁殖鳥類の3分の1が固有種と考えられている。",
      "④ フィンチはスズメ目の小鳥で、ガラパゴス諸島近海にのみ生息するものはチャールズ・フィンチと呼ばれる。"
    ],
    "answer": "① 大小19の島々と多くの岩礁からなり、チャールズ・ダーウィンが生物を観察し進化論の着想を得た。",
    "explanation": "正解は①です[cite: 35]。②は2001年に「範囲拡大」[cite: 35]、③は植物の「3分の1」、繁殖鳥類の「半数」、爬虫類のほぼすべてが固有種[cite: 35]、④は「ダーウィン・フィンチ」と呼ばれます[cite: 35]。",
    "tag": "登録年: 1978年・2001年範囲拡大 / 基準(vii)(viii)(ix)(x) / ガラパゴス諸島",
    "trivia": "ダーウィンはゾウガメやウミイグアナ、フィンチなどを観察し、同じ種でも島ごとに進化して異なる特徴をもつ亜種になっていることに気づきました[cite: 35]。"
  },
  {
    "question": "「キトの市街」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① エクアドルの首都キトは、アンデス山脈中腹の標高2,850mの高地に築かれた都市である。",
      "② 先住民のキトス族が築いた街があったが、15世紀にインカ帝国の支配下に入り、インカ第2の都市として発展した。",
      "③ 16世紀のスペイン人の侵略で廃墟となった後、スペイン人によって教会や修道院が数多く建設され、キリスト教布教の拠点となった。",
      "④ 旧市街に残る宗教建築は、ヨーロッパのゴシック様式やイスラム伝統のビザンツ様式などが融合したものである。"
    ],
    "answer": "④ 旧市街に残る宗教建築は、ヨーロッパのゴシック様式やイスラム伝統のビザンツ様式などが融合したものである。",
    "explanation": "正解は④です。キトの旧市街に残る16〜18世紀頃の教会堂や修道院は、ヨーロッパの「バロック様式」やスペイン伝統の「ムデハル様式」などが融合した植民地特有のスタイルで建てられています[cite: 36]。",
    "tag": "登録年: 1978年 / 基準(ii)(iv) / キトの市街",
    "trivia": "キトの旧市街には現在、16〜18世紀頃の教会堂や修道院が30以上も残っています[cite: 36]。"
  },
  {
    "question": "「クラクフの歴史地区」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 11世紀初頭から17世紀のワルシャワ遷都までの600年間、ポーランド王国の首都として栄えた。",
      "② 13世紀半ばに来襲したオスマン帝国軍による破壊に遭うが、再建されて自治都市として繁栄した。",
      "③ 旧市街のヴァヴェル城は、レオナルド・ダ・ヴィンチの油彩画『白貂を抱く貴婦人』を所蔵している。",
      "④ コペルニクスの学んだヴァヴェル大学などの建造物が集まる。"
    ],
    "answer": "① 11世紀初頭から17世紀のワルシャワ遷都までの600年間、ポーランド王国の首都として栄えた。",
    "explanation": "正解は①です[cite: 36]。②の破壊は「モンゴル軍」によるもの[cite: 36]、③の『白貂を抱く貴婦人』を所蔵しているのはポーランド最古の美術館である「チャルトリスキ美術館」[cite: 36]、④は「ヤギェウォ大学」です[cite: 36]。",
    "tag": "登録年: 1978年・2010年範囲変更 / 基準(iv) / クラクフの歴史地区",
    "trivia": "旧市街にはヴァヴェル城やルネサンス様式の織物会館、レンガ造の聖マリア教会などが集まります[cite: 36]。"
  },
  {
    "question": "「アーヘンの大聖堂」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① カール大帝の宮廷礼拝堂を起源とする805年完成の建造物で、16世紀までの間に神聖ローマ皇帝30人の戴冠式が行われた。",
      "② 聖堂は十六角形の中心部を八角形の周歩廊が取り囲む集中式の構造である。",
      "③ 13世紀にはゴシック様式の内陣が追加され、15世紀初めに「カール大帝の聖遺物箱」が奉じられた。",
      "④ 扉や棚は現存する唯一のメロヴィング朝時代の青銅製の作品である。"
    ],
    "answer": "① カール大帝の宮廷礼拝堂を起源とする805年完成の建造物で、16世紀までの間に神聖ローマ皇帝30人の戴冠式が行われた。",
    "explanation": "正解は①です[cite: 37]。②は「八角形の中心部を十六角形の周歩廊」が取り囲む集中式の構造[cite: 37]、③は13世紀に「カール大帝の聖遺物箱」、15世紀初めに「ゴシック様式の内陣」[cite: 37]、④は「カロリング朝時代」の青銅製の作品です[cite: 37]。",
    "tag": "登録年: 1978年・2013年範囲変更 / 基準(i)(ii)(iv)(vi) / アーヘンの大聖堂",
    "trivia": "ドイツ連邦共和国に位置し、カール大帝（シャルルマーニュ）によってフランク王国カロリング朝の事実上の首都となったアーヘンにあります[cite: 37]。"
  },
  {
    "question": "「ラリベラの岩の聖堂群」に関する次の文中の空欄（ A ）、（ B ）に当てはまる語句の組み合わせとして、正しいものはどれか。\n\n「12〜13世紀に造営されたエチオピア正教会の岩窟聖堂群で、聖地エルサレムがイスラム教徒に支配されていた12世紀末、（ A ）7代国王ラリベラが、都を『第2のエルサレム』にしようと岩窟聖堂の造営を開始し、わずか20数年の間に11の岩窟聖堂が完成した。聖堂には（ B ）の様式を用いたものや、古代ギリシャやローマ、ビザンツ様式の影響を感じさせるものも多い。」",
    "options": [
      "① A. ザグウェ朝 — B. アクスム王国",
      "② A. アクスム王国 — B. ザグウェ朝",
      "③ A. ソロモン朝 — B. アクスム王国",
      "④ A. ザグウェ朝 — B. メロエ王国"
    ],
    "answer": "① A. ザグウェ朝 — B. アクスム王国",
    "explanation": "正解は①です。12世紀末に「ザグウェ朝」7代国王ラリベラが造営を開始し、聖堂には紀元前後にエチオピア北部に栄えた「アクスム王国」の様式を用いたものなどがあります[cite: 37]。",
    "tag": "登録年: 1978年 / 基準(i)(ii)(iii) / ラリベラの岩の聖堂群",
    "trivia": "11の聖堂群は、ヨルダン川を挟んだ北岸と南岸に5つずつ、そこから300mほど離れた場所にひとつあります[cite: 37]。"
  },
 {
    "question": "「ヴィエリチカとボフニャの王立岩塩坑」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① クラクフ郊外にある世界最古の岩塩採掘場で、最盛期の14〜16世紀には岩塩坑の収入がポーランド王国の財源の3分の1を占めた。",
      "② 地下101mの「聖キンガの礼拝堂」では、レオナルド・ダ・ヴィンチの『最後の晩餐』をモチーフとしたレリーフなどが見られる。",
      "③ 礼拝堂のシャンデリアは、硬い岩塩を削り出して作られたものである。",
      "④ 2013年、ボフニャの王立岩塩坑とヴィエリチカ製塩所が構成資産に追加された。"
    ],
    "answer": "③ 礼拝堂のシャンデリアは、硬い岩塩を削り出して作られたものである。",
    "explanation": "正解は③です。シャンデリアは硬い岩塩を削り出したものではなく、「塩の結晶でつくられた見事なシャンデリア」と記載されています。④は紙面の記載どおり正しい記述です。",
    "tag": "登録年: 1978年・2008年範囲変更・2008年,2013年範囲拡大 / 基準(iv) / ヴィエリチカとボフニャ",
    "trivia": "聖キンガ（1224〜1292）は岩塩窟を発見したとされるハンガリーの王女で、ポーランド王子との結婚に乗り気でなかった彼女が指輪を投げ捨てた場所から最初の岩塩窟が見つかったとの伝説が残ります。"
  },
  {
    "question": "「ゴレ島」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 15世紀以降、ポルトガル、オランダ、イギリス、フランスの支配を次々と受け、奴隷貿易が廃止された1815年まで三角貿易の拠点であった。",
      "② 島の東岸に残る「奴隷の家」は、1階が奴隷商人たちの住居で、2階に船の出港を待つ奴隷たちが収容されていた。",
      "③ 「奴隷の家」の2.6m四方の正方形の部屋には、10人が鎖でつながれて詰め込まれていたといわれる。",
      "④ 島の南端には、オランダによって完成されたエストレ要塞が歴史博物館として残っている。"
    ],
    "answer": "① 15世紀以降、ポルトガル、オランダ、イギリス、フランスの支配を次々と受け、奴隷貿易が廃止された1815年まで三角貿易の拠点であった。",
    "explanation": "正解は①です[cite: 38]。②は「2階が奴隷商人たちの住居、1階に奴隷たちが収容」[cite: 38]、③は「20人」が詰め込まれていた[cite: 38]、④は島の「北端」に「フランス」によって完成されたエストレ要塞が残っています[cite: 38]。",
    "tag": "登録年: 1978年 / 基準(vi) / ゴレ島",
    "trivia": "セネガル共和国に位置する「負の遺産」で、多くの黒人たちを奴隷としてアメリカ大陸に送り込みました[cite: 38]。"
  },
  {
    "question": "「メサ・ヴェルデ国立公園」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① コロラド州にあり、メサ・ヴェルデとはスペイン語で「緑の台地」を意味する。",
      "② 12世紀末に先住民のキトス族が断崖の壁面に築いた鳥の巣のような住居群の遺跡である。",
      "③ 全部で3つの住居群のうち最大のクリフ・パレスは、全体が3層構造で23の部屋がある。",
      "④ キヴァと呼ばれる220の円形地下礼拝所や、貯水・灌漑システムが備わっている。"
    ],
    "answer": "① コロラド州にあり、メサ・ヴェルデとはスペイン語で「緑の台地」を意味する。",
    "explanation": "正解は①です[cite: 39]。②はキトス族ではなく先住民の「アナサジ族」[cite: 39]、③・④は最大のクリフ・パレスは「4層構造」で、「220の部屋」とキヴァと呼ばれる「23の円形地下礼拝所」があります[cite: 39]。",
    "tag": "登録年: 1978年 / 基準(iii) / メサ・ヴェルデ国立公園",
    "trivia": "クリフ・パレスは崖下にあり、200〜250人が居住していました[cite: 39]。"
  },
  {
    "question": "「ランス・オー・メドー国立歴史公園」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① ニューファンドランド島の北端に位置し、1000年頃に北欧から渡来してきたヴァイキングの集落跡がある。",
      "② 現在、3つの建物が復元されている。",
      "③ 12〜13世紀頃に編纂された北欧の伝承文学『サガ』の記述に基づき、1960年代にノルウェーの歴史学者が調査を行った。",
      "④ 調査では8ヵ所の住居跡や製材所、鍛冶場の他、青銅器や鉄器などが発見され、いずれもデンマークの様式と一致した。"
    ],
    "answer": "④ 調査では8ヵ所の住居跡や製材所、鍛冶場の他、青銅器や鉄器などが発見され、いずれもデンマークの様式と一致した。",
    "explanation": "正解は④です。発見された遺跡や遺物はいずれもデンマークではなく「ノルウェーの様式」と一致しており、この地に北アメリカにおける最初のヨーロッパ人の入植地が築かれたことが裏づけられました[cite: 39]。",
    "tag": "登録年: 1978年・2017年範囲変更 / 基準(vi) / ランス・オー・メドー",
    "trivia": "ヴァイキングとはスカンジナビア半島およびバルト海沿岸を原住地としたノルマン人の別称で、船でヨーロッパや北米まで進出しました[cite: 39]。"
  },
  {
    "question": "「紅河ハニ族棚田群の文化的景観」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 中国南部にそびえる哀牢山の中の雲南省紅河ハニ族イ族自治州元陽県を中心とする斜面に広がり、3,000段を有すともされる。",
      "② 1,300年にわたり伝統的な生活を守り続け、山頂部の森林を伐採して貯水池を人工的に造り上げた。",
      "③ ハニ族は「森林」「水系」「棚田」「祭壇」の四つの要素からなる循環型灌漑システムをつくり上げている。",
      "④ 村の半分を占める伝統的な家屋は、レンガ造りの平らな屋根が特徴である。"
    ],
    "answer": "① 中国南部にそびえる哀牢山の中の雲南省紅河ハニ族イ族自治州元陽県を中心とする斜面に広がり、3,000段を有すともされる。",
    "explanation": "正解は①です[cite: 40]。②は森林を伐採しておらず「山頂部の森林は天然の貯水池」として長年森林を保護[cite: 40]、③の四つの要素は「森林」「水系」「棚田」「村」[cite: 40]、④は石や日干しレンガにわらなどを葺いた「キノコのような形状」が特徴です[cite: 40]。",
    "tag": "登録年: 2013年 / 基準(iii)(v) / 紅河ハニ族棚田群",
    "trivia": "この地域は亜熱帯性の気候で年間降雨量は1,400mmに達し、水は山頂から用水路を伝って上段から下段に流れ、くまなく棚田を潤しています[cite: 40]。"
  },
  {
    "question": "「普洱（プーアル）の景邁山古茶林の文化的景観」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2023年に登録された文化的景観で、10世紀以降、布朗族と傣族によって伝統的な方法で茶の栽培が行われてきた。",
      "② 自然林をすべて伐採した後に茶樹を植える「段々畑栽培」という手法が編み出された。",
      "③ 祖先の霊が茶畑に宿るとする「祖先崇拝」をもち、村人・商人・僧侶の3つが一体となった社会システムに従っている。",
      "④ 登録基準は（iii）（iv）が適用されている。"
    ],
    "answer": "① 2023年に登録された文化的景観で、10世紀以降、布朗族と傣族によって伝統的な方法で茶の栽培が行われてきた。",
    "explanation": "正解は①です[cite: 41]。②は自然林の一部の樹木と低木を間引きし、そこに茶樹を植える「林下栽培」という手法[cite: 41]、③は精霊が茶畑や動植物に宿るとする「茶祖信仰」をもち、「部族・政府・宗教」の3つが一体となった社会システム[cite: 41]、④の登録基準は（iii）（v）です[cite: 41]。",
    "tag": "登録年: 2023年 / 基準(iii)(v) / 普洱の景邁山古茶林",
    "trivia": "林下栽培は、中国南西部の景邁山の山岳環境や亜熱帯モンスーン気候に合わせて編み出された手法です[cite: 41]。"
  },
  {
    "question": "「キューバ南東部におけるコーヒー農園発祥地の景観」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① スペインの植民地だった19世紀に造られたキューバで初めてのコーヒー農園の跡である。",
      "② 19〜20世紀にかけての植民地におけるプランテーションによるコーヒー栽培の様子を伝えている。",
      "③ 171の古いコーヒー農園だけでなく、コーヒーを輸出するための道路や橋梁などのインフラも構成資産に含まれる。",
      "④ 2000年に登録された文化的景観で、登録基準は（iv）（v）が適用されている。"
    ],
    "answer": "④ 2000年に登録された文化的景観で、登録基準は（iv）（v）が適用されている。",
    "explanation": "正解は④です。2000年に登録された文化的景観ですが、登録基準は（iv）（v）ではなく（iii）（iv）が適用されています[cite: 41]。①〜③はいずれも紙面の記載どおり正しい内容です[cite: 41]。",
    "tag": "登録年: 2000年 / 基準(iii)(iv) / キューバ南東部のコーヒー農園",
    "trivia": "開拓当時のコーヒー農園の農業形態を残す場所は世界でもここしかなく、貴重な遺構です[cite: 41]。"
  },
  {
    "question": "「メイマンドの文化的景観」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① イラン中央山脈南端の渓谷に位置し、村人は春と秋には渓谷へ降りて洞窟住居で暮らし、冬の間は山の上で放牧を行う。",
      "② 乾燥砂漠地域に独特な軟岩を掘った洞窟住居があり、半乾燥地帯における自給自足の生活が営まれている。",
      "③ 家畜のみを季節ごとに移動させ、人間は年間を通して同じ住居に定住する独自の生活様式を伝えている。",
      "④ 2015年に登録された文化的景観で、登録基準は（iii）（v）が適用されている。"
    ],
    "answer": "② 乾燥砂漠地域に独特な軟岩を掘った洞窟住居があり、半乾燥地帯における自給自足の生活が営まれている。",
    "explanation": "正解は②です[cite: 41]。①は季節が逆で、「春と秋には一時的な住居を構え、山の上で放牧を行い、冬の間は渓谷へと降り、洞窟住居で暮らす」[cite: 41]、③は「家畜ではなく人間が移動する独自の生活様式」[cite: 41]、④の登録基準は（v）のみです[cite: 41]。",
    "tag": "登録年: 2015年 / 基準(v) / メイマンドの文化的景観",
    "trivia": "厳しく乾燥した地帯の環境を生きぬく人々の知恵を伝える文化的景観です[cite: 41]。"
  },
  {
    "question": "「ラヴォー地域のブドウ畑」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① カトリック修道会のベネディクト会とシトー会の指導のもと、11世紀からワイン生産が続いている。",
      "② ジュネーヴ湖に沿うように広がるブドウの段々畑は、ローザンヌからシヨン城までの約30kmに及ぶ。",
      "③ 緩やかな斜面のブドウ畑の間に民家やワイン工場が点在し、ピレネー山脈をあおぐ景観を生み出している。",
      "④ 2007年に登録された文化的景観で、登録基準は（iii）（v）が適用されている。"
    ],
    "answer": "① カトリック修道会のベネディクト会とシトー会の指導のもと、11世紀からワイン生産が続いている。",
    "explanation": "正解は①です[cite: 42]。②はジュネーヴ湖ではなく「レマン湖」[cite: 42]、③は緩やかな斜面ではなく「急斜面」で「アルプス山脈」をあおぐ景観[cite: 42]、④の登録基準は（iii）（iv）（v）です[cite: 42]。",
    "tag": "登録年: 2007年 / 基準(iii)(iv)(v) / ラヴォー地域のブドウ畑",
    "trivia": "スイス連邦に位置し、ローザンヌからシヨン城までの約30kmにわたってブドウの段々畑が広がります[cite: 42]。"
  },
  {
    "question": "「クラドルビ・ナド・ラベムにある式典馬車用の馬の繁殖・訓練地の景観」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① エルベ川の氾濫原に位置する国営の種馬飼育牧場である。",
      "② 1579年に皇帝ルドルフ2世により宮廷馬飼育場に指定されて以来、ハプスブルク家の儀礼用馬車馬クラドルバー種の繁殖と訓練に特化してきた。",
      "③ フランス式庭園設計に基づく中央路や水路、並木道、シンメトリー構造などの他、イギリス式景観理念も取り入れられている。",
      "④ 2019年に登録された文化的景観で、登録基準は（iii）（iv）が適用されている。"
    ],
    "answer": "④ 2019年に登録された文化的景観で、登録基準は（iii）（iv）が適用されている。",
    "explanation": "正解は④です。2019年に登録された文化的景観ですが、登録基準は（iii）（iv）ではなく（iv）（v）が適用されています[cite: 42]。①〜③はいずれも紙面の記載どおり正しい内容です[cite: 42]。",
    "tag": "登録年: 2019年・2021年範囲変更 / 基準(iv)(v) / クラドルビ・ナド・ラベム",
    "trivia": "チェコ共和国にあり、周囲の田園風景と調和するイギリス式景観理念も取り入れられ、ヨーロッパの高い造園技術と馬術文化の歴史を示しています[cite: 42]。"
  },
  {
    "question": "「オリーヴとワインの土地 - バッティールの丘：南エルサレムの文化的景観」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2014年に世界遺産に登録され、同年、イスラエルが分離壁の建設を計画していることなどから緊急的登録推薦で危機遺産リストにも登録された。",
      "② エルサレム北部に位置するバッティールの丘には、レンガ造りの段々畑が続く渓谷の景観が広がる。",
      "③ 湿潤な気候を生かし、灌漑設備を一切使わずにブドウやオリーヴの木が栽培されている。",
      "④ 登録基準は（iii）（iv）（v）が適用されている。"
    ],
    "answer": "① 2014年に世界遺産に登録され、同年、イスラエルが分離壁の建設を計画していることなどから緊急的登録推薦で危機遺産リストにも登録された。",
    "explanation": "正解は①です[cite: 42]。②はエルサレム「南部」に位置する「石造りの段々畑」[cite: 42]、③は「乾燥した土地」で「水を利用した農業」として灌漑を備えた畑などがあり[cite: 42]、④の登録基準は（iv）（v）です[cite: 42]。",
    "tag": "登録年: 2014年・2014年危機遺産登録 / 基準(iv)(v) / バッティールの丘",
    "trivia": "緊急的登録推薦とは、緊急な保護が必要なため正規の手順を経ずに登録する方法です[cite: 42]。"
  },
  {
    "question": "「ビニャーレス渓谷」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① キューバ最西端に位置し、モゴーテ（断崖）と呼ばれる石灰岩の岩山や洞窟が点在する渓谷に伝統的な農業風景が広がる。",
      "② モゴーテは大きなものでは高さ500mにもなり、洞窟では岩絵や鍾乳石を見ることができる。",
      "③ 古くからサトウキビの産地として知られ、スペイン文化に起源をもつレンガ造りの家屋が見られる。",
      "④ 1999年に登録された文化的景観で、登録基準は（iii）（iv）が適用されている。"
    ],
    "answer": "① キューバ最西端に位置し、モゴーテ（断崖）と呼ばれる石灰岩の岩山や洞窟が点在する渓谷に伝統的な農業風景が広がる。",
    "explanation": "正解は①です[cite: 43]。②のモゴーテの高さは大きなもので「300m」[cite: 43]、③はサトウキビではなく「葉タバコの産地」で「先住民文化に起源をもつ独特の木造家屋」[cite: 43]、④の登録基準は（iv）のみです[cite: 43]。",
    "tag": "登録年: 1999年 / 基準(iv) / ビニャーレス渓谷",
    "trivia": "洞窟はかつて先住民の住居や奴隷の隠れ家として用いられました[cite: 43]。"
  },
  {
    "question": "「聖山スレイマン・トー」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① キルギス初の世界遺産となった聖山で、長年にわたりシルク・ロードの旅人にとって灯台の役割を果たした。",
      "② 5つの峰と山腹には古代の耕作跡地、数多くの岩面画が描かれた洞窟群、そして16世紀に再建された2つのモスクがある。",
      "③ 古くからの民間信仰とイスラム教信仰が混在し、宗教的儀礼が行われた場所も多い。",
      "④ 2009年に登録された文化的景観で、登録基準は（iii）（v）が適用されている。"
    ],
    "answer": "④ 2009年に登録された文化的景観で、登録基準は（iii）（v）が適用されている。",
    "explanation": "正解は④です。2009年に登録された文化的景観ですが、登録基準は（iii）（v）ではなく（iii）（vi）が適用されています[cite: 43]。①〜③はいずれも紙面の記載どおり正しい内容です[cite: 43]。",
    "tag": "登録年: 2009年 / 基準(iii)(vi) / 聖山スレイマン・トー",
    "trivia": "中央アジアに多いこの種の聖山の典型ともいえる遺産です[cite: 43]。"
  },
  {
    "question": "「タウリカ半島の古代都市とチョーラ」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① クリミア（タウリカ）半島の南端のケルソネソスにある、紀元前5世紀にドーリア人によって築かれた古代ギリシャの都市遺跡である。",
      "② 黒海の南岸に位置し、チョーラといわれる等分に円形に区画された農地も含まれる。",
      "③ 2013年に登録され、登録基準は（iii）（iv）が適用されている。",
      "④ 2014年にウクライナが一方的に併合し、2022年以降は戦闘が収束して保全状況が安定した。"
    ],
    "answer": "① クリミア（タウリカ）半島の南端のケルソネソスにある、紀元前5世紀にドーリア人によって築かれた古代ギリシャの都市遺跡である。",
    "explanation": "正解は①です[cite: 43]。②は黒海の「北岸」に位置し、チョーラは等分に「長方形に区画された農地」[cite: 43]、③の登録基準は（ii）（v）[cite: 43]、④は2014年に「ロシアが一方的に併合」し、2022年に始まったロシアのウクライナ侵略でもクリミア付近で戦闘が起きており「遺産の保全状況が懸念」されています[cite: 43]。",
    "tag": "登録年: 2013年 / 基準(ii)(v) / タウリカ半島の古代都市とチョーラ",
    "trivia": "ウクライナに位置する文化的景観で、古代ギリシャの都市遺跡と周囲の区画農地（チョーラ）が一体となって評価されています[cite: 43]。"
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
