<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Getting On With The Show</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@300;500;700&family=DM+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-deep: #020408;
    --bg-surface: #080b14;
    --bg-card: rgba(12, 15, 30, 0.65);
    --bg-card-hover: rgba(20, 25, 55, 0.7);
    --border-subtle: rgba(120,140,255,0.06);
    --border-hover: rgba(120,140,255,0.18);
    --text-primary: #e4e2ef;
    --text-secondary: #8888aa;
    --text-muted: #484866;

    --blue: #6B9AE8;
    --green: #5ECC8A;
    --teal: #5EE0C8;
    --coral: #F28BA8;
    --peach: #F5A97A;
    --gold: #E8C55E;
    --mint: #5EDEC0;
    --violet: #A78BFA;
    --pink: #F472B6;
    --cyan: #67E8F9;

    --font-display: 'Playfair Display', 'Noto Serif SC', serif;
    --font-body: 'Crimson Pro', 'Noto Serif SC', serif;
    --font-mono: 'DM Mono', monospace;

    --glow-blue: rgba(107,154,232,0.35);
    --glow-violet: rgba(167,139,250,0.3);
    --glow-cyan: rgba(103,232,249,0.25);

    --gh-header-h: 200px;
  }

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  html {
    scroll-behavior: smooth;
    scrollbar-width: thin;
    scrollbar-color: rgba(120,140,255,0.12) transparent;
  }

  body {
    background: var(--bg-deep);
    color: var(--text-primary);
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    cursor: none;
    padding-top: 0;
  }

  a, button, .card, .pill-btn { cursor: none; }

  a, a:hover, a:active, a:focus, a:visited {
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
    color: inherit;
  }
  a *, a *::before, a *::after,
  a:hover *, a:active *, a:focus *, a:visited * {
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
  }
  .card, .card:hover, .card:active, .card:focus,
  .card *, .card:hover *, .card:active *, .card:focus * {
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
  }
  .pill-btn, .pill-btn:hover, .pill-btn:active, .pill-btn:focus,
  .pill-btn *, .pill-btn:hover *, .pill-btn:active * {
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
  }
  button, button:hover, button:active, button:focus {
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
  }
  ::selection {
    background: rgba(167,139,250,0.25);
    color: #fff;
    text-decoration: none !important;
    -webkit-text-decoration: none !important;
  }
  ::-moz-selection {
    background: rgba(167,139,250,0.25);
    color: #fff;
    text-decoration: none !important;
  }

  /* ===== Custom Cursor =====
     策略：left/top + CSS transition 驱动跟随
     CSS transition 引擎在合成线程运行，不阻塞主线程 JS
  */
  .cursor-dot {
    position: fixed;
    width: 6px;
    height: 6px;
    background: #fff;
    border-radius: 50%;
    pointer-events: none;
    z-index: 99999;
    box-shadow: 0 0 6px 2px rgba(255,255,255,0.6), 0 0 20px 4px var(--glow-cyan);
    /* 合成层优化 */
    will-change: left, top, width, height, background, box-shadow;
    /* 跟手过渡：0.08s 几乎零延迟感，但仍比逐帧跳变平滑 */
    transition:
      left 0.08s cubic-bezier(0.25, 0.1, 0.25, 1),
      top 0.08s cubic-bezier(0.25, 0.1, 0.25, 1),
      width 0.2s ease, height 0.2s ease,
      background 0.2s ease, box-shadow 0.2s ease;
  }

  .cursor-ring {
    position: fixed;
    width: 36px;
    height: 36px;
    border: 1.5px solid rgba(167,139,250,0.35);
    border-radius: 50%;
    pointer-events: none;
    z-index: 99998;
    will-change: left, top, width, height, border-color, background;
    transition:
      left 0.15s cubic-bezier(0.25, 0.1, 0.25, 1),
      top 0.15s cubic-bezier(0.25, 0.1, 0.25, 1),
      width 0.3s cubic-bezier(0.2, 0.8, 0.3, 1.2),
      height 0.3s cubic-bezier(0.2, 0.8, 0.3, 1.2),
      border-color 0.25s, background 0.25s;
  }

  .cursor-ring.hovering {
    width: 56px;
    height: 56px;
    border-color: rgba(103,232,249,0.5);
    background: rgba(103,232,249,0.04);
  }

  .cursor-dot.hovering {
    width: 10px;
    height: 10px;
    background: var(--cyan);
    box-shadow: 0 0 10px 4px rgba(103,232,249,0.6), 0 0 30px 8px rgba(103,232,249,0.2);
  }

  /* Grain overlay */
  body::after {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
    background-size: 128px 128px;
    opacity: 0.018;
    pointer-events: none;
    z-index: 99990;
  }

  /* ===== GALAXY CANVAS ===== */
  #galaxyCanvas {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }

  /* ===== NEBULA BLOBS ===== */
  .nebula-layer {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
  }

  .nebula-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.07;
    animation: nebulaFloat 60s ease-in-out infinite alternate;
  }

  .nebula-blob:nth-child(1) {
    width: 700px; height: 500px;
    top: -10%; left: 5%;
    background: radial-gradient(ellipse, rgba(107,154,232,0.5), transparent 70%);
    animation-delay: 0s;
  }
  .nebula-blob:nth-child(2) {
    width: 500px; height: 600px;
    top: 30%; right: -5%;
    background: radial-gradient(ellipse, rgba(167,139,250,0.4), transparent 70%);
    animation-delay: -15s;
    animation-duration: 70s;
  }
  .nebula-blob:nth-child(3) {
    width: 600px; height: 400px;
    bottom: 5%; left: 20%;
    background: radial-gradient(ellipse, rgba(103,232,249,0.25), transparent 70%);
    animation-delay: -30s;
    animation-duration: 80s;
  }

  @keyframes nebulaFloat {
    0%   { transform: translate(0, 0) scale(1); }
    33%  { transform: translate(30px, -20px) scale(1.05); }
    66%  { transform: translate(-20px, 30px) scale(0.97); }
    100% { transform: translate(15px, -15px) scale(1.02); }
  }

  /* ========================================
     HERO
     ======================================== */
  .hero {
    position: relative;
    min-height: calc(100vh + var(--gh-header-h));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: calc(var(--gh-header-h) + 1rem) 2rem 5rem;
    overflow: hidden;
    z-index: 2;
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
    font-size: clamp(2.4rem, 5.5vw, 4.2rem);
    font-weight: 700;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 0.5s;
    text-shadow: 0 0 60px rgba(167,139,250,0.15);
  }

  .hero-title em {
    font-style: italic;
    background: linear-gradient(135deg, var(--cyan), var(--violet), var(--pink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% 200%;
    animation: gradientShift 4s ease-in-out infinite;
  }

  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }

  .typing-wrap {
    height: 2.4rem;
    margin-bottom: 2.5rem;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 0.8s;
  }

  .typing-text {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    color: var(--cyan);
    letter-spacing: 0.02em;
    text-shadow: 0 0 15px var(--glow-cyan);
  }

  .typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1.1em;
    background: var(--cyan);
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blink 1s steps(1) infinite;
    box-shadow: 0 0 8px var(--glow-cyan);
  }

  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }

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

  .pill-btn {
    display: inline-block;
    padding: 0.55rem 1.8rem;
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 100px;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    backdrop-filter: blur(8px);
    background: rgba(167,139,250,0.04);
    transition: all 0.35s cubic-bezier(0.2, 0.8, 0.3, 1.2);
    opacity: 0;
    animation: fadeUp 0.8s ease forwards 1.2s;
    position: relative;
    overflow: hidden;
  }

  .pill-btn::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 100px;
    background: conic-gradient(from var(--btn-angle, 0deg), transparent 40%, var(--violet) 50%, var(--cyan) 55%, transparent 60%);
    opacity: 0;
    transition: opacity 0.4s;
    z-index: -1;
  }

  .pill-btn:hover {
    color: var(--text-primary);
    border-color: transparent;
    background: rgba(167,139,250,0.1);
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(167,139,250,0.15), 0 0 60px rgba(103,232,249,0.08);
  }

  .pill-btn:hover::before { opacity: 0.5; }

  .scroll-hint {
    position: absolute;
    bottom: 3rem;
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
    background: linear-gradient(to bottom, var(--violet), transparent);
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
    position: relative;
    z-index: 2;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2rem 6rem;
  }

  .section { margin-bottom: 4rem; }

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

  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }

  .card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 1rem 1.2rem;
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.3, 1.1);
    overflow: hidden;
  }

  .card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 12px 0 0 12px;
    opacity: 0.5;
    transition: opacity 0.3s ease, width 0.3s ease, box-shadow 0.3s ease;
  }

  .card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
  }

  .card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-hover);
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  }

  .card:hover::before { opacity: 1; width: 4px; }
  .card:hover::after { opacity: 1; }

  .card-icon {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    flex-shrink: 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .card:hover .card-icon { transform: scale(1.15); }

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
    transition: text-shadow 0.3s;
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
  .card[data-color="blue"]::before { background: var(--blue); box-shadow: 0 0 12px var(--glow-blue); }
  .card[data-color="blue"] .card-icon { background: rgba(107,154,232,0.12); color: var(--blue); }
  .card[data-color="blue"]:hover { border-color: rgba(107,154,232,0.25); }
  .card[data-color="blue"]:hover .card-icon { box-shadow: 0 0 15px rgba(107,154,232,0.3); }
  .card[data-color="blue"]:hover .card-name { text-shadow: 0 0 12px rgba(107,154,232,0.3); }
  .card[data-color="blue"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(107,154,232,0.06) 0%, transparent 70%); }

  .card[data-color="green"]::before { background: var(--green); box-shadow: 0 0 12px rgba(94,204,138,0.3); }
  .card[data-color="green"] .card-icon { background: rgba(94,204,138,0.12); color: var(--green); }
  .card[data-color="green"]:hover { border-color: rgba(94,204,138,0.2); }
  .card[data-color="green"]:hover .card-icon { box-shadow: 0 0 15px rgba(94,204,138,0.3); }
  .card[data-color="green"]:hover .card-name { text-shadow: 0 0 12px rgba(94,204,138,0.3); }
  .card[data-color="green"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(94,204,138,0.06) 0%, transparent 70%); }

  .card[data-color="teal"]::before { background: var(--teal); box-shadow: 0 0 12px rgba(94,224,200,0.3); }
  .card[data-color="teal"] .card-icon { background: rgba(94,224,200,0.12); color: var(--teal); }
  .card[data-color="teal"]:hover { border-color: rgba(94,224,200,0.2); }
  .card[data-color="teal"]:hover .card-icon { box-shadow: 0 0 15px rgba(94,224,200,0.3); }
  .card[data-color="teal"]:hover .card-name { text-shadow: 0 0 12px rgba(94,224,200,0.3); }
  .card[data-color="teal"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(94,224,200,0.06) 0%, transparent 70%); }

  .card[data-color="coral"]::before { background: var(--coral); box-shadow: 0 0 12px rgba(242,139,168,0.3); }
  .card[data-color="coral"] .card-icon { background: rgba(242,139,168,0.12); color: var(--coral); }
  .card[data-color="coral"]:hover { border-color: rgba(242,139,168,0.2); }
  .card[data-color="coral"]:hover .card-icon { box-shadow: 0 0 15px rgba(242,139,168,0.3); }
  .card[data-color="coral"]:hover .card-name { text-shadow: 0 0 12px rgba(242,139,168,0.3); }
  .card[data-color="coral"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(242,139,168,0.06) 0%, transparent 70%); }

  .card[data-color="peach"]::before { background: var(--peach); box-shadow: 0 0 12px rgba(245,169,122,0.3); }
  .card[data-color="peach"] .card-icon { background: rgba(245,169,122,0.12); color: var(--peach); }
  .card[data-color="peach"]:hover { border-color: rgba(245,169,122,0.2); }
  .card[data-color="peach"]:hover .card-icon { box-shadow: 0 0 15px rgba(245,169,122,0.3); }
  .card[data-color="peach"]:hover .card-name { text-shadow: 0 0 12px rgba(245,169,122,0.3); }
  .card[data-color="peach"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(245,169,122,0.06) 0%, transparent 70%); }

  .card[data-color="gold"]::before { background: var(--gold); box-shadow: 0 0 12px rgba(232,197,94,0.3); }
  .card[data-color="gold"] .card-icon { background: rgba(232,197,94,0.12); color: var(--gold); }
  .card[data-color="gold"]:hover { border-color: rgba(232,197,94,0.2); }
  .card[data-color="gold"]:hover .card-icon { box-shadow: 0 0 15px rgba(232,197,94,0.3); }
  .card[data-color="gold"]:hover .card-name { text-shadow: 0 0 12px rgba(232,197,94,0.3); }
  .card[data-color="gold"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(232,197,94,0.06) 0%, transparent 70%); }

  .card[data-color="mint"]::before { background: var(--mint); box-shadow: 0 0 12px rgba(94,222,192,0.3); }
  .card[data-color="mint"] .card-icon { background: rgba(94,222,192,0.12); color: var(--mint); }
  .card[data-color="mint"]:hover { border-color: rgba(94,222,192,0.2); }
  .card[data-color="mint"]:hover .card-icon { box-shadow: 0 0 15px rgba(94,222,192,0.3); }
  .card[data-color="mint"]:hover .card-name { text-shadow: 0 0 12px rgba(94,222,192,0.3); }
  .card[data-color="mint"]::after { background: radial-gradient(ellipse at 20% 50%, rgba(94,222,192,0.06) 0%, transparent 70%); }

  /* ========================================
     FOOTER
     ======================================== */
  .site-footer {
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 4rem 2rem 3rem;
  }

  .site-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(167,139,250,0.1), transparent);
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
    opacity: 0.6;
  }

  .footer-wave span:nth-child(1) { background: var(--blue); animation: waveBar 2s ease-in-out infinite 0s; box-shadow: 0 0 6px var(--glow-blue); }
  .footer-wave span:nth-child(2) { background: var(--teal); animation: waveBar 2s ease-in-out infinite 0.1s; box-shadow: 0 0 6px rgba(94,224,200,0.3); }
  .footer-wave span:nth-child(3) { background: var(--green); animation: waveBar 2s ease-in-out infinite 0.2s; box-shadow: 0 0 6px rgba(94,204,138,0.3); }
  .footer-wave span:nth-child(4) { background: var(--cyan); animation: waveBar 2s ease-in-out infinite 0.3s; box-shadow: 0 0 6px var(--glow-cyan); }
  .footer-wave span:nth-child(5) { background: var(--gold); animation: waveBar 2s ease-in-out infinite 0.4s; box-shadow: 0 0 6px rgba(232,197,94,0.3); }
  .footer-wave span:nth-child(6) { background: var(--peach); animation: waveBar 2s ease-in-out infinite 0.5s; box-shadow: 0 0 6px rgba(245,169,122,0.3); }
  .footer-wave span:nth-child(7) { background: var(--coral); animation: waveBar 2s ease-in-out infinite 0.6s; box-shadow: 0 0 6px rgba(242,139,168,0.3); }

  @keyframes waveBar {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(2.5); }
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
    animation: cosmicBreathing 6s ease-in-out infinite;
  }

  @keyframes cosmicBreathing {
    0%   { color: var(--cyan); text-shadow: 0 0 20px rgba(103,232,249,0.3); }
    33%  { color: var(--violet); text-shadow: 0 0 20px rgba(167,139,250,0.3); }
    66%  { color: var(--gold); text-shadow: 0 0 20px rgba(232,197,94,0.3); }
    100% { color: var(--cyan); text-shadow: 0 0 20px rgba(103,232,249,0.3); }
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

  .card-grid .card {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease, transform 0.5s ease, background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
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
     PLANET ORBIT
     ======================================== */
  .planet-orbit {
    position: fixed;
    bottom: -120px; right: -120px;
    width: 350px; height: 350px;
    border: 1px solid rgba(167,139,250,0.06);
    border-radius: 50%;
    animation: orbitSpin 80s linear infinite;
    pointer-events: none;
    z-index: 1;
  }

  .planet-orbit::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    width: 8px; height: 8px;
    background: var(--violet);
    border-radius: 50%;
    box-shadow: 0 0 15px 4px rgba(167,139,250,0.4);
    transform: translate(-50%, -50%);
  }

  .planet-orbit-2 {
    position: fixed;
    top: -100px; left: -100px;
    width: 280px; height: 280px;
    border: 1px solid rgba(103,232,249,0.04);
    border-radius: 50%;
    animation: orbitSpin 60s linear infinite reverse;
    pointer-events: none;
    z-index: 1;
  }

  .planet-orbit-2::before {
    content: '';
    position: absolute;
    bottom: 0; left: 50%;
    width: 5px; height: 5px;
    background: var(--cyan);
    border-radius: 50%;
    box-shadow: 0 0 12px 3px rgba(103,232,249,0.4);
    transform: translate(-50%, 50%);
  }

  @keyframes orbitSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  /* ========================================
     RESPONSIVE
     ======================================== */
  @media (max-width: 640px) {
    .main-content { padding: 0 1.2rem 4rem; }
    .card-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 2rem; }
    .section-header { flex-wrap: wrap; }
    .cursor-dot, .cursor-ring { display: none; }
    body { cursor: auto; }
    a, button, .card, .pill-btn { cursor: auto; }
  }
