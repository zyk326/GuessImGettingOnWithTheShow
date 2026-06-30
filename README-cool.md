<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Getting On With The Show</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@300;500;700&family=DM+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet">
<style>
  /* ========================================
     ROOT & TOKENS
     ======================================== */
  :root {
    --bg-deep: #0a0b0f;
    --bg-surface: #111318;
    --bg-card: #16181f;
    --bg-card-hover: #1c1f28;
    --border-subtle: rgba(255,255,255,0.04);
    --border-hover: rgba(255,255,255,0.1);
    --text-primary: #e8e6e1;
    --text-secondary: #8a8780;
    --text-muted: #4e4c48;

    /* Section accent colors */
    --blue: #5E8EC6;
    --green: #6DA55E;
    --teal: #6B9E8A;
    --coral: #F0A3A0;
    --peach: #F7B38C;
    --gold: #C0A36E;
    --mint: #6CC4B0;

    --font-display: 'Playfair Display', 'Noto Serif SC', serif;
    --font-body: 'Crimson Pro', 'Noto Serif SC', serif;
    --font-mono: 'DM Mono', monospace;
  }

  /* ========================================
     RESET & BASE
     ======================================== */
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  html {
    scroll-behavior: smooth;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.08) transparent;
  }

  body {
    background: var(--bg-deep);
    color: var(--text-primary);
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
  }

  /* Grain overlay */
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
    background-size: 128px 128px;
    opacity: 0.025;
    pointer-events: none;
    z-index: 9999;
  }

  ::selection {
    background: rgba(94,142,198,0.25);
    color: #fff;
  }

  a { color: inherit; text-decoration: none; }

  /* ========================================
     HERO SECTION
     ======================================== */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow: hidden;
  }

  /* Animated gradient mesh background */
  .hero::before {
    content: '';
    position: absolute;
    inset: -50%;
    background:
      radial-gradient(ellipse 600px 400px at 20% 30%, rgba(94,142,198,0.08) 0%, transparent 70%),
      radial-gradient(ellipse 500px 500px at 75% 60%, rgba(107,158,138,0.06) 0%, transparent 70%),
      radial-gradient(ellipse 400px 300px at 50% 80%, rgba(192,163,110,0.04) 0%, transparent 70%);
    animation: meshDrift 20s ease-in-out infinite alternate;
    z-index: 0;
  }

  @keyframes meshDrift {
    0%   { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(-40px, 30px) rotate(2deg); }
  }

  .hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 800px;
  }

  .hero-label {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 2rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 0.2s;
  }

  .hero-title {
    font-family: var(--font-display);
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 0.5s;
  }

  .hero-title em {
    font-style: italic;
    background: linear-gradient(135deg, var(--blue), var(--teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Typing line */
  .typing-wrap {
    height: 2.4rem;
    margin-bottom: 2.5rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 0.8s;
  }

  .typing-text {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    color: var(--blue);
    letter-spacing: 0.02em;
  }

  .typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1.1em;
    background: var(--blue);
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blink 1s steps(1) infinite;
  }

  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }

  /* Hero tagline */
  .hero-desc {
    font-family: var(--font-body);
    font-size: 1.05rem;
    color: var(--text-secondary);
    font-weight: 300;
    line-height: 1.8;
    margin-bottom: 2.5rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 1s;
  }

  /* Classic mode pill button */
  .pill-btn {
    display: inline-block;
    padding: 0.5rem 1.6rem;
    border: 1px solid var(--border-hover);
    border-radius: 100px;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.3, 1.2);
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 1.2s;
  }

  .pill-btn:hover {
    color: var(--text-primary);
    border-color: var(--blue);
    background: rgba(94,142,198,0.06);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(94,142,198,0.08);
  }

  /* Scroll indicator */
  .scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 1.6s;
  }

  .scroll-hint span {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .scroll-line {
    width: 1px;
    height: 40px;
    background: linear-gradient(to bottom, var(--text-muted), transparent);
    animation: scrollPulse 2s ease-in-out infinite;
  }

  @keyframes scrollPulse {
    0%, 100% { opacity: 0.3; transform: scaleY(0.6); transform-origin: top; }
    50% { opacity: 1; transform: scaleY(1); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ========================================
     MAIN CONTENT
     ======================================== */
  .main-content {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2rem 6rem;
  }

  /* Section spacing */
  .section {
    margin-bottom: 4rem;
  }

  .section-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 1.6rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .section-index {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    min-width: 2rem;
  }

  .section-title {
    font-family: var(--font-display);
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 0.02em;
  }

  .section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border-subtle), transparent);
  }

  /* Card grid */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 0.9rem;
  }

  .card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 1rem 1.2rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.2, 0.8, 0.3, 1.1);
    overflow: hidden;
  }

  /* Colored left accent bar */
  .card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 10px 0 0 10px;
    opacity: 0.6;
    transition: opacity 0.3s ease, width 0.3s ease;
  }

  .card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-hover);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
  }

  .card:hover::before {
    opacity: 1;
    width: 4px;
  }

  .card-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    flex-shrink: 0;
    transition: transform 0.3s ease;
  }

  .card:hover .card-icon {
    transform: scale(1.1);
  }

  .card-info { min-width: 0; }

  .card-name {
    font-family: var(--font-body);
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.15rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .card-sub {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.02em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Color variants */
  .card[data-color="blue"]::before { background: var(--blue); }
  .card[data-color="blue"] .card-icon { background: rgba(94,142,198,0.12); color: var(--blue); }
  .card[data-color="blue"]:hover { border-color: rgba(94,142,198,0.2); }

  .card[data-color="green"]::before { background: var(--green); }
  .card[data-color="green"] .card-icon { background: rgba(109,165,94,0.12); color: var(--green); }
  .card[data-color="green"]:hover { border-color: rgba(109,165,94,0.2); }

  .card[data-color="teal"]::before { background: var(--teal); }
  .card[data-color="teal"] .card-icon { background: rgba(107,158,138,0.12); color: var(--teal); }
  .card[data-color="teal"]:hover { border-color: rgba(107,158,138,0.2); }

  .card[data-color="coral"]::before { background: var(--coral); }
  .card[data-color="coral"] .card-icon { background: rgba(240,163,160,0.12); color: var(--coral); }
  .card[data-color="coral"]:hover { border-color: rgba(240,163,160,0.2); }

  .card[data-color="peach"]::before { background: var(--peach); }
  .card[data-color="peach"] .card-icon { background: rgba(247,179,140,0.12); color: var(--peach); }
  .card[data-color="peach"]:hover { border-color: rgba(247,179,140,0.2); }

  .card[data-color="gold"]::before { background: var(--gold); }
  .card[data-color="gold"] .card-icon { background: rgba(192,163,110,0.12); color: var(--gold); }
  .card[data-color="gold"]:hover { border-color: rgba(192,163,110,0.2); }

  .card[data-color="mint"]::before { background: var(--mint); }
  .card[data-color="mint"] .card-icon { background: rgba(108,196,176,0.12); color: var(--mint); }
  .card[data-color="mint"]:hover { border-color: rgba(108,196,176,0.2); }

  /* ========================================
     FOOTER
     ======================================== */
  .site-footer {
    text-align: center;
    padding: 4rem 2rem 3rem;
    position: relative;
  }

  .site-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--border-subtle), transparent);
  }

  .footer-wave {
    display: flex;
    justify-content: center;
    gap: 3px;
    margin-bottom: 1.5rem;
    animation: gentleFloat 6s ease-in-out infinite;
  }

  .footer-wave span {
    display: block;
    width: 3px;
    height: 16px;
    border-radius: 3px;
    opacity: 0.5;
  }

  .footer-wave span:nth-child(1) { background: var(--blue); animation: waveBar 2s ease-in-out infinite 0s; }
  .footer-wave span:nth-child(2) { background: var(--teal); animation: waveBar 2s ease-in-out infinite 0.1s; }
  .footer-wave span:nth-child(3) { background: var(--green); animation: waveBar 2s ease-in-out infinite 0.2s; }
  .footer-wave span:nth-child(4) { background: var(--mint); animation: waveBar 2s ease-in-out infinite 0.3s; }
  .footer-wave span:nth-child(5) { background: var(--gold); animation: waveBar 2s ease-in-out infinite 0.4s; }
  .footer-wave span:nth-child(6) { background: var(--peach); animation: waveBar 2s ease-in-out infinite 0.5s; }
  .footer-wave span:nth-child(7) { background: var(--coral); animation: waveBar 2s ease-in-out infinite 0.6s; }

  @keyframes waveBar {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(2.2); }
  }

  @keyframes gentleFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
  }

  .footer-text {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 1rem;
    font-weight: 400;
    animation: colorBreathing 5s ease-in-out infinite;
  }

  @keyframes colorBreathing {
    0%   { color: var(--teal); }
    33%  { color: #8D9AAF; }
    66%  { color: var(--gold); }
    100% { color: var(--teal); }
  }

  /* ========================================
     SCROLL REVEAL
     ======================================== */
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .reveal.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Staggered cards */
  .card-grid .card {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease, transform 0.5s ease, background 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
  }

  .card-grid.visible .card {
    opacity: 1;
    transform: translateY(0);
  }

  .card-grid.visible .card:nth-child(1) { transition-delay: 0.05s; }
  .card-grid.visible .card:nth-child(2) { transition-delay: 0.1s; }
  .card-grid.visible .card:nth-child(3) { transition-delay: 0.15s; }
  .card-grid.visible .card:nth-child(4) { transition-delay: 0.2s; }
  .card-grid.visible .card:nth-child(5) { transition-delay: 0.25s; }
  .card-grid.visible .card:nth-child(6) { transition-delay: 0.3s; }

  /* ========================================
     RESPONSIVE
     ======================================== */
  @media (max-width: 640px) {
    .main-content { padding: 0 1.2rem 4rem; }
    .card-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 2rem; }
    .section-header { flex-wrap: wrap; }
  }
