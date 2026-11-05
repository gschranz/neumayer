# neumayer

Audit, Redesign-Draft und Umsetzungsbasis für **www.weinbauneumayer.at** — Weinbau & Heuriger Neumayer, Sonnbergstraße 89, 2380 Perchtoldsdorf (Niederösterreich).

> Stand: 2026-11-05 · Auftrag: Audit + Redesign-Draft (Higgsfield-Visuals + Opus-Agent)
>
> **Demo live:** https://gschranz.github.io/neumayer/ — bewusst `noindex` (Entwurf, nicht die offizielle Seite des Betriebs)

---

## Inhalt des Repos

| Pfad | Was |
|---|---|
| `REPORT.md` | **Website-Audit** — Stack, Performance, SEO, Accessibility, Security, Inhaltsinventar, Top-10-Befunde mit Priorisierung |
| `PROJEKTPLAN.md` | Projektplan, Risiko-Radar, Meilensteine, offene Punkte |
| `.kanban/BOARD.md` | Kanban-Board (Arbeitspakete A–D) |
| `docs/` | **Demo-Site** (GitHub Pages, Quelle `/docs`): Startseite + Termine, Speisen & Wein, Ab Hof, Feiern, Besuch & Kontakt, Impressum, Datenschutz — erzeugt aus `scripts/build_demo.py` |
| `docs/design-draft/REDESIGN-DRAFT.md` | Redesign-Konzept (Opus-Agent): IA, Seitenkonzepte, Textenwürfe, Tokens, Schema, Phasen |
| `docs/design-draft/mockup.html` | Klickbarer High-Fidelity-Mockup der neuen Startseite (responsive) |
| `docs/design-draft/mockup-desktop-preview.jpg` | Render Desktop (1000 px Breite) |
| `docs/design-draft/mockup-mobile-preview.jpg` | Render Mobile (390 px CSS-Breite, 2×) |
| `docs/design-draft/assets/` | Generierte Bildmotive für den Draft (FAL `flux-2-pro`) |
| `mirror/` | Vollständiger Spiegel der aktuellen Live-Seite (Stand 2026-11-05, 39 URLs / 228 Dateien / 48 MB) |
| `scripts/mirror.py` | Reproduzierbarer Crawl des Ausgangsstands |

---

## Kernbefunde in einem Satz

Inhaltlich stark, technisch ~2014: unkomprimierte 166 KB HTML, 39,6 MB unoptimierte Bilder, **null Meta-Descriptions und null strukturierte Daten**, kein Open Graph, 13 Seiten ohne H1, keine `tel:`-Links — und ein live durchgeschleuster `http://localhost`-Bildpfad im Seitenkopf.

Vollständig: [REPORT.md](REPORT.md)

---

## Reproduzieren

```bash
python3 -m pip install httpx beautifulsoup4
python3 scripts/mirror.py      # schreibt nach /data/.hermes/cache/scratch/neumayer-mirror
```

Mockup rendern (Chromium headless):

```bash
chromium --headless=new --no-sandbox --hide-scrollbars \
  --window-size=1440,9000 --screenshot=mockup-desktop.png \
  file://$PWD/docs/design-draft/mockup.html
```
