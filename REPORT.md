# Website-Audit — www.weinbauneumayer.at

> **Projekt:** neumayer — Audit + Redesign
> **Objekt:** Weinbau & Heuriger Neumayer, Sonnbergstraße 89, 2380 Perchtoldsdorf
> **Stand:** 2026-11-05
> **Methodik:** Live-Crawl (39 URLs), vollständiger Mirror (228 Dateien / 48 MB), Header-/TLS-Probing, Asset-Analyse, Offline-Auswertung des Mirrors
> **Erstellt von:** Hermes (PM/TPO) · **Rohdaten:** `mirror/` + `scripts/mirror.py`

---

## 0. Executive Summary

Die Seite ist **inhaltlich stark, technisch aber ~2014 stehengeblieben**. Sie läuft auf WordPress mit einem veralteten Theme (`wp_nuvo`), vier überlappenden Seitenbaukästen und **ohne jede Kompression** — die Startseite liefert 166 KB HTML unkomprimiert aus, einzelne Fotos sind **bis 2,25 MB groß** und werden als 700-px-Thumbnail angezeigt.

Gleichzeitig fehlt **die gesamte SEO-/Shareability-Basis**: keine einzige Meta-Description, keine Open-Graph-Tags, keine strukturierten Daten (LocalBusiness/Restaurant), 26 Bilder ohne Alt-Text, 13 Seiten ohne H1, Startseite mit 6 H1. Für ein Ausflugslokal, das zu ~90 % über „Heuriger Perchtoldsdorf“-Suchen und WhatsApp/Messenger-Weiterleitungen gefunden wird, ist das der teuerste Mangel.

