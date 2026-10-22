# -*- coding: utf-8 -*-
"""VoiceGrace サイトのビルド。src/ の部品から index/kids/adults/business の4ページを組む。
   使い方: python3 build.py
"""
import re, os
SRC = os.path.join(os.path.dirname(__file__), "src")
OUT = os.path.dirname(__file__)
def part(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f: return f.read()

LINE = "https://line.me/R/ti/p/@036bejox"
CATCH = "帝劇の舞台から、「声の仕組み」を教える人へ。"

# ---------- 共通部品 ----------
def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,700;1,400&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
'''

def nav(current):
    items = [("index.html","ホーム"),("kids.html","子ども・保護者の方"),("adults.html","大人の方"),("business.html","企業・団体の方")]
    lis = "".join(f'<li><a href="{h}"{" class=current" if h==current else ""}>{t}</a></li>' for h,t in items)
    cta = f'<li><a href="{LINE}" target="_blank" class="nav-cta" style="background:#06C755;">LINEで相談</a></li>'
    return f'''<nav>
  <a class="nav-logo" href="index.html" style="text-decoration:none;">VoiceGrace<span>ボイストレーニング・ミュージカル</span></a>
  <ul class="nav-links">{lis}{cta}</ul>
  <button class="hamburger" onclick="toggleMenu()"><span></span><span></span><span></span></button>
</nav>
'''

ANNOUNCE = part("announce.html")

def footer():
    return f'''<footer>
  <div class="footer-logo">VoiceGrace</div>
  <div class="footer-tagline">{CATCH}</div>
  <div class="footer-sns">
    <a href="https://www.threads.com/@shoko.sakai.1102" target="_blank" class="sns-btn" title="Threads">🧵</a>
    <a href="https://www.instagram.com/shoko.sakai.1102" target="_blank" class="sns-btn" title="Instagram（日常）">📸</a>
    <a href="https://www.instagram.com/shoko.sing1102" target="_blank" class="sns-btn" title="Instagram（歌唱動画）">🎶</a>
    <a href="https://note.com/shkski1102" target="_blank" class="sns-btn" title="note">📝</a>
    <a href="{LINE}" target="_blank" class="sns-btn" title="公式LINE" style="background:#06C755;">💬</a>
  </div>
  <div class="footer-links">
    <a href="index.html">ホーム</a>
    <a href="kids.html">子ども・保護者の方</a>
    <a href="adults.html">大人の方</a>
    <a href="business.html">企業・団体の方</a>
    <a href="index.html#about">講師について</a>
  </div>
  <p class="footer-copy">© 2026 VoiceGrace / 酒井翔子. All rights reserved.</p>
</footer>
<a href="{LINE}" target="_blank" class="line-float">💬 LINEで相談</a>
<script src="site.js"></script>
</body>
</html>
'''

def page_head(label, title_html, sub):
    return f'''<section class="page-head">
  <div class="section-inner">
    <div class="section-label">{label}</div>
    <h1 class="section-title">{title_html}</h1>
    <p class="section-sub">{sub}</p>
  </div>
</section>
'''

def line_box(h, p, btn="LINEで友だち追加"):
    return f'''<div class="line-box">
      <h4>{h}</h4>
      <p>{p}</p>
      <a href="{LINE}" target="_blank" class="btn-line">{btn}</a>
    </div>'''

def booking(options, intro, show_dur=True):
    """options: list of (value, label, sub, price)"""
    radios = "".join(
        f'<div class="lt-option"><input type="radio" name="lt" id="lt{i}" value="{v}"{" checked" if i==0 else ""} onchange="onLtChange()"><label for="lt{i}">{l}<span class="lt-sub">{s}</span><span class="lt-price">{pr}</span></label></div>'
        for i,(v,l,s,pr) in enumerate(options))
    cols = "compact" if len(options) <= 4 else ""
    return f'''<section id="booking">
  <div class="booking-wrap">
    <div class="section-label">Booking</div>
    <h2 class="section-title">レッスンを<em>予約する</em></h2>
    <p class="section-sub">{intro}</p>
    <div id="bForm">
      <div class="form-field">
        <label>レッスン種別<span class="req">*</span></label>
        <div class="lt-grid {cols}">{radios}</div>
      </div>
      <div class="form-field" id="durField"{"" if show_dur else ' style="display:none"'}>
        <label>レッスン時間<span class="req">*</span></label>
        <select id="bDur"><option value="25分">25分</option><option value="50分">50分</option></select>
      </div>
      <div class="date-row">
        <div class="form-field"><label>希望日<span class="req">*</span> <span class="hint">空き状況を確認してご返信します</span></label><input type="date" id="bDate"></div>
        <div class="form-field"><label>希望時間<span class="req">*</span></label><select id="bTime"></select></div>
      </div>
      <div class="form-field">
        <label>レッスン形式<span class="req">*</span></label>
        <select id="bFormat"><option value="">選択してください</option><option value="オンライン（Zoom）">オンライン（Zoom）</option><option value="対面（川崎）">対面（川崎）※近郊の方のみ</option></select>
      </div>
      <div class="sub-note">📅 <strong>第2・第3希望日時</strong>（任意）<br><span>第1希望が埋まっていた場合に備えてご記入ください</span></div>
      <div class="date-row">
        <div class="form-field"><label>第2希望日</label><input type="date" id="bDate2"></div>
        <div class="form-field"><label>第2希望時間</label><select id="bTime2"></select></div>
      </div>
      <div class="date-row">
        <div class="form-field"><label>第3希望日</label><input type="date" id="bDate3"></div>
        <div class="form-field"><label>第3希望時間</label><select id="bTime3"></select></div>
      </div>
      <div class="form-field"><label>お名前<span class="req">*</span></label><input type="text" id="bName" placeholder="山田 花子"></div>
      <div class="form-field"><label>メールアドレス<span class="req">*</span></label><input type="email" id="bEmail" placeholder="example@email.com"></div>
      <div class="form-field"><label>ご要望・現在のお悩み</label><textarea id="bNote" placeholder="例：高い声が出ない、オーディションに向けて準備したいなど"></textarea></div>
      <button class="form-submit" onclick="submitForm()">予約リクエストを送る 🌸</button>
    </div>
    <div class="booking-success" id="bSuccess">
      <div class="success-emoji">🎉</div>
      <h3>予約リクエスト<em>完了！</em></h3>
      <p>ご予約リクエストありがとうございます。<br>空き状況を確認のうえ、2日以内にメールでご連絡します。</p>
      <div class="confirm-box" id="bConfirmBox"></div>
      <button class="btn-reset" onclick="resetBooking()">別の日程で予約する</button>
    </div>
  </div>
</section>
'''

def faq(items):
    inner = "".join(f'''
      <div class="faq-item">
        <button class="faq-q" onclick="toggleFaq(this)">Q. {q}<span class="faq-arrow">▼</span></button>
        <div class="faq-a">{a}</div>
      </div>''' for q,a in items)
    return f'''<section id="faq">
  <div class="section-inner">
    <div class="section-label">FAQ</div>
    <h2 class="section-title">よくある<em>質問</em></h2>
    <div class="faq-list">{inner}
    </div>
  </div>
</section>
'''

def testimonials(cards):
    inner = "".join(f'''
      <div class="testimonial-card">
        <div class="testimonial-stars">★★★★★</div>
        <div class="testimonial-quote">"</div>
        <p>{t}</p>
        <div class="testimonial-author"><div class="testimonial-avatar">{em}</div><div><div class="testimonial-name">{n}</div><div class="testimonial-role">{r}</div></div></div>
      </div>''' for em,t,n,r in cards)
    return f'''<section id="testimonials">
  <div class="section-inner">
    <div class="section-label">Voice</div>
    <h2 class="section-title">生徒さんの<em>声</em></h2>
    <div class="testimonials-grid reveal">{inner}
    </div>
  </div>
</section>
'''

# ---------- データ ----------
FAQ = {
 "beginner": ("完全初心者でも大丈夫ですか？","もちろんです！カラオケで上手に歌いたい方から、本格的に舞台を目指したい方まで大歓迎。初めての方も安心して受講できるよう、丁寧にサポートします。"),
 "online": ("オンラインはどんな環境が必要ですか？","スマートフォン・パソコン・タブレットとZoomがあればOKです。有線イヤホンがあると音質がよくなります。また、Zoomに接続する機器とは別にカラオケ音源を流せる機材（スマホ・タブレットなど）があるとレッスンがよりスムーズです。川崎近郊の方は対面レッスンも可能です。"),
 "withkids": ("子どもが横にいても受講できますか？","もちろんです！私自身が2人の娘を持つ現役ママなので、お子さんがいる環境は大歓迎。途中でお子さんが来てしまっても全く問題ありません。"),
 "kids": ("何歳から受けられますか？","3歳から受け付けています。小さいお子さんは25分レッスンがおすすめです。歌だけでなく、演技・表現力・オーディションの書類や動画まで総合的に見ます。"),
 "parent": ("親はレッスンに同席できますか？","はい、同席大歓迎です。おうちでの練習の見方もお伝えするので、むしろ一緒に聞いていただくのがおすすめです。"),
 "audition": ("オーディションの紹介はしてもらえますか？","レッスンを継続している生徒さんで、準備が整っていると判断した場合には、オーディション情報の紹介やマネージメントのサポートも行っています。まずはご相談ください。"),
 "cancel": ("キャンセルはいつまでできますか？","レッスンの2日前までのご連絡であれば無料でキャンセル・変更できます。前日のキャンセルはレッスン料の50%、当日キャンセルは100%をいただいております。お子さんの急な体調不良など、事前にご連絡いただければ柔軟に対応します。"),
}
T_AM = ("🌸","歌い方に限界を感じていたところ、翔子先生のレッスンで全然違うアプローチを知り衝撃でした。理由がわかると身体が変わる感覚があります。","A.Mさん（20代・会社員）","ボイストレーニング受講中")
T_KT = ("🌿","子育て中でも夜に受けられるオンラインが最高。ママ同士だから話しやすいし、子どもが横に来ても全然OK。夢を諦めなくていいんだと思えます。","K.Tさん（30代・2児のママ）","ミュージカル曲レッスン受講中")
T_RI = ("⭐","子どものオーディション対策をお願いしました。書類の書き方から当日の心構えまで丁寧にサポートしていただき、無事合格できました！","R.Iさん（お子様の保護者）","子役オーディション対策")

# ---------- index ----------
def build_index():
    hero = f'''<section class="hero portal" id="top">
  <div class="hero-inner">
    <div class="hero-text">
      <div class="hero-badge">🎭 元ミュージカル俳優 × 音声学ベースのボイストレーナー</div>
      <h1>帝劇の舞台から、<br>「声の<em>仕組み</em>」を教える人へ。</h1>
      <p class="hero-tagline">オーディションに100回以上落ちて、それでも帝劇に立った。<br>その経験と音声学で、<strong>「なんとなく」ではなく「理由がわかる」</strong>声づくりを。</p>
      <div class="hero-stats">
        <span>🎬 東宝『SPY×FAMILY』子役歌唱指導</span>
        <span>🌟 劇団四季・アニー 合格者多数</span>
        <span>🏛 帝国劇場ほか 商業ミュージカル出演</span>
      </div>
    </div>
    <div class="hero-visual">{part("hero_visual.html")}</div>
  </div>
</section>
<section id="doors">
  <div class="doors-wrap">
    <h2 class="section-title" style="text-align:center;">あなたは<em>どちら？</em></h2>
    <p class="section-sub" style="text-align:center;margin:0 auto;">目的に合わせて、ページを分けています。扉を選んでください。</p>
    <div class="doors-grid">
      <a href="kids.html" class="door kids">
        <div class="door-icon">🌟</div>
        <div class="door-who">保護者の方へ</div>
        <h3>子役・ミュージカルを<br>目指すお子さん</h3>
        <p>3歳〜中学生。歌・演技・オーディション対策。四季・アニーなど合格実績多数。</p>
        <span class="door-cta">子ども向けページへ →</span>
      </a>
      <a href="adults.html" class="door adult">
        <div class="door-icon">🎤</div>
        <div class="door-who">ご本人へ</div>
        <h3>歌・話し声を<br>変えたい大人の方</h3>
        <p>趣味からプロ志望まで。音声学で「なぜ出ないか」を解き、発声を根本から変える。</p>
        <span class="door-cta">大人向けページへ →</span>
      </a>
      <a href="business.html" class="door biz">
        <div class="door-icon">🏢</div>
        <div class="door-who">企業・団体のご担当者へ</div>
        <h3>社員の「伝わる声」を<br>つくりたい</h3>
        <p>営業・接客の話し方研修、管理職のプレゼン指導、講師のボイスケア。</p>
        <span class="door-cta">企業向けページへ →</span>
      </a>
    </div>
  </div>
</section>
'''
    return (head("VoiceGrace | 酒井翔子 ボイストレーニング・ミュージカルレッスン",
                 "元ミュージカル俳優・音声学ベースのボイストレーナー酒井翔子。子役・大人・企業研修。川崎／オンライン。")
            + ANNOUNCE + nav("index.html") + hero + part("about.html") + part("blog.html") + footer())

# ---------- kids ----------
def build_kids():
    body = page_head("For Kids & Parents", "子役・ミュージカルを<br>目指す<em>お子さん</em>へ",
        "3歳〜中学生。歌・演技・表現力・オーディション対策を、音声学とプロの現場経験で。劇団四季・アニーなど合格実績多数。")
    body += f'''<section id="why" class="soft">
  <div class="section-inner">
    <div class="section-label">Why</div>
    <h2 class="section-title">なぜ<em>受かる子</em>が育つのか</h2>
    <div class="why-grid">
      <div class="why-card"><div class="why-icon">🎬</div><h3>審査する側を知っている</h3><p>東宝ミュージカル『SPY×FAMILY』の子役歌唱指導を担当。オーディションで「何を見られているか」を現場目線でお伝えします。</p></div>
      <div class="why-card"><div class="why-icon">🔬</div><h3>「それっぽい」で終わらせない</h3><p>音声学ベースの指導で、高い声が出ない・声が細い理由を仕組みから解決。モノマネではなく、その子の良さが出る声に。</p></div>
      <div class="why-card"><div class="why-icon">🧒</div><h3>私も元子役・2児の母</h3><p>4歳から舞台に立ち、100回以上オーディションに落ちてきました。落ちた日の親子の過ごし方まで一緒に考えます。</p></div>
    </div>
  </div>
</section>
<section id="lessons">
  <div class="section-inner">
    <div class="section-label">Lessons</div>
    <h2 class="section-title">レッスン内容・<em>料金</em></h2>
    <p class="section-sub">基本オンライン（Zoom）、川崎近郊の方は対面も可能です。保護者の方の同席歓迎。</p>
    <div class="lessons-grid two">
      <div class="lesson-card green">
        <div class="lesson-badge">合格実績あり</div>
        <div class="lesson-icon">🌟</div>
        <h3>子役・ジュニアレッスン</h3>
        <p>3歳〜中学生対象。歌・演技・表現力を総合的に指導。おうちでの練習の見方も保護者の方にお伝えします。優秀な生徒へはオーディション紹介やマネージメントサポートも。</p>
        <div class="lesson-price">¥4,500<span> / 25分　</span>¥9,000<span> / 50分</span></div>
      </div>
      <div class="lesson-card yellow">
        <div class="lesson-badge">書類・動画・本番</div>
        <div class="lesson-icon">⭐</div>
        <h3>オーディション対策</h3>
        <p>楽曲選び・書類の書き方・動画の撮り方から当日の心構えまで一貫サポート。劇団四季・アニー・ミュージカル子役の公募に対応。</p>
        <div class="lesson-price">¥4,500<span> / 25分　</span>¥9,000<span> / 50分</span></div>
      </div>
    </div>
    <div class="ticket"><div class="ticket-label">10回券</div><div class="ticket-price">¥100,000</div><div class="ticket-sub">50分レッスン×10回　有効期限6ヶ月</div></div>
    {line_box("💬 まずはLINEで気軽にご相談ください", "「うちの子に合う？」「オーディションの準備は何から？」など、保護者の方からの相談を受け付けています。オーディション情報やnoteの更新もLINEでお知らせします。", "LINEで相談する")}
  </div>
</section>
'''
    body += testimonials([T_RI, T_KT])
    body += faq([FAQ["kids"], FAQ["parent"], FAQ["audition"], FAQ["online"], FAQ["cancel"]])
    body += booking([("子役・ジュニアレッスン","子役・ジュニア","3歳〜中学生","¥4,500/25分・¥9,000/50分"),
                     ("オーディション対策（子ども）","オーディション対策","書類・動画・本番","¥4,500/25分・¥9,000/50分")],
                    "お子さんのお名前と年齢を「ご要望」欄にご記入ください🌸")
    return head("子役・ジュニアレッスン | VoiceGrace 酒井翔子", "子役・ミュージカルを目指すお子さんのレッスン。四季・アニー合格実績。川崎／オンライン。") + nav("kids.html") + body + footer()

# ---------- adults ----------
def build_adults():
    body = page_head("For Adults", "歌・話し声を変えたい<br><em>大人の方</em>へ",
        "趣味でもっと上手く歌いたい方から、プロ・オーディションを目指す方、プレゼンや声枯れに悩む方まで。音声学で「なぜ出ないか」を解き、根本から変えます。")
    body += f'''<section id="lessons">
  <div class="section-inner">
    <div class="section-label">Lessons</div>
    <h2 class="section-title">レッスン内容・<em>料金</em></h2>
    <p class="section-sub">基本オンライン（Zoom）、川崎近郊の方は対面も可能です。子育て中の方・お子さんが横にいる環境も歓迎。</p>
    <div class="lessons-grid">
      <div class="lesson-card coral">
        <div class="lesson-badge">人気 No.1</div>
        <div class="lesson-icon">🎙️</div>
        <h3>ボイストレーニング</h3>
        <p>Voice Professionalsメソッドをベースに音声学的アプローチで発声改善。歌・話し声どちらも対応。セミナーやプレゼンで声枯れが気になる方にも。</p>
        <div class="lesson-price">¥5,500<span> / 25分　</span>¥11,000<span> / 50分</span></div>
        <p class="lesson-note">※<a href="https://note.com/shkski1102" target="_blank">noteをご購入</a>の方は初回特別価格あり</p>
      </div>
      <div class="lesson-card yellow">
        <div class="lesson-badge">元ミュージカル俳優</div>
        <div class="lesson-icon">⭐</div>
        <h3>オーディション対策</h3>
        <p>オーディションで苦戦中の方へ。何が足りないか・取り組み方を、100回以上落ちて帝劇に立った経験から。楽曲選びから書類・動画・本番対策まで。</p>
        <div class="lesson-price">¥5,500<span> / 25分　</span>¥11,000<span> / 50分</span></div>
      </div>
      <div class="lesson-card purple">
        <div class="lesson-icon">💬</div>
        <h3>LINEサポート</h3>
        <p>動画添削・質問し放題の月額サポート。レッスンとレッスンの間も成長を止めない。</p>
        <div class="lesson-price">¥15,000<span> / 月（単品）</span></div>
        <p class="lesson-note">レッスン受講者は¥10,000/月</p>
      </div>
    </div>
    <div class="ticket"><div class="ticket-label">10回券</div><div class="ticket-price">¥100,000</div><div class="ticket-sub">50分レッスン×10回　有効期限6ヶ月</div></div>
    {line_box("💬 どのコースが合うか迷ったら", "LINEで気軽に聞いてください。今の悩みを教えてもらえれば、合う進め方を提案します。")}
  </div>
</section>
'''
    body += testimonials([T_AM, T_KT])
    body += faq([FAQ["beginner"], FAQ["online"], FAQ["withkids"], FAQ["cancel"]])
    body += booking([("ボイストレーニング","ボイストレーニング","歌・話し声","¥5,500/25分・¥11,000/50分"),
                     ("オーディション対策（大人）","オーディション対策","書類・動画・本番","¥5,500/25分・¥11,000/50分"),
                     ("LINEサポート","LINEサポート","動画添削・質問し放題","¥10,000〜/月")],
                    "まずはお気軽にご予約ください🌸")
    return head("大人のボイストレーニング | VoiceGrace 酒井翔子", "歌・話し声・オーディション対策。音声学ベースのボイストレーニング。川崎／オンライン。") + nav("adults.html") + body + footer()

# ---------- business ----------
def build_business():
    body = page_head("For Business", "企業・団体向け<em>研修</em>",
        "舞台で培った「届く声・伝わる話し方」を、仕事の現場へ。音声学に基づくので、感覚論ではなく再現できる形でお伝えします。")
    body += part("business_body.html")
    body += faq([("対面とオンライン、どちらも可能ですか？","どちらも対応しています。対面は川崎・都内近郊、オンラインはZoomで全国対応。ハイブリッドも可能です。"),
                 ("料金の目安は？","内容・人数・時間によってお見積りします。まずはお問い合わせフォームから、ご希望の内容と規模をお知らせください。"),
                 ("講師はどんな人ですか？","酒井翔子。帝国劇場をはじめ商業ミュージカルに出演後、音声学ベースの指導者に。Voice Professionals認定コーチ、東宝ミュージカル『SPY×FAMILY』子役歌唱指導。詳しくは<a href='index.html#about'>講師について</a>。")])
    return head("企業・団体向け研修 | VoiceGrace 酒井翔子", "営業・接客の話し方研修、管理職プレゼン指導、講師のボイスケア。元ミュージカル俳優×音声学。") + nav("business.html") + body + footer()

for name, fn in [("index.html",build_index),("kids.html",build_kids),("adults.html",build_adults),("business.html",build_business)]:
    with open(os.path.join(OUT,name),"w",encoding="utf-8") as f: f.write(fn())
    print("built", name)
