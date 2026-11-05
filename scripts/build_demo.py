#!/usr/bin/env python3
"""Baut die statische Demo-Site unter docs/ (GitHub-Pages-Quelle).

Erzeugt: docs/index.html, docs/<seite>/index.html, docs/assets/style.css,
docs/robots.txt, docs/.nojekyll
Inhalte stammen aus dem Mirror (mirror/) und dem Redesign-Draft.
Unbekannte Fakten sind als [PLATZHALTER: ...] markiert.
"""
import os, re, shutil, pathlib

ROOT = pathlib.Path("/data/neumayer")
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"

TEL = "+436642110825"
TEL_LABEL = "+43 664 211 08 25"
MAIL = "christian@weinbauneumayer.at"

CSS = r""":root{
  --weinrot:#6B1520; --weinrot-hell:#8C2230; --ocker:#C08A3E;
  --papier:#FAF6EF; --papier-2:#F1EADE; --ink:#1F1B17; --ink-soft:#5A5148;
  --linie:#DED4C4; --gruen:#3F5233; --radius:4px; --maxw:1200px;
  --display:"Fraunces",Georgia,"Times New Roman",serif;
  --text:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--papier);color:var(--ink);font-family:var(--text);font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--weinrot);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.12;margin:0 0 .6em;letter-spacing:-.01em}
h1{font-size:clamp(1.9rem,4.6vw,3.3rem)}
h2{font-size:clamp(1.5rem,3.2vw,2.4rem)}
h3{font-size:1.15rem}
p{margin:0 0 1.1em;color:var(--ink-soft)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.kicker{font-family:var(--text);font-size:.72rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--ocker);margin:0 0 .9em}
.note{background:#FBEAD2;color:#6B4A0F;border-left:3px solid var(--ocker);padding:12px 16px;font-size:.88rem;border-radius:0 var(--radius) var(--radius) 0;margin:22px 0}
.note strong{color:#6B4A0F}

.demo-banner{background:var(--ink);color:#EDE7DA;font-size:.8rem;text-align:center;padding:8px 16px;letter-spacing:.02em}
.demo-banner a{color:#F0CE93;text-decoration:underline}

.statusbar{background:var(--gruen);color:#EDE7DA;font-size:.85rem}
.statusbar .wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between;padding-top:9px;padding-bottom:9px}
.status{display:flex;align-items:center;gap:9px;font-weight:500}
.dot{width:9px;height:9px;border-radius:50%;background:#8FC97A;box-shadow:0 0 0 4px rgba(143,201,122,.22);flex:0 0 auto}
.statusbar a{color:#EDE7DA;text-decoration:underline;text-underline-offset:3px}

header.site{background:var(--papier);border-bottom:1px solid var(--linie);position:sticky;top:0;z-index:20}
.navrow{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px 0}
.brand{display:flex;flex-direction:column;line-height:1.1}
.brand strong{font-family:var(--display);font-weight:700;font-size:1.28rem;color:var(--weinrot)}
.brand small{font-size:.64rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-soft);margin-top:3px}
nav.main{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
nav.main a{font-size:.92rem;font-weight:500;color:var(--ink)}
nav.main a[aria-current="page"]{color:var(--weinrot);box-shadow:inset 0 -2px 0 var(--ocker)}
.navcta{display:flex;gap:10px;align-items:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:12px 22px;border-radius:var(--radius);font-size:.93rem;font-weight:600;border:1px solid transparent;cursor:pointer}
.btn-primary{background:var(--weinrot);color:#fff}
.btn-primary:hover{background:var(--weinrot-hell);text-decoration:none}
.btn-ghost{border-color:var(--linie);color:var(--ink);background:transparent}
.btn-ghost:hover{border-color:var(--ink);text-decoration:none}
.btn-white{background:#fff;color:var(--weinrot)}
.btn-white:hover{background:var(--papier-2);text-decoration:none}
.burger{display:none;min-height:44px;min-width:44px;border:1px solid var(--linie);border-radius:var(--radius);background:transparent;align-items:center;justify-content:center}

.hero{position:relative;isolation:isolate;color:#fff}
.hero img{width:100%;height:min(74vh,720px);object-fit:cover}
.hero::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(100deg,rgba(20,12,10,.88) 0%,rgba(20,12,10,.72) 32%,rgba(20,12,10,.34) 62%,rgba(20,12,10,.10) 100%)}
.hero-inner{position:absolute;inset:0;z-index:2;display:flex;align-items:center}
.hero-inner .wrap{width:100%}
.hero-copy{max-width:640px}
.hero h1{color:#fff;margin-bottom:.35em}
.hero h1 em{font-style:normal;color:#F0CE93}
.hero p{color:rgba(255,255,255,.9);font-size:1.1rem;max-width:48ch}
.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.hero-meta{display:flex;gap:26px;flex-wrap:wrap;margin-top:32px;font-size:.86rem;color:rgba(255,255,255,.82)}
.hero-meta b{display:block;font-family:var(--display);font-size:1.45rem;font-weight:600;color:#fff}

.pagehead{background:var(--papier-2);border-bottom:1px solid var(--linie);padding:52px 0 44px}
.pagehead h1{margin-bottom:.3em}
.pagehead p{max-width:62ch;margin:0;font-size:1.05rem}

section{padding:76px 0}
section.tight{padding:56px 0}
.alt{background:var(--papier-2)}
.dark{background:var(--ink);color:#EDE7DA}
.dark h2,.dark h3{color:#fff}
.dark p{color:rgba(237,231,218,.78)}
.head{max-width:660px;margin-bottom:44px}
.grid{display:grid;gap:26px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.card{background:#fff;border:1px solid var(--linie);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column}
.card img{height:200px;object-fit:cover;width:100%}
.card-body{padding:22px 24px 26px;display:flex;flex-direction:column;gap:8px;flex:1}
.card .date{font-family:var(--display);font-size:1.8rem;font-weight:700;color:var(--weinrot);line-height:1}
.card .date small{display:block;font-family:var(--text);font-size:.7rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);margin-top:7px}
.card p{font-size:.95rem;margin:0}
.box{background:#fff;border:1px solid var(--linie);border-radius:var(--radius);padding:26px 26px 22px}
.tag{display:inline-block;font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:4px 10px;border-radius:100px;background:var(--papier-2);color:var(--weinrot);width:fit-content}
.tag.warn{background:#FBEAD2;color:#8A5A12}
.usp{display:flex;gap:18px;align-items:flex-start}
.usp .num{font-family:var(--display);font-size:1.5rem;font-weight:600;color:var(--ocker);line-height:1;min-width:34px}
.usp h3{margin-bottom:.25em}
.usp p{font-size:.95rem;margin:0}
.split{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}
.split img{border-radius:var(--radius);height:100%;object-fit:cover;min-height:360px}
.wl{list-style:none;margin:0;padding:0;border-top:1px solid var(--linie)}
.wl li{display:flex;justify-content:space-between;gap:20px;padding:14px 0;border-bottom:1px solid var(--linie)}
.wl b{font-weight:600;display:block}
.wl span{color:var(--ink-soft);font-size:.9rem}
.wl i{font-family:var(--display);color:var(--ocker);font-style:normal;font-size:.9rem;white-space:nowrap}
.hours{font-variant-numeric:tabular-nums}
table.db{width:100%;border-collapse:collapse;font-size:.94rem}
table.db th,table.db td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--linie);vertical-align:top}
table.db th{font-family:var(--text);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}
form.demo{display:grid;gap:16px;max-width:560px}
label{font-size:.85rem;font-weight:600;display:block;margin-bottom:6px}
input,select,textarea{width:100%;min-height:46px;padding:11px 13px;border:1px solid var(--linie);border-radius:var(--radius);font:inherit;background:#fff;color:var(--ink)}
textarea{min-height:120px;resize:vertical}
footer.site{background:var(--ink);color:rgba(237,231,218,.72);padding:66px 0 34px;font-size:.92rem}
footer.site .cols{display:grid;grid-template-columns:1.3fr 1fr 1fr 1.1fr;gap:40px}
footer.site h4{font-family:var(--text);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:#fff;margin:0 0 16px}
footer.site a{color:rgba(237,231,218,.88)}
footer.site ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
footer.site .legal{border-top:1px solid rgba(255,255,255,.14);margin-top:44px;padding-top:20px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:.8rem}
.mobile-cta{display:none}
@media (max-width:1000px){
  nav.main{display:none}
  .burger{display:flex}
  .navcta .btn-ghost{display:none}
  .split{grid-template-columns:1fr;gap:32px}
  .g3{grid-template-columns:repeat(2,1fr)}
  footer.site .cols{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  body{font-size:16px}
  .wrap{padding:0 18px}
  section{padding:52px 0}
  .g2,.g3{grid-template-columns:1fr}
  .brand strong{font-size:1.02rem}
  .brand small{font-size:.56rem;letter-spacing:.16em}
  .navcta .btn-primary{display:none}
  .hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% center}
  .hero::after{background:linear-gradient(180deg,rgba(20,12,10,.55) 0%,rgba(20,12,10,.86) 45%,rgba(20,12,10,.94) 100%)}
  .hero-inner{position:relative;inset:auto;display:block;padding:44px 0 40px;align-items:stretch}
  .hero h1{font-size:1.95rem}
  .hero p{font-size:1rem}
  .hero-actions .btn{width:100%}
  .hero-meta{gap:16px;margin-top:22px;font-size:.8rem;flex-direction:column}
  .hero-meta b{font-size:1.2rem;display:inline;margin-right:6px}
  footer.site .cols{grid-template-columns:1fr}
  .mobile-cta{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;position:fixed;bottom:0;left:0;right:0;z-index:40;background:rgba(250,246,239,.97);border-top:1px solid var(--linie);padding:10px 12px calc(10px + env(safe-area-inset-bottom))}
  .mobile-cta .btn{padding:10px 8px;font-size:.86rem}
  body{padding-bottom:78px}
}
"""