</style>
</head>
<body>

<!-- ============ HERO ============ -->
<section class="hero">
  <div class="hero-content">
    <p class="hero-label">Learning &middot; Coding &middot; Creating</p>
    <h1 class="hero-title">Guess I'm Getting On<br>With <em>The Show</em></h1>
    <div class="typing-wrap">
      <span class="typing-text" id="typingTarget"></span><span class="typing-cursor"></span>
    </div>
    <p class="hero-desc">
      机器学习 &middot; 算法工程师 &middot; C++ &amp; PyTorch<br>
      摄影师 &middot; 音乐制作 &middot; 永远在路上
    </p>
    <a href="./README-simple.html" class="pill-btn">&larr; 经典模式</a>
  </div>
  <div class="scroll-hint">
    <span>Scroll</span>
    <div class="scroll-line"></div>
  </div>
</section>

<!-- ============ MAIN ============ -->
<main class="main-content">

  <!-- 01 人工智能 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">01</span>
      <h2 class="section-title">人工智能 · 深度学习</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="blue" href="./Learning/ML.html">
        <div class="card-icon">&#x1F9E0;</div>
        <div class="card-info">
          <div class="card-name">机器学习</div>
          <div class="card-sub">基石与实战</div>
        </div>
      </a>
      <a class="card" data-color="blue" href="./Learning/DL.html">
        <div class="card-icon">&#x1F4CA;</div>
        <div class="card-info">
          <div class="card-name">深度学习</div>
          <div class="card-sub">神经网络前沿</div>
        </div>
      </a>
      <a class="card" data-color="blue" href="./Learning/PyT.html">
        <div class="card-icon">&#x1F525;</div>
        <div class="card-info">
          <div class="card-name">PyTorch</div>
          <div class="card-sub">入门与动态图</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 02 编程 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">02</span>
      <h2 class="section-title">编程 · 全栈修炼</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="green" href="./Learning/Python_Code.html">
        <div class="card-icon">&#x1F40D;</div>
        <div class="card-info">
          <div class="card-name">Python</div>
          <div class="card-sub">进阶之路</div>
        </div>
      </a>
      <a class="card" data-color="green" href="./Learning/WorkingLikeNiuma.html">
        <div class="card-icon">&#x2699;</div>
        <div class="card-info">
          <div class="card-name">C++</div>
          <div class="card-sub">进阶 · 性能之巅</div>
        </div>
      </a>
      <a class="card" data-color="green" href="./Learning/Search.html">
        <div class="card-icon">&#x1F50D;</div>
        <div class="card-info">
          <div class="card-name">搜索技术</div>
          <div class="card-sub">变强的外挂</div>
        </div>
      </a>
      <a class="card" data-color="green" href="./Learning/Anomalib.html">
        <div class="card-icon">&#x1F4E1;</div>
        <div class="card-info">
          <div class="card-name">Anomalib</div>
          <div class="card-sub">异常检测实战</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 03 研究生 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">03</span>
      <h2 class="section-title">研究生 · 学术引擎</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="teal" href="./Learning/PostGraduate/Experimental_part.html">
        <div class="card-icon">&#x1F52C;</div>
        <div class="card-info">
          <div class="card-name">实验设计</div>
          <div class="card-sub">科学逻辑闭环</div>
        </div>
      </a>
      <a class="card" data-color="teal" href="./Learning/PostGraduate/Essay_notes.html">
        <div class="card-icon">&#x1F4D6;</div>
        <div class="card-info">
          <div class="card-name">论文笔记</div>
          <div class="card-sub">文献拆解与重构</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 04 认知就业 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">04</span>
      <h2 class="section-title">认知就业 · 算法工程师之路</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="coral" href="./Learning/KAW.html">
        <div class="card-icon">&#x1F4AD;</div>
        <div class="card-info">
          <div class="card-name">认知与就业</div>
          <div class="card-sub">职业破局思考</div>
        </div>
      </a>
      <a class="card" data-color="coral" href="./Learning/Working.html">
        <div class="card-icon">&#x1F4BB;</div>
        <div class="card-info">
          <div class="card-name">真的就业了</div>
          <div class="card-sub">算法工程师实战</div>
        </div>
      </a>
      <a class="card" data-color="coral" href="./Learning/Maobing.html">
        <div class="card-icon">&#x1F41B;</div>
        <div class="card-info">
          <div class="card-name">疑难杂症</div>
          <div class="card-sub">职场排雷手册</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 05 影音 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">05</span>
      <h2 class="section-title">影音 · 创造与漫游</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="peach" href="./Learning/Movie_History.html">
        <div class="card-icon">&#x1F3AC;</div>
        <div class="card-info">
          <div class="card-name">电影历史</div>
          <div class="card-sub">百年光影叙事</div>
        </div>
      </a>
      <a class="card" data-color="peach" href="./Learning/Cubase.html">
        <div class="card-icon">&#x1F3B5;</div>
        <div class="card-info">
          <div class="card-name">Cubase</div>
          <div class="card-sub">进化为编曲人</div>
        </div>
      </a>
      <a class="card" data-color="peach" href="./Learning/Camerist.html">
        <div class="card-icon">&#x1F4F7;</div>
        <div class="card-info">
          <div class="card-name">摄影师成长计划</div>
          <div class="card-sub">光影美学</div>
        </div>
      </a>
      <a class="card" data-color="peach" href="./Learning/OutPlay.html">
        <div class="card-icon">&#x2708;</div>
        <div class="card-info">
          <div class="card-name">粗去玩</div>
          <div class="card-sub">行迹与漫游灵感</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 06 历史 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">06</span>
      <h2 class="section-title">历史 · 博弈与智识</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="gold" href="./Learning/Hidden_rules.html">
        <div class="card-icon">&#x1F4DC;</div>
        <div class="card-info">
          <div class="card-name">潜规则</div>
          <div class="card-sub">中国历史上的真实游戏</div>
        </div>
      </a>
      <a class="card" data-color="gold" href="./Learning/Those_Happenings_of_the_Ming_Dynasty.html">
        <div class="card-icon">&#x1F3DB;</div>
        <div class="card-info">
          <div class="card-name">明朝那些事儿</div>
          <div class="card-sub">Those Happenings</div>
        </div>
      </a>
    </div>
  </section>

  <!-- 07 自我 -->
  <section class="section reveal">
    <div class="section-header">
      <span class="section-index">07</span>
      <h2 class="section-title">自我 · 语言与边界</h2>
      <div class="section-line"></div>
    </div>
    <div class="card-grid">
      <a class="card" data-color="mint" href="./Learning/Self.html">
        <div class="card-icon">&#x1F4AC;</div>
        <div class="card-info">
          <div class="card-name">我能这么说吗</div>
          <div class="card-sub">表达与觉察</div>
        </div>
      </a>
    </div>
  </section>