</style>
</head>
<body>

<!-- Custom Cursor -->
<div class="cursor-dot" id="cursorDot"></div>
<div class="cursor-ring" id="cursorRing"></div>

<!-- Galaxy Canvas -->
<canvas id="galaxyCanvas"></canvas>

<!-- Nebula Blobs -->
<div class="nebula-layer">
  <div class="nebula-blob"></div>
  <div class="nebula-blob"></div>
  <div class="nebula-blob"></div>
</div>

<!-- Orbital decoration -->
<div class="planet-orbit"></div>
<div class="planet-orbit-2"></div>

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
  /* ================================================================
     MILKY WAY — 预计算三角函数优化版
     ================================================================ */
  (function () {
    var canvas = document.getElementById('galaxyCanvas');
    var ctx = canvas.getContext('2d');
    var W, H, diag;
    var time = 0;

    var bgStars = [], armStars = [], coreStars = [];
    var dustLanes = [], nebulaClouds = [], farFieldStars = [];

    var TILT = 0.38;
    var ROT_SPEED = 0.000012;
    var VIEW_OFFSET_X = 0.48;
    var VIEW_OFFSET_Y = 0.44;
    var DRIFT_AMPLITUDE = 30;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
      diag = Math.sqrt(W * W + H * H);
      buildScene();
    }

    function buildScene() {
      bgStars = []; armStars = []; coreStars = [];
      dustLanes = []; nebulaClouds = []; farFieldStars = [];
      var i, arm, t, angle, radius, projX, projY, hue, sat, bri;
      var majorR = diag * 0.56;

      for (i = 0; i < 600; i++) {
        farFieldStars.push({
          x: Math.random() * W, y: Math.random() * H,
          r: Math.random() * 0.9 + 0.15,
          a: 0.04 + Math.random() * 0.18,
          tw: 0.001 + Math.random() * 0.008,
          ph: Math.random() * Math.PI * 2,
          hue: 200 + Math.random() * 60
        });
      }

      for (i = 0; i < 120; i++) {
        bgStars.push({
          x: Math.random() * W, y: Math.random() * H,
          r: Math.random() * 1.3 + 0.3,
          a: 0.15 + Math.random() * 0.45,
          tw: 0.002 + Math.random() * 0.012,
          ph: Math.random() * Math.PI * 2,
          hue: [30, 45, 210, 230, 340][Math.floor(Math.random() * 5)],
          sat: 20 + Math.random() * 40
        });
      }

      for (arm = 0; arm < 2; arm++) {
        var armBase = (arm / 2) * Math.PI * 2;
        var extraArm = arm === 1 ? Math.PI * 0.6 : 0;
        for (i = 0; i < 500; i++) {
          t = Math.random();
          var spiralAngle = armBase + extraArm + t * Math.PI * 3.2;
          var spread = (8 + t * 65) * (0.6 + Math.random() * 0.8);
          angle = spiralAngle + (Math.random() - 0.5) * 0.6;
          radius = t * majorR + (Math.random() - 0.5) * spread;
          if (radius < 2) continue;
          projX = Math.cos(angle) * radius;
          projY = Math.sin(angle) * radius * TILT;
          if (t < 0.08) { hue = 32 + Math.random() * 18; sat = 50 + Math.random() * 30; bri = 85 + Math.random() * 15; }
          else if (t < 0.3) { hue = Math.random() < 0.3 ? 35 + Math.random() * 10 : 210 + Math.random() * 25; sat = 35 + Math.random() * 40; bri = 75 + Math.random() * 20; }
          else { hue = 210 + Math.random() * 45; sat = 25 + Math.random() * 40; bri = 68 + Math.random() * 22; }
          armStars.push({ ox: projX, oy: projY, size: (1 - t * 0.4) * (Math.random() * 1.4 + 0.25), alpha: (1 - t * 0.5) * (0.12 + Math.random() * 0.5), hue: hue, sat: sat, bri: bri, depth: t, drift: (Math.random() - 0.5) * 0.00003 });
        }
      }

      for (arm = 0; arm < 2; arm++) {
        var armBase2 = (arm / 2) * Math.PI * 2 + Math.PI * 0.9;
        for (i = 0; i < 200; i++) {
          t = Math.random();
          angle = armBase2 + t * Math.PI * 2.8 + (Math.random() - 0.5) * 0.8;
          radius = t * majorR * 0.92 + (Math.random() - 0.5) * 40;
          if (radius < 5) continue;
          armStars.push({ ox: Math.cos(angle) * radius, oy: Math.sin(angle) * radius * TILT, size: 0.3 + Math.random() * 0.6, alpha: 0.04 + Math.random() * 0.12, hue: 220 + Math.random() * 50, sat: 30 + Math.random() * 30, bri: 60 + Math.random() * 15, depth: t, drift: (Math.random() - 0.5) * 0.00003 });
        }
      }

      for (i = 0; i < 250; i++) {
        angle = Math.random() * Math.PI * 2;
        radius = Math.pow(Math.random(), 2.2) * majorR * 0.07;
        coreStars.push({ ox: Math.cos(angle) * radius, oy: Math.sin(angle) * radius * TILT, size: Math.random() * 2.5 + 0.5, alpha: 0.2 + Math.random() * 0.6, hue: 35 + Math.random() * 20, sat: 50 + Math.random() * 40, bri: 80 + Math.random() * 20 });
      }

      for (arm = 0; arm < 2; arm++) {
        var armBase3 = (arm / 2) * Math.PI * 2 + 0.1;
        for (i = 0; i < 45; i++) {
          t = 0.15 + Math.random() * 0.7;
          angle = armBase3 + t * Math.PI * 3 + (Math.random() - 0.5) * 0.4;
          radius = t * majorR + (Math.random() - 0.5) * 50;
          dustLanes.push({ ox: Math.cos(angle) * radius, oy: Math.sin(angle) * radius * TILT, w: 30 + Math.random() * 100, h: 8 + Math.random() * 25, rot: angle + Math.random() * 0.3, alpha: 0.008 + Math.random() * 0.015, hue: [215, 240, 270, 300][Math.floor(Math.random() * 4)] });
        }
      }

      for (i = 0; i < 25; i++) {
        arm = Math.floor(Math.random() * 2);
        t = 0.2 + Math.random() * 0.6;
        angle = (arm / 2) * Math.PI * 2 + t * Math.PI * 3 + (Math.random() - 0.5) * 0.5;
        radius = t * majorR + (Math.random() - 0.5) * 40;
        nebulaClouds.push({ ox: Math.cos(angle) * radius, oy: Math.sin(angle) * radius * TILT, size: 20 + Math.random() * 70, hue: [330, 280, 210, 30][Math.floor(Math.random() * 4)], alpha: 0.012 + Math.random() * 0.025 });
      }
    }

    function draw(ts) {
      ctx.clearRect(0, 0, W, H);
      time = ts;

      var cx = W * VIEW_OFFSET_X, cy = H * VIEW_OFFSET_Y;
      var globalRot = time * ROT_SPEED;
      var driftX = Math.sin(time * 0.00004) * DRIFT_AMPLITUDE;
      var driftY = Math.cos(time * 0.00003) * DRIFT_AMPLITUDE * 0.5;
      var gcx = cx + driftX, gcy = cy + driftY;

      // 预算三角函数
      var cosGR = Math.cos(globalRot), sinGR = Math.sin(globalRot);
      var sinGR15 = sinGR * 0.15;
      var cosGR5 = Math.cos(globalRot * 0.5), sinGR5 = Math.sin(globalRot * 0.5);
      var sinGR5_15 = sinGR5 * 0.15;
      var corePulse = 1 + Math.sin(time * 0.0003) * 0.12 + Math.sin(time * 0.00007) * 0.08;

      var i, s, d, n, x, y, tw, a, g, cr1, cr2, cg1, cg2, rotA, ca, sa;

      // farFieldStars
      for (i = 0; i < farFieldStars.length; i++) {
        s = farFieldStars[i];
        tw = Math.sin(time * s.tw + s.ph) * 0.5 + 0.5;
        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, 6.2832);
        ctx.fillStyle = 'rgba(180,190,220,' + (s.a * (0.3 + tw * 0.7)).toFixed(4) + ')';
        ctx.fill();
      }

      ctx.globalCompositeOperation = 'lighter';

      // dustLanes
      for (i = 0; i < dustLanes.length; i++) {
        d = dustLanes[i];
        x = gcx + d.ox * cosGR - d.oy * sinGR;
        y = gcy + d.ox * sinGR15 + d.oy * cosGR;
        ctx.save(); ctx.translate(x, y);
        rotA = d.rot + globalRot * 0.6;
        ctx.rotate(rotA);
        g = ctx.createRadialGradient(0, 0, 0, 0, 0, d.w);
        g.addColorStop(0, 'hsla(' + d.hue + ',30%,45%,' + d.alpha + ')');
        g.addColorStop(0.5, 'hsla(' + d.hue + ',20%,35%,' + (d.alpha * 0.4) + ')');
        g.addColorStop(1, 'transparent');
        ctx.fillStyle = g;
        ctx.scale(1, d.h / d.w);
        ctx.beginPath(); ctx.arc(0, 0, d.w, 0, 6.2832); ctx.fill();
        ctx.restore();
      }

      // nebulaClouds
      for (i = 0; i < nebulaClouds.length; i++) {
        n = nebulaClouds[i];
        x = gcx + n.ox * cosGR - n.oy * sinGR;
        y = gcy + n.ox * sinGR15 + n.oy * cosGR;
        g = ctx.createRadialGradient(x, y, 0, x, y, n.size);
        g.addColorStop(0, 'hsla(' + n.hue + ',50%,55%,' + n.alpha + ')');
        g.addColorStop(0.5, 'hsla(' + n.hue + ',40%,45%,' + (n.alpha * 0.35) + ')');
        g.addColorStop(1, 'transparent');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, n.size, 0, 6.2832); ctx.fill();
      }

      // armStars
      for (i = 0; i < armStars.length; i++) {
        s = armStars[i];
        a = globalRot + s.drift * time * 0.05;
        ca = Math.cos(a); sa = Math.sin(a);
        x = gcx + s.ox * ca - s.oy * sa;
        y = gcy + s.ox * sa * 0.15 + s.oy * ca;
        ctx.beginPath(); ctx.arc(x, y, s.size, 0, 6.2832);
        ctx.fillStyle = 'hsla(' + s.hue + ',' + s.sat + '%,' + s.bri + '%,' + s.alpha + ')';
        ctx.fill();
        if (s.size > 0.9 && s.alpha > 0.3) {
          ctx.beginPath(); ctx.arc(x, y, s.size * 3, 0, 6.2832);
          ctx.fillStyle = 'hsla(' + s.hue + ',' + s.sat + '%,' + s.bri + '%,' + (s.alpha * 0.05).toFixed(4) + ')';
          ctx.fill();
        }
      }

      // coreStars
      for (i = 0; i < coreStars.length; i++) {
        s = coreStars[i];
        x = gcx + s.ox * cosGR5 - s.oy * sinGR5;
        y = gcy + s.ox * sinGR5_15 + s.oy * cosGR5;
        ctx.beginPath(); ctx.arc(x, y, s.size * corePulse, 0, 6.2832);
        ctx.fillStyle = 'hsla(' + s.hue + ',' + s.sat + '%,' + s.bri + '%,' + s.alpha + ')';
        ctx.fill();
      }

      // Core glow
      ctx.save(); ctx.translate(gcx, gcy);
      cr1 = diag * 0.06 * corePulse;
      cg1 = ctx.createRadialGradient(0, 0, 0, 0, 0, cr1);
      cg1.addColorStop(0, 'hsla(40,70%,92%,0.18)');
      cg1.addColorStop(0.25, 'hsla(35,60%,85%,0.09)');
      cg1.addColorStop(0.6, 'hsla(30,45%,70%,0.03)');
      cg1.addColorStop(1, 'transparent');
      ctx.fillStyle = cg1; ctx.scale(1, TILT);
      ctx.beginPath(); ctx.arc(0, 0, cr1, 0, 6.2832); ctx.fill();
      ctx.restore();

      ctx.save(); ctx.translate(gcx, gcy);
      cr2 = diag * 0.18 * corePulse;
      cg2 = ctx.createRadialGradient(0, 0, cr1 * 0.5, 0, 0, cr2);
      cg2.addColorStop(0, 'hsla(35,40%,70%,0.04)');
      cg2.addColorStop(0.5, 'hsla(280,30%,50%,0.015)');
      cg2.addColorStop(1, 'transparent');
      ctx.fillStyle = cg2; ctx.scale(1, TILT * 0.85);
      ctx.beginPath(); ctx.arc(0, 0, cr2, 0, 6.2832); ctx.fill();
      ctx.restore();

      ctx.globalCompositeOperation = 'source-over';

      // bgStars
      for (i = 0; i < bgStars.length; i++) {
        s = bgStars[i];
        tw = Math.sin(time * s.tw + s.ph) * 0.5 + 0.5;
        a = s.a * (0.5 + tw * 0.5);
        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, 6.2832);
        ctx.fillStyle = 'hsla(' + s.hue + ',' + s.sat + '%,85%,' + a.toFixed(4) + ')';
        ctx.fill();
        if (s.r > 1.0 && s.a > 0.4) {
          ctx.strokeStyle = 'hsla(' + s.hue + ',' + s.sat + '%,90%,' + (a * 0.3).toFixed(4) + ')';
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(s.x - s.r * 4, s.y); ctx.lineTo(s.x + s.r * 4, s.y);
          ctx.moveTo(s.x, s.y - s.r * 4); ctx.lineTo(s.x, s.y + s.r * 4);
          ctx.stroke();
        }
      }

      ctx.globalCompositeOperation = 'source-over';
      requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    requestAnimationFrame(draw);
  })();

  /* ========================================================
     CUSTOM CURSOR
     方案：left/top + CSS transition 直接驱动
     CSS transition 在合成线程运行，不阻塞主线程 JS
     ======================================================== */
  (function () {
    var dot = document.getElementById('cursorDot');
    var ring = document.getElementById('cursorRing');
    if (!dot || !ring) return;

    // 触控设备不启用
    if ('ontouchstart' in window && navigator.maxTouchPoints > 0) return;

    var visible = false;

    document.addEventListener('mousemove', function (e) {
      if (!visible) {
        dot.style.opacity = '1';
        ring.style.opacity = '1';
        visible = true;
      }
      // 光标元素固定宽高，居中偏移 = 尺寸/2
      // dot: 6px → -3, hover 10px → -5 (hover时JS会重设)
      // ring: 36px → -18, hover 56px → -28
      var isDotHovering = dot.classList.contains('hovering');
      var isRingHovering = ring.classList.contains('hovering');
      var dotOff = isDotHovering ? 5 : 3;
      var ringOff = isRingHovering ? 28 : 18;

      dot.style.left = (e.clientX - dotOff) + 'px';
      dot.style.top  = (e.clientY - dotOff) + 'px';
      ring.style.left = (e.clientX - ringOff) + 'px';
      ring.style.top  = (e.clientY - ringOff) + 'px';
    }, { passive: true });

    document.addEventListener('mouseleave', function () {
      dot.style.opacity = '0';
      ring.style.opacity = '0';
      visible = false;
    });

    document.addEventListener('mouseenter', function () {
      dot.style.opacity = '1';
      ring.style.opacity = '1';
      visible = true;
    });

    // Hover 效果
    var interactives = document.querySelectorAll('a, .card, .pill-btn, button');
    interactives.forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        dot.classList.add('hovering');
        ring.classList.add('hovering');
      });
      el.addEventListener('mouseleave', function () {
        dot.classList.remove('hovering');
        ring.classList.remove('hovering');
      });
    });
  })();

  /* ========================================================
     TYPING
     ======================================================== */
  var lines = [
    '\u{1F9E0} Machine Learning & Deep Learning',
    '\u{1F48A} Algorithm Engineer | C++ | PyTorch',
    '\u{1F4F8} Photographer | Music Producer',
    '\u2728 Always getting on with the show'
  ];

  var target = document.getElementById('typingTarget');
  var lineIdx = 0, charIdx = 0, deleting = false;

  function typeLoop() {
    var current = lines[lineIdx];
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

  /* ========================================================
     SCROLL REVEAL
     ======================================================== */
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el) { observer.observe(el); });
  document.querySelectorAll('.card-grid').forEach(function (el) { observer.observe(el); });
</script>

</body>
</html>