NAV = [
    ("Termine", "termine/", "termine"),
    ("Speisen &amp; Wein", "speisen-wein/", "speisen-wein"),
    ("Ab Hof", "ab-hof/", "ab-hof"),
    ("Feiern", "feiern/", "feiern"),
    ("Besuch &amp; Kontakt", "kontakt/", "kontakt"),
]


def header(active=""):
    links = "\n".join(
        f'      <a href="{url}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for label, url, key in NAV
    )
    return f"""<div class="demo-banner">
  Designentwurf zur Ansicht — Inhalte teils Platzhalter, Bilder KI-generiert.
  <a href="design-draft/REDESIGN-DRAFT.md">Konzept lesen</a> ·
  <a href="design-draft/mockup.html">Startseiten-Mockup</a>
</div>

<div class="statusbar">
  <div class="wrap">
    <div class="status"><span class="dot"></span> Ausg'steckt: 7.–8. November (Stelzen-Wochenende)</div>
    <div>Zwischen den Terminen: Ab Hof &amp; Getränkeautomat rund um die Uhr</div>
  </div>
</div>

<header class="site">
  <div class="wrap navrow">
    <a class="brand" href="./" aria-label="Weinbau und Heuriger Neumayer, Startseite">
      <strong>Weinbau &amp; Heuriger Neumayer</strong>
      <small>Perchtoldsdorf seit 1986</small>
    </a>
    <nav class="main" aria-label="Hauptnavigation">
{links}
    </nav>
    <div class="navcta">
      <a class="btn btn-ghost" href="tel:{TEL}">0664 2110825</a>
      <a class="btn btn-primary" href="kontakt/#reservieren">Tisch reservieren</a>
      <button class="burger" aria-label="Menü öffnen">
        <svg width="20" height="14" viewBox="0 0 20 14" aria-hidden="true"><rect width="20" height="2" y="0" fill="#1F1B17"/><rect width="20" height="2" y="6" fill="#1F1B17"/><rect width="20" height="2" y="12" fill="#1F1B17"/></svg>
      </button>
    </div>
  </div>
</header>"""


FOOTER = f"""<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <h4>Weinbau &amp; Heuriger Neumayer</h4>
        <p style="color:rgba(237,231,218,.72)">Familienbetrieb in Perchtoldsdorf. Eigener Weinbau, Heuriger mit Küche, Gastgarten und Stüberl für Feiern.</p>
      </div>
      <div>
        <h4>Seiten</h4>
        <ul>
          <li><a href="termine/">Termine</a></li>
          <li><a href="speisen-wein/">Speisen &amp; Wein</a></li>
          <li><a href="ab-hof/">Ab Hof</a></li>
          <li><a href="feiern/">Feiern</a></li>
          <li><a href="kontakt/">Besuch &amp; Kontakt</a></li>
        </ul>
      </div>
      <div>
        <h4>Öffnungszeiten</h4>
        <ul class="hours">
          <li>Mo–Sa 10:30–23:00</li>
          <li>So 10:30–22:30</li>
          <li style="margin-top:8px">nur während der Aussteckzeiten</li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>
        <ul>
          <li>Sonnbergstraße 89<br>2380 Perchtoldsdorf</li>
          <li><a href="tel:{TEL}">{TEL_LABEL}</a></li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© 2026 Weinbau &amp; Heuriger Neumayer · Designentwurf</span>
      <span><a href="impressum/">Impressum</a> · <a href="datenschutz/">Datenschutz</a></span>
    </div>
  </div>
</footer>

<div class="mobile-cta" role="group" aria-label="Schnellaktionen">
  <a class="btn btn-ghost" href="tel:{TEL}">Anrufen</a>
  <a class="btn btn-primary" href="kontakt/#reservieren">Reservieren</a>
  <a class="btn btn-ghost" href="kontakt/#anfahrt">Route</a>
</div>"""


