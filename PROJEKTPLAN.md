# neumayer — Projektplan

> **Projekt:** Relaunch weinbauneumayer.at (Weinbau & Heuriger Neumayer, Perchtoldsdorf) — Audit, Redesign-Draft, Umsetzung
> **Stand:** 2026-11-05
> **PM:** Hermes (leitender KI-Projektmanager)
> **Implementierung:** Hermes direkt (`patch`/`write_file`) — Claude Code / Coding-Agents nur auf ausdrücklichen Wunsch
> **Repo:** https://github.com/gschranz/neumayer

---

## Zielbild

Moderner, mobile-first Auftritt für einen Familien-Heurigen mit Weinbau in Perchtoldsdorf. Kern der Seite ist **eine Information**: *ist heute ausgesteckt, was gibt es, wie reserviere ich*. Alles andere ordnet sich dem unter.

- Statt 10 Navigationspunkten → 5
- Öffnungsstatus & nächster Ausstecktermin immer sichtbar
- Tischreservierung in 3 Schritten mobil
- Local-SEO: Rich Results für Lokalbetrieb, Menü, Events
- Ladezeit: Startseite < 1,5 s auf 4G, < 900 KB total

---

## Datenquellen

| Quelle | Status | Zweck |
|---|---|---|
| Live-Crawl + Mirror (39 URLs, 228 Dateien, 48 MB) | ✅ 2026-11-05 | Inhalts- und Asset-Basis |
| `REPORT.md` (Audit) | ✅ 2026-11-05 | Befundlage, Priorisierung |
| `docs/design-draft/REDESIGN-DRAFT.md` | 🤖 Opus-Agent (läuft) | Design-/IA-Konzept |
| Bildwelt (Fotos Haus, Weingarten, Speisen, Wein) | ⏳ vom Betreiber | Redesign-Assets |
| Aktuelle Weinliste mit Jahrgängen/Preisen | ⏳ vom Betreiber | Getränkekarte, Schema |
| Freigabe Hosting/Domain-Zugang | ⏳ offen | Deployment |

---

## Architektur (Vorschlag, nicht fixiert)

| Baustein | Vorschlag | Begründung |
|---|---|---|
| Frontend | Statisches HTML/CSS/JS (11ty oder Astro) | < 50 KB CSS, kein jQuery, keine Builder |
| Inhaltspflege | Headless-WP (bestehende Redaktion bleibt) **oder** schlanker Redaktor | Inhalte liegen schon in WP 7.1.4 |
| Termine | Ausstecktermine als JSON/YAML im Repo, Build generiert Kalender | Kein Events-Manager-JS (428 KB) |
| Reservierung | Bestehende Redi-Lösung hinter eigenem 3-Schritt-Formular **oder** Telefon-first | Bestand prüfen |
| Bilder | AVIF/WebP + `srcset`, CDN | Aus 39,6 MB werden < 5 MB |
| Hosting | Cloud-managed, EU-Region | DSGVO, kein Tracker |

---

## Stundenbudget (Monats-Tracking)

| Monat | Verbraucht | Notizen |
|---|---|---|
| 2026-11 | 3 h | Audit, Mirror, Report, Draft-Erstellung |

---

## Risiko-Radar

| Risiko | Status | Workaround |
|---|---|---|
| Bilderwelt in Altbestand (2014/2016/2018, gemischt, teils 2 MB) | 🟡 offen | Neue Bildwelt erst nach Fotofreigabe; Draft nutzt Platzhalter + generierte Motive |
| Kein Zugang zu Server/Hosting/DNS | 🟡 offen | Quick Wins als Patch-Liste für Agentur übergeben |
| Öffnungszeiten widersprüchlich („Mo–Sa 10:30–23:00" vs. „bis zu zehn mal im Jahr") | 🟡 fachlich klären | Betreiber-Interview nötig vor IA-Finalisierung |
| WooCommerce aktiv, aber ungenutzt (Shop-Ballast, Sicherheitsfläche) | 🟡 offen | Beim Relaunch entscheiden: Ab-Hof-Bestellstrecke ja/nein |
| Bestehende Agentur (jeromedia.eu) hält Zugänge | 🟡 offen | Zugänge klären, bevor Umsetzung startet |
| Higgsfield-CLI benötigt Browser-OAuth (localhost-Callback) | 🔴 blockiert | Siehe §Offene Punkte — API-Key oder lokaler Login nötig |

---

## Meilensteine

| Meilenstein | Deadline | Abhängigkeit |
|---|---|---|
| M1: Audit + Report + Draft im Repo | ✅ 2026-11-05 | — |
| M2: Quick-Win-Patchliste an Agentur/Betreiber | TBD | Freigabe M1 |
| M3: Bildwelt + Wizard-of-Oz-Mockup (klickbar) | TBD | Fotos, Entscheidung §Offene Punkte |
| M4: Umsetzung Frontend | TBD | M3 + Hosting |
| M5: Go-Live + Redirects + Search Console | TBD | M4 |

---

## Offene Punkte an 👌

1. **Higgsfield-Zugang**: Die CLI (`@higgsfield/cli` 1.2.2, installiert) authentifiziert ausschließlich per Browser-OAuth mit Callback auf `localhost:8765` — auf dem Hermes-Host nicht abschließbar. Optionen: (a) API-Key aus `console.higgsfield.ai` (dann REST statt CLI), (b) `higgsfield auth login` lokal + Token-Datei herüberkopieren, (c) Bildwelt stattdessen über die bereits aktive FAL-Route (`nano-banana-pro`).
2. **Domain-/Hosting-Zugang** und Verhältnis zur bisherigen Agentur (jeromedia.eu)?
3. **Öffnungszeiten**: echte Zeiten inkl. Aussteck-Logik (nur an Ausstecktagen offen? oder täglich mit eingeschränkter Küche?) — Kerninformation der Seite.
4. **Ab-Hof-Verkauf**: soll der Relaunch eine Bestellstrecke bekommen (Wein + Heurigenboxen)?
5. **Sprachvarianten**: nur DE, oder zusätzlich EN (Wien-Tourismus / Gäste)?

---

## Referenzen

- `REPORT.md` — Website-Audit (Befunde, Priorisierung)
- `docs/design-draft/` — Redesign-Draft (Opus-Agent + Visuals)
- `mirror/` — vollständiger Website-Mirror (Stand 2026-11-05)
- `scripts/mirror.py` — Reproduzierbarer Crawl