Drei Dinge funktionieren erstaunlich gut: **Inhalt** (Termine, Menüs, Weinliste, Fackelwanderung — echte Differenzierung), **Technik-Basis** (HTTP/2, gültiges Let's-Encrypt-Zertifikat, xmlrpc geschlossen, robots.txt + Sitemap vorhanden) und **Datenschutz-Basis** (kein Google Analytics, keine Tracker, kein Cookie-Banner nötig).

**Top-Befund:** Ein Theme-Bug zeigt live auf der Startseite ein `http://localhost/...`-Bild — die Hintergrundgrafik des Seitenkopfs ist damit auf allen Unterseiten defekt (Dev-Umgebung durchgeleakt). Details: [§5.1](#51--dev-leak-live-auf-produktion-kritisch).

---

## 1. Top-10-Findings (nach Wirkung sortiert)

| # | Befund | Kategorie | Schwere | Aufwand |
|---|--------|-----------|---------|---------|
| 1 | **Keine Kompression** — HTML 166 KB roh statt ~25 KB gzip; alle CSS/JS unkomprimiert | Performance | 🔴 hoch | 30 min (Server) |
| 2 | **Keine Meta-Descriptions** auf allen 36 gecrawlten Seiten | SEO | 🔴 hoch | 2 h |
| 3 | **Keine strukturierten Daten** (LocalBusiness/Restaurant/Menu/Event) → keine Rich Results | SEO | 🔴 hoch | 3 h |
| 4 | **Keine Open-Graph-/Twitter-Cards** → beim Teilen erscheint nackter Link | Marketing | 🔴 hoch | 1 h |
| 5 | **Bilder unoptimiert**: 83 JPEG / 39,6 MB im Mirror, Spitzenreiter 2,25 MB — kein WebP/AVIF, keine srcset | Performance | 🔴 hoch | 1 Tag |
| 6 | **`http://localhost`-Bild live** + Staging-URLs im RSS (`nmt82.joomexp.com`) | Qualität/Dev-Leak | 🟠 mittel | 1 h |
| 7 | **Keine `tel:`-Links** — Telefonnummer ist toter Text; auf Mobile kein Tap-to-Call | Conversion | 🟠 mittel | 30 min |
| 8 | **Heading-Chaos**: 13 Seiten ohne H1, Startseite mit 6 H1, /speisen mit 9 H1 | SEO/A11y | 🟠 mittel | 3 h |
| 9 | **URL-Wildwuchs & Duplicate Content**: `/?p=904`, `/pointofsale_category/weine/`, http+www+Slash-Varianten | SEO | 🟠 mittel | 4 h |
| 10 | **Keine Security-Header** (HSTS, CSP, X-Content-Type-Options, Referrer-Policy) | Security | 🟡 niedrig | 2 h |

---

## 2. Technischer Stack

| Komponente | Befund | Bewertung |
|---|---|---|
| CMS | WordPress **7.1.4** | aktuell gepflegt ✅ |
| Shop | WooCommerce **9.7.3** (installiert, **aber kein sichtbarer Shop**) | Ballast ⚠️ |
| Theme | `wp_nuvo` — Bootstrap-3-Ära, bxSlider, eigene Font-Faces | veraltet 🔴 |
| Page Builder | **WPBakery** (`js_composer`) + **Slider Revolution 6.7.30** + **Essential Grid** + Theme-eigener Builder | 3–4 überlappende Builder 🔴 |
| Fonts | self-hosted OpenSans (5 Schnitte), Novecentowide, Herr von Muellerhoff — in `eot/woff/ttf/svg` | Legacy-Formate ⚠️ |
| Server | Apache, HTTP/2, kein CDN davor | ok |
| TLS | Let's Encrypt Wildcard `*.weinbauneumayer.at`, gültig bis 2027-01-08 | ✅ |
| Plugins | Contact Form 7, Events Manager, Redi Restaurant Reservation, NextGEN (`ngg`), gallery-by-supsystic, si-captcha, news-twitter, Redirection, Jetpack, MC4WP | Plugin-Zoo, teils ohne sichtbare Funktion ⚠️ |
| Urheber | „Programmiert von Jeromedia.eu" im Footer | — |

**Konsequenz:** Migration auf einen modernen Block-Editor/Theme-Setup (oder Headless) ist realistischer als ein Facelift — vier Builder und ein 12 Jahre altes Theme kann man nicht sinnvoll „aufhübschen".

---

## 3. Performance

| Messwert | Wert | Zielwert |
|---|---|---|
| TTFB Startseite | **1,93 s** | < 0,5 s |
| HTML-Transfer Startseite | **166 KB** (ungekomprimiert) | ~25 KB (gzip/br) |
| Kompression | **aus** — gzip/br/identity liefern identisch 166.710 Bytes | an |
| Bilddaten gesamt im Mirror | **39,6 MB** (83 JPEG) | < 5 MB |
| Größtes Einzelbild | **2,25 MB** (Stelzen-Wochenende, angezeigt mit 700×990 px) | < 150 KB |
| Extra-Requests pro Seite | 70 JS-Dateien / 32 CSS-Dateien im Mirror | bündeln |
| Größte JS-Brocken | `rs6.min.js` 416 KB, `events-manager.js` 428 KB, `js_composer.css` 459 KB + 270 KB | Tree-shaking |
| HTTP-Protokoll | HTTP/2 | HTTP/2/3 ✅ |
| CDN / Cache | keiner | CDN empfohlen |

**Weitere Auffälligkeiten**
- **Kein Lazy-Loading** für Bilder unterhalb des Folds feststellbar.
- Bilder von **2014/2016/2018** werden unverändert in Originalgröße ausgeliefert (`JER_6132.jpg` 1,54 MB, `DSC_0653.jpg` 1,21 MB).
- **Inline-CSS pro Seite dupliziert**: das Theme bettet ~25 KB Theme-Options-CSS in jedes HTML ein (im Mirror mehrfach identisch) — ungecacht, unminifiziert, nicht cachebar.
- Legacy-Fontformate (`.eot`, `.svg`) werden zusätzlich zu `.woff` geladen.

---

## 4. SEO

| Prüfpunkt | Status |
|---|---|
| Meta-Description | ❌ **0 von 36** Seiten |
| Title-Tag | ✅ vorhanden, Muster `Seite – Weinbau & Heuriger Neumayer` |
| H1-Struktur | ❌ 13 Seiten ohne H1; Startseite **6**, `/speisen` **9**, `/feiern` und `/ueber` je 4 |
| Strukturierte Daten (JSON-LD) | ❌ keine (`Restaurant`, `LocalBusiness`, `Menu`, `Event`, `AggregateRating` fehlen) |
| Open Graph / Twitter Card | ❌ keine |
| `lang`-Attribut | ✅ `<html lang="de">` |
| hreflang | ✅ nicht nötig (rein DE) |
| Canonical | ✅ gesetzt |
| robots.txt | ✅ mit `Sitemap:`-Verweis |
| Sitemap | ✅ `/wp-sitemap.xml` (inkl. Events, Produkte, Restaurantmenus, PointOfSale) |
| `robots`-Meta | ✅ `max-image-preview:large` — **keine Index-Sperre aktiv** |
| Alt-Texte | ❌ **26 von 108** Bildern ohne `alt` |
| Bild-Dateinamen | ⚠️ `JER_6132.jpg`, `DSC_0651.jpg` — keine Keywords |
| Duplicate Content | ❌ `/?p=904` ≡ `/reservierung/`, http/www/Slash-Varianten, `/pointofsale_category/weine/` ≡ `/weine/` |
| User-Enumeration | ⚠️ `/wp-json/wp/v2/users` → **HTTP 200** |
| Aufgeblähte Endpunkte | ⚠️ `/readme.html`, `/license.txt` öffentlich → WordPress-Version sichtbar |

**URL-Inventar (Auszug, aus dem Crawl):**

| Sauber | Problematisch |
|---|---|
| `/`, `/ueber/`, `/termine/`, `/speisen/`, `/schmankerl/`, `/tagesmenues/`, `/weine/`, `/feiern/`, `/galerie/`, `/reservierung/`, `/kontakt/`, `/impressum/`, `/datenschutz/` | `/?p=1717` … `/?p=3312`, `/pointofsale_category/essen/`, `/pointofsale/friendly/`, `/reservierung` vs `/reservierung/`, `http://` vs `https://` vs `www` |

---

## 5. Funktionalität & Qualität

### 5.1 🔴 Dev-Leak live auf Produktion (kritisch)

Auf **allen** Seiten steht im Inline-CSS des Themes:

```css
#cs-page-title-wrapper{ background-image:url(http://localhost/wp_nuvo/wp-content/uploads/2014/09/topbannerimage.jpg); }
```

Der Seitenkopf-Banner lädt also von `localhost` → **die Hintergrundgrafik ist live defekt**. Zusätzlich leaken Entwicklungs-URLs:

- RSS-`<guid>`: `http://localhost/wp_nuvo/?p=753`
- weitere `<guid>`: `http://nmt82.joomexp.com/wp-nuvo/?p=259` (Staging-Host der Agentur)

### 5.2 Conversion / Nutzerführung

| Befund | Wirkung |
|---|---|
| **Keine `tel:`-Links** (0 Treffer im gesamten Mirror) — Nummer nur als Fließtext | Auf iOS kostet jeder Anruf Copy-Paste — der wichtigste Kanal ist kaputt |
| Reservierung nur über ein Formular der Redi-Erweiterung (40+ Zeit-Slots als Dropdown, Datum in 3 Feldern) | hohe Abbruchrate, Mobile unhandlich |
| Öffnungszeiten nur als Prosa auf `/termine` („Mo–Sa 10:30–23:00, So 10:30–22:30"), im selben Absatz aber „**bis zu zehn mal** im Jahr geöffnet" | **widersprüchliche Kernaussage** — der Gast weiß nicht, wann offen ist |
| Nächster Ausstecktermin / Countdown nicht dauerhaft oben sichtbar | wichtigste Entscheidungsinfo nicht auf einen Blick |
| Kontaktformular + „Newsletter abonnieren"-Checkbox (MC4WP) ohne Double-Opt-in-Hinweis | DSGVO-Risiko |
| Google-Maps-iframe ohne Consent-Gate | DSGVO-Risiko (IP-Übermittlung an Google) |
| Heurigenboxen verlinken auf `www.heurigenbox.at` (fremde Domain) | Sitzung geht verloren |
| Getränkeautomat, Spritzer TO GO, KOSTBAR in ROT, Fackelwanderung | **starke Alleinstellungsmerkmale, die im Menü nicht vorkommen** — nur als Textblöcke auf der Startseite |

### 5.3 Accessibility (Quick-Audit)

- 26 Bilder ohne Alt-Text
- 13 Seiten ohne H1, Startseite mit 6 H1 → sprunghafte Dokumentstruktur
- Icon-Fonts (Glyphicons, FontAwesome, vc_grid) statt Semantik
- Kontrast: Body-Text `#888` auf Weiß = **3,54:1** → WCAG AA (4,5:1) **nicht erfüllt**; zusätzlich nur 14 px Grundschrift
- Kein Skip-Link, keine sichtbaren Focus-States prüfbar, Slider ohne Pause-Steuerung
- Formularfelder mit Platzhaltern statt Labels (nur „(Pflichtfeld)" im Text)

### 5.4 Security & Datenschutz

**Fehlende Response-Header (alle):** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`. Der Server schickt nur `server`, `content-type`, `date`, `link`.

- **HTTP → HTTPS**: `http://weinbauneumayer.at` → 302 auf `http://www.weinbauneumayer.at` → erst dann HTTPS. **Ein zusätzlicher Klartext-Hop**, ohne HSTS.
- `xmlrpc.php` → 404 ✅ (deaktiviert)
- `/wp-content/debug.log`, `/.env` → 404 ✅
- `/readme.html`, `/license.txt` → 200 ⚠️ (Version disclosure)
- `/wp-json/wp/v2/users` → 200 ⚠️
- **Positiv:** kein Google Analytics, kein GTM, keine Tracker im Mirror → derzeit **kein Cookie-Banner nötig** und DSGVO-freundlich. Diese Eigenschaft sollte beim Redesign erhalten bleiben (matomo self-hosted oder gar nichts).

---

## 6. Inhalt & Informationsarchitektur

**Vorhandene Inhalte (gut gepflegt, echtes Marketing-Asset):**

| Seite | Inhalt |
|---|---|
| Startseite | Ausstecktermine, Save-the-Date, KOSTBAR in ROT, Getränkeautomat, Heurigenboxen, Spritzer TO GO |
| `/termine` | „Alles auf einen Blick": Ausstecktermine, Veranstaltungen, Öffnungszeiten |
| `/speisen`, `/schmankerl`, `/tagesmenues` | Speisen, Saisonales, wechselnde Tagesmenüs |
| `/weine` | 12+ Weine mit Verkostungsnotizen (Weiß/Heuriger/Rot/Rosé/Frizzante) |
| `/feiern` | Firmenfeier, Hochzeit, Seminar + **Fackelwanderung auf die Perchtoldsdorfer Heide** |
| `/galerie` | 30 Bilder |
| `/ueber` | Familienbetrieb seit 40 Jahren, zwei Ebenen, Stüberl, Gastgarten, Kinderspielplatz |
| `/reservierung`, `/kontakt`, `/impressum`, `/datenschutz` | Standard |

**Strukturprobleme**
1. **Doppel-Struktur**: Startseite ist eine lange Scroll-Seite, deren Inhalte zugleich unter eigenen URLs existieren (Termine, KOSTBAR, Heurigenboxen) → Pflege doppelt, SEO verwässert.
2. **Navigation mit 10 Punkten** (Über, Ausgsteckt'is, Speisen, Schmankerl, Tagesmenüs, Weine, Feiern, Galerie, Reservierung, Kontakt) — Redundanz: „Speisen / Schmankerl / Tagesmenüs" gehören in **ein** Menü; „Ausgsteckt'is" ist lokaler Dialekt und Nicht-Einheimischen unverständlich („Termine" wäre klar).
3. **Kein Shop**: WooCommerce ist installiert und aktiv, aber es gibt keinen kaufbaren Wein. Bei „Ab-Hof-Verkauf + 24h-Getränkeautomat" liegt ein **Direktverkauf-Kanal** auf der Hand.
4. **Keine Ansprechperson/E-Mail** öffentlich (nur Telefon) — für Firmenanfragen („Feiern") zu wenig.

---

## 7. Empfehlung (Kurzfassung)

**Strategie: Relaunch, nicht Facelift.** Ein 12 Jahre altes Theme mit vier Baukästen zu restylen konserviert den Ballast. Empfohlen: statisches/moderat dynamisches Frontend mit den bestehenden Inhalten, Datenpflege über WordPress-Headless oder einen schlanken Redaktor, Hosting mit CDN + Kompression.

**Priorität 1 — sofort, ohne Relaunch (Quick Wins, < 1 Tag gesamt)**
1. gzip/brotli am Server aktivieren → 166 KB → ~25 KB
2. `http://localhost`-Bildpfad korrigieren, Staging-URLs aus dem Feed entfernen
3. `tel:`-Links auf allen Seiten (Header + Footer + „Anrufen"-Button)
4. Öffnungszeiten-Widerspruch auflösen, Öffnungszeiten + nächster Ausstecktermin in den Seitenkopf
5. 10 größten Bilder komprimieren (2,25 MB → 150 KB) + WebP
6. Meta-Descriptions für die 12 Inhaltsseiten

**Priorität 2 — Relaunch (siehe `docs/design-draft/REDESIGN-DRAFT.md`)**
- News-Architektur: 5 Hauptpunkte (Heuriger, Speisen & Wein, Termine, Feiern, Kontakt) statt 10
- Sticky „Heute offen / Nächster Ausstecktermin"-Leiste, Online-Tischreservierung in 3 Schritten
- LocalBusiness- + Menu- + Event-Schema, Open Graph, Alt-Texte
- Bildkonzept aus einer Bilderwelt (siehe Draft), statt 12 Jahre gemischter Fotos
- Ab-Hof-Bestellstrecke (Weinbox + Heurigenbox) als zusätzlicher Kanal

---

## 8. Methodik & Rohdaten

- **Crawl + Mirror:** `scripts/mirror.py` (39 URLs, 228 Dateien, 48 MB) → `mirror/`
- **Header/TLS:** `curl -sI`, `openssl s_client -connect www.weinbauneumayer.at:443`
- **Offline-Auswertung:** BeautifulSoup über alle 36 HTML-Dateien (Titles, Descriptions, H1, Alt, Formulare), Dateigrößen-Statistik über den Mirror
- **Live-Verifikation** der kritischen Einzelbefunde (localhost-Bild, H1-Anzahl, Kompression, Header) am 2026-11-05, 09:2x–09:4x CET
- Nicht geprüft (nicht öffentlich zugänglich): im Backend gesetzte SEO-Plugins, Serverkonfiguration, Core-Web-Vitals-Felddaten aus der Search Console