LINK_RE = re.compile(r'(href|src)="([^"]*)"')


def fix_links(html, rel):
    """Interne Links/SRCs stehen relativ zur docs-Wurzel im Quelltext; für
    Unterseiten wird der Prefix ergänzt. Externe, Anker- und bereits relative
    Ziele bleiben unverändert."""
    if not rel:
        return html

    def rep(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(#|https?:|mailto:|tel:|data:|\.\.?/)", val):
            return m.group(0)
        return f'{attr}="{rel}{val}"'

    return LINK_RE.sub(rep, html)


def page(slug, title, active, body, root=False):
    """slug: '' für Startseite, sonst Ordnername. Pfade relativ zur Datei."""
    rel = "" if root else "../"
    hdr = header(active)
    ftr = FOOTER
    html = f"""<!DOCTYPE html>
<html lang="de-AT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
{fix_links(hdr, rel)}
{fix_links(body, rel)}
{fix_links(ftr, rel)}
</body>
</html>
"""
    out = DOCS / (slug + "index.html" if slug else "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ---------------------------------------------------------------- Startseite
HOME_BODY = """
<div class="hero">
  <img src="assets/hero-terrasse.jpg" alt="Gedeckte Holztische unter Reben auf der Terrasse des Heurigen Neumayer im Abendlicht" width="2560" height="1428">
  <div class="hero-inner">
    <div class="wrap">
      <div class="hero-copy">
        <p class="kicker">Weinbau &amp; Heuriger · Perchtoldsdorf</p>
        <h1>Heuriger, wie er sein soll. <em>Seit 40 Jahren.</em></h1>
        <p>Eigener Weinkeller, Küche den ganzen Tag, Gastgarten unter den Reben und ein Blick über Wien, den man nicht vergisst. Mitten in Perchtoldsdorf.</p>
        <div class="hero-actions">
          <a class="btn btn-white" href="tel:+436642110825">Anrufen &amp; Tisch sichern</a>
          <a class="btn btn-ghost" href="termine/" style="color:#fff;border-color:rgba(255,255,255,.55)">Ausstecktermine ansehen</a>
        </div>
        <div class="hero-meta">
          <div><b class="hours">10:30–23:00</b>Montag bis Samstag</div>
          <div><b class="hours">10:30–22:30</b>Sonntag &amp; Feiertag</div>
          <div><b>24 Std.</b>Getränkeautomat im Eingang</div>
        </div>
      </div>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="head">
      <p class="kicker">Save the Date</p>
      <h2>Die nächsten Termine</h2>
      <p>Achtmal im Jahr stecken wir aus — jeweils rund drei Wochen, immer von Samstag bis Sonntag. Diese Termine sollten Sie im Kalender haben.</p>
    </div>
    <div class="grid g3">
      <article class="card">
        <img src="assets/hero-terrasse.jpg" alt="Gedeckter Tisch beim Heurigen Neumayer" loading="lazy">
        <div class="card-body">
          <span class="tag warn">Bestellung bis 5. 11.</span>
          <p class="date">07.–08.<small>November</small></p>
          <h3>Stelzen-Wochenende</h3>
          <p>Unsere legendären Stelzen — im Lokal oder zum Abholen. Senf, Kren, Krautsalat, Brot und Wein nach Wahl. Vorbestellung unbedingt erforderlich.</p>
          <p style="margin-top:auto"><a href="tel:+436642110825">Stelze bestellen: 0664 2110825</a></p>
        </div>
      </article>
      <article class="card">
        <img src="assets/kostbar.jpg" alt="Vier Weingläser mit Rotwein bei Kerzenlicht" loading="lazy">
        <div class="card-body">
          <span class="tag">Verkostung</span>
          <p class="date">KOSTBAR<small>in ROT</small></p>
          <h3>Vier Weine, ein Brett</h3>
          <p>Blauer Portugieser, Pinot Noir, Zweigelt und Zweigelt Barrique — je 80 ml, allein oder zu zweit. Unsere Art der Weinverkostung.</p>
          <p style="margin-top:auto"><a href="speisen-wein/">Zur Weinliste</a></p>
        </div>
      </article>
      <article class="card">
        <img src="assets/weinkeller.jpg" alt="Weinkeller mit Eichenfässern" loading="lazy">
        <div class="card-body">
          <span class="tag">Menüabend</span>
          <p class="date">28.<small>November</small></p>
          <h3>Engerl &amp; Bengerl</h3>
          <p>Licht aus, Kerzen an: ein besinnlicher Abend mit zwei 3-Gänge-Menüs zur Wahl. Inklusive Frizzante und Gruß aus der Küche, € 41 pro Menü.</p>
          <p style="margin-top:auto"><a href="tel:+436642110825">Reservieren: 0664 2110825</a></p>
        </div>
      </article>
    </div>
    <div class="note"><strong>Demo-Hinweis:</strong> Im fertigen Aufbau liest die Statusleiste oben einen Terminkalender (<code>termine.yaml</code>) und zeigt automatisch „heute ausg'steckt" oder den nächsten Termin. Hier ist er statisch hinterlegt. <em>[PLATZHALTER: vollständiger Terminkalender 2026/2027]</em></div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Warum Neumayer</p>
      <h2>Vier Dinge, die es woanders nicht gibt</h2>
    </div>
    <div class="grid g2" style="gap:34px 56px">
      <div class="usp"><div class="num">01</div><div>
        <h3>Fackelwanderung auf die Heide</h3>
        <p>Wir verteilen Fackeln an Ihre Gäste und wandern gemeinsam in unsere Weingärten auf die Perchtoldsdorfer Heide — rund 20 Minuten Fußweg. Oben wartet eine Erfrischung und der Blick über ganz Wien.</p>
      </div></div>
      <div class="usp"><div class="num">02</div><div>
        <h3>KOSTBAR in ROT</h3>
        <p>Vier unserer Weine, je 80 ml, auf einem Brett serviert. Die ehrlichste Art, unseren Keller kennenzulernen — ohne gleich eine Flasche kaufen zu müssen.</p>
      </div></div>
      <div class="usp"><div class="num">03</div><div>
        <h3>Wein, wann Sie wollen</h3>
        <p>Auch an Tagen ohne Ausstecken müssen Sie nicht verzichten: Unser Getränkeautomat im Eingangsbereich ist rund um die Uhr zugänglich — Wein, Traubensaft gespritzt, Traubensaft pur.</p>
      </div></div>
      <div class="usp"><div class="num">04</div><div>
        <h3>Heurigenboxen für Ihre Gäste</h3>
        <p>Das fertig angerichtete Buffet ab 5 Personen: Klassik, Mediterran, Kärnten, Käse, Brötchen — auf Wunsch individuell, mit Dessertbox.</p>
      </div></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <p class="kicker">Speisen &amp; Wein</p>
      <h2>Aus dem eigenen Keller, aus der eigenen Küche</h2>
      <p>Vom gemischten Satz über Grünen Veltliner bis zum Zweigelt Barrique: Unsere Weine wachsen auf den Hängen über Perchtoldsdorf und werden im Haus ausgebaut. Dazu kommt, was die Jahreszeit hergibt — Spargel, Wild, Stelzen, und an Werktagen ein wechselndes Tagesmenü.</p>
      <ul class="wl">
        <li><div><b>Zweigelt Barrique</b><span>Voll im Geschmack, zartes Eichenfassaroma</span></div><i>Rot</i></li>
        <li><div><b>Grüner Veltliner</b><span>Pfeffrig, würzige Frucht, jugendlich-frische Säure</span></div><i>Weiß</i></li>
        <li><div><b>Blauer Portugieser</b><span>Weich und mild, samtige Tannine</span></div><i>Rot</i></li>
        <li><div><b>Gelber Muskateller</b><span>Blumige Aromen, Duft nach Muskat</span></div><i>Weiß</i></li>
      </ul>
      <p style="margin-top:24px"><a class="btn btn-primary" href="speisen-wein/">Komplette Weinliste &amp; Speisenkarte</a></p>
    </div>
    <img src="assets/kostbar.jpg" alt="Vier Gläser Rotwein bei Kerzenlicht auf dunklem Holz" loading="lazy">
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Feiern &amp; Seminare</p>
      <h2>Ihre Feier — auch wenn wir nicht ausgesteckt haben</h2>
      <p>Geburtstag, Hochzeit, Weihnachtsfeier oder Seminar: Wir richten Ihre Veranstaltung aus, wann und wie Sie möchten. Zwei Ebenen, ein eigenes Stüberl, im Sommer der Gastgarten.</p>
    </div>
    <div class="grid g3">
      <div><h3>Hochzeit &amp; Familie</h3><p>Menü nach Absprache, Kinderspielplatz und Spielecke für die Kleinen.</p></div>
      <div><h3>Firma &amp; Seminar</h3><p>Stüberl für Ihre Veranstaltung, Pausenbetreuung aus der Küche, Weinverkostung als Programmpunkt.</p></div>
      <div><h3>Fackelwanderung</h3><p>Das Extra, das bleibt: gemeinsame Wanderung in den Weingarten mit Wien-Blick.</p></div>
    </div>
    <p style="margin-top:36px"><a class="btn btn-white" href="feiern/">Unverbindlich anfragen</a></p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Ab Hof</p>
      <h2>Auch ohne Ausstecken versorgt</h2>
      <p>Rund 188 Tage im Jahr ist bei uns nicht ausg'steckt. Wein gibt es trotzdem — im Karton, aus dem Automaten oder als Geschenk.</p>
    </div>
    <div class="grid g3">
      <div class="box"><span class="tag">24 Stunden</span><h3>Getränkeautomat</h3><p>Im Eingangsbereich, täglich rund um die Uhr: Wein, Traubensaft gespritzt, Traubensaft pur.</p></div>
      <div class="box"><span class="tag">To go</span><h3>Spritzer TO GO</h3><p>Der klassische weiße Spritzer in der 0,33-l-Glasflasche mit Drehverschluss — recycelbar.</p></div>
      <div class="box"><span class="tag">Geschenk</span><h3>Geschenkebox</h3><p>Holzbox mit zwei Gläsern und einer Flasche Wein. <em>[PLATZHALTER: Preis bestätigen]</em></p></div>
    </div>
    <p style="margin-top:32px"><a class="btn btn-primary" href="ab-hof/">Zu Ab Hof</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="kicker">Reservierung</p>
      <h2>In drei Schritten zum Tisch</h2>
      <p>Kein Formular-Dschungel: Datum, Uhrzeit, Personen — fertig. Wer lieber spricht, ruft an; wir sind unter <a href="tel:+436642110825">0664 2110825</a> für Sie da.</p>
    </div>
    <div class="grid g3">
      <div class="box"><p class="kicker" style="margin-bottom:.4em">Schritt 1</p><h3>Wann?</h3><p>Kalender mit den Aussteckterminen — nur an Tagen, an denen wir ausgesteckt haben, ist eine Reservierung möglich.</p></div>
      <div class="box"><p class="kicker" style="margin-bottom:.4em">Schritt 2</p><h3>Uhrzeit &amp; Personen</h3><p>Nur realistisch buchbare Zeiten, Personenzahl über Plus und Minus statt Dropdown. Ab 11 Personen geht es zur Feieranfrage.</p></div>
      <div class="box"><p class="kicker" style="margin-bottom:.4em">Schritt 3</p><h3>Kontakt</h3><p>Name, Telefon oder E-Mail — keine Registrierung, keine unnötigen Pflichtfelder. Bestätigung sofort.</p></div>
    </div>
    <p style="margin-top:32px"><a class="btn btn-primary" href="kontakt/#reservieren">Reservierung starten</a></p>
  </div>
</section>

<section class="alt">
  <div class="wrap split">
    <div>
      <p class="kicker">Kontakt &amp; Anfahrt</p>
      <h2>Wir freuen uns auf Ihren Besuch</h2>
      <p>
        Weinbau &amp; Heuriger Neumayer<br>
        Sonnbergstraße 89<br>
        2380 Perchtoldsdorf, Österreich
      </p>
      <p>
        Telefon <a href="tel:+436642110825">+43 664 211 08 25</a><br>
        E-Mail <a href="mailto:christian@weinbauneumayer.at">christian@weinbauneumayer.at</a><br>
        <span class="hours">Mo–Sa 10:30–23:00 · So 10:30–22:30</span>
      </p>
      <p style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn btn-primary" href="tel:+436642110825">Jetzt anrufen</a>
        <a class="btn btn-ghost" href="kontakt/#anfahrt">Route planen</a>
      </p>
    </div>
    <img src="assets/fackelwanderung.jpg" alt="Weg durch die Weingärten auf der Perchtoldsdorfer Heide im Abendlicht, im Hintergrund Wien" loading="lazy">
  </div>
</section>
"""

# ------------------------------------------------------------------- Termine
TERMINE_BODY = """
<div class="pagehead">
  <div class="wrap">
    <p class="kicker">Ausg'steckt is</p>
    <h1>Ausstecktermine</h1>
    <p>Achtmal im Jahr stecken wir aus. Die Termine werden hier künftig automatisch aus dem Kalender gelesen — inklusive Statusleiste, die auf jeder Seite sagt, ob gerade offen ist.</p>
  </div>
</div>

<section class="tight">
  <div class="wrap">
    <div class="note"><strong>Demo-Hinweis:</strong> Der vollständige Kalender 2026/2027 liegt derzeit nur als Plakat vor und ist hier noch nicht eingetragen. <em>[PLATZHALTER: Termine aus den Plakaten in <code>termine.yaml</code> übernehmen — bestätigen lassen]</em></div>

    <div class="head" style="margin-top:44px">
      <h2>Was 2026 gilt</h2>
    </div>
    <table class="db">
      <tr><th>Öffnungstage 2026</th><td>177 Tage, verteilt auf acht Zeiträume</td></tr>
      <tr><th>Muster</th><td>immer Samstag bis Sonntag, je Zeitraum rund drei Wochen</td></tr>
      <tr><th>Öffnungszeiten in diesen Zeiträumen</th><td class="hours">Montag bis Samstag 10:30–23:00<br>Sonntag 10:30–22:30</td></tr>
      <tr><th>Außerhalb der Aussteckzeiten</th><td>kein Lokalbetrieb — Ab-Hof-Verkauf nach Vereinbarung, Getränkeautomat rund um die Uhr</td></tr>
      <tr><th>Veranstaltungen außerhalb</th><td>Feiern und Seminare richten wir auf Wunsch außerhalb der Aussteckzeiten aus</td></tr>
    </table>
    <div class="note">Die Angaben stammen aus den beiden Plakatgrafiken im Spiegel der bestehenden Website (<code>ausstecken26</code>, <code>ausstecken27</code>). Auf der bestehenden Seite steht dagegen „bis zu zehn mal im Jahr geöffnet" — bitte bestätigen, was stimmt.</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Save the Date</p>
      <h2>Bekannte Termine</h2>
    </div>
    <div class="grid g2">
      <div class="box">
        <span class="tag warn">Bestellung bis Donnerstag, 5. 11.</span>
        <h3>Stelzen-Wochenende · 7. &amp; 8. November</h3>
        <p>Unsere legendären Stelzen, im Lokal oder zum Abholen. Dazu Senf, Kren, Krautsalat, Brot und Wein nach Wahl. Stelzen müssen vorbestellt werden.</p>
        <p><a class="btn btn-primary" href="tel:+436642110825">Stelze bestellen</a></p>
      </div>
      <div class="box">
        <span class="tag">Menüabend</span>
        <h3>Engerl &amp; Bengerl · 28. November</h3>
        <p>Ein besinnlicher Abend bei Kerzenschein mit leiser Musik. Zwei 3-Gänge-Menüs zur Wahl, je inklusive einem Glas Frizzante und einem Gruß aus der Küche. € 41 pro Menü.</p>
        <p><a class="btn btn-primary" href="tel:+436642110825">Reservieren: 0664 2110825</a></p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <p class="kicker">Zwischen den Terminen</p>
      <h2>Nicht ausg'steckt heißt nicht geschlossen für Sie</h2>
      <p>Rund 188 Tage im Jahr ist kein Heurigenbetrieb. Genau dafür gibt es unsere Ab-Hof-Angebote: Wein im Karton, Spritzer TO GO und den Getränkeautomaten, der täglich rund um die Uhr zugänglich ist. Feiern richten wir ohnehin nach Ihrem Wunschtermin aus.</p>
      <p><a class="btn btn-primary" href="ab-hof/">Zu Ab Hof</a></p>
    </div>
    <img src="assets/weinkeller.jpg" alt="Weinkeller mit alten Eichenfässern" loading="lazy">
  </div>
</section>
"""

# ------------------------------------------------------------ Speisen & Wein
SPEISEN_BODY = """
<div class="pagehead">
  <div class="wrap">
    <p class="kicker">Küche &amp; Keller</p>
    <h1>Speisen &amp; Wein</h1>
    <p>Frisch zubereitete Speisen zu jeder Tageszeit, saisonale Schmankerl und der passende Wein aus dem hauseigenen Weinkeller — dazu an Werktagen ein wechselndes Tagesmenü.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="head">
      <p class="kicker">Unsere Weine</p>
      <h2>Aus dem eigenen Weingarten</h2>
      <p>Weißwein, Heuriger, Rot- und Roséweine sowie Frizzante und Sekt. Die Verkostungsnotizen stammen von der bestehenden Seite.</p>
    </div>
    <div class="grid g2" style="gap:18px 48px">
      <div>
        <h3>Weißwein &amp; Heuriger</h3>
        <ul class="wl">
          <li><div><b>Traditionell gemischter Satz</b></div><i>Heuriger</i></li>
          <li><div><b>Grüner Veltliner</b><span>Pfeffrig im Geschmack mit würziger Frucht und jugendlich-frischer Säure</span></div><i>Weiß</i></li>
          <li><div><b>Weissburgunder</b><span>Ausgewogenes Restzucker-Säure-Verhältnis mit Apfel-Mandel-Bukett</span></div><i>Weiß</i></li>
          <li><div><b>Neuburger</b><span>Mild, gehaltvoll mit feinem Bukett</span></div><i>Weiß</i></li>
          <li><div><b>Gelber Muskateller</b><span>Blumige Aromen, Duft nach Muskat</span></div><i>Weiß</i></li>
          <li><div><b>Chardonnay (Spätlese)</b><span>Mango- und Birnennoten, exotische Früchte, pikante Würze</span></div><i>Weiß</i></li>
          <li><div><b>Gemischter Satz</b><span>Frische Aromen, lebendig und spritzig</span></div><i>Weiß</i></li>
          <li><div><b>Donau Veltliner</b><span>Fruchtig und würzig, tropische Früchte, Marille, pfeffrige Note</span></div><i>Weiß</i></li>
          <li><div><b>Rotgipfler</b><span>Fruchtbetont und extraktreich</span></div><i>Weiß</i></li>
          <li><div><b>Königsast</b><span>Charaktervoll mit fruchtigem Aroma</span></div><i>Weiß</i></li>
          <li><div><b>Summertime (Welschriesling)</b><span>Rassig mit fruchtigem Bukett</span></div><i>Weiß</i></li>
        </ul>
      </div>
      <div>
        <h3>Rot &amp; Rosé</h3>
        <ul class="wl">
          <li><div><b>Zweigelt</b><span>Kräftig, rassig, mit feinem Bukett</span></div><i>Rot</i></li>
          <li><div><b>Rosé</b><span>Feines Duft- und Geschmacksspiel nach Kirschen und Waldbeeren</span></div><i>Rosé</i></li>
          <li><div><b>Zweigelt Barrique</b><span>Voll im Geschmack, mit zartem Eichenfassaroma</span></div><i>Rot</i></li>
          <li><div><b>Blauer Portugieser</b><span>Weich und mild, samtige Tannine, frische Säure, zarte Würze im Abgang</span></div><i>Rot</i></li>
        </ul>
        <h3 style="margin-top:36px">Frizzante &amp; Sekt</h3>
        <ul class="wl">
          <li><div><b>Frizzante &amp; Sekt</b><span>Auswahl je nach Anlass und Jahreszeit</span></div><i>—</i></li>
        </ul>
        <div class="note">Zwei Weine fehlen in der bestehenden Liste, obwohl sie beworben werden: der <b>Pinot Noir</b> (steht auf der KOSTBAR in ROT) und ein <b>prämierter Riesling 2025</b>. Beide sollten ergänzt werden. <em>[PLATZHALTER: Jahrgänge und Preise]</em></div>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap split">
    <div>
      <p class="kicker">KOSTBAR in ROT</p>
      <h2>Vier Weine auf einem Brett</h2>
      <p>Bei der KOSTBAR in ROT verkosten Sie vier unserer Weine — Blauer Portugieser, Pinot Noir, Zweigelt und Zweigelt Barrique. Pro Wein 80 ml, allein oder zu zweit. Prost.</p>
      <p><em>[PLATZHALTER: Preis pro KOSTBAR bestätigen]</em></p>
      <p><a class="btn btn-primary" href="termine/">Zu den Terminen</a></p>
    </div>
    <img src="assets/kostbar.jpg" alt="Vier kleine Weingläser mit Rotwein auf einem dunklen Holzbrett bei Kerzenlicht" loading="lazy">
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <p class="kicker">Küche</p>
      <h2>Speisen, Schmankerl, Tagesmenüs</h2>
      <p>Auf der bestehenden Seite sind das drei getrennte Menüpunkte. Hier laufen sie zusammen: eine Speisenkarte, darunter die saisonalen Schmankerl und die wechselnden Tagesmenüs.</p>
    </div>
    <div class="grid g3">
      <div class="box"><h3>Speisen</h3><p>Frisch zubereitet zu jeder Tageszeit — mittags wie abends.</p></div>
      <div class="box"><h3>Saisonale Schmankerl</h3><p>Was die Jahreszeit hergibt: Spargel, Wild, Gansl, Stelzen.</p></div>
      <div class="box"><h3>Tagesmenüs</h3><p>An Werktagen wechselnd. <em>[PLATZHALTER: aktuelles Tagesmenü]</em></p></div>
    </div>
    <div class="note">Die vollständige Speisenkarte liegt derzeit nur als Bild bzw. PDF vor. Im Relaunch wird sie als Text gepflegt — durchsuchbar, vorlesbar und auf dem Handy ohne Zoom lesbar.</div>
  </div>
</section>
"""

# -------------------------------------------------------------------- Ab Hof
ABHOF_BODY = """
<div class="pagehead">
  <div class="wrap">
    <p class="kicker">Rund um die Uhr</p>
    <h1>Ab Hof</h1>
    <p>Wein, Traubensaft und fertige Boxen — auch an den rund 188 Tagen, an denen wir nicht ausg'steckt haben. Diese Angebote waren auf der bestehenden Seite nirgends im Menü zu finden.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:26px">
      <div class="box">
        <span class="tag">24 Stunden</span>
        <h3>Getränkeautomat</h3>
        <p>Im Eingangsbereich, täglich rund um die Uhr zugänglich: Wein, Traubensaft gespritzt und Traubensaft pur. Auch wenn wir nicht ausgesteckt haben.</p>
      </div>
      <div class="box">
        <span class="tag">To go</span>
        <h3>Spritzer TO GO</h3>
        <p>Der klassische weiße Spritzer in der 0,33-l-Glasflasche mit einfachem Drehverschluss — praktisch für unterwegs, recycelbar.</p>
      </div>
      <div class="box">
        <span class="tag">Geschenk</span>
        <h3>Geschenkebox</h3>
        <p>Holzbox mit zwei Gläsern und einer Flasche Wein. Ideal als Mitbringsel aus Perchtoldsdorf.</p>
        <p><em>[PLATZHALTER: Preis bestätigen]</em></p>
      </div>
      <div class="box">
        <span class="tag">Lieferung</span>
        <h3>Wein im Karton</h3>
        <p>Ab-Hof-Verkauf während der Aussteckzeiten zu den Öffnungszeiten, außerhalb nach Vereinbarung. Weinlieferung ist ebenfalls nach Vereinbarung möglich.</p>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Für Gäste</p>
      <h2>Heurigenboxen</h2>
      <p>Das fertig angerichtete Buffet für Ihre Gäste — optisch ein Highlight und geschmacklich auf dem Niveau unserer Küche. Jede Box gibt es ab 5 Personen.</p>
    </div>
    <table class="db">
      <tr><th>Boxen</th><td>Klassik · Kärnten · Käse · Mediterran · Brötchenbox · Dessertbox · auf Wunsch individuell</td></tr>
      <tr><th>Ab</th><td>5 Personen</td></tr>
      <tr><th>Beispielpreise</th><td>Klassik für 5 Personen 60 € · Klassik für 10 Personen 90 € <em>[PLATZHALTER: Preisliste bestätigen]</em></td></tr>
      <tr><th>Details</th><td>Die bestehende Seite verlinkt auf die fremde Domain heurigenbox.at — im Relaunch stehen die Inhalte hier, damit die Sitzung nicht verloren geht.</td></tr>
    </table>
    <p style="margin-top:28px"><a class="btn btn-primary" href="#anfrage">Heurigenbox anfragen</a></p>
  </div>
</section>

<section id="anfrage">
  <div class="wrap split">
    <div>
      <p class="kicker">Bestellanfrage</p>
      <h2>Was dürfen wir vorbereiten?</h2>
      <p>Heurigenbox, Wein im Karton oder Geschenkebox — schreiben Sie uns kurz, wir melden uns mit Bestätigung und Abholzeit. Oder rufen Sie an: <a href="tel:+436642110825">0664 2110825</a>.</p>
      <form class="demo" onsubmit="return false">
        <div>
          <label for="art">Was möchten Sie bestellen?</label>
          <select id="art"><option>Heurigenbox</option><option>Wein im Karton</option><option>Geschenkebox</option><option>Spritzer TO GO</option></select>
        </div>
        <div>
          <label for="pers">Für wie viele Personen?</label>
          <select id="pers"><option>5</option><option>6–10</option><option>11–20</option><option>mehr als 20</option></select>
        </div>
        <div>
          <label for="wann">Wann möchten Sie abholen?</label>
          <input id="wann" type="date">
        </div>
        <div>
          <label for="name">Name</label>
          <input id="name" type="text" autocomplete="name">
        </div>
        <div>
          <label for="kontakt">Telefon oder E-Mail</label>
          <input id="kontakt" type="text" autocomplete="tel">
        </div>
        <div>
          <button class="btn btn-primary" type="submit">Anfrage senden</button>
        </div>
      </form>
      <div class="note">Das Formular ist in dieser Demo funktionslos. Im fertigen Aufbau geht es an einen eigenen Endpunkt auf demselben Host und wird per E-Mail an <a href="mailto:christian@weinbauneumayer.at">christian@weinbauneumayer.at</a> zugestellt — ohne Formulardaten bei US-Drittanbietern.</div>
    </div>
    <img src="assets/weinkeller.jpg" alt="Weinflasche und Glas im Weinkeller" loading="lazy">
  </div>
</section>
"""

# -------------------------------------------------------------------- Feiern
FEIERN_BODY = """
<div class="pagehead">
  <div class="wrap">
    <p class="kicker">Feiern &amp; Seminare</p>
    <h1>Ob Firmenfeier, Hochzeit oder Seminar</h1>
    <p>Bei uns richten Sie Ihre Veranstaltung aus, wann und wie Sie möchten — unabhängig davon, ob wir gerade ausgesteckt haben.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="grid g3">
      <div class="box"><h3>Hochzeit &amp; Familie</h3><p>Geburtstag im kleinen Rahmen oder die ganze Hochzeitsgesellschaft. Kinderspielplatz und Spielecke im Gastraum für die Kleinen.</p></div>
      <div class="box"><h3>Firma &amp; Seminar</h3><p>Räumlichkeiten für Seminare und Weihnachtsfeiern, Menü nach Absprache, Weinverkostung als Programmpunkt.</p></div>
      <div class="box"><h3>Zwei Ebenen &amp; Stüberl</h3><p>Das Lokal teilt sich auf zwei Ebenen auf und bietet zusätzlich ein eigenes Stüberl für Ihre Veranstaltung. Im Sommer der Gastgarten.</p></div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap split">
    <div>
      <p class="kicker">Besonderes Highlight</p>
      <h2>Fackelwanderung</h2>
      <p>Jedes Event verdient es, unvergesslich zu werden. Wir verteilen unter all Ihren Gästen Fackeln und wandern gemeinsam zu einem unserer Weingärten auf die Perchtoldsdorfer Heide — rund 20 Minuten Fußweg. Oben angekommen erwartet Ihre Gäste eine kleine Erfrischung und ein unglaublicher Blick über ganz Wien.</p>
      <p><a class="btn btn-white" href="#anfrage">Fackelwanderung anfragen</a></p>
    </div>
    <img src="assets/fackelwanderung.jpg" alt="Fackeln auf einem Weg durch die Weingärten, im Hintergrund die Lichter Wiens" loading="lazy">
  </div>
</section>

<section id="anfrage">
  <div class="wrap split">
    <div>
      <p class="kicker">Anfrage</p>
      <h2>Sagen Sie uns, was Sie vorhaben</h2>
      <p>Ihr Ansprechpartner: <b>Christian Neumayer</b> · <a href="tel:+436642110825">0664 211 08 25</a> · <a href="mailto:christian@weinbauneumayer.at">christian@weinbauneumayer.at</a></p>
      <form class="demo" onsubmit="return false">
        <div>
          <label for="anlass">Anlass</label>
          <select id="anlass"><option>Geburtstag</option><option>Hochzeit</option><option>Firmenfeier</option><option>Seminar</option><option>Sonstiges</option></select>
        </div>
        <div>
          <label for="datum">Wunschtermin</label>
          <input id="datum" type="date">
        </div>
        <div>
          <label for="gaeste">Anzahl der Gäste</label>
          <input id="gaeste" type="text" inputmode="numeric">
        </div>
        <div>
          <label for="wunsch">Ihre Wünsche</label>
          <textarea id="wunsch" placeholder="Menü, Fackelwanderung, Musik, Technik …"></textarea>
        </div>
        <div>
          <label for="name">Name und Kontakt</label>
          <input id="name" type="text" autocomplete="name">
        </div>
        <div>
          <button class="btn btn-primary" type="submit">Unverbindlich anfragen</button>
        </div>
      </form>
      <div class="note">Demo — im fertigen Aufbau wird die Anfrage per E-Mail zugestellt. Wir richten Ihre Veranstaltung auch außerhalb unserer regulären Aussteckzeiten aus.</div>
    </div>
    <img src="assets/hero-terrasse.jpg" alt="Gedeckte Tafel im Gastgarten des Heurigen" loading="lazy">
  </div>
</section>
"""

# -------------------------------------------------------------------- Kontakt
KONTAKT_BODY = """
<div class="pagehead">
  <div class="wrap">
    <p class="kicker">Besuch &amp; Kontakt</p>
    <h1>Wir freuen uns auf Ihren Besuch</h1>
    <p>Sonnbergstraße 89, 2380 Perchtoldsdorf — wenige Kilometer von Wien entfernt, mitten im Weinbaugebiet Thermenregion.</p>
  </div>
</div>

<section class="tight">
  <div class="wrap">
    <div class="grid g3">
      <div class="box">
        <h3>Adresse</h3>
        <p>Weinbau &amp; Heuriger Neumayer<br>Sonnbergstraße 89<br>2380 Perchtoldsdorf<br>Österreich</p>
        <p><a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&amp;query=Weinbau+%26+Heuriger+Neumayer+Sonnbergstra%C3%9Fe+89+Perchtoldsdorf" target="_blank" rel="noopener">Route planen</a></p>
      </div>
      <div class="box">
        <h3>Kontakt</h3>
        <p>Telefon <a href="tel:+436642110825">+43 664 211 08 25</a><br>
        E-Mail <a href="mailto:christian@weinbauneumayer.at">christian@weinbauneumayer.at</a></p>
        <p><a class="btn btn-primary" href="tel:+436642110825">Jetzt anrufen</a></p>
      </div>
      <div class="box">
        <h3>Öffnungszeiten</h3>
        <p class="hours">Montag bis Samstag<br>10:30 – 23:00<br><br>Sonntag &amp; Feiertag<br>10:30 – 22:30</p>
        <p>Diese Zeiten gelten während der Aussteckzeiten. Außerhalb: Ab-Hof-Verkauf nach Vereinbarung, Getränkeautomat rund um die Uhr.</p>
      </div>
    </div>
    <div class="note">Auf der bestehenden Seite gibt es <b>keinen einzigen <code>tel:</code>-Link</b> — die Telefonnummer steht nur als Fließtext, auf dem Handy ist Anrufen damit Copy-and-paste. Hier ist jede Nummer antippbar. Die Anfahrtskarte wird als Link geöffnet, nicht als Google-Maps-iframe eingebettet: Das spart das Einwilligungs-Banner.</div>
  </div>
</section>

<section id="reservieren" class="alt">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Reservierung</p>
      <h2>Tisch reservieren</h2>
      <p>Drei Schritte, keine Registrierung. An Tagen ohne Ausstecken ist keine Reservierung möglich — für Feiern nutzen Sie bitte die <a href="feiern/#anfrage">Feieranfrage</a>.</p>
    </div>
    <form class="demo" onsubmit="return false">
      <div>
        <label for="tag">Wunschtag</label>
        <input id="tag" type="date" min="2026-11-07">
      </div>
      <div>
        <label for="zeit">Uhrzeit</label>
        <select id="zeit"><option>11:30</option><option>12:00</option><option>12:30</option><option>13:00</option><option>17:30</option><option>18:00</option><option>18:30</option><option>19:00</option></select>
      </div>
      <div>
        <label for="personen">Personen</label>
        <input id="personen" type="text" inputmode="numeric" placeholder="z. B. 4">
      </div>
      <div>
        <label for="name">Name</label>
        <input id="name" type="text" autocomplete="name">
      </div>
      <div>
        <label for="kontakt">Telefon oder E-Mail (für die Bestätigung)</label>
        <input id="kontakt" type="text" autocomplete="tel">
      </div>
      <div>
        <button class="btn btn-primary" type="submit">Reservierung anfragen</button>
      </div>
    </form>
    <div class="note">Demo — das Formular ist funktionslos. Im fertigen Aufbau sind nur Ausstecktage wählbar, ab 11 Personen leitet es automatisch zur Feieranfrage, und die Bestätigung kommt sofort per SMS oder E-Mail.</div>
  </div>
</section>

<section id="anfahrt">
  <div class="wrap split">
    <div>
      <p class="kicker">Anfahrt</p>
      <h2>Mitten in Perchtoldsdorf</h2>
      <p>Die Sonnbergstraße liegt im Ortskern von Perchtoldsdorf, wenige Minuten von der Kaltenleutgebner Bahn und der Wiener Stadtgrenze entfernt. Der Gastgarten liegt direkt beim Haus.</p>
      <p><a class="btn btn-primary" href="https://www.google.com/maps/search/?api=1&amp;query=Weinbau+%26+Heuriger+Neumayer+Sonnbergstra%C3%9Fe+89+Perchtoldsdorf" target="_blank" rel="noopener">In Google Maps öffnen</a></p>
    </div>
    <img src="assets/fackelwanderung.jpg" alt="Weingärten über Perchtoldsdorf im Abendlicht" loading="lazy">
  </div>
</section>
"""

# ------------------------------------------------------- Impressum/Datenschutz
IMPRESSUM_BODY = """
<div class="pagehead">
  <div class="wrap">
    <h1>Impressum</h1>
    <p>Angaben gemäß Mediengesetz und E-Commerce-Gesetz.</p>
  </div>
</div>
<section class="tight">
  <div class="wrap">
    <table class="db">
      <tr><th>Firma</th><td>Weinbau &amp; Heuriger Neumayer</td></tr>
      <tr><th>Inhaber</th><td>Christian Neumayer</td></tr>
      <tr><th>Firmensitz</th><td>Sonnbergstraße 89, 2380 Perchtoldsdorf, Österreich</td></tr>
      <tr><th>Rechtsform</th><td>Einzelunternehmen</td></tr>
      <tr><th>UID-Nummer</th><td>ATU66212699</td></tr>
      <tr><th>Gerichtsstand</th><td>Mödling</td></tr>
      <tr><th>Telefon</th><td><a href="tel:+436642110825">+43 664 211 08 25</a></td></tr>
      <tr><th>E-Mail</th><td><a href="mailto:christian@weinbauneumayer.at">christian@weinbauneumayer.at</a></td></tr>
    </table>
    <div class="note">Diese Seite ist ein Designentwurf und keine offizielle Website des Betriebs.</div>
  </div>
</section>
"""

DATENSCHUTZ_BODY = """
<div class="pagehead">
  <div class="wrap">
    <h1>Datenschutz</h1>
    <p>Diese Demo-Seite setzt keine Cookies und lädt kein Tracking. Zur Erklärung, wie die Seite später damit umgeht.</p>
  </div>
</div>
<section class="tight">
  <div class="wrap" style="max-width:820px">
    <h2>Grundsatz</h2>
    <p>Die bestehende Website verzichtet bereits auf Google Analytics und jede Form von Tracking — deshalb braucht sie auch kein Cookie-Banner. Dieses Prinzip bleibt im Relaunch erhalten: keine Cookies, kein Tracking, kein Consent-Banner.</p>
    <h2>Server-Logfiles</h2>
    <p>Beim Aufruf der Seite speichert der Webserver technisch notwendige Zugriffsdaten (Datum, Uhrzeit, aufgerufene Seite). Diese Daten werden nicht mit anderen Datenquellen zusammengeführt und nicht zur Identifikation von Personen verwendet.</p>
    <h2>Externe Verbindungen in dieser Demo</h2>
    <table class="db">
      <tr><th>Schriftarten</th><td>In der Demo von Google Fonts geladen. Im fertigen Aufbau selbst gehostet — dann fließen keine Daten an Dritte.</td></tr>
      <tr><th>Karten</th><td>Kein eingebettetes Karten-iframe. Die Route öffnet erst auf Klick in Google Maps — bis dahin wird nichts übertragen.</td></tr>
      <tr><th>Formulare</th><td>Ohne Funktion in dieser Demo. Im fertigen Aufbau serverseitig auf demselben Host, Zustellung per E-Mail.</td></tr>
      <tr><th>Bilder</th><td>KI-generierte Motive als Platzhalter, keine Personenbezüge.</td></tr>
    </table>
  </div>
</section>
"""


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "style.css").write_text(CSS, encoding="utf-8")

    src = DOCS / "design-draft" / "assets"
    for f in sorted(src.glob("*.jpg")):
        shutil.copy2(f, ASSETS / f.name)

    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "robots.txt").write_text(
        "# Demo-Entwurf: bewusst aus dem Index gehalten\nUser-agent: *\nDisallow: /\n",
        encoding="utf-8",
    )

    written = []
    written.append(page("", "Weinbau &amp; Heuriger Neumayer — Demo-Entwurf", "", HOME_BODY, root=True))
    written.append(page("termine/", "Ausstecktermine — Demo", "termine", TERMINE_BODY))
    written.append(page("speisen-wein/", "Speisen &amp; Wein — Demo", "speisen-wein", SPEISEN_BODY))
    written.append(page("ab-hof/", "Ab Hof — Demo", "ab-hof", ABHOF_BODY))
    written.append(page("feiern/", "Feiern &amp; Seminare — Demo", "feiern", FEIERN_BODY))
    written.append(page("kontakt/", "Besuch &amp; Kontakt — Demo", "kontakt", KONTAKT_BODY))
    written.append(page("impressum/", "Impressum — Demo", "", IMPRESSUM_BODY))
    written.append(page("datenschutz/", "Datenschutz — Demo", "", DATENSCHUTZ_BODY))

    for w in written:
        print("written:", w.relative_to(ROOT))


if __name__ == "__main__":
    main()