</main>

<!-- ============ FOOTER ============ -->
<footer class="site-footer">
  <div class="footer-wave">
    <span></span><span></span><span></span><span></span><span></span><span></span><span></span>
  </div>
  <p class="footer-text">愿平静的力量长盛不息</p>
</footer>

<script>
  /* ======== Typing animation ======== */
  const lines = [
    '\u{1F9E0} Machine Learning & Deep Learning',
    '\u{1F48A} Algorithm Engineer | C++ | PyTorch',
    '\u{1F4F8} Photographer | Music Producer',
    '\u2728 Always getting on with the show'
  ];

  const target = document.getElementById('typingTarget');
  let lineIdx = 0, charIdx = 0, deleting = false, pauseTimer = 0;

  function typeLoop() {
    const current = lines[lineIdx];

    if (!deleting) {
      target.textContent = current.substring(0, charIdx + 1);
      charIdx++;
      if (charIdx === current.length) {
        deleting = true;
        setTimeout(typeLoop, 1800);
        return;
      }
      setTimeout(typeLoop, 55 + Math.random() * 35);
    } else {
      target.textContent = current.substring(0, charIdx - 1);
      charIdx--;
      if (charIdx === 0) {
        deleting = false;
        lineIdx = (lineIdx + 1) % lines.length;
        setTimeout(typeLoop, 400);
        return;
      }
      setTimeout(typeLoop, 30);
    }
  }

  setTimeout(typeLoop, 1200);

  /* ======== Scroll reveal ======== */
  const observerOptions = { threshold: 0.12, rootMargin: '0px 0px -40px 0px' };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  document.querySelectorAll('.card-grid').forEach(el => observer.observe(el));
</script>

</body>
</html>