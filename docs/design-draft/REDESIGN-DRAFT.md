# REDESIGN-DRAFT — www.weinbauneumayer.at

> **Projekt:** neumayer — Relaunch Weinbau & Heuriger Neumayer, Sonnbergstraße 89, 2380 Perchtoldsdorf
> **Dokument:** Konzept, Informationsarchitektur, Design- und Content-Spezifikation (umsetzungsreif)
> **Stand:** 2026-11-05 · **Basis:** `REPORT.md` (Audit vom 2026-11-05), `PROJEKTPLAN.md`, vollständiger Mirror unter `mirror/`
> **Status:** Entwurf zur Freigabe durch Daniel Goldmann. Alle mit **[PLATZHALTER: …]** markierten Stellen sind nicht belegt und müssen vom Betrieb geliefert werden. Alle Fakten in diesem Dokument stammen aus `REPORT.md` oder aus dem Mirror (Seitentexte **und** Plakatgrafiken, die ich transkribiert habe — Quelle jeweils angegeben).

---

## §0 Executive Summary

1. **Relaunch statt Facelift:** WordPress mit `wp_nuvo`-Theme, vier Baukästen und 70 JS-Dateien wird durch eine statisch generierte Astro-Site ersetzt (kein jQuery, CSS < 50 KB, Startseite < 900 KB, LCP < 1,5 s auf 4G).
2. **Eine Frage zuerst beantworten:** „Ist heute ausg'steckt — und wenn nicht, wann wieder?“ Dafür gibt es eine Statusleiste auf jeder Seite, die automatisch aus einer Termindatei (`termine.yaml`) erzeugt wird.
3. **Der Widerspruch bei den Öffnungszeiten ist aufgelöst:** Laut den Plakaten im Mirror ist 2026 und 2027 jeweils **achtmal** ausg'steckt (2026: 177 Tage, immer Samstag bis Sonntag), nicht „bis zu zehn Mal“. Die Zeiten Mo–Sa 10:30–23:00 und So 10:30–22:30 gelten **nur während dieser Zeiträume**.
4. **Navigation von 10 auf 5 Punkte:** Termine · Speisen & Wein · Ab Hof · Feiern · Besuch & Kontakt — dazu ein fixer Button „Tisch reservieren“ und auf dem iPhone eine Aktionsleiste unten (Anrufen · Reservieren · Route).
5. **Die Besonderheiten bekommen eigene Plätze im Menü:** Fackelwanderung (eigene Seite), KOSTBAR in ROT, 24-h-Getränkeautomat, Spritzer TO GO und Heurigenboxen standen bisher nur als Textblöcke auf der Startseite. Jetzt bekommen sie eigene Seiten bzw. Abschnitte mit klaren Handlungsaufforderungen.
6. **Reservierung in 3 Schritten statt 40-Slot-Dropdown:** Es sind nur Ausstecktage wählbar. Ab 11 Personen geht's direkt zur Feieranfrage bzw. zum Anruf. Die Telefonnummer ist überall als `tel:`-Link antippbar.
7. **Local SEO von null auf vollständig:** Meta-Descriptions, Open Graph, ein sauberes H1 pro Seite, Alt-Texte, JSON-LD (`Restaurant` + `Winery` mit saisonalen Öffnungszeiten, `FoodEvent`, `Menu`) und eine 301-Weiterleitung für jede alte URL.
8. **Lesbar und zugänglich nach WCAG 2.1 AA:** Fließtext #2A211C auf #FAF6EF erreicht 14,63:1 (Bestand: #888 auf Weiß mit 3,54:1). Grundschrift 17–18 px statt 14 px, echte Formular-Labels, Skip-Link, sichtbarer Fokus.
9. **Datenschutz bleibt sauber:** kein Tracking, kein Cookie, kein Google-Maps-iframe, keine Google Fonts, kein reCAPTCHA. Gemessen wird über Search Console und anonymisierte Serverlogs.
10. **Aufwand:** ca. 136 h plus 15 % Puffer (≈ 156 h) in 9 Phasen. Ein Fotoshooting ist nötig (externe Kosten [PLATZHALTER]). Kritischer Pfad: Öffnungslogik bestätigen, Zugang zu Hosting/Domain, Bildmaterial.

### §0.1 Befund → Maßnahme (jeder Top-Befund des Audits adressiert)

| # | Befund aus `REPORT.md` | Maßnahme im Redesign | Wo spezifiziert |
|---|---|---|---|
| 1 | Keine Kompression (166 KB HTML roh) | Build erzeugt vorkomprimierte `.br`/`.gz`-Dateien; Server liefert `Content-Encoding: br`. Ziel: HTML Startseite ≤ 30 KB komprimiert. | §6.6, §6.9 |
| 2 | 0 von 36 Seiten mit Meta-Description | Pflichtfeld im Seiten-Frontmatter, Build bricht ohne Description ab; Texte für alle Seiten ausformuliert | §7.1 |
| 3 | Keine strukturierten Daten | JSON-LD `Restaurant`+`Winery` mit saisonalen `openingHoursSpecification`, `FoodEvent`, `Menu`, `BreadcrumbList` — generiert aus Datendateien | §7.2 |
| 4 | Keine Open-Graph-/Twitter-Cards | OG-Block pro Seite, eigenes 1200×630-Bild pro Seite und pro Veranstaltung (WhatsApp-Vorschau) | §7.3 |
| 5 | 39,6 MB Bilder, Einzelbild bis 2,25 MB | Bildpipeline `astro:assets`: AVIF + WebP + JPEG-Fallback, `srcset` 480–1600 w, Budget ≤ 150 KB pro Bild; Plakatgrafiken werden durch HTML-Text ersetzt | §1.4, §6.6, §6.7 |
| 6 | `http://localhost`-Bild live, Staging-URLs im RSS | Altsystem entfällt vollständig; Build-Check verbietet `localhost`, `joomexp` und `http://` in Ausgabedateien; Feeds → 410 | §6.9, §7.4 |
| 7 | Keine `tel:`-Links | `tel:+436642110825` in Header, Statusleiste, Aktionsleiste, Footer und jedem Formular; Anruf-Pfad als eigener Konversionspfad | §5.2 |
| 8 | Heading-Chaos (13 Seiten ohne H1, Startseite 6 H1) | genau ein `<h1>` pro Seite, Überschriftenhierarchie im Komponentenmodell festgelegt, automatischer Check im Build | §3, §6.8 |
| 9 | URL-Wildwuchs, Duplicate Content | eine kanonische Host-Variante (`https://www.`), Trailing-Slash-Regel, vollständige 301-Tabelle inkl. `/?p=`-IDs aus `wp-json` | §2.2, §7.4 |
| 10 | Keine Security-Header | HSTS, CSP ohne `unsafe-inline`, nosniff, Referrer-Policy, Permissions-Policy, `frame-ancestors 'none'`; WordPress-Angriffsfläche (`/wp-json/wp/v2/users`, `readme.html`) entfällt | §6.10 |

**Weitere Audit-Befunde, die ebenfalls gelöst werden:** Öffnungszeiten-Widerspruch (§2.3, §4.2), nächster Ausstecktermin nicht sichtbar (Statusleiste §3.0), Reservierungsformular mit 40+ Slots und Datum in 3 Feldern (§5.1), Newsletter-Checkbox ohne Double-Opt-in (entfernt, §5, Frage 13), Google-Maps-iframe ohne Consent (ersetzt durch statische Karte + Routen-Links, §3.9), Heurigenboxen auf fremder Domain (Integration unter `/ab-hof/`, §3.6, Frage 4), Besonderheiten nicht im Menü (§2), 26 Bilder ohne Alt-Text (Alt-Text-Pflicht im Bildschema, §4.9, §6.8), Kontrast 3,54:1 (§1.5), 14 px Grundschrift (§6.4), Platzhalter statt Labels (§4.8), kein Skip-Link, Slider ohne Pause (kein Autoplay-Slider mehr, §6.8), WooCommerce ohne Shop (entfällt, §5.3, Frage 5).

**Eine Korrektur am Audit:** `REPORT.md` §6 sagt, es gebe „keine Ansprechperson/E-Mail öffentlich“. Das stimmt nur halb. Im Impressum steht `christian[at]weinbauneumayer.at`, auf den Plakatgrafiken (Aussteckzeiten, Stelzen, Ab Hof) `christian@weinbauneumayer.at`. Das Problem ist also, dass die Adresse versteckt ist, nicht dass sie fehlt. Der Draft setzt die E-Mail auf der Seite „Besuch & Kontakt“ und auf „Feiern“ sichtbar ein (Frage 11 zur Freigabe).

---

## §1 Marken- und Positionierungsstrategie

### §1.1 Positionierung in einem Satz

> **Der Familienheurige in der Sonnbergstraße: eigener Wein aus dem eigenen Keller, Küche von Traude Neumayer, achtmal im Jahr ausg'steckt — und dazwischen für Feiern, Heurigenboxen und den Weinautomaten rund um die Uhr da.**

Der Satz ist bewusst konkret gehalten. Jeder Teil lässt sich mit dem Mirror belegen:

- „eigener Wein aus dem eigenen Keller“: `/ueber/` („von unserem hauseigenen Weinkeller“)
- Traude Neumayer als „Küchenfee“: `/ueber/`
- „achtmal im Jahr“: Plakate `ausstecken26`/`ausstecken27`
- Feiern auch außerhalb der Aussteckzeiten: `/feiern/` und die Plakate
- Automat 24 h: Startseite und `/termine/`

Die Website verkauft also keine austauschbare „Heurigen-Gemütlichkeit“, sondern drei handfeste Unterschiede: **verlässliche Termine**, **Dinge, die es nur hier gibt** (Fackelwanderung auf die Perchtoldsdorfer Heide, KOSTBAR in ROT, Stelzen-Wochenende, Engerl & Bengerl) und **Erreichbarkeit auch an Tagen ohne Ausstecken** (Automat, Ab Hof, Heurigenbox, Feiern nach Vereinbarung).

### §1.2 Zielgruppen und ihre eine Frage

| Zielgruppe | Ihre erste Frage | Was die Seite sofort liefern muss | Primärer Pfad |
|---|---|---|---|
| Wiener Tagesausflügler (Familien, Wanderer, Radfahrer) | „Haben die heute offen — und gibt's was für die Kinder?“ | Statusleiste, Öffnungszeiten heute, Gastgarten + Spielplatz + Spielecke, Anfahrt | Statusleiste → Route oder Reservieren |
| Stammgäste aus Perchtoldsdorf und Umgebung | „Wann ist das nächste Mal ausg'steckt, was ist das Schmankerl?“ | nächster Termin mit Motto (z. B. Pfandlwochen), Tagesmenü, Sonderveranstaltungen | Termine → Kalender / Anruf |
| Firmen (Weihnachtsfeier, Seminar) | „Geht das an unserem Wunschtermin, für wie viele, was kostet das?“ | Kapazität bis 200 Personen*, Räume (Stüberl, zwei Ebenen, Gastgarten), Buffet oder Menü, Ansprechperson, E-Mail | Feiern → Feieranfrage |
| Hochzeitspaare und private Feiern | „Wirkt das schön genug, und machen die was Besonderes?“ | Fotos der Räume und des Gartens, Fackelwanderung mit Blick über Wien, Ablauf einer Feier | Feiern → Fackelwanderung → Anfrage |
| Gastgeber zu Hause und im Büro | „Kann ich ein Heurigenbuffet bestellen und wie viel kostet es?“ | Heurigenboxen ab 5 Personen, Beispielpreise, Bestellanfrage | Ab Hof → Heurigenbox-Anfrage |

(*laut `/feiern/`: „abhängig davon ob die Veranstaltung während unserer Ausstecktermine stattfindet oder nicht“)

### §1.3 Tonalität

**Leitsätze**

1. **Sagen, was ist.** „Wir haben von 21. November bis 6. Dezember ausg'steckt“, nicht „Erleben Sie unvergessliche Momente“.
2. **Herzlich, nicht anbiedernd.** Wienerisch-niederösterreichische Wörter sind dort erlaubt, wo sie jeder versteht: Achterl, Gspritzter, Stelze, Gansl, Schmankerl, Stüberl, ausg'steckt. Dialekt wird nie in Navigationspunkten oder Formularfeldern verwendet, weil Gäste aus Deutschland oder Wien-Touristen diese Wörter nicht immer kennen (Audit §6, Punkt 2).
3. **Durchgehend „Sie“.** Der Bestand mischt „Sie“ und „ihr“, oft im selben Absatz (Startseite: „Wir bitten um zeitnahe Reservierung“ neben „Die Stelzen könnt ihr direkt im Lokal genießen“). Das Redesign verwendet konsequent „Sie“, weil Firmen- und Hochzeitsanfragen das tragen müssen. Die Wärme kommt aus Wortwahl und Inhalt, nicht aus dem Duzen (Alternative „ihr“: Frage 15).
4. **Familie als Absender.** Texte sind mit „wir“ geschrieben. Wo es passt, steht ein Name dabei: Christian Neumayer empfiehlt den Wein, Traude Neumayer kocht.
5. **Keine Großbuchstaben- und Ausrufezeichen-Ketten.** Im Bestand gibt es „Stelzen MÜSSEN bis !!! Donnerstag 05.11. !!! bestellt werden!“. Neu: „Bitte bis Donnerstag, 5. November, vorbestellen.“ Fristen werden im Layout hervorgehoben (Hinweisbox), nicht durch Satzzeichen.
6. **Zahlen ausschreiben, die man braucht:** Datum mit Wochentag, Uhrzeit, Personenzahl, Preis, sofern belegt. Unbelegte Preise erscheinen nicht.

**Vorher/Nachher-Beispiele (Bestand → neu)**

| Bestand | Neu |
|---|---|
| „Hier finden Sie alle Ausstecktermine, Veranstaltungen und Öffnungszeiten“ | „Achtmal im Jahr ausg'steckt. Hier steht, wann.“ |
| „Über das Jahr verteilt haben wir bis zu zehn mal für Sie geöffnet.“ | „2026 haben wir achtmal ausg'steckt, jeweils rund drei Wochen, immer von Samstag bis Sonntag.“ |
| „Wir schenken Ihnen ein Lächeln!“ | (entfällt — Aussage ohne Information) |
| „Jeder Schluck ein Genuss!“ | „Weine aus unseren eigenen Weingärten, gekeltert in unserem Keller.“ |
| „Zur Tischreservierung“ (13× auf der Startseite) | je nach Kontext: „Tisch für die Pfandlwochen reservieren“, „Für Engerl & Bengerl reservieren“ |

**Wortliste (verbindlich)**

- Ja: ausg'steckt, Ausstecken, Ausstecktermin, Heuriger, Gastgarten, Stüberl, Schank, Achterl, Spritzer, Heurigenbox, Ab Hof, Schmankerlwochen
- Nein: Location, Event-Location, Kulinarik-Erlebnis, Genusswelt, einzigartig, unvergesslich, Highlight, „Gönnen Sie sich …“

### §1.4 Bildsprache

**Grundsatz:** Echte Fotografie aus dem Betrieb. Keine Illustrationen, keine Stock-Fotos. KI-generierte Motive (siehe Kanban B-02) dürfen nur im internen Mockup als gekennzeichnete Platzhalter stehen, **niemals live**. Ein Gast, der „das Stüberl“ auf der Website sieht, muss genau dieses Stüberl vorfinden.

**Licht und Stimmung**

- **Tag:** natürliches, warmes Seitenlicht (Vormittag oder später Nachmittag), Gastgarten unter Laub, Holztische, Weingläser mit Lichtreflex. Keine überstrahlten Mittagsaufnahmen.
- **Abend:** Kerzen- und Fackellicht, warme Weißbalance (ca. 3200–3800 K), Schatten dürfen tief sein. Hier ist die Fackelwanderung das Schlüsselmotiv.
- **Farbbearbeitung:** leicht warm, zurückhaltende Sättigung, kein HDR-Look, kein Teal-Orange-Filter, keine Vignetten-Effekte.
- **Menschen:** Familie und Team mit Namen (Christian, Traude, Angelika, Friederike — laut `/ueber/`). Gäste nur mit schriftlicher Einwilligung und nicht frontal im Mittelpunkt (DSGVO, Recht am eigenen Bild).

**Shotliste für das Fotoshooting (Pflichtmotive, nach Priorität)**

1. Hausansicht Sonnbergstraße 89 mit Buschen/Ausstecktafel — Hero-Kandidat, Querformat 3:2 und Hochformat 4:5
2. Gastgarten belegt (Tisch mit Achterl, Spritzer, Brettljause), Querformat
3. Fackelwanderung: Gruppe mit Fackeln im Weingarten, Dämmerung (blaue Stunde) — Hero für `/feiern/fackelwanderung/`
4. Blick von der Perchtoldsdorfer Heide über Wien bei Dämmerung (ohne Menschen) — Panorama 21:9 und 4:5
5. Die vier Gläser der KOSTBAR in ROT auf dem Holzbrett, Draufsicht und 45° (das Bestandsfoto `weinreise-scaled-990x700.jpg` zeigt das Motiv, ist aber eine Grafik mit Text — neu fotografieren ohne Text)
6. Heurigenbox geöffnet auf Holztisch. Das Bestandsfoto `2021/03/FEZU4913-1000x700.jpg` ist brauchbar und wird bis zum Shooting weiterverwendet (zuschneiden, neu komprimieren).
7. Getränkeautomat im Eingangsbereich, mit Mensch beim Entnehmen (Größenvergleich, Echtheit)
8. Spritzer TO GO: Flasche 0,33 l mit Drehverschluss in der Hand, Gastgarten im Hintergrund
9. Stelze auf Brett mit Senf und Kren (ersetzt das 2,25-MB-Plakat `stelzeflwochenende-scaled-700x990.jpg`)
10. Gansl mit Rotkraut und Knödel; Schweinsbratenpfandl; Backhendl — je ein Teller, 45°, Holz
11. Stüberl eingedeckt für eine Feier (Kerzen, weiße Tischwäsche oder Holz — je nach Realität)
12. Beide Ebenen des Lokals, Weitwinkel, menschenleer und belebt
13. Kinderspielplatz und Spielecke (ohne erkennbare Kinder oder mit Einwilligung der Eltern)
14. Weinkeller: Fässer, Flaschenlager, Christian Neumayer bei der Arbeit
15. Weingarten im Jahreslauf (mindestens Herbstlaub; Frühling als Nachlieferung)
16. Familienporträt neu (das Bestandsfoto `2019/09/team-1446x1024.jpg` ist sieben Jahre alt, Frage 9)
17. Detail: Schank mit Gläsern, Doppler, Weinkarte auf dem Tisch
18. Engerl & Bengerl: Tisch im Kerzenschein, Teller Gansl oder Schweinsmedaillons
19. Geschenkebox (Holzbox, 2 Gläser, 1 Flasche)
20. Saisonmotive pro Schmankerlwoche (Spargel, Bärlauch, Schwammerl, Kürbis, Wild) — Nachlieferung im Jahreslauf

**Umgang mit dem Bestand**

- **Plakatgrafiken** (`ausstecken26`, `ausstecken27`, `stelzeflwochenende`, `engerlbengerlMenue`, `auszeichnung`, `abhofverkauf2`, `weinreise`, `soritzerTOGO`) werden **nicht** mehr als Inhaltsbild verwendet. Ihr Text kommt als echtes HTML auf die Seite. Grund: Text in Bildern ist für Google, Screenreader und die iPhone-Schriftvergrößerung unsichtbar. Außerdem liegen drei dieser Grafiken bei über 2 MB.
- **Galerie-Fotos 2016/2018** (`JER_*`, `DSC_*`): Ich sichte sie und übernehme höchstens 8 in den Abschnitt „Das Lokal“. Sie werden neu exportiert (≤ 150 KB, AVIF/WebP) und bekommen beschreibende Dateinamen (`stueberl-eingedeckt.jpg` statt `DSC_0653.jpg`).
- **Bildverhältnisse:** Hero 3:2 (Desktop) und 4:5 (Mobile) mit *Art Direction* über `<picture>` und eigenem Ausschnitt pro Format. Kacheln 4:3, Porträts 4:5, Panorama 21:9 nur auf Desktop.

### §1.5 Farbwelt

Die Farbwelt ist aus dem Logo (#990000, Markenrot laut Bestand) und den Materialien des Betriebs abgeleitet: Kalkputz, Holz, Rebe, Kerzenlicht, Keller. Alle Kontrastwerte habe ich nach der WCAG-2.1-Formel gerechnet. Sie sind nicht geschätzt.

| Token | Hex | Rolle | Kontrast (gerechnet) |
|---|---|---|---|
| `--c-rot` | **#990000** | Markenrot: Logo, Primär-Buttons, Links, Akzentlinien | 8,28:1 auf Papier · Weiß auf Rot 8,92:1 |
| `--c-rot-tief` | **#6E0E12** | Hover/Active der Primär-Buttons, Fußzeile, „Weinkeller“-Flächen | 11,24:1 auf Papier · Papier auf Rot-tief 10,33:1 |
| `--c-papier` | **#FAF6EF** | Seitenhintergrund (warmes Kalkweiß statt kaltem #FFF) | Basis |
| `--c-papier-2` | **#F1E9DC** | abgesetzte Sektionen, Karten, Tabellenzeilen | Text darauf 13,08:1 |
| `--c-text` | **#2A211C** | Fließtext und Überschriften (Kellerbraun statt Schwarz) | 14,63:1 auf Papier |
| `--c-text-2` | **#5C4F45** | Sekundärtext, Bildunterschriften, Metadaten (ersetzt #888) | 7,33:1 auf Papier · 6,55:1 auf Papier-2 |
| `--c-holz` | **#7A4E2D** | Eyebrows, Trennornamente, Icons | 6,60:1 auf Papier |
| `--c-rebe` | **#4A5A2A** | Status „heute offen“, Gastgarten/Natur-Akzente | 6,99:1 auf Papier · Papier-Text auf Rebe 6,43:1 |
| `--c-kerze` | **#C9952B** | nur dekorativ auf hellem Grund (2,49:1, **nie für Text auf Papier**); als Text nur auf Nacht | 6,44:1 auf Nacht · 4,51:1 auf Rot-tief |
| `--c-nacht` | **#211915** | dunkle Sektionen (Fackelwanderung, Engerl & Bengerl) | Basis dunkel |
| `--c-nacht-text` | **#F4ECDF** | Text auf Nacht | 14,75:1 |
| `--c-nacht-text-2` | **#CBBBA6** | Sekundärtext auf Nacht | 9,22:1 |
| `--c-linie` | **#D9CBB6** | dekorative Trennlinien (nicht für Bedienelemente) | 1,48:1 (rein dekorativ) |
| `--c-feld-rand` | **#7D6B5C** | Rahmen von Eingabefeldern, Checkboxen (WCAG 1.4.11 verlangt ≥ 3:1) | 4,72:1 auf Papier |
| `--c-fokus` | **#1F5FBF** | Fokusring (bewusst Blau, damit er sich vom Markenrot unterscheidet) | 5,65:1 auf Papier |
| `--c-ok` | **#2F6B34** | Erfolgsmeldungen | 5,95:1 |
| `--c-fehler` | **#A1261B** | Fehlermeldungen (immer mit Text + Icon, nie nur Farbe) | 6,94:1 |

**Regeln**

1. Rot ist eine Signalfarbe, keine Fläche. Pro Bildschirmhöhe gibt es höchstens ein großes rotes Element (in der Regel den Primär-Button). Ganzseitige rote Hintergründe gibt es nicht; Rot-tief ist nur für Footer und kleine Flächen zugelassen.
2. Die Statusleiste nutzt die Farbe *zusätzlich* zum Text: Rebe-Grün für „heute offen“, Holz für „derzeit nicht ausg'steckt“, Rot-tief für „heute schon zu“. Die Information steckt immer im Wort, nie nur in der Farbe (WCAG 1.4.1).
3. Dunkle Sektionen (Nacht) gibt es höchstens zweimal pro Seite. Sie sind den Abend-Themen vorbehalten: Fackelwanderung, Engerl & Bengerl, Kerzenschein.
4. Keine Verläufe, kein Glas-Blur, keine farbigen Schatten. Die Tiefe entsteht durch Fotografie und die Papierabstufung (Papier → Papier-2).
5. Dark Mode: in Phase 1 **nicht** angeboten (Begründung: zusätzlicher Test- und Fotoaufwand, Zielgruppe nutzt die Seite tagsüber zur Planung). `color-scheme: light` wird gesetzt, damit iOS Formularfelder nicht dunkel darstellt.

### §1.6 Typografie

**Display: Alegreya** (Juan Pablo del Peral / Huerta Tipográfica, SIL Open Font License, Variable Font 400–900)
**Text: Source Sans 3** (Paul D. Hunt / Adobe, SIL Open Font License, Variable Font 200–900)

**Warum Alegreya für Überschriften**

1. Alegreya ist eine Antiqua mit kalligrafischem Strich. Das passt zum handgezogenen „WN“ des Logos, ohne eine Schreibschrift zu sein. Der Bestand nutzt „Herr von Muellerhoff“ (Script) — die ist ab Größen unter 30 px unlesbar und auf dem iPhone kaum zu entziffern.
2. Die Schrift wirkt literarisch und bodenständig zugleich. Das ist das Gegenteil der glatten Grotesk-Headlines, die heute jede generische Landingpage hat. Fraunces und Playfair Display habe ich verworfen: Fraunces ist derzeit die Standardwahl für „warm & craft“ und wirkt deshalb austauschbar, Playfair hat mit seinem hohen Strichkontrast einen Mode- und Lifestyle-Ton.
3. Alegreya hat echte Kapitälchen (Alegreya SC) für Eyebrows wie „AUSG'STECKT IS“ und deckt ä, ö, ü, ß und Gedankenstriche sauber ab.
4. Die Mediävalziffern passen zu Fließtext-Überschriften. Für Datumsangaben in Überschriften (z. B. „21. November“) wird `font-variant-numeric: lining-nums` gesetzt.

**Warum Source Sans 3 für Text**

1. Die Schrift ist sehr gut lesbar in 15–18 px auf Retina-Displays und hat offene Formen (a, e, g sind gut unterscheidbar). Das ist wichtig für ältere Stammgäste.
2. Tabellenziffern (`tabular-nums`) lassen Zeitspannen, Uhrzeiten und Preise in Spalten sauber untereinander stehen (Terminliste, Heurigenbox-Preise).
3. Source Sans 3 ist neutral genug, um Alegreya nicht zu konkurrieren, und hat mehr Charakter als Systemschriften.

**Technik**

- Beide Schriften sind selbst gehostet (keine Google-Fonts-Verbindung → keine IP-Übermittlung). Es gibt nur `woff2`. Die Legacy-Formate `eot`/`svg`/`ttf` entfallen (Audit §3).
- Subset auf Latin + Latin-Extended-A (Deutsch, Tschechisch und Ungarisch für Namen). Geschätztes Budget: Source Sans 3 Variable (Roman) ≈ 45 KB, Source Sans 3 Italic nicht geladen (Hervorhebungen über Gewicht), Alegreya Variable (Roman) ≈ 55 KB. Gesamt ≤ 110 KB.
- Nur die Textschrift wird mit `<link rel="preload">` vorgeladen. Alegreya lädt mit `font-display: swap`. Damit beim Tausch nichts springt, gibt es eine Fallback-Metrik-Anpassung (`size-adjust`, `ascent-override`) auf Georgia bzw. Arial.

### §1.7 Logo

- Das bestehende **WN-Stempel-Logo** („Weinbau Christian Neumayer · 2380 Perchtoldsdorf“, rot, rund, Pinselstrich) bleibt. Es ist im Ort bekannt, steht auf Flaschen, Heurigenboxen und Plakaten und hat Charakter.
- **Benötigt:** Vektordatei (SVG/AI/PDF) von der Agentur oder vom Betrieb (Frage 23). Im Mirror liegt nur `Logo-Neumayer_rot.png` (38 KB). Falls keine Vektordatei existiert, wird das Logo nachgezeichnet (ca. 2 h, in §9 enthalten).
- **Varianten:** (a) Rot #990000 auf Papier, (b) Papier #F4ECDF auf Rot-tief und Nacht, (c) einfarbig Kellerbraun für den Druck-Stylesheet.
- **Mindestgröße:** 48 px Durchmesser (darunter ist der Kreisschriftzug nicht lesbar). Für den Header auf Mobile kommt deshalb ein **Wortmarken-Lockup** zum Einsatz: Stempel 40 px + „Heuriger Neumayer“ in Alegreya 20 px. Der Kreistext darf dabei unlesbar sein, die Wortmarke trägt den Namen.
- **Schutzzone:** ¼ des Durchmessers rundherum. Das Logo steht nie direkt auf unruhigen Fotos.

### §1.8 Anti-Slop-Regeln (verbindlich für Design und Umsetzung)

1. Kein Verlaufs-Hero, kein „Glassmorphism“, kein Blur hinter Karten, keine Neon- oder Pastellflächen.
2. Keine Emoji in Navigation, Überschriften oder Buttons. Im Fließtext ebenfalls nicht (der Bestand nutzt ein Zwinker-Emoji in Überschriften und lädt ein Emoji-Bild vom Facebook-CDN).
3. Keine Icon-Raster mit drei generischen Kacheln („Freundliches Team / Aromatische Weine / Hausgemachtes Essen“). Stattdessen konkrete Inhalte mit Foto.
4. Keine Auto-Slider und Karussells mit Autoplay (Audit: „Slider ohne Pause-Steuerung“). Bildreihen sind horizontal wischbar (CSS Scroll-Snap) und starten nie von selbst.
5. Keine Einblend-Animationen beim Scrollen. Erlaubt sind nur Übergänge ≤ 200 ms bei Interaktionen, und `prefers-reduced-motion` wird respektiert.
6. Keine Pop-ups, kein Newsletter-Overlay, kein Chat-Widget.
7. Ornamentik ist sparsam und aus dem Material abgeleitet: eine feine Linie in Holzbraun, ein kleiner Rebzweig als Trennzeichen (als SVG gezeichnet, ≤ 1 KB). Sie wird nicht als Hintergrundmuster gekachelt.

---

## §2 Informationsarchitektur

### §2.1 Neue Hauptnavigation (5 Punkte + 1 Aktion)

| # | Label | URL | Was dahinter liegt |
|---|---|---|---|
| 1 | **Termine** | `/termine/` | Ausstecktermine 2026 und 2027 mit Motto, Öffnungszeiten während des Aussteckens, Sonderveranstaltungen (Stelzen-Wochenende, Engerl & Bengerl), Kalender-Download (.ics) |
| 2 | **Speisen & Wein** | `/speisen/` (mit Unterseite `/weine/`) | Speisekarte, aktuelle Schmankerlwochen, Tagesmenü; Weine, KOSTBAR in ROT, Prämierungen |
| 3 | **Ab Hof** | `/ab-hof/` | 24-h-Getränkeautomat, Wein im Karton, Geschenkebox, Spritzer TO GO, Heurigenboxen mit Bestellanfrage, Weinlieferung nach Vereinbarung |
| 4 | **Feiern** | `/feiern/` (mit Unterseite `/feiern/fackelwanderung/`) | Firmenfeier, Hochzeit, Seminar, Geburtstag; Räume; Fackelwanderung; Feieranfrage |
| 5 | **Besuch & Kontakt** | `/besuch/` | Anfahrt, das Lokal (zwei Ebenen, Stüberl, Gastgarten, Spielplatz), Familie & Team, Kontakt, Fotoauswahl |
| — | **Tisch reservieren** (Button) | `/reservierung/` | 3-Schritt-Reservierung |

**Verhalten**

- **Desktop (≥ 960 px):** Alle fünf Punkte stehen sichtbar in einer Zeile, rechts daneben der rote Button „Tisch reservieren“. Es gibt **keine Hover-Dropdowns**. „Speisen & Wein“ und „Feiern“ verlinken auf ihre Übersichtsseiten. Die Unterseiten erreicht man über eine Unternavigation am Seitenkopf (Segmente „Speisekarte · Saisonales · Tagesmenü · Weine“ bzw. „Feiern · Fackelwanderung“).
- **Mobile (< 960 px):** Im Header stehen Logo-Lockup links und rechts zwei Elemente: „Reservieren“ (Text-Button, 44 px hoch) und „Menü“ (Text + Icon, 44 × 44 px). „Menü“ öffnet eine vollflächige Navigationsebene als `<dialog>`: fünf Punkte in Alegreya 28 px mit je 56 px Zeilenhöhe, darunter Telefonnummer, Adresse und Statuszeile. Schließen über „Schließen“-Button, Escape oder Wischen ist nicht nötig — der Button reicht und ist 44 px groß.
- **Aktionsleiste Mobile:** fix am unteren Rand, 3 gleich breite Buttons — **Anrufen** (`tel:`), **Reservieren**, **Route** (Apple-Karten-Link). Höhe 56 px + `env(safe-area-inset-bottom)`. Sie erscheint nach 200 px Scrolltiefe oder sofort auf Unterseiten. Auf `/reservierung/` und in Formularen wird sie ausgeblendet, damit sie die Tastatur und den Absenden-Button nicht verdeckt.
- **Warum „Termine“ statt „Ausgsteckt'is“:** Das Audit (§6, Punkt 2) hat festgestellt, dass Nicht-Einheimische den Begriff nicht verstehen. „Ausg'steckt is“ bleibt erhalten — als Eyebrow und Überschrift auf der Terminseite und in der Statusleiste. Dort ist es Atmosphäre, nicht Orientierung.

### §2.2 Sitemap alt → neu

| Alte URL (Bestand) | Inhalt alt | Neue URL | Aktion | HTTP |
|---|---|---|---|---|
| `/` | Lange Scroll-Seite: Termine, Save the Date, KOSTBAR, Automat, Heurigenboxen, Spritzer TO GO, Aussteckzeiten als Bild | `/` | neu aufgebaut, Inhalte nur noch als Teaser mit Link zur jeweiligen Fachseite | 200 |
| `/termine/` („Ausgsteckt'is“) | Aktuelles Ausstecken, Öffnungszeiten, Hinweis Feiern | `/termine/` | bleibt; Terminliste aus `termine.yaml`, Öffnungszeiten, Veranstaltungen | 200 |
| — (nur auf der Startseite) | Stelzen-Wochenende, Engerl & Bengerl | `/termine/stelzen-wochenende-2026-11/`, `/termine/engerl-bengerl-2026/` | neu: eigene Detailseite pro Sonderveranstaltung (teilbar, `FoodEvent`-Schema) | 200 |
| `/speisen/` | Speisekarte (ohne Preise) | `/speisen/` | bleibt; Abschnitte Speisekarte, `#saison`, `#tagesmenue` | 200 |
| `/schmankerl/` | Gansl- und Wildwochen | `/speisen/#saison` | zusammengelegt | 301 |
| `/speisen/tagesmenues/` | Tagesmenüs als Liste + PDF | `/speisen/#tagesmenue` | zusammengelegt | 301 |
| `weinbauneumayer.at/tagesmenues/` (Host ohne www) | Duplikat | `/speisen/#tagesmenue` | zusammengelegt | 301 |
| `/weine/` | Weinliste mit Notizen | `/weine/` | bleibt; ergänzt um KOSTBAR in ROT, Prämierungen | 200 |
| — (nur auf der Startseite) | KOSTBAR in ROT | `/weine/#kostbar` | neu verortet | — |
| — (nur auf der Startseite) | Getränkeautomat, Spritzer TO GO, Heurigenboxen (Link auf heurigenbox.at) | `/ab-hof/` (`#automat`, `#spritzer`, `#heurigenbox`, `#geschenkebox`) | neu | 200 |
| `/feiern/` | Feiern, Leistungen, Fackelwanderung | `/feiern/` | bleibt; Fackelwanderung ausgegliedert | 200 |
| — (Abschnitt auf `/feiern/`) | Fackelwanderung | `/feiern/fackelwanderung/` | neu: eigene Seite | 200 |
| `/ueber/` | Über uns, Team | `/besuch/#familie` | zusammengelegt | 301 |
| `/galerie/` | 30 Fotos | `/besuch/#lokal` | zusammengelegt (kuratierte Auswahl) | 301 |
| `/kontakt/` | Doppeltes Kontaktformular, Maps-iframe | `/besuch/#kontakt` | zusammengelegt | 301 |
| `/reservierung/` | Redi-Formular | `/reservierung/` | bleibt; 3-Schritt-Formular | 200 |
| `/reservierung` (ohne Slash) | Duplikat | `/reservierung/` | Slash-Normalisierung | 301 |
| `/impressum/` | Impressum + veralteter Datenschutztext | `/impressum/` | bleibt; Datenschutztext wandert nach `/datenschutz/` | 200 |
| `/datenschutz/` | Datenschutzerklärung | `/datenschutz/` | bleibt; neu geschrieben (keine Facebook-Plugins, keine Maps, keine Cookies) | 200 |
| `/pointofsale_category/weine/` | Theme-Duplikat | `/weine/` | entfernt | 301 |
| `/pointofsale_category/essen/` | Theme-Duplikat | `/speisen/` | entfernt | 301 |
| `/pointofsale_category/team/`, `/pointofsale/friendly/` | Theme-Reste | `/besuch/#familie` | entfernt | 301 |
| `/?p=…` / `/?page_id=…` (13 IDs) | Shortlinks | jeweilige neue URL (Tabelle §7.4) | entfernt | 301 |
| `/feed/`, `/comments/feed/`, `/ueber/feed/` | RSS mit Staging-URLs | — | entfällt | 410 |
| `/wp-json/…`, `/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`, `/readme.html`, `/license.txt` | WordPress-Interna | — | entfällt | 410 |
| `/wp-content/uploads/2026/09/menueoktober26-1.pdf` | Tagesmenü-PDF | `/speisen/#tagesmenue` | ersetzt | 301 |
| `/wp-content/uploads/…` (übrige Bilder) | Bilddateien | — | entfällt | 410 |
| — | — | `/danke/reservierung/`, `/danke/anfrage/` | neu, `noindex` | 200 |
| — | — | `/404` | eigene Fehlerseite mit Statuszeile und Links | 404 |

**Neue Sitemap (indexierbar, 11 Seiten + Veranstaltungsseiten)**

```
/
├── termine/
│   └── {veranstaltung-slug}/        (generiert aus termine.yaml, nur zukünftige)
├── speisen/                         (#karte, #saison, #tagesmenue)
├── weine/                           (#weiss, #rot, #frizzante, #kostbar, #praemierungen)
├── ab-hof/                          (#automat, #wein, #geschenkebox, #spritzer, #heurigenbox)
├── feiern/
│   └── fackelwanderung/
├── besuch/                          (#anfahrt, #lokal, #familie, #kontakt)
├── reservierung/
├── impressum/
└── datenschutz/
```

### §2.3 Begründung jedes Schnitts

1. **„Speisen“, „Schmankerl“ und „Tagesmenüs“ → eine Seite `/speisen/`.** Der Gast fragt „Was gibt's zu essen?“ und nicht „Ist das ein Schmankerl oder ein Tagesmenü?“. Drei Seiten mit je einem Absatz Querverweis („Bitte beachten Sie auch unsere …“) sind ein Zeichen dafür, dass die Inhalte zusammengehören. Auf der neuen Seite steht das zeitlich Relevante oben (aktuelle Schmankerlwochen, Tagesmenü dieser Woche), die ständige Karte darunter. Nebeneffekt: Der veraltete Satz „Wir sind ab dem 08.06.2019 mit unseren Schwammerl-Wochen wieder für Sie da“, der heute noch auf `/schmankerl/` **und** `/tagesmenues/` steht, verschwindet. Künftig wird dieser Text aus der Termindatei erzeugt und kann nicht mehr veralten.
2. **„Weine“ bleibt eigene Seite, aber unter „Speisen & Wein“.** Wein ist das Kernprodukt des Weinbaus und ein eigenes Suchthema („Rotgipfler Thermenregion“, „Gemischter Satz Perchtoldsdorf“). Eine eigene URL hält die bestehenden Rankings. Im Menü gehört sie zu den Speisen, weil der Gast beides gleichzeitig plant.
3. **Neuer Punkt „Ab Hof“.** Die stärksten Alleinstellungsmerkmale — 24-h-Automat, Spritzer TO GO, Heurigenbox, Geschenkebox, Weinlieferung — kamen im Menü bisher nicht vor (Audit §5.2). Sie haben eines gemeinsam: Man bekommt sie **auch dann, wenn nicht ausg'steckt ist**. Damit hat die Seite an rund 188 Tagen im Jahr (365 − 177 Ausstecktage 2026) eine Antwort auf „Und was jetzt?“. Das ist auch der Ort für eine spätere Bestellstrecke (Frage 5).
4. **„Über uns“, „Galerie“ und „Kontakt“ → „Besuch & Kontakt“.** Alle drei beantworten die Frage „Wie ist es dort und wie komme ich hin?“. Die Galerie mit 30 unsortierten Bildern ersetzt eine kuratierte Bildreihe mit Bildunterschriften („Das Stüberl, eingedeckt für eine Feier“ statt `DSC_0653`) im Abschnitt „Das Lokal“. Das Team bekommt dort einen Abschnitt mit Namen und Rollen aus `/ueber/`. Kontakt war auf zwei Seiten doppelt vorhanden (`/kontakt/` hat das Formular zweimal) — jetzt gibt es ihn einmal.
5. **„Reservierung“ wird vom Menüpunkt zum Button.** Reservieren ist eine Handlung, kein Thema. Als roter Button rechts im Header und als Teil der mobilen Aktionsleiste ist sie auf jeder Seite einen Tap entfernt — besser als ein zehnter Menüpunkt in derselben Optik wie „Galerie“.
6. **Fackelwanderung bekommt eine eigene Seite.** Sie ist das emotionalste Motiv des Betriebs (Fackeln, Weingarten, Blick über ganz Wien) und ein eigener Suchbegriff („Fackelwanderung Perchtoldsdorf“, „Firmenfeier mit Fackelwanderung Wien“). Als Absatz auf `/feiern/` ist sie nicht teilbar und nicht auffindbar.
7. **Sonderveranstaltungen bekommen Detailseiten.** Stelzen-Wochenende und Engerl & Bengerl werden heute per WhatsApp und Facebook weitergeleitet (Audit §0). Ein Link auf die Startseite landet aber in einer langen Scroll-Seite, deren Inhalt sich wöchentlich ändert. Eine Detailseite pro Veranstaltung hat ein eigenes Vorschaubild, Datum, Menü, Preis und Reservierungsknopf. Nach dem Termin wird sie automatisch auf `noindex` gesetzt und leitet 90 Tage später per 301 auf `/termine/` um (§7.4).
8. **Impressum und Datenschutz werden getrennt.** Das Impressum enthält heute einen veralteten Datenschutzabsatz und einen Abschnitt zu Facebook-Plugins, die es nach dem Relaunch nicht mehr gibt. Ein falscher Datenschutzhinweis ist ein rechtliches Risiko.
9. **WooCommerce, Events Manager, NextGEN, Jetpack, MC4WP und Co. entfallen ersatzlos.** Keines davon hat eine sichtbare Funktion, die nicht schlanker gelöst wird (Audit §2). Das nimmt 416 KB (`rs6.min.js`) + 428 KB (`events-manager.js`) + 729 KB (`js_composer.css`) aus jeder Seite.

### §2.4 URL- und Host-Konventionen

- **Kanonischer Host:** `https://www.weinbauneumayer.at` (bisheriger Canonical, steht so auf Plakaten, Flaschenetiketten und Facebook — keine Umstellung auf die Domain ohne www, weil das ohne Nutzen Risiko schafft).
- `http://weinbauneumayer.at`, `http://www.…` und `https://weinbauneumayer.at` gehen in **einem einzigen Sprung** per 301 auf `https://www.weinbauneumayer.at/…` (heute: Klartext-Zwischenschritt mit 302, Audit §5.4).
- Alle Seiten-URLs enden mit `/`. URLs ohne Slash werden per 301 ergänzt.
- Slugs sind deutsch, klein geschrieben und mit Bindestrich: `ab-hof`, `fackelwanderung`. Umlaute werden aufgelöst (ä→ae), damit WhatsApp- und SMS-Links nicht brechen.
- Anker-IDs sind stabil und dokumentiert (`#saison`, `#tagesmenue`, `#kostbar`, `#heurigenbox`, `#anfahrt`, `#kontakt`), weil die 301-Ziele darauf zeigen.

### §2.5 Footer-Struktur

1. **Spalte „Heuriger Neumayer“:** Logo (Papier-Variante auf Rot-tief), Adresse, Telefon als Link, E-Mail als Link
2. **Spalte „Nächstes Mal ausg'steckt“:** die nächsten zwei Aussteckzeiträume mit Motto, Link „Alle Termine“
3. **Spalte „Ab Hof“:** „Getränkeautomat im Eingangsbereich, täglich 24 Stunden“, Link „Ab Hof“
4. **Spalte „Seiten“:** alle 5 Hauptpunkte + Reservierung
5. **Unterzeile:** © Weinbau & Heuriger Neumayer · Impressum · Datenschutz · Facebook (Text-Link, kein Plugin)

Den Hinweis „Programmiert von Jeromedia.eu“ übernehme ich nicht. Ob eine Credit-Zeile für die neue Umsetzung gewünscht ist, klärt Frage 24.

---

## §3 Seitenkonzept

**Lesart der Spezifikation:** Jede Sektion ist in der Reihenfolge der Seite aufgeführt und mit Nummer versehen. Für jede Sektion stehen **Zweck**, **Inhalt**, **CTA**, **Bild** sowie **Desktop** und **Mobile**. Die Überschriftenebene steht in Klammern (H1/H2/H3). Die ausformulierten Texte stehen in §4, hier stehen Struktur und Verhalten.

### §3.0 Globale Elemente (auf allen Seiten)

**G1 — Skip-Link.** Der erste fokussierbare Link „Zum Inhalt springen“ ist nur bei Tastaturfokus sichtbar und springt zu `<main id="inhalt">`.

**G2 — Statusleiste („Heute“-Leiste).**
- *Zweck:* beantwortet auf jeder Seite die Hauptfrage (Audit §5.2: „Nächster Ausstecktermin nicht dauerhaft oben sichtbar“).
- *Inhalt:* Sie hat vier Zustände, die aus `termine.yaml` und der aktuellen Uhrzeit (Europe/Vienna) berechnet werden:
  1. **heute offen** — Rebe-Grün, Text „Heute ausg'steckt · offen bis 23:00 · {Motto} bis {Enddatum}“
  2. **heute schon zu, morgen offen** — Rot-tief, „Für heute ist Sperrstunde · morgen ab 10:30 wieder offen“
  3. **derzeit nicht ausg'steckt** — Holz, „Derzeit nicht ausg'steckt · nächstes Mal ab {Wochentag}, {Datum}: {Motto} · Getränkeautomat 24 h offen“
  4. **letzter Tag** — Rebe-Grün mit Zusatz „Heute letzter Tag der {Motto}“
- *CTA:* Der ganze Balken ist ein Link auf `/termine/`. Rechts steht im Zustand 1 zusätzlich „Anrufen“ (`tel:`).
- *Technik:* Der Build berechnet den Zustand für den Build-Zeitpunkt. Ein Inline-Skript (≤ 1,5 KB, ohne Bibliothek) rechnet beim Laden mit der Geräteuhr neu, damit eine Seite aus dem Cache nicht „offen“ anzeigt, wenn schon zu ist. Ohne JavaScript zeigt die Leiste die nächsten Termine als Text, ohne Live-Zustand („Nächstes Ausstecken: …“). Zusätzlich wird die Site täglich um 00:05 Uhr neu gebaut (geplanter CI-Lauf), damit auch die Version ohne JS stimmt.
- *Desktop:* eine Zeile, 40 px hoch, zentriert über dem Header.
- *Mobile:* eine Zeile, 44 px hoch (Touch-Target). Lange Texte werden gekürzt auf „Heute offen bis 23:00 · Wild- & Ganslwochen“. Die Leiste ist nicht sticky, damit sie nicht dauerhaft Platz kostet. Sticky ist stattdessen die Aktionsleiste unten.
- *A11y:* `role="status"` wird **nicht** gesetzt (sonst würde der Screenreader es bei jedem Seitenaufruf vorlesen). Es ist ein normaler Link mit vollständigem Text.

**G3 — Header.**
- *Desktop:* Logo-Lockup links (Stempel 56 px + Wortmarke), Navigation mittig/rechts, roter Button „Tisch reservieren“. Höhe 80 px. Beim Scrollen verkleinert er sich nicht (kein Layout-Sprung, kein Scroll-Listener).
- *Mobile:* 64 px hoch, Logo-Lockup 40 px, rechts „Reservieren“ und „Menü“. Oben gibt es `padding-top: env(safe-area-inset-top)` für die iPhone-Notch bei `viewport-fit=cover`.
- Die aktuelle Seite ist in der Navigation mit `aria-current="page"` und einer 2-px-Unterstreichung in Rot markiert.

**G4 — Mobile Aktionsleiste.** Siehe §2.1. Die drei Buttons sind je ≥ 56 px hoch, Icon + Text, nie nur ein Icon. „Route“ öffnet `https://maps.apple.com/?daddr=Sonnbergstra%C3%9Fe+89,+2380+Perchtoldsdorf`. Safari auf iOS öffnet damit Apple Karten, andere Geräte bekommen die Web-Ansicht. Eine Google-Maps-Alternative steht auf `/besuch/#anfahrt`.

**G5 — Footer.** Siehe §2.5. Hintergrund Rot-tief, Text Papier (10,33:1).

**G6 — Abschluss-Band „Reservieren“** am Ende jeder Inhaltsseite. Es ersetzt die 13 identischen „Zur Tischreservierung“-Buttons des Bestands durch **ein** kontextbezogenes Band: Überschrift (H2) + ein Satz + zwei Buttons (Reservieren / Anrufen). Auf `/feiern/` lautet es stattdessen „Feier anfragen“, auf `/ab-hof/` „Heurigenbox anfragen“.

---

### §3.1 Startseite `/`

Ziel der Seite: In 5 Sekunden ist klar, ob offen ist, was es gerade gibt und wie man reserviert. In 30 Sekunden versteht man, warum gerade dieser Heurige. Die Seite ist **kein** Inhaltsspeicher mehr — jeder Block verlinkt auf seine Fachseite.

**S1 — Hero (H1).**
- *Zweck:* Ort und Absender zeigen, Hauptaktion anbieten.
- *Inhalt:* Eyebrow „Weinbau & Heuriger in Perchtoldsdorf“, H1, Subline (2 Sätze), zwei Buttons, darunter eine Faktenzeile: „Sonnbergstraße 89 · 0664 211 08 25 · Gastgarten · Spielplatz“.
- *CTA:* Primär „Tisch reservieren“, sekundär „Ausstecktermine“. Die Telefonnummer in der Faktenzeile ist ein `tel:`-Link.
- *Bild:* Hausansicht mit Ausg'steckt-Buschen oder Gastgarten belegt (Shotliste 1/2). LCP-Element, `fetchpriority="high"`, kein Lazy-Loading.
- *Desktop:* Zweispaltig: Text links (5/12), Foto rechts (7/12), Foto im Format 3:2 bis zur Rasterkante. **Text liegt nicht auf dem Foto** — keine Lesbarkeitsprobleme, kein dunkles Overlay.
- *Mobile:* Foto oben 4:5 auf voller Breite (max. 60 vh), darunter Text und Buttons untereinander (volle Breite, 52 px hoch).

**S2 — „Jetzt ausg'steckt“ bzw. „Nächstes Mal ausg'steckt“ (H2).**
- *Zweck:* der aktuelle oder nächste Zeitraum im Detail.
- *Inhalt:* Motto (z. B. „Pfandlwochen“), Zeitraum mit Wochentagen („Sa, 21. November – So, 6. Dezember 2026“), Öffnungszeiten (Mo–Sa 10:30–23:00, So 10:30–22:30), 3–4 Gerichte aus der Saisonkarte (aus `speisen.yaml`, Abschnitt Saison), Link „Ganze Saisonkarte“.
- *CTA:* „Für die {Motto} reservieren“ → `/reservierung/?datum={erster Tag}`. Dazu „In den Kalender“ (.ics-Download des Zeitraums).
- *Bild:* Saisonmotiv (Shotliste 20). Fehlt eins, gibt es keinen Bildplatz, sondern eine typografische Lösung (großes Motto in Alegreya).
- *Desktop:* Karte auf Papier-2, links Datum groß (Alegreya 48 px, Tabellenziffern), rechts Gerichte.
- *Mobile:* einspaltig, Datum oben.

**S3 — Sonderveranstaltungen (H2 „Was heuer noch ansteht“).**
- *Zweck:* datierte Veranstaltungen verkaufen, die ein eigenes Reservierungs- oder Vorbestellfenster haben.
- *Inhalt:* bis zu 3 Karten aus `termine.yaml` (`typ: veranstaltung`), jeweils Datum, Titel, ein Satz, Frist (falls vorhanden, z. B. „Vorbestellung bis Do, 5. November“), Preis (falls belegt, z. B. „Menü € 41“).
- *CTA pro Karte:* „Details & reservieren“ → Detailseite.
- *Bild:* je Karte ein Foto 4:3 (Engerl & Bengerl: Kerzenschein; Stelze: Teller).
- *Desktop:* 3 Spalten (bei einer Veranstaltung: eine breite Karte).
- *Mobile:* untereinander, keine horizontale Scroll-Reihe (Termine darf man nicht übersehen).
- *Leerzustand:* Gibt es keine kommende Veranstaltung, entfällt die Sektion komplett. Es erscheint kein „Derzeit keine Veranstaltungen“.

**S4 — „Was es nur bei uns gibt“ (H2).**
- *Zweck:* die Besonderheiten sichtbar machen (Audit §5.2).
- *Inhalt:* vier Blöcke mit Foto und je 2 Sätzen: (1) Fackelwanderung auf die Perchtoldsdorfer Heide, (2) KOSTBAR in ROT, (3) Getränkeautomat 24 h, (4) Heurigenbox ab 5 Personen.
- *CTA pro Block:* Textlink zur Fachseite („Mehr zur Fackelwanderung“, „Zur Weinkarte“, „Ab Hof“, „Heurigenbox anfragen“).
- *Bild:* Shotliste 3, 5, 7, 6.
- *Desktop:* Raster 2 × 2. Die Fackelwanderung ist als großer Block in Nacht-Optik hervorgehoben (spannt über 2 Spalten, Foto 21:9).
- *Mobile:* untereinander; die Fackelwanderung zuerst, Foto 4:5.

**S5 — Wein (H2 „Aus unserem Keller“).**
- *Zweck:* Weinkompetenz und Auszeichnungen belegen, ohne Medaillen-Bildchen.
- *Inhalt:* 3 hervorgehobene Weine mit Prämierung als Text (z. B. „Gemischter Satz 2025, Thermenregion DAC — Gold, Frankfurt International Trophy 2026“; Quelle: Grafik `auszeichnung-scaled-700x990.jpg`, **vor Veröffentlichung vom Betrieb bestätigen**, Frage 7). Ein Satz von Christian Neumayer als Zitat [PLATZHALTER: Zitat freigeben lassen].
- *CTA:* „Alle Weine & Prämierungen“ → `/weine/`.
- *Bild:* Keller oder Christian Neumayer (Shotliste 14).
- *Desktop:* Foto links, Liste rechts. *Mobile:* Foto oben, Liste darunter.

**S6 — Feiern (H2 „Ihre Feier bei uns“).**
- *Zweck:* Firmen- und Hochzeitsanfragen anstoßen.
- *Inhalt:* 3 Fakten als kurze Zeilen: „bis zu 200 Gäste*“, „Stüberl, zwei Ebenen, Gastgarten“, „auch wenn nicht ausg'steckt ist“, dazu eine Fußnote zur Kapazität.
- *CTA:* „Feier anfragen“ → `/feiern/#anfrage`; Textlink „So läuft eine Feier bei uns ab“.
- *Bild:* Stüberl eingedeckt (Shotliste 11).

**S7 — Familie (H2 „Seit 40 Jahren Familie Neumayer“).**
- *Inhalt:* 3 Sätze und ein Porträt. Namen mit Rolle in einer Zeile.
- *CTA:* „Lernen Sie uns kennen“ → `/besuch/#familie`.

**S8 — Anfahrt kurz (H2 „So finden Sie uns“).**
- *Inhalt:* Adresse, statische Kartengrafik (§3.9), Buttons „Route planen“ und „Anrufen“, Hinweis zu Öffis und Parken [PLATZHALTER: Öffi-Anbindung, Parkmöglichkeiten, Radabstellplätze — vom Betrieb].
- *Mobile:* Die Karte ist 16:9 und als Ganzes ein Link zur Route.

**S9 — Abschluss-Band** (G6) mit „Tisch reservieren“.

**H-Struktur Startseite:** 1 × H1 (Hero), 7 × H2 (S2–S8), H3 nur innerhalb von S3/S4/S5. Im Bestand waren es 6 × H1.

---

### §3.2 Termine `/termine/`

**T1 — Seitenkopf (H1 „Ausstecktermine 2026 und 2027“).** Eyebrow „Ausg'steckt is“. Lead: achtmal im Jahr, jeweils rund drei Wochen, Öffnungszeiten. Kein Foto im Kopf — die Termine sind der Inhalt. Mobile: Lead ≤ 3 Zeilen.

**T2 — Öffnungszeiten während des Aussteckens (H2).**
- *Inhalt:* Tabelle „Montag bis Samstag 10:30–23:00 · Sonntag und Feiertag 10:30–22:30“ [PLATZHALTER: Gilt die Sonntagszeit auch an Feiertagen? Frage 1]. Darunter ein Satz: „Außerhalb der Aussteckzeiten: Getränkeautomat im Eingangsbereich täglich 24 Stunden, Ab-Hof-Verkauf und Feiern nach Vereinbarung.“
- *CTA:* „Anrufen“ (`tel:`).
- *Desktop/Mobile:* Definitionsliste (`<dl>`), keine Bildgrafik.

**T3 — Terminliste (H2 „2026“ / H2 „2027“).**
- *Inhalt:* pro Zeitraum eine Zeile: Motto, Zeitraum mit Wochentagen, Status-Badge („jetzt“, „vorbei“, „als Nächstes“). Vergangene Zeiträume des laufenden Jahres sind gedimmt (Text-2) und eingeklappt („Bereits vorbei: 6 Zeiträume anzeigen“, `<details>`). Daten laut Plakaten im Mirror:

| 2026 | Motto | 2027 |
|---|---|---|
| Sa 03.01. – So 25.01. | Rindfleischwochen | Mi 06.01. – So 24.01. |
| Sa 28.02. – So 22.03. | Schnitzel- & Bärlauchwochen | Sa 20.02. – So 14.03. |
| Sa 18.04. – So 10.05. | Spargelwochen | Sa 10.04. – So 02.05. |
| Sa 06.06. – So 28.06. | Schwammerlwochen | Sa 05.06. – So 27.06. |
| Sa 25.07. – So 16.08. | Kürbis- & Burgerwochen | Sa 24.07. – So 15.08. |
| Sa 05.09. – So 27.09. | Wild- & Burgerwochen | Sa 04.09. – So 26.09. |
| Sa 17.10. – So 08.11. | Wild- & Ganslwochen | Sa 09.10. – Mo 01.11. |
| Sa 21.11. – So 06.12. | Pfandlwochen | Sa 20.11. – So 05.12. |

  (Wochentage von mir aus den Daten berechnet. Quelle: `wp-content/uploads/2025/11/ausstecken26-scaled-1150x800.jpg`, `…/2026/09/ausstecken27-1-scaled-1150x800.jpg`.)
- *CTA pro Zeile:* „Reservieren“ (nur bei zukünftigen) und „In den Kalender“ (.ics pro Zeitraum). Ganz oben: „Alle Termine 2027 in den Kalender“ (eine .ics mit 8 Einträgen) — praktisch für Stammgäste.
- *Desktop:* Tabelle mit 4 Spalten (Zeitraum · Motto · Status · Aktion).
- *Mobile:* Jede Zeile ist eine Karte: Motto als H3, Datum darunter, zwei Buttons nebeneinander (je ≥ 44 px). Keine horizontal scrollende Tabelle.

**T4 — Veranstaltungen (H2 „Besondere Abende und Wochenenden“).** Karten wie Startseite S3, aber alle zukünftigen Veranstaltungen. Vergangene stehen in einer eingeklappten Liste.

**T5 — Hinweis Feiern (H2 „Ihr Termin ist nicht dabei?“).** Ein Satz + CTA „Feier anfragen“.

**T6 — Abschluss-Band.**

### §3.3 Veranstaltungs-Detailseite `/termine/{slug}/` (Template)

**V1 — Kopf (H1 = Titel der Veranstaltung).** Datum mit Wochentag, Uhrzeit [PLATZHALTER, falls nicht bekannt: „ab Öffnung“], Preis (falls belegt). Foto 3:2/4:5.
**V2 — Frist-Box** (nur wenn `vorbestellung_bis` gesetzt ist): auffällige Box mit Holz-Rand: „Bitte bis Donnerstag, 5. November, vorbestellen.“ Ist die Frist vorbei, ändert sich der Text automatisch in „Vorbestellfrist abgelaufen — rufen Sie uns an, vielleicht geht's noch.“
**V3 — Beschreibung + Menü (H2).** Bei Engerl & Bengerl zwei Spalten „Menü Engerl“ / „Menü Bengerl“ (Mobile untereinander), darüber „Jedes Menü beinhaltet: 1 Glas Frizzante, Gruß aus der Küche, 3-Gänge-Menü“.
**V4 — CTA:** „Für diesen Abend reservieren“ → `/reservierung/?datum=2026-11-28&anlass=engerl-bengerl` + „Anrufen“. Beim Stelzen-Wochenende zusätzlich „Stelzen zum Abholen vorbestellen“ → Anruf oder E-Mail mit vorausgefülltem Betreff (`mailto:christian@weinbauneumayer.at?subject=Stelzen-Vorbestellung%207.%2F8.%20November`).
**V5 — „Teilen“**: ein Button, der `navigator.share()` nutzt (iOS-Teilen-Menü → WhatsApp). Fallback ist „Link kopieren“. Keine Social-Plugins.
**V6 — Mehr Termine** (3 nächste Ausstecktermine) + Abschluss-Band.

### §3.4 Speisen `/speisen/`

**SP1 — Kopf (H1 „Speisen“).** Lead: „Alles aus unserer Küche — täglich frisch gekocht, dazu wechselnde Schmankerl je nach Saison.“ Darunter die **Unternavigation** als Segmente (sticky unter dem Header, 48 px): Saisonales · Tagesmenü · Speisekarte · Weine (→ `/weine/`). Auf Mobile ist die Segmentleiste horizontal wischbar mit sichtbarem Anschnitt rechts.

**SP2 — Saisonales (H2 „{Motto}: unsere Schmankerl bis {Enddatum}“, Anker `#saison`).**
- *Inhalt:* während eines Aussteckens die Saisonkarte (z. B. Wild- & Ganslwochen: Ganslsuppe mit Knödel, Gansl mit Rotkraut und Kartoffelknödel, gespickter Hirschbraten, Wildschweinbraten mit Specklinsen, Gamsgulasch, Wildragout; vegetarisch/vegan: veganes Schnitzerl, veganes Cevapcici; süß: Schokokuchen mit flüssigem Kern, drei Waffelvarianten — Quelle `/schmankerl/`). Außerhalb des Aussteckens steht hier „Nächste Schmankerlwochen: {Motto} ab {Datum}“ — der Text kommt aus der Termindatei, ohne Pflegeaufwand.
- *Bild:* ein Saisonteller.
- *Kennzeichnung:* „vegetarisch“ / „vegan“ als Textlabel (nicht nur ein Blatt-Icon).

**SP3 — Tagesmenü (H2 „Tagesmenü diese Woche“, Anker `#tagesmenue`).**
- *Inhalt:* „Jedes Tagesmenü mit Suppe (Nudeln oder Frittaten)“ (Quelle `/speisen/tagesmenues/`). Liste Mo–So der laufenden Woche, der heutige Tag ist hervorgehoben („Heute“). Vergangene Tage dieser Periode stehen eingeklappt darunter. Optional: PDF-Download des Monatsplans, mit Größe und Format im Linktext („Tagesmenüs Oktober als PDF, 1 Seite, ca. … KB“).
- *Datenquelle:* `tagesmenue.yaml` (Datum + Gericht). Siehe Frage 12 zur Pflege.
- *Mobile:* Heute ganz oben, die restlichen Tage darunter.

**SP4 — Speisekarte (H2 „Unsere Karte“, Anker `#karte`).**
- *Inhalt:* Kategorien als H3: Vorspeisen · Gebackenes · Hausmannskost · Vegetarisch & vegan · Für Kinder · Riesenbrote (40 cm) · Beilagen · Nachspeisen. Gerichte laut `/speisen/`. **Preise:** im Bestand nicht veröffentlicht → [PLATZHALTER: Preise ja/nein, Frage 6]. Die Komponente kann Preise anzeigen (rechtsbündig, Tabellenziffern), zeigt aber nichts an, solange das Feld leer ist.
- *Allergene:* [PLATZHALTER: Allergenkennzeichnung A–R gemäß Allergeninformationsverordnung — derzeit nicht online; Empfehlung: Hinweis „Allergeninformationen erhalten Sie bei unserem Personal“].
- *Desktop:* zweispaltig (Kategorien fließen in 2 Spalten).
- *Mobile:* einspaltig; jede Kategorie ist als `<details>` aufklappbar, die erste ist offen.

**SP5 — Kinder (H2 „Für unsere kleinen Gäste“).** Kindergerichte + Hinweis auf Spielplatz und Spielecke im Gastraum (Quelle `/ueber/`), Link `/besuch/#lokal`.

**SP6 — Querverweis Heurigenbox** (eine Zeile, Link `/ab-hof/#heurigenbox`), **Abschluss-Band**.

### §3.5 Weine `/weine/`

**W1 — Kopf (H1 „Unsere Weine“).** Lead: eigene Weingärten, eigener Keller, Christian Neumayer als Schankmeister mit Empfehlung. Die Unternavigation wie auf `/speisen/` (Segment „Weine“ aktiv).

**W2 — Weiß (H2 „Weißwein“, Anker `#weiss`).** Karte je Wein: Name (H3), Jahrgang [PLATZHALTER, außer wo durch Prämierungsgrafik belegt], Herkunftsangabe (Thermenregion DAC, wo belegt), Verkostungsnotiz aus dem Bestand (sprachlich geglättet, Inhalt unverändert), Prämierungen als Textzeile. Reihenfolge wie im Bestand: Heuriger (traditionell gemischter Satz), Grüner Veltliner, Weissburgunder, Neuburger, Gelber Muskateller, Chardonnay Spätlese, Gemischter Satz, Donau Veltliner, Rotgipfler, Königsast, Summertime (Welschriesling).

**W3 — Rot & Rosé (H2, Anker `#rot`).** Zweigelt, Rosé, Zweigelt Barrique, Blauer Portugieser. **Offen:** Pinot Noir steht auf der KOSTBAR, aber nicht auf der Weinliste; Riesling 2025 steht auf der Prämierungsgrafik, aber nicht auf der Weinliste (Frage 7).

**W4 — Frizzante & Sekt (H2, Anker `#frizzante`).** „DIE Perle — Königsast-Frizzante“.

**W5 — KOSTBAR in ROT (H2, Anker `#kostbar`, Nacht-Sektion).**
- *Inhalt:* vier Rote à 80 ml auf einem Holzbrett — Blauer Portugieser 2024, Pinot Noir 2024, Zweigelt 2023, Zweigelt Barrique 2024 (Jahrgänge laut Grafik `weinreise-scaled-990x700.jpg`), „allein oder zu zweit“, Kostpreis € 6,90 (laut derselben Grafik — **aktuell bestätigen lassen**, Frage 22).
- *Bild:* Shotliste 5. *Desktop:* Bild links groß, Text rechts. *Mobile:* Bild oben.
- *CTA:* „Tisch reservieren und verkosten“.

**W6 — Prämierungen (H2 „Prämiert 2025 und 2026“, Anker `#praemierungen`).** Tabelle Wein · Auszeichnung · Wettbewerb · Jahr. Inhalt aus der Grafik `auszeichnung-scaled-700x990.jpg` transkribiert (Heuriger 2025; Donauveltliner 2025; Gemischter Satz 2025; Rotgipfler 2025; Riesling 2025; Gelber Muskateller 2025; Welschriesling „Summertime“ 2024; Weißburgunder 2024; Neuburger 2024 — mit Gold/Silber von Land Niederösterreich, Thermenregion, Berliner Wein Trophy, Concours International de Lyon, Frankfurt International Trophy, AWC Vienna). Medaillenlogos werden **nicht** eingebunden (Markenrechte der Wettbewerbe, Ladegewicht), nur Text.

**W7 — Ab Hof kaufen (H2 „Diese Weine für zu Hause“).** Zwei Sätze, CTA „Ab Hof & Getränkeautomat“ → `/ab-hof/`. **Abschluss-Band.**

### §3.6 Ab Hof `/ab-hof/`

**A1 — Kopf (H1 „Ab Hof: Wein, Spritzer und Heurigenbox“).** Lead: „Auch wenn wir nicht ausg'steckt haben, müssen Sie auf unseren Wein nicht verzichten.“ Darunter eine Sprungliste mit 4 Ankern.

**A2 — Getränkeautomat (H2 „Der Getränkeautomat: täglich 24 Stunden“, Anker `#automat`).**
- *Inhalt:* Standort „im Eingangsbereich, Sonnbergstraße 89“, Sortiment laut Bestand („Lieblingswein, Traubensaft gespritzt oder pur usw.“), Hinweis „Die Preisliste Ab Hof hängt im Schaukasten neben dem Automaten und steht direkt beim jeweiligen Produkt“ (Quelle: Grafik `abhofverkauf2`). Zahlungsmittel [PLATZHALTER: Münzen / Karte / NFC?].
- *Bild:* Shotliste 7. *CTA:* „Route planen“.

**A3 — Wein im Karton & Lieferung (H2, Anker `#wein`).**
- *Inhalt:* „Wein im Karton oder Geschenkebox erhalten Sie während des Aussteckens zu den Öffnungszeiten oder nach Vereinbarung. Weinlieferungen sind ebenfalls nach Vereinbarung möglich.“ (Quelle: Grafik `abhofverkauf2`). Preisliste [PLATZHALTER: Preisliste Ab Hof als Datendatei, Frage 6].
- *CTA:* „Wein bestellen“ → Bestellanfrage (§5.3).

**A4 — Geschenkebox (H2, Anker `#geschenkebox`).** 2 Gläser, 1 Flasche Wein, Holzbox — € 65 (Grafik `abhofverkauf2`, Stand 01/2025 → bestätigen). Foto: Shotliste 19. CTA „Geschenkebox anfragen“.

**A5 — Spritzer TO GO (H2, Anker `#spritzer`).** Klassischer weißer Spritzer in der recycelbaren 0,33-l-Glasflasche mit Drehverschluss („Dreh & Geh“). Hinweis: Der Bestand schreibt „0,33ml“ — das ist ein Tippfehler und wird korrigiert. Erhältlich [PLATZHALTER: im Automaten und/oder an der Schank? Preis?].

**A6 — Heurigenbox (H2 „Die Heurigenbox: unser Buffet zum Mitnehmen“, Anker `#heurigenbox`).**
- *Inhalt:* Sorten Klassik, Kärnten, Käse, Mediterran, Brötchen, Dessert, individuell — jede ab 5 Personen. Preisbeispiel laut Bestand: Klassik für 5 Personen € 60, für 10 Personen € 90. Andere Preise: [PLATZHALTER]. Zustellung „nach Hause bzw. ins Büro“ (Bestand) — Liefergebiet und Vorlaufzeit [PLATZHALTER].
- *Bild:* `FEZU4913` (Bestand, die Holzbox mit Brandzeichen) bis zum Shooting.
- *Desktop:* Sortenauswahl als 3 × 2 Kartenraster mit je einem Satz Inhalt [PLATZHALTER: Inhalte pro Box von heurigenbox.at übernehmen, Frage 4].
- *Mobile:* Karten untereinander, CTA am Ende jeder Karte, die die Sorte im Formular vorauswählt.
- *CTA:* „Heurigenbox anfragen“ → Formular unten auf derselben Seite (§5.3).

**A7 — Bestellanfrage-Formular (H2 „Bestellung anfragen“, Anker `#bestellen`).** Siehe §5.3.

### §3.7 Feiern `/feiern/`

**F1 — Kopf (H1 „Feiern beim Heurigen Neumayer“).** Lead: Geburtstag, Hochzeit, Weihnachtsfeier, Seminar — „WANN und WIE Sie möchten“, auch außerhalb der Aussteckzeiten. Foto: Stüberl oder Gastgarten mit Festtafel. CTA „Feier anfragen“ (Anker zum Formular).

**F2 — Anlässe (H2 „Wofür Gäste bei uns feiern“).** Vier Kacheln mit Foto und je 2 Sätzen: Firmenfeier & Weihnachtsfeier · Hochzeit · Geburtstag & Familienfeier · Seminar. Bei Seminar fehlen Angaben zur Technik [PLATZHALTER: Beamer, WLAN, Flipchart?].

**F3 — Räume (H2 „Platz für 10 bis 200 Gäste“).**
- *Inhalt:* Gasträume auf zwei Ebenen, Stüberl, Gastgarten. Kapazität gesamt bis 200 Personen, abhängig davon, ob ausg'steckt ist (Bestand). Plätze pro Raum [PLATZHALTER, Frage 20]. Die untere Grenze „10“ in der Überschrift ist eine Annahme (ab 11 Personen leitet die Reservierung auf Feiern um, §5.1) → mit Frage 20 bestätigen.
- *Darstellung:* Tabelle Raum · Sitzplätze · geeignet für. *Mobile:* Karten.

**F4 — Fünf Zusagen (H2 „So richten wir Ihre Feier aus“).** Die fünf Bestandsaussagen werden zu einer nummerierten Liste: Feiern, **wann** Sie wollen · **wo** Sie wollen · mit **wem** Sie wollen · essen, **was** Sie möchten · essen, **wie** Sie möchten (Buffet oder serviertes Menü). Je 1–2 Sätze, ausformuliert in §4.

**F5 — Fackelwanderung-Teaser (H2, Nacht-Sektion).** Foto 21:9 (Desktop) / 4:5 (Mobile), 3 Sätze, CTA „So läuft die Fackelwanderung ab“ → `/feiern/fackelwanderung/`.

**F6 — Heurigenbox für auswärts (H3-Zeile).** „Sie feiern lieber im Büro oder zu Hause? → Heurigenbox“.

**F7 — Ablauf einer Anfrage (H2 „Von der Anfrage bis zum Fest“).** 4 Schritte: Anfrage senden → wir melden uns [PLATZHALTER: binnen X Werktagen] → Besichtigung/Menü abstimmen → feiern. Als `<ol>` mit großen Ziffern.

**F8 — Feieranfrage-Formular (H2 „Feier anfragen“, Anker `#anfrage`).** Siehe §5.4. Neben dem Formular (Desktop) bzw. darüber (Mobile): Ansprechperson Christian Neumayer, Telefon, E-Mail.

### §3.8 Fackelwanderung `/feiern/fackelwanderung/`

**FW1 — Hero (H1 „Mit Fackeln auf die Perchtoldsdorfer Heide“).** Nacht-Sektion über die ganze Breite. Foto Fackelgruppe im Weingarten. Darunter 1 Satz Subline. **Desktop:** Foto 21:9 vollbreit, Text **unter** dem Foto (kein Text auf dem Bild). **Mobile:** Foto 4:5.

**FW2 — Ablauf (H2 „So läuft's ab“).** Drei nummerierte Schritte aus dem Bestand: (1) Jeder Gast bekommt eine Fackel. (2) Gemeinsam wandern wir zu einem unserer Weingärten auf die Perchtoldsdorfer Heide, ca. 20 Minuten zu Fuß. (3) Oben wartet eine kleine Erfrischung und der Blick über ganz Wien. Danach zurück zum Fest [PLATZHALTER: Rückweg/Gesamtdauer].

**FW3 — Praktisches (H2 „Gut zu wissen“).** Als `<dl>`: Für wen (nur im Rahmen einer Feier? Frage 21), Gruppengröße [PLATZHALTER], Jahreszeit/Uhrzeit [PLATZHALTER], Schuhwerk („feste Schuhe empfohlen“ — als allgemeiner Hinweis ohne Faktenbehauptung), Wetter [PLATZHALTER: Ausweichprogramm bei Regen?], Preis [PLATZHALTER], Barrierefreiheit (Weg über Weingarten — nicht barrierefrei; vom Betrieb bestätigen).

**FW4 — Panorama (Bild ohne Überschrift, mit `<figcaption>`).** Blick über Wien (Shotliste 4).

**FW5 — CTA-Band (Nacht):** „Fackelwanderung zur Feier dazubuchen“ → `/feiern/?fackelwanderung=ja#anfrage` (Checkbox im Formular vorausgewählt) + „Anrufen“.

### §3.9 Besuch & Kontakt `/besuch/`

**B1 — Kopf (H1 „Besuch & Kontakt“).** Lead: „Mitten in Perchtoldsdorf, nur wenige Kilometer von Wien.“ (Bestand). Darunter der Kontaktblock **sofort sichtbar:** Adresse, Telefon (groß, `tel:`), E-Mail (`mailto:`), Statuszeile (wie G2).

**B2 — Anfahrt (H2 „Anfahrt“, Anker `#anfahrt`).**
- *Karte:* **Statisches Bild** (AVIF/WebP, ≤ 60 KB), beim Build aus OpenStreetMap-Kacheln erzeugt, mit Markierung und Pflicht-Attribution „© OpenStreetMap-Mitwirkende“. Kein iframe, keine Verbindung zu Google beim Seitenaufruf (Audit §5.2 „Google-Maps-iframe ohne Consent-Gate“).
- *Buttons:* „Route in Apple Karten“, „Route in Google Maps“ (`https://www.google.com/maps/dir/?api=1&destination=48.12844,16.25613`), „In OpenStreetMap öffnen“. Die Koordinaten 48.12844 / 16.25613 stammen aus dem Bestands-Maps-Embed und werden vor Ort verifiziert.
- *Text:* Mit dem Auto [PLATZHALTER: Parken], mit Öffis [PLATZHALTER: Linie/Haltestelle — nichts erfunden], mit dem Rad / zu Fuß [PLATZHALTER: Radabstellplätze, Anbindung an Wanderwege].

**B3 — Das Lokal (H2 „Das Lokal“, Anker `#lokal`).** Text aus `/ueber/` (zwei Ebenen, extra Stüberl, sonniger Gastgarten, Kinderspielplatz, Spielecke im Gastraum), dazu eine kuratierte Bildreihe mit 8–12 Fotos und Bildunterschriften. *Desktop:* Raster 3 Spalten. *Mobile:* horizontale Scroll-Snap-Reihe mit sichtbarem Anschnitt + Zähler „3 / 12“. Ein Tap öffnet das Bild im nativen `<dialog>` (Schließen-Button 44 px, Escape, kein Lightbox-Plugin). Barrierefreiheit des Lokals [PLATZHALTER: stufenloser Zugang? barrierefreies WC? Frage 16].

**B4 — Familie & Team (H2 „Familie Neumayer und Team“, Anker `#familie`).** Gruppenfoto + 4 Personen mit Rolle (Bestand `/ueber/`): Christian Neumayer — Hausherr, Weinbauer und Schankmeister · Traude Neumayer — Küche · Angelika Wolf — Medien und „Mädchen für alles“ · Friederike Wolf — Buffet. Text „Seit 40 Jahren …“ [PLATZHALTER: Gründungsjahr für die Formulierung „seit {Jahr}“ statt „seit 40 Jahren“ — veraltet sonst nächstes Jahr, Frage 18].

**B5 — Kontakt (H2 „Schreiben Sie uns“, Anker `#kontakt`).** Ein kurzes Formular (Name, E-Mail oder Telefon, Nachricht) mit Wegweiser oben: „Tisch reservieren? → Reservierung. Feier planen? → Feieranfrage. Heurigenbox? → Bestellanfrage.“ Damit landen Anfragen im richtigen, strukturierten Formular. Social: „Facebook: Weinbau & Heuriger Neumayer“ als Textlink.

**B6 — Häufige Fragen (H2 „Gut zu wissen“).** `<details>`-Liste, nur mit belegten Antworten oder Platzhaltern: Haben Sie einen Ruhetag? (laut Bestand nicht — während des Aussteckens Mo–So geöffnet, bestätigen) · Kann man reservieren? · Gibt es vegetarische und vegane Speisen? (ja, Bestand) · Gibt es etwas für Kinder? (Spielplatz, Spielecke, Kindergerichte) · Kann ich mit Karte zahlen? [PLATZHALTER] · Sind Hunde erlaubt? [PLATZHALTER] · Wo kann ich Wein kaufen, wenn nicht ausg'steckt ist? (Automat, Ab Hof).

### §3.10 Reservierung `/reservierung/`

**R1 — Kopf (H1 „Tisch reservieren“).** Ein Satz, darunter sofort die Alternative: „Lieber anrufen? 0664 211 08 25“ (`tel:`). Ab 11 Personen oder für eine Feier → Hinweis mit Link auf Feieranfrage.
**R2 — 3-Schritt-Formular.** Vollständig in §5.1.
**R3 — Was danach passiert (H2).** „Ihre Reservierung ist eine Anfrage. Wir bestätigen sie [PLATZHALTER: per E-Mail/SMS/Anruf, binnen …].“
**Mobile:** Die Aktionsleiste ist ausgeblendet. Der „Weiter“-Button ist am Formularende, nicht sticky (verdeckt sonst bei offener iOS-Tastatur das Feld).

### §3.11 Danke-Seiten, 404, Rechtliches

- `/danke/reservierung/` und `/danke/anfrage/`: `noindex`, Zusammenfassung der Angaben (aus dem Formular-Response, nicht aus der URL — keine personenbezogenen Daten in Query-Strings), nächste Schritte, „In den Kalender“ (.ics mit Datum und Uhrzeit der Anfrage, Titel „Reservierungsanfrage Heuriger Neumayer — noch nicht bestätigt“), Link Startseite.
- `/404`: H1 „Diese Seite gibt's bei uns nicht (mehr)“, Statusleiste, Suchhilfe als 5 Links der Hauptnavigation, Telefon.
- `/impressum/`: Pflichtangaben gemäß § 5 ECG und § 25 MedienG mit den Daten aus dem Bestand (Einzelunternehmen, Inhaber Christian Neumayer, Sonnbergstraße 89, 2380 Perchtoldsdorf, UID ATU66212699, Gerichtsstand Mödling, Telefon, E-Mail) + [PLATZHALTER: Gewerbebehörde/Kammerzugehörigkeit (WKO-Fachgruppe bzw. Landwirtschaftskammer bei Buschenschank) — vom Betrieb/Steuerberatung bestätigen].
- `/datenschutz/`: neu, passend zum neuen technischen Stand: Server-Logs (anonymisiert), Formulare (Zweck, Rechtsgrundlage Art. 6 Abs. 1 lit. b DSGVO, Speicherdauer), lokal gehostete Schriften, keine Cookies, keine Analyse, keine Plugins, externe Links (Facebook, Kartendienste) nur bei Klick. Hosting-Anbieter [PLATZHALTER]. Juristische Prüfung empfohlen.

---

## §4 Redaktioneller Teil (Textentwürfe)

Alle Texte sind einsatzbereit formuliert. Eckige Klammern mit `{…}` sind Variablen aus den Datendateien, **[PLATZHALTER: …]** sind fehlende Fakten.

### §4.1 Globale Texte

**Statusleiste**

- offen: „**Heute ausg'steckt** · offen bis 23:00 · {Motto} bis {Wochentag}, {Datum}“
- offen, Sonntag: „**Heute ausg'steckt** · offen bis 22:30 · {Motto} bis {Wochentag}, {Datum}“
- letzter Tag: „**Heute letzter Tag** der {Motto} · offen bis {Uhrzeit}“
- nach Sperrstunde: „Für heute ist Sperrstunde · **morgen ab 10:30** wieder offen“
- nicht ausg'steckt: „Derzeit nicht ausg'steckt · **nächstes Mal ab {Wochentag}, {Datum}**: {Motto} · Getränkeautomat 24 h offen“
- vor 10:30 an Ausstecktag: „**Heute ausg'steckt** · ab 10:30 offen · {Motto}“
- ohne JavaScript: „Nächstes Ausstecken: {Datum}–{Datum} · {Motto}“

Beispiel am 5. November 2026: „**Heute ausg'steckt** · offen bis 23:00 · Wild- & Ganslwochen bis Sonntag, 8. November“.

**Header/Navigation:** Termine · Speisen & Wein · Ab Hof · Feiern · Besuch & Kontakt · Button „Tisch reservieren“ (Mobile: „Reservieren“) · „Menü“ / „Schließen“.

**Aktionsleiste Mobile:** „Anrufen“ · „Reservieren“ · „Route“. Barrierefreie Namen: „Anrufen: 0664 211 08 25“, „Tisch reservieren“, „Route zur Sonnbergstraße 89 planen“.

**Skip-Link:** „Zum Inhalt springen“

**Abschluss-Band Standard:** H2 „Reservieren Sie Ihren Tisch“ · Text „Online in drei Schritten oder einfach anrufen — wir freuen uns auf Sie.“ · Buttons „Tisch reservieren“ / „0664 211 08 25 anrufen“

**Footer:** „Weinbau & Heuriger Neumayer · Sonnbergstraße 89 · 2380 Perchtoldsdorf“ · „Getränkeautomat im Eingangsbereich, täglich 24 Stunden“ · „© {Jahr} Weinbau & Heuriger Neumayer · Impressum · Datenschutz · Facebook“

### §4.2 Startseite

**Hero — drei Varianten**

- **Variante A (empfohlen):**
  Eyebrow: „Weinbau & Heuriger in Perchtoldsdorf“
  H1: „**Eigener Wein. Eigene Küche. Seit 40 Jahren.**“
  Subline: „Achtmal im Jahr haben wir in der Sonnbergstraße ausg'steckt — mit Schmankerlwochen, sonnigem Gastgarten und Spielplatz für die Kleinen. Dazwischen feiern wir mit Ihnen, packen Heurigenboxen und der Weinautomat hat rund um die Uhr offen.“
  Buttons: „Tisch reservieren“ · „Ausstecktermine“
  *Begründung:* Die H1 nennt die drei belegbaren Unterschiede zu Gastronomie ohne eigenen Weinbau. Die Subline beantwortet „wann“ und „was noch“.
- **Variante B (datengetrieben):** H1 „**Ausg'steckt is — bis 8. November.**“ (dynamisch; außerhalb: „Wieder ausg'steckt ab 21. November.“). *Nachteil:* Die H1 ändert sich, Google sieht wechselnde Hauptüberschriften. Deshalb ist diese Aussage in S2 und in der Statusleiste besser aufgehoben.
- **Variante C (familiär):** H1 „**Der Heurige der Familie Neumayer.**“ *Nachteil:* Der Satz ist schön, aber ohne Information.

**Faktenzeile unter dem Hero:** „Sonnbergstraße 89, Perchtoldsdorf · 0664 211 08 25 · Gastgarten · Kinderspielplatz“

**S2:** H2 „Jetzt ausg'steckt: Wild- & Ganslwochen“ (bzw. „Nächstes Mal ausg'steckt: Pfandlwochen“) · Datumszeile „Samstag, 17. Oktober bis Sonntag, 8. November 2026“ · Zeiten „Montag bis Samstag 10:30–23:00 · Sonntag 10:30–22:30“ · Zwischenzeile „Diesmal auf der Schmankerlkarte:“ · Link „Ganze Saisonkarte“ · Buttons „Für die Wild- & Ganslwochen reservieren“, „In den Kalender“

**S3:** H2 „Was heuer noch ansteht“
- Karte 1: Datumsmarke „Sa 7. & So 8. November“ · H3 „Stelzen-Wochenende“ · „Knusprig und saftig nach Art des Hauses — im Lokal oder zum Mitnehmen.“ · Frist „Bitte bis Donnerstag, 5. November, vorbestellen.“ · Link „Details & vorbestellen“
- Karte 2: Datumsmarke „Sa 28. November“ · H3 „Engerl & Bengerl: Licht aus“ · „Ein Abend bei Kerzenschein und leiser Musik, mit zwei 3-Gänge-Menüs zur Wahl. € 41 pro Menü.“ · Link „Menüs ansehen & reservieren“

**S4:** H2 „Was es nur bei uns gibt“
- H3 „Mit Fackeln auf die Heide“ · „Für Ihre Feier: Mit Fackeln wandern wir gemeinsam zu unserem Weingarten auf der Perchtoldsdorfer Heide. Oben gibt's eine Erfrischung und den Blick über ganz Wien.“ · „So läuft die Fackelwanderung ab“
- H3 „KOSTBAR in ROT“ · „Vier unserer Roten zu je 80 ml auf einem Brett — zum Verkosten allein oder zu zweit.“ · „Zur Weinkarte“
- H3 „Wein rund um die Uhr“ · „Auch wenn wir nicht ausg'steckt haben: Der Getränkeautomat im Eingang hat täglich 24 Stunden offen — mit unserem Wein und Traubensaft.“ · „Ab Hof“
- H3 „Die Heurigenbox“ · „Unser Heurigenbuffet in der Holzbox, für zu Hause oder ins Büro. Ab 5 Personen, zum Beispiel ‚Klassik‘ für 5 Personen um € 60.“ · „Heurigenbox anfragen“

**S5:** H2 „Aus unserem Keller“ · Lead „Wir begleiten die Traube vom Weingarten bis ins Glas. Heuer wurden mehrere unserer Weine prämiert.“ · Link „Alle Weine & Prämierungen“

**S6:** H2 „Ihre Feier bei uns“ · Fakten „Bis zu 200 Gäste*“ · „Stüberl, zwei Ebenen, Gastgarten“ · „Auch wenn nicht ausg'steckt ist“ · Fußnote „* abhängig davon, ob die Feier während unserer Aussteckzeiten stattfindet“ · Buttons „Feier anfragen“ / Link „So läuft eine Feier bei uns ab“

**S7:** H2 „Seit 40 Jahren Familie Neumayer“ · „Christian Neumayer kümmert sich um Weingarten, Keller und Schank, Traude Neumayer um die Küche. Unterstützt werden sie von Angelika und Friederike Wolf und einem Team in Service, Schank und Küche.“ · Link „Lernen Sie uns kennen“

**S8:** H2 „So finden Sie uns“ · „Sonnbergstraße 89, 2380 Perchtoldsdorf — nur wenige Kilometer von Wien.“ · Buttons „Route planen“ / „Anrufen“

### §4.3 Termine

- H1: „**Ausstecktermine 2026 und 2027**“ · Eyebrow „Ausg'steckt is“
- Lead: „Achtmal im Jahr haben wir ausg'steckt, jeweils rund drei Wochen, immer von Samstag bis Sonntag. Jedes Mal mit einem eigenen Schmankerl-Schwerpunkt — von den Rindfleischwochen im Jänner bis zu den Pfandlwochen im Advent.“
- H2: „Öffnungszeiten während des Aussteckens“ · „Montag bis Samstag: 10:30 bis 23:00 Uhr“ · „Sonntag: 10:30 bis 22:30 Uhr“
- Unterzeile: „Wenn wir nicht ausg'steckt haben: Der Getränkeautomat im Eingangsbereich ist täglich 24 Stunden zugänglich. Ab-Hof-Verkauf, Weinlieferung und Feiern gerne nach Vereinbarung.“
- H2 „2026“ · H2 „2027“ · Button „Alle Termine 2027 in den Kalender“ · `<summary>` „Bereits vorbei: {n} Zeiträume anzeigen“ · Badges „Jetzt“, „Als Nächstes“, „Vorbei“
- H2: „Besondere Abende und Wochenenden“
- H2: „Ihr Wunschtermin ist nicht dabei?“ · „Wir richten Ihre Feier auch dann aus, wenn wir nicht ausg'steckt haben.“ · „Feier anfragen“

### §4.4 Veranstaltungsseiten

**Engerl & Bengerl**
- H1: „**Engerl & Bengerl: ein Abend bei Kerzenschein**“
- Datumszeile: „Samstag, 28. November 2026 · [PLATZHALTER: Beginn] · € 41 pro Menü“
- Lead: „Licht aus! Am 28. November gibt's bei uns Kerzenschein, leise Musik und zwei 3-Gänge-Menüs zur Wahl.“
- „Jedes Menü beinhaltet ein Glas Frizzante, einen Gruß aus der Küche und drei Gänge.“
- H2 „Menü Engerl“: Kärntner Rauchschinken mit Schnittlauch-Kräutergervais · Schweinsmedaillons im Speckmantel mit Kaisergemüse · Vanille-Eierlikörtraum
- H2 „Menü Bengerl“: Räucherlachs und Räucherforelle mit Krengervais · Gansl mit Rotkraut und Kartoffelknödel · Schokotraum
- Hinweis: „Bitte reservieren Sie rechtzeitig — telefonisch oder online.“ [PLATZHALTER: vegetarische Variante?]
- Buttons: „Für diesen Abend reservieren“ · „Anrufen“ · „Teilen“

**Stelzen-Wochenende**
- H1: „**Stelzen-Wochenende am 7. und 8. November**“
- Lead: „Knusprig und saftig nach Art des Hauses. Unsere Stelzen gibt's an beiden Tagen im Lokal — oder zum Mitnehmen für zu Hause.“
- Frist-Box: „Bitte bis **Donnerstag, 5. November**, vorbestellen — telefonisch unter 0664 211 08 25 oder per E-Mail.“
- „Dazu bestellen Sie, was zur Stelze gehört: Senf, Kren, Krautsalat, Brot und natürlich ein Glas Wein.“
- Buttons: „Jetzt anrufen und vorbestellen“ · „Per E-Mail vorbestellen“ · „Tisch reservieren“

### §4.5 Speisen & Weine

- `/speisen/` H1 „**Speisen**“ · Lead „Bei uns wird täglich frisch gekocht. Zur Speisekarte kommen bei jedem Ausstecken saisonale Schmankerl und ein wechselndes Tagesmenü.“
- Segmente: „Saisonales“ · „Tagesmenü“ · „Speisekarte“ · „Weine“
- H2 Saison: „**Wild- & Ganslwochen: unsere Schmankerl bis 8. November**“ · Zwischenüberschriften H3 „Gansl & Wild“, „Vegetarisch & vegan“, „Süßes“
- außerhalb: H2 „Die nächsten Schmankerl: Pfandlwochen ab 21. November“ · „Die Karte für die Pfandlwochen veröffentlichen wir kurz vor dem Start.“
- H2 Tagesmenü: „**Tagesmenü diese Woche**“ · Lead „Jedes Tagesmenü kommt mit Suppe — Nudeln oder Frittaten.“ · Markierung „Heute“
- H2 Karte: „**Unsere Karte**“ · H3 „Vorspeisen & Suppen“, „Gebackenes“, „Hausmannskost“, „Vegetarisch & vegan“, „Für Kinder“, „Riesenbrote, 40 cm lang“, „Beilagen“, „Nachspeisen“
- Allergenhinweis: „Fragen Sie uns nach Allergenen — unser Team gibt Ihnen gern Auskunft.“
- `/weine/` H1 „**Unsere Weine**“ · Lead „Unsere Weine wachsen in Perchtoldsdorf und werden in unserem eigenen Keller ausgebaut. Welcher heute zu Ihrem Essen passt, sagt Ihnen Christian Neumayer an der Schank.“
- H2 „Weißwein“ · „Rot & Rosé“ · „Frizzante & Sekt“ · „KOSTBAR in ROT“ · „Prämiert 2025 und 2026“ · „Diese Weine für zu Hause“
- KOSTBAR-Text: „Unsere Art der Weinverkostung: vier Rote zu je 80 ml auf einem Holzbrett — Blauer Portugieser, Pinot Noir, Zweigelt und Zweigelt Barrique. Allein oder zu zweit. Prost!“ · Preiszeile „Kostpreis € 6,90“ (nach Bestätigung)

### §4.6 Ab Hof

- H1 „**Ab Hof: Wein, Spritzer und Heurigenbox**“
- Lead „Auch wenn wir nicht ausg'steckt haben, müssen Sie auf unseren Wein nicht verzichten.“
- Sprungliste: „Getränkeautomat“ · „Wein & Lieferung“ · „Geschenkebox“ · „Spritzer TO GO“ · „Heurigenbox“
- H2 „Der Getränkeautomat: täglich 24 Stunden“ · „Im Eingangsbereich in der Sonnbergstraße 89 holen Sie sich jederzeit Ihren Lieblingswein, gespritzten oder puren Traubensaft. Die Preise stehen direkt beim Produkt und auf der Preisliste im Schaukasten neben dem Automaten.“
- H2 „Wein im Karton und Lieferung“ · „Wein im Karton bekommen Sie während des Aussteckens zu den Öffnungszeiten, sonst nach Vereinbarung. Wir liefern auch — sagen Sie uns einfach, was und wohin.“ · Button „Wein bestellen“
- H2 „Die Geschenkebox“ · „Zwei Gläser, eine Flasche Wein, in einer Holzbox. € 65.“ · Button „Geschenkebox anfragen“
- H2 „Spritzer TO GO“ · „Der klassische weiße Spritzer in der 0,33-l-Glasflasche mit Drehverschluss. Aufdrehen, mitnehmen, die Flasche ist recycelbar.“
- H2 „Die Heurigenbox: unser Buffet zum Mitnehmen“ · „Optisch ein Hingucker, geschmacklich ein echter Heuriger: Wir richten Ihnen unser Heurigenbuffet in der Holzbox an — für die Firmenfeier, den Geburtstag oder einfach so. Jede Box gibt es ab 5 Personen.“ · Sortennamen: „Klassik“, „Kärnten“, „Käse“, „Mediterran“, „Brötchen“, „Dessert“, „Ganz nach Ihrem Wunsch“ · Preiszeile „Zum Beispiel ‚Klassik‘: 5 Personen € 60 · 10 Personen € 90“ · Button „Heurigenbox anfragen“

### §4.7 Feiern & Fackelwanderung

- `/feiern/` H1 „**Feiern beim Heurigen Neumayer**“ · Lead „Ob Geburtstag im kleinen Kreis, Hochzeit, Weihnachtsfeier oder Seminar: Wir richten Ihre Feier aus, wann und wie Sie möchten — auch wenn wir gerade nicht ausg'steckt haben.“ · Button „Feier anfragen“
- H2 „Wofür Gäste bei uns feiern“ · H3 „Firmen- und Weihnachtsfeier“, „Hochzeit“, „Geburtstag und Familienfeier“, „Seminar“
- H2 „Platz für 10 bis 200 Gäste“ · „Je nach Gästezahl feiern Sie in unseren Gasträumen auf zwei Ebenen, im Stüberl oder — wenn das Wetter mitspielt — im Gastgarten. Insgesamt haben bis zu 200 Gäste Platz; wie viele es genau sind, hängt davon ab, ob wir zu Ihrem Termin ausg'steckt haben.“
- H2 „So richten wir Ihre Feier aus“
  1. „**Wann Sie wollen.** Ihr Wunschtermin liegt außerhalb unserer Aussteckzeiten? Dann sperren wir für Sie auf.“
  2. „**Wo Sie wollen.** Stüberl, Gastraum oder Gastgarten — wir suchen mit Ihnen den passenden Platz für Ihre Gästezahl.“
  3. „**Mit wem Sie wollen.** Von den engsten Freunden bis zu ein paar Dutzend Gästen und mehr.“
  4. „**Was Sie essen möchten.** Schweinsbraten und Co., Schnitzel-Variationen oder ein süßer Abschluss — wir richten uns nach Ihnen.“
  5. „**Wie Sie essen möchten.** Klassisches Buffet oder serviertes Menü — sagen Sie uns einfach, was Ihnen lieber ist.“
- H2 „Von der Anfrage bis zum Fest“ · 1 „Sie schicken uns Ihre Anfrage — online oder am Telefon.“ 2 „Wir melden uns [PLATZHALTER: innerhalb von zwei Werktagen] mit Rückfragen und einem Vorschlag.“ 3 „Wir stimmen Menü, Ablauf und Raum mit Ihnen ab, gern auch vor Ort.“ 4 „Sie feiern, wir kümmern uns um den Rest.“
- H2 „Feier anfragen“ · Kontaktzeile „Ihr Ansprechpartner: Christian Neumayer · 0664 211 08 25 · christian@weinbauneumayer.at“
- `/feiern/fackelwanderung/` H1 „**Mit Fackeln auf die Perchtoldsdorfer Heide**“ · Subline „Das gewisse Extra für Ihre Feier: eine Nachtwanderung zu unserem Weingarten, mit Blick über ganz Wien.“ · H2 „So läuft's ab“: 1 „Jeder Ihrer Gäste bekommt eine Fackel.“ 2 „Gemeinsam wandern wir zu einem unserer Weingärten auf der Perchtoldsdorfer Heide — rund 20 Minuten zu Fuß.“ 3 „Oben wartet eine kleine Erfrischung und ein Blick über ganz Wien, den man so schnell nicht vergisst.“ · H2 „Gut zu wissen“ · CTA-Band H2 „Fackelwanderung zur Feier dazubuchen“ · Button „Feier mit Fackelwanderung anfragen“

### §4.8 Formular-Microcopy (alle Formulare)

**Grundregeln:** Jedes Feld hat ein sichtbares `<label>` über dem Feld (keine Platzhalter als Label, Audit §5.3). Pflichtfelder sind mit „(Pflichtfeld)“ im Label markiert — nicht nur mit einem Sternchen. Optionale Felder tragen „(freiwillig)“. Fehlermeldungen stehen direkt unter dem Feld, beginnen mit dem Feldnamen und sagen, was zu tun ist. Beim Absenden mit Fehlern springt der Fokus auf eine Fehlerzusammenfassung oben („2 Angaben fehlen noch:“ mit Links zu den Feldern).

**Reservierung**

| Element | Text |
|---|---|
| Schritt-Anzeige | „Schritt 1 von 3: Tag“ · „Schritt 2 von 3: Uhrzeit und Personen“ · „Schritt 3 von 3: Ihre Kontaktdaten“ |
| Schritt 1 Überschrift | „An welchem Tag kommen Sie?“ |
| Schritt 1 Hinweis | „Wählbar sind alle Tage, an denen wir ausg'steckt haben.“ |
| Schritt 1 Leer | „In den nächsten Wochen haben wir nicht ausg'steckt. Nächstes Mal ab {Datum} — oder planen Sie eine Feier? → Feier anfragen“ |
| Schritt 2 Überschrift | „Um wie viel Uhr, und wie viele sind Sie?“ |
| Label Personen | „Personen (Pflichtfeld)“ · Buttons „Eine Person weniger“ / „Eine Person mehr“ |
| Hinweis > 10 | „Mehr als 10 Personen? Dann planen wir das gern mit Ihnen persönlich: 0664 211 08 25 anrufen oder Feier anfragen.“ |
| Label Uhrzeit | „Uhrzeit (Pflichtfeld)“ · Gruppen „Mittag“, „Nachmittag“, „Abend“ |
| Label Bereich | „Wo möchten Sie sitzen? (freiwillig)“ · Optionen „Egal, Hauptsache gemütlich“ · „Drinnen“ · „Im Gastgarten (bei Schönwetter)“ |
| Schritt 3 Überschrift | „Wie erreichen wir Sie?“ |
| Label Name | „Vor- und Nachname (Pflichtfeld)“ |
| Label Telefon | „Telefonnummer (Pflichtfeld)“ · Hinweis „Für Rückfragen am Tag Ihres Besuchs.“ |
| Label E-Mail | „E-Mail-Adresse (freiwillig)“ · Hinweis „Wenn Sie die Bestätigung lieber per E-Mail möchten.“ |
| Label Anmerkung | „Anmerkung (freiwillig)“ · Hinweis „Zum Beispiel Kinderwagen, Hochstuhl oder ein Geburtstag am Tisch.“ |
| Zusammenfassung | „Sie fragen an: {Wochentag}, {Datum}, {Uhrzeit} Uhr, {n} Personen, {Bereich}.“ · Link „Ändern“ |
| Datenschutz-Hinweis (kein Häkchen nötig) | „Wir verwenden Ihre Angaben nur, um Ihre Reservierung zu bearbeiten, und löschen sie [PLATZHALTER: 3 Monate] nach Ihrem Besuch. Mehr in der Datenschutzerklärung.“ |
| Buttons | „Weiter“ · „Zurück“ · „Reservierungsanfrage senden“ |
| Senden läuft | „Wird gesendet …“ (Button deaktiviert, `aria-busy`) |
| Erfolg H1 | „Danke, {Vorname}! Ihre Anfrage ist bei uns.“ |
| Erfolg Text | „{Wochentag}, {Datum}, {Uhrzeit} Uhr für {n} Personen. Bitte beachten Sie: Das ist noch keine Bestätigung. Wir melden uns [PLATZHALTER: bis … per SMS/Anruf/E-Mail]. Kurzfristig? Rufen Sie uns an: 0664 211 08 25.“ |
| Fehler Server | „Das hat leider nicht geklappt. Ihre Angaben sind noch da — bitte versuchen Sie es noch einmal oder rufen Sie uns an: 0664 211 08 25.“ |
| Fehler Tag | „Tag: Bitte wählen Sie einen Tag aus.“ |
| Fehler Uhrzeit | „Uhrzeit: Bitte wählen Sie eine Uhrzeit aus.“ |
| Fehler Name | „Name: Bitte geben Sie Ihren Vor- und Nachnamen an.“ |
| Fehler Telefon | „Telefonnummer: Bitte geben Sie eine Nummer an, unter der wir Sie erreichen, zum Beispiel 0664 1234567.“ |
| Fehler E-Mail | „E-Mail-Adresse: Bitte prüfen Sie die Schreibweise, zum Beispiel name@beispiel.at.“ |

**Feieranfrage**

| Element | Text |
|---|---|
| Label Anlass | „Was feiern Sie? (Pflichtfeld)“ · „Firmen- oder Weihnachtsfeier“ · „Hochzeit“ · „Geburtstag oder Familienfeier“ · „Seminar“ · „Etwas anderes“ |
| Label Datum | „Wunschtermin (Pflichtfeld)“ · Hinweis „Auch außerhalb unserer Aussteckzeiten möglich.“ |
| Label Ausweichtermin | „Ausweichtermin (freiwillig)“ |
| Label Gäste | „Ungefähre Gästezahl (Pflichtfeld)“ · Hinweis „Eine Schätzung genügt.“ |
| Label Essen | „Wie möchten Sie essen? (freiwillig)“ · „Buffet“ · „Serviertes Menü“ · „Heurigenbox“ · „Noch offen — beraten Sie uns“ |
| Label Fackelwanderung | „Fackelwanderung auf die Perchtoldsdorfer Heide dazubuchen? (freiwillig)“ · „Ja, gern“ · „Vielleicht — bitte mehr Infos“ · „Nein“ |
| Label Firma | „Firma (freiwillig)“ |
| Label Nachricht | „Was sollten wir noch wissen? (freiwillig)“ · Hinweis „Zum Beispiel Uhrzeit, Kinder, Unverträglichkeiten, Budget.“ |
| Button | „Feieranfrage senden“ |
| Erfolg | „Danke! Ihre Anfrage für {Anlass} am {Datum} ist bei uns. Christian Neumayer meldet sich [PLATZHALTER: innerhalb von zwei Werktagen] bei Ihnen.“ |

**Heurigenbox-/Weinbestellung**

| Element | Text |
|---|---|
| Label Art | „Was möchten Sie bestellen? (Pflichtfeld)“ · „Heurigenbox“ · „Wein“ · „Geschenkebox“ |
| Label Sorte | „Welche Heurigenbox? (Pflichtfeld bei Heurigenbox)“ · Checkboxen der Sorten |
| Label Personen | „Für wie viele Personen? (Pflichtfeld bei Heurigenbox)“ · Hinweis „Ab 5 Personen.“ · Fehler „Personen: Die Heurigenbox gibt es ab 5 Personen.“ |
| Label Wein | „Welcher Wein, wie viel? (Pflichtfeld bei Wein)“ · Hinweis „Zum Beispiel: 6 Flaschen Grüner Veltliner, 1 Karton Zweigelt.“ |
| Label Übergabe | „Abholen oder liefern lassen? (Pflichtfeld)“ · „Ich hole ab“ · „Bitte liefern — nach Vereinbarung“ |
| Label Termin | „Wann brauchen Sie es? (Pflichtfeld)“ · Hinweis „[PLATZHALTER: Vorlaufzeit, z. B. mindestens 3 Tage vorher]“ |
| Label Lieferadresse | „Lieferadresse (Pflichtfeld bei Lieferung)“ |
| Altershinweis (Wein) | „Wein geben wir nur an Personen ab 16 Jahren ab.“ [PLATZHALTER: rechtlich prüfen lassen; NÖ Jugendgesetz] |
| Button | „Bestellung anfragen“ |
| Erfolg | „Danke! Wir haben Ihre Bestellanfrage. Wir melden uns mit Preis und Termin, bevor etwas fix ist.“ |

**Kontakt kurz:** „Ihr Name (Pflichtfeld)“ · „E-Mail oder Telefonnummer (Pflichtfeld)“ · „Ihre Nachricht (Pflichtfeld)“ · Button „Nachricht senden“ · Erfolg „Danke für Ihre Nachricht — wir melden uns.“

**Spam-Schutz:** Es gibt kein CAPTCHA. Ein unsichtbares Honeypot-Feld trägt das Label „Bitte dieses Feld leer lassen“ und ist für Screenreader ausgeblendet. Formulare, die schneller als 3 Sekunden abgeschickt werden, werden verworfen.

### §4.9 Alt-Texte und Bildunterschriften (Muster)

- Hero: „Das Haus des Heurigen Neumayer in der Sonnbergstraße 89 mit ausgestecktem Buschen“ (an den tatsächlichen Bildinhalt anpassen)
- Heurigenbox: „Heurigenbox aus Holz mit Schinken, Speck und Käse auf einem Tisch im Gastgarten“ (Bestand `FEZU4913`, beschreibt den tatsächlichen Bildinhalt)
- KOSTBAR: „Vier kleine Karaffen mit Rotwein auf einem Holzbrett, beschriftet mit Blauer Portugieser, Pinot Noir, Zweigelt und Zweigelt Barrique“
- Fackelwanderung: „Eine Gruppe mit Fackeln auf dem Weg durch den Weingarten in der Dämmerung“
- Dekorative Bilder (Ornamente): `alt=""`
- Regel: Der Alt-Text beschreibt, was zu sehen ist, und wiederholt nicht die Überschrift. Er ist im Bildschema ein Pflichtfeld — ohne Alt-Text bricht der Build ab (Audit: 26 Bilder ohne Alt).

---

## §5 Konversionspfade

Es gibt vier Pfade, geordnet nach Häufigkeit (Annahme, Frage 25 zur Prüfung mit dem Betrieb): **Anruf** > **Tischreservierung** > **Feieranfrage** > **Heurigenbox/Wein**. Für jeden Pfad gilt: höchstens 2 Taps von jeder Seite bis zum Ziel, und das Telefon ist immer die gleichwertige Alternative.

### §5.1 Tischreservierung in 3 Schritten

**Einstiege:** Header-Button, mobile Aktionsleiste, Abschluss-Band, Startseite S2 (mit vorausgewähltem Datum), Terminliste (mit vorausgewähltem Zeitraum), Veranstaltungsseiten (mit Datum und Anlass). Parameter: `?datum=YYYY-MM-DD`, `?anlass={slug}`. Sie werden nur zum Vorausfüllen genutzt und landen nie im Log mit Personendaten.

**Grundsatzentscheidung:** Die Reservierung ist eine **Anfrage mit Bestätigung durch den Betrieb**. Genau so arbeitet der Bestand auch: Die Redi-Erfolgsmeldung im Mirror sagt „Wir prüfen die Verfügbarkeit und werden uns so schnell wie möglich bei Ihnen melden“. Echtzeit-Tischverfügbarkeit bräuchte ein Buchungssystem mit Datenverarbeitung bei Dritten und Pflege der Tischbelegung. Das ist für 177 Ausstecktage mit überwiegend Laufkundschaft unverhältnismäßig (Frage 2).

**Wireframe Schritt 1 — Tag (Mobile, 390 px)**

```
┌──────────────────────────────────────┐
│ [WN] Heuriger Neumayer      [Menü]   │  Header 64 px
├──────────────────────────────────────┤
│ Tisch reservieren                (H1)│
│ Lieber anrufen? 0664 211 08 25  [tel]│
│                                      │
│ ●───○───○   Schritt 1 von 3: Tag     │  Fortschritt (Text + Punkte)
│                                      │
│ An welchem Tag kommen Sie?     (H2)  │
│ Wählbar sind alle Tage, an denen     │
│ wir ausg'steckt haben.               │
│                                      │
│ Pfandlwochen · 21. Nov – 6. Dez      │  Gruppenüberschrift je Zeitraum
│ ┌──────┐┌──────┐┌──────┐┌──────┐     │
│ │ Sa   ││ So   ││ Mo   ││ Di   │     │  Tages-Chips 72×64 px
│ │ 21.11││ 22.11││ 23.11││ 24.11│     │  (radio, role=radiogroup)
│ └──────┘└──────┘└──────┘└──────┘     │
│ ┌──────┐┌──────┐ …                   │
│ │ Sa 28.11 · Engerl & Bengerl │      │  Sondertag mit Zusatzzeile
│ └─────────────────────────────┘      │
│ [ Weitere Tage anzeigen ]            │  lädt die nächsten 14 Tage
│                                      │
│ Anderer Tag? → Feier anfragen        │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │             Weiter               │ │  52 px, volle Breite
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

- **Logik:** Es werden nur Tage innerhalb von Aussteckzeiträumen angeboten, ab heute für [PLATZHALTER: 60] Tage im Voraus. Heute ist wählbar bis [PLATZHALTER: 2 Stunden vor Sperrstunde]. Danach erscheint der Hinweis „Für heute bitte anrufen“.
- **Desktop:** Statt der Chips gibt es ein Monatsraster (7 Spalten). Nicht-Aussteck-Tage sind ausgegraut, deaktiviert und mit `aria-disabled` + Text „nicht ausg'steckt“ für Screenreader versehen. Rechts daneben steht eine Zusammenfassungsspalte, die sich mitfüllt.
- **Ohne JavaScript:** Das Formular ist eine einzige Seite mit drei `<fieldset>`. Tage sind als `<select>` mit `<optgroup>` pro Zeitraum gruppiert. Absenden funktioniert identisch.

**Wireframe Schritt 2 — Uhrzeit und Personen**

```
┌──────────────────────────────────────┐
│ ●───●───○   Schritt 2 von 3          │
│ Sa, 21. November  [Ändern]           │
│                                      │
│ Um wie viel Uhr, und wie viele       │
│ sind Sie?                      (H2)  │
│                                      │
│ Personen (Pflichtfeld)               │
│ ┌────┐  ┌────────┐  ┌────┐           │
│ │ –  │  │   4    │  │ +  │           │  Stepper, 48 px Buttons,
│ └────┘  └────────┘  └────┘           │  input type=number inputmode=numeric
│                                      │
│ Uhrzeit (Pflichtfeld)                │
│ Mittag                               │
│ [10:30][11:00][11:30][12:00][12:30]  │  Chips 64×44 px, 30-min-Raster
│ Nachmittag                           │
│ [13:00][13:30] … [17:30]             │
│ Abend                                │
│ [18:00][18:30] … [21:00]             │
│                                      │
│ Wo möchten Sie sitzen? (freiwillig)  │
│ (•) Egal, Hauptsache gemütlich       │
│ ( ) Drinnen                          │
│ ( ) Im Gastgarten (bei Schönwetter)  │
│                                      │
│ [ Zurück ]        [    Weiter     ]  │
└──────────────────────────────────────┘
```

- **Personen:** 1–10 ist online möglich. Bei 11 und mehr erscheint statt „Weiter“ ein Hinweisblock mit „Anrufen“ und „Feier anfragen“. Das entspricht der Bestandsregel „>10 — Bei mehr als 10 Personen rufen wir Sie gerne an“.
- **Uhrzeiten:** 10:30–21:00 wie im Bestand, aber im 30- statt 15-Minuten-Raster (16 statt 43 Optionen). Sonntags endet das Angebot [PLATZHALTER: 20:30?], weil um 22:30 Sperrstunde ist (Frage 3).
- **Bereich:** Die Bestandsoption „Nichtraucher“ entfällt. In der österreichischen Gastronomie gilt seit 1. November 2019 generelles Rauchverbot in Innenräumen, die Unterscheidung ist also hinfällig.
- **Gastgarten:** wird nur in den Zeiträumen April–September angeboten [PLATZHALTER: Saison des Gastgartens bestätigen].

**Wireframe Schritt 3 — Kontakt und Absenden**

```
┌──────────────────────────────────────┐
│ ●───●───●   Schritt 3 von 3          │
│ Sa, 21.11. · 18:30 · 4 Personen ·    │
│ egal wo                   [Ändern]   │
│                                      │
│ Wie erreichen wir Sie?         (H2)  │
│ Vor- und Nachname (Pflichtfeld)      │
│ [______________________________]     │  autocomplete=name
│ Telefonnummer (Pflichtfeld)          │
│ Für Rückfragen am Tag Ihres Besuchs. │
│ [______________________________]     │  type=tel autocomplete=tel
│ E-Mail-Adresse (freiwillig)          │
│ [______________________________]     │  type=email autocomplete=email
│ Anmerkung (freiwillig)               │
│ [______________________________]     │  textarea, 3 Zeilen
│                                      │
│ Wir verwenden Ihre Angaben nur für   │
│ Ihre Reservierung … Datenschutz      │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │  Reservierungsanfrage senden     │ │
│ └──────────────────────────────────┘ │
│ [ Zurück ]                           │
└──────────────────────────────────────┘
```

- Eingabefelder haben mindestens 16 px Schriftgröße. Das ist zwingend, sonst zoomt iOS Safari beim Fokus automatisch hinein.
- `enterkeyhint="next"` / `"send"` setzen, damit die iOS-Tastatur „Weiter“ bzw. „Senden“ zeigt.
- Beim Schrittwechsel wandert der Fokus auf die Überschrift des neuen Schritts (`tabindex="-1"`). Der Fortschritt wird über eine `aria-live="polite"`-Region angesagt („Schritt 2 von 3“).
- Die Zurück-Geste des Browsers funktioniert: Jeder Schritt setzt einen `history.pushState`-Eintrag, damit „Zurück“ in Safari nicht das ganze Formular verlässt.
- Eingaben bleiben bei Seitenneuladen erhalten (`sessionStorage`, nur auf dem Gerät, wird nach Absenden gelöscht). Das ist kein Cookie, nicht einwilligungspflichtig und technisch notwendig für die vom Nutzer angeforderte Funktion. Im Datenschutztext wird es erwähnt.
- **Neue Felder gegenüber Bestand:** keine. **Entfallen:** Anrede (Herr/Frau — unnötig und nicht inklusiv), getrennte Vor-/Nachnamefelder, Newsletter-Checkbox, E-Mail als Pflichtfeld.

**Nach dem Absenden**

1. Der Server prüft die Angaben (Tag im Aussteckzeitraum? Uhrzeit gültig? Personen 1–10? Honeypot leer?). Danach verschickt er eine E-Mail an den Betrieb mit dem Betreff „Reservierung Sa 21.11. 18:30 · 4 P. · {Name}“ — sortierbar im Posteingang, Telefonnummer als anklickbarer Link.
2. Gibt der Gast eine E-Mail an, bekommt er eine Eingangsbestätigung (ausdrücklich „noch nicht bestätigt“) mit der Telefonnummer des Betriebs.
3. Die Danke-Seite zeigt eine Zusammenfassung und bietet „In den Kalender (vorläufig)“ an.
4. **Bestätigung durch den Betrieb:** per Rückruf, SMS oder Antwort-Mail [PLATZHALTER: Prozess beim Betrieb, Frage 3]. Optionale Ausbaustufe: Ein Bestätigungslink in der Betriebs-Mail löst eine automatische Bestätigungsmail an den Gast aus (+4 h Aufwand, §9).

### §5.2 Anruf-Pfad

Das Telefon ist laut Bestand der Hauptkanal: Jede Aktion auf der Seite verweist auf die Nummer, und die Stelzen-Vorbestellung geht nur telefonisch oder per Mail. Trotzdem gab es keinen einzigen `tel:`-Link (Audit Befund 7).

1. **Format:** angezeigt als „0664 211 08 25“ (österreichische Schreibweise, gruppiert). Verlinkt ist `tel:+436642110825`. Im Schema steht `+43 664 2110825`.
2. **Platzierung (Mobile):** Aktionsleiste „Anrufen“ (immer erreichbar), Statusleiste im Zustand „heute offen“, Hero-Faktenzeile, Abschluss-Band jeder Seite, Reservierungs-Kopf, jede Formular-Fehlermeldung, Footer, Veranstaltungsseiten mit Frist.
3. **Desktop:** Die Nummer steht als lesbarer Text mit Link. Auf dem Mac mit iPhone-Kopplung startet der Anruf über Handoff. Es gibt kein „Rückruf anfordern“-Formular (zusätzlicher Prozess ohne klaren Nutzen).
4. **Erreichbarkeit:** Neben der Nummer steht, wann jemand abhebt [PLATZHALTER: z. B. „während des Aussteckens ab 10:00, sonst Mo–Fr …“]. Ohne diese Angabe gilt: Außerhalb der Aussteckzeiten steht beim Anruf-Button der Hinweis „Auch wenn wir nicht ausg'steckt haben, erreichen Sie uns telefonisch oder per E-Mail.“
5. **Screenreader:** Der Link-Text heißt „0664 211 08 25 anrufen“, damit klar ist, dass ein Anruf startet.
6. **Messung:** siehe §8 (anonymer Zähler ohne Cookie, optional).

### §5.3 Heurigenbox- und Weinbestellung

**Ist-Zustand:** Die Heurigenbox wird auf der Startseite beworben, die Details liegen auf der fremden Domain `www.heurigenbox.at` — die Sitzung geht verloren (Audit §5.2). Wein im Karton und Geschenkebox kommen online nur als Bildgrafik vor. WooCommerce ist installiert, wird aber nicht genutzt.

**Soll (Phase 1): Bestellanfrage statt Shop.**

1. **Einstieg:** `/ab-hof/` (Karten „Heurigenbox anfragen“, „Wein bestellen“, „Geschenkebox anfragen“), Startseite S4, `/feiern/` F6, `/weine/` W7. Jeder Einstieg wählt im Formular die passende Art vor.
2. **Formular (eine Seite, ein Formular, bedingte Felder):**
   - Art: Heurigenbox / Wein / Geschenkebox (Mehrfachauswahl möglich)
   - Bei Heurigenbox: Sorte(n), Personen (Stepper, Minimum 5, Fehlermeldung bei weniger)
   - Bei Wein: Freitext „Welcher Wein, wie viel?“ (bis Preisliste vorliegt; danach Mengenfelder pro Wein aus `weine.yaml`)
   - Übergabe: Abholen / Liefern nach Vereinbarung (bei Lieferung: Adresse)
   - Wunschtermin (Datum + ungefähre Uhrzeit), Vorlaufzeit-Hinweis [PLATZHALTER]
   - Name, Telefon (Pflicht), E-Mail (freiwillig), Anmerkung
3. **Preisanzeige:** Sobald eine Sorte mit hinterlegtem Preis gewählt ist (derzeit nur „Klassik“ für 5 bzw. 10 Personen), zeigt das Formular eine unverbindliche Orientierung: „Richtwert laut Preisliste: € 60 für 5 Personen. Den genauen Preis bestätigen wir Ihnen.“ Für andere Personenzahlen wird **nicht** hochgerechnet (die Preise skalieren nicht linear: 5 P. € 60, 10 P. € 90).
4. **Danach:** Betrieb bekommt eine E-Mail mit dem Betreff „Heurigenbox Klassik · 8 P. · Abholung Fr 13.11.“. Gast bekommt Eingangsbestätigung. Der Betrieb bestätigt Preis und Termin persönlich. Erst dann ist die Bestellung fix (keine Zahlung online, kein Fernabsatzvertrag mit Widerrufsbelehrung im Online-Prozess).
5. **heurigenbox.at:** Empfehlung: Inhalte (Sorten, Inhalt, Fotos, Preise) auf `/ab-hof/#heurigenbox` übernehmen und die Domain per 301 auf diesen Anker leiten. Vorbedingung: Die Domain gehört dem Betrieb (Frage 4).
6. **Phase 2 (optional):** echter Bestellprozess mit Online-Zahlung nur, wenn die Anfragezahl das rechtfertigt (Messung §8). Für Wein mit Versand kämen Altersprüfung, AGB, Widerrufsbelehrung und Versandkosten dazu — das ist ein eigenes Projekt (Frage 5).

### §5.4 Feieranfrage

1. **Einstiege:** `/feiern/` (Kopf, Anker `#anfrage`), Fackelwanderung (mit Vorauswahl), Reservierung ab 11 Personen, Terminseite T5, Startseite S6.
2. **Formular in zwei Blöcken auf einer Seite** (keine Schritte — Feieranfragen werden oft am Desktop ausgefüllt und gern vorab komplett überblickt):
   - Block „Ihre Feier“: Anlass · Wunschtermin · Ausweichtermin · Gästezahl · Bereich (Stüberl / Gastraum / Gastgarten / beraten Sie uns) · Essen (Buffet / Menü / Heurigenbox / offen) · Fackelwanderung (ja / vielleicht / nein) · Nachricht
   - Block „Ihre Kontaktdaten“: Name · Firma (freiwillig) · Telefon (Pflicht) · E-Mail (Pflicht — für Angebote braucht es eine schriftliche Antwort)
3. **Live-Hinweis beim Datum:** Liegt der Wunschtermin in einem Aussteckzeitraum, erscheint „An diesem Tag haben wir ausg'steckt — für große Gruppen ist das Stüberl ideal, wir beraten Sie.“ Liegt er außerhalb: „An diesem Tag haben wir nicht ausg'steckt — wir sperren für Sie auf.“ Die Kapazitätsangabe „bis 200“ hängt laut Bestand genau davon ab. Den Hinweis formuliere ich nach Klärung von Frage 20 präziser.
4. **Danach:** E-Mail an den Betrieb mit dem Betreff „Feieranfrage Hochzeit · Sa 12.06.2027 · ca. 80 Gäste · Fackelwanderung: ja“. Eingangsbestätigung an den Gast mit Name der Ansprechperson und Antwortfrist.
5. **Ansprechperson sichtbar:** Christian Neumayer mit Telefon und E-Mail neben dem Formular (Audit §6.4: „Keine Ansprechperson/E-Mail öffentlich — für Firmenanfragen zu wenig“).
6. **Für Firmen:** Eine Zeile „Auf Wunsch mit Rechnung auf Ihre Firma“ [PLATZHALTER: bestätigen] und die Möglichkeit, ein PDF-Infoblatt „Feiern beim Heurigen Neumayer“ herunterzuladen (Phase 2, Inhalt aus `/feiern/`, ≤ 300 KB).

---

## §6 Technische Spezifikation

### §6.1 Stack-Entscheidung

| Baustein | Entscheidung | Begründung |
|---|---|---|
| Generator | **Astro 5** (statischer Output, `output: 'static'`) | Liefert standardmäßig kein JavaScript aus. `astro:assets` erzeugt AVIF/WebP/`srcset` ohne Zusatzwerkzeug, und die Content Collections prüfen Datendateien per Zod-Schema: Ein falsches Datum in `termine.yaml` bricht den Build ab, statt live falsch zu sein. 11ty könnte das auch (mit `eleventy-img` und eigener Validierung), braucht aber mehr eigenen Klebecode. |
| Styling | handgeschriebenes CSS mit Custom Properties, eine Datei pro Komponente, gebündelt + minifiziert (Lightning CSS) | < 50 KB Vorgabe; ohne Utility-Framework realistisch 20–28 KB roh |
| JavaScript | Vanilla, pro Komponente als Astro-`<script>` (wird gebündelt), kein Framework, kein jQuery | Reservierungsassistent ≈ 8 KB, Statusleiste ≈ 1,5 KB, Menü-Dialog ≈ 1 KB, Galerie-Dialog ≈ 1 KB |
| Inhalte | YAML/Markdown im Repo (`src/content/`) | Vorgabe „Termine als Datenquelle im Repo“ |
| Redaktion | Phase 1: Pflege durch Hermes/Daniel per Pull Request. Phase 2 optional: Git-basiertes CMS (Sveltia CMS oder Decap CMS) mit Formularen für Termine und Tagesmenü | Kein WordPress-Backend mehr nötig, keine Datenbank, keine Plugin-Updates (Frage 12) |
| Formulare | kleiner serverseitiger Endpunkt auf demselben Host (PHP 8.3 ≈ 150 Zeilen, oder Node/Go, je nach Hosting), Versand per SMTP an `christian@weinbauneumayer.at` | Keine Formulardaten bei US-Drittanbietern. Validierung serverseitig, Rate-Limit pro IP (IP wird nur flüchtig im Speicher gehalten) |
| Hosting | EU-Anbieter mit Brotli-fähigem Webserver und eigener Header-Konfiguration (z. B. Caddy oder Apache auf einem österreichischen oder deutschen Webhosting) | DSGVO, Vorgabe „kein Tracking“. Ein CDN ist bei dieser Seitengröße und regionaler Zielgruppe nicht nötig, darf aber ergänzt werden, wenn es EU-gehostet ist (Frage 10) |
| Build/Deploy | GitHub Actions (Repo `gschranz/neumayer`): Build, Prüfungen, Upload per rsync/SFTP; geplanter Neubau täglich 00:05 Europe/Vienna | Statusleiste und Terminlisten bleiben ohne Zutun aktuell |

### §6.2 Datenmodell

**`src/content/termine.yaml`** (Auszug, echte Daten aus den Plakaten):

```yaml
oeffnungszeiten_ausstecken:
  mo_sa: { von: "10:30", bis: "23:00" }
  so:    { von: "10:30", bis: "22:30" }
  feiertag: so            # [PLATZHALTER: bestätigen]

ausstecken:
  - von: 2026-10-17
    bis: 2026-11-08
    motto: "Wild- & Ganslwochen"
    slug: wild-gansl-2026
  - von: 2026-11-21
    bis: 2026-12-06
    motto: "Pfandlwochen"
    slug: pfandl-2026
  - von: 2027-01-06
    bis: 2027-01-24
    motto: "Rindfleischwochen"
    slug: rindfleisch-2027
  # … alle 8 Zeiträume 2027

ausnahmen: []             # z. B. { datum: 2026-12-24, geschlossen: true } [PLATZHALTER]

veranstaltungen:
  - slug: engerl-bengerl-2026
    titel: "Engerl & Bengerl: ein Abend bei Kerzenschein"
    datum: 2026-11-28
    beginn: null          # [PLATZHALTER]
    preis_eur: 41
    preis_einheit: "pro Menü"
    inklusive: ["1 Glas Frizzante", "Gruß aus der Küche", "3-Gänge-Menü"]
    menues:
      - name: "Engerl"
        gaenge: ["Kärntner Rauchschinken mit Schnittlauch-Kräutergervais",
                 "Schweinsmedaillons im Speckmantel mit Kaisergemüse",
                 "Vanille-Eierlikörtraum"]
      - name: "Bengerl"
        gaenge: ["Räucherlachs und Räucherforelle mit Krengervais",
                 "Gansl mit Rotkraut und Kartoffelknödel",
                 "Schokotraum"]
    bild: engerl-bengerl-kerzen.jpg
    bild_alt: "…"
  - slug: stelzen-wochenende-2026-11
    titel: "Stelzen-Wochenende"
    datum: 2026-11-07
    datum_bis: 2026-11-08
    vorbestellung_bis: 2026-11-05
    mitnehmen: true
```

Das Zod-Schema erzwingt: `von` ≤ `bis`, keine Überlappungen, `motto` nicht leer, jedes Bild hat `bild_alt`, `vorbestellung_bis` ≤ `datum`. Weitere Dateien: `speisen.yaml` (Kategorien, Gerichte, Kennzeichen vegetarisch/vegan, optional Preis), `saison/{slug}.yaml` (Schmankerl pro Zeitraum), `tagesmenue.yaml`, `weine.yaml` (Name, Jahrgang, Kategorie, Notiz, Herkunft, Prämierungen[], Preis_ab_hof optional), `heurigenbox.yaml`, `team.yaml`, `site.yaml` (Name, Adresse, Telefon, E-Mail, Geo, Social).

### §6.3 Komponentenliste

| # | Komponente | Zweck | JS | Anmerkungen |
|---|---|---|---|---|
| 1 | `SkipLink` | zum Inhalt springen | — | erstes Element im `<body>` |
| 2 | `StatusBar` | Heute-Status | 1,5 KB | 4 Zustände, Fallback ohne JS |
| 3 | `SiteHeader` | Logo, Navigation, Reservieren | — | `aria-current` |
| 4 | `NavDialog` | mobile Navigation | 1 KB | natives `<dialog>`, `showModal()`, Fokusfalle durch den Browser |
| 5 | `ActionBar` | Anrufen/Reservieren/Route | 0,5 KB | nur < 960 px; ausgeblendet in Formularen; Safe-Area |
| 6 | `SubNav` | Segmente Speisen/Weine, Feiern | — | Scroll-Snap, `aria-current` |
| 7 | `Hero` | Seitenkopf mit Bild | — | `<picture>` Art Direction, LCP-Priorität |
| 8 | `PageHead` | Seitenkopf ohne Bild | — | Eyebrow + H1 + Lead |
| 9 | `AussteckCard` | aktueller/nächster Zeitraum | — | Datum groß, Saisongerichte |
| 10 | `TerminTable` | Jahresliste | — | Tabelle (Desktop) / Karten (Mobile), `<details>` für Vergangenes |
| 11 | `EventCard` | Sonderveranstaltung | — | Datumsmarke, Frist, Preis |
| 12 | `DeadlineNotice` | Vorbestellfrist | — | ändert Text nach Fristablauf (Build + JS-Check) |
| 13 | `IcsLink` | Kalenderdatei | — | .ics wird beim Build erzeugt (RFC 5545, `TZID=Europe/Vienna`) |
| 14 | `MenuSection` / `MenuItem` | Speisekarte | — | optionaler Preis, Diät-Label als Text |
| 15 | `DailyMenu` | Tagesmenü der Woche | 0,3 KB | markiert „Heute“ clientseitig |
| 16 | `WineCard` | Wein mit Notiz und Prämierung | — | Prämierung als Text |
| 17 | `AwardTable` | Prämierungstabelle | — | — |
| 18 | `FeatureBlock` | USP-Block mit Bild | — | Varianten `hell` / `nacht` |
| 19 | `OfferCard` | Ab-Hof-Angebot | — | CTA wählt Formularoption vor |
| 20 | `NumberedSteps` | Ablauf (Feier, Fackelwanderung) | — | `<ol>` |
| 21 | `FactList` | Fakten/„Gut zu wissen“ | — | `<dl>` |
| 22 | `Gallery` | Bildreihe + Großansicht | 1 KB | Scroll-Snap, `<dialog>` |
| 23 | `StaticMap` | Karte als Bild + Routen-Links | — | Build-Skript erzeugt das Bild aus OSM, Attribution |
| 24 | `Faq` | Häufige Fragen | — | `<details>/<summary>` |
| 25 | `CtaBand` | Abschluss-Band | — | Varianten Reservieren / Feier / Heurigenbox |
| 26 | `ShareButton` | Teilen | 0,4 KB | `navigator.share`, Fallback Kopieren |
| 27 | `ReservationWizard` | 3-Schritt-Reservierung | 8 KB | Progressive Enhancement über ein Formular mit 3 Fieldsets |
| 28 | `FormField` | Label, Hinweis, Fehler | — | `aria-describedby`, `aria-invalid` |
| 29 | `Stepper` | Personenzahl | 0,5 KB | basiert auf `input type=number` |
| 30 | `ChoiceChips` | Tage/Uhrzeiten | — | echte Radio-Inputs, gestylt |
| 31 | `ErrorSummary` | Fehlerübersicht | 0,5 KB | Fokus beim Absenden |
| 32 | `Button` | primär/sekundär/Text/Tel | — | min. 44 × 44 px |
| 33 | `SiteFooter` | Footer | — | — |
| 34 | `SeoHead` | Title, Description, Canonical, OG, JSON-LD | — | Pflichtfelder per Typ |

### §6.4 Design-Tokens

**Farben** — siehe §1.5 (dort mit gerechneten Kontrastwerten). Benennung in CSS: `--c-rot`, `--c-rot-tief`, `--c-papier`, `--c-papier-2`, `--c-text`, `--c-text-2`, `--c-holz`, `--c-rebe`, `--c-kerze`, `--c-nacht`, `--c-nacht-text`, `--c-nacht-text-2`, `--c-linie`, `--c-feld-rand`, `--c-fokus`, `--c-ok`, `--c-fehler`.

**Semantische Zuordnung**

| Token | Wert | Verwendung |
|---|---|---|
| `--bg` | `var(--c-papier)` | Seite |
| `--bg-alt` | `var(--c-papier-2)` | Karten, abgesetzte Sektionen |
| `--fg` | `var(--c-text)` | Text |
| `--fg-muted` | `var(--c-text-2)` | Metadaten |
| `--link` | `var(--c-rot)` | Links (unterstrichen, `text-underline-offset: 0.18em`) |
| `--btn-primary-bg` / `-fg` | `#990000` / `#FFFFFF` | Primär-Button (8,92:1) |
| `--btn-primary-bg-active` | `#6E0E12` | gedrückt/hover |
| `--btn-secondary` | Rahmen 2 px `#990000`, Text `#990000`, Grund transparent | Sekundär-Button |
| `--status-open` | `#4A5A2A` + Text `#F4ECDF` (6,43:1) | Statusleiste offen |
| `--status-closed-today` | `#6E0E12` + Text `#F4ECDF` (10,33:1) | Sperrstunde |
| `--status-not-open` | `#7A4E2D` + Text `#FFFFFF` (7,11:1) | nicht ausg'steckt |
| `--focus-ring` | `3px solid #1F5FBF`, `outline-offset: 2px` | alle fokussierbaren Elemente |

**Abstände** (4-px-Basis, als rem bei 16 px Root)

| Token | Wert | Verwendung |
|---|---|---|
| `--space-1` | 0.25rem (4 px) | Icon-Abstand |
| `--space-2` | 0.5rem (8 px) | eng zusammengehörige Elemente |
| `--space-3` | 0.75rem (12 px) | Label → Feld |
| `--space-4` | 1rem (16 px) | Standard-Innenabstand Mobile, Seitenrand Mobile |
| `--space-5` | 1.5rem (24 px) | Kartenpadding, Seitenrand Tablet |
| `--space-6` | 2rem (32 px) | zwischen Blöcken |
| `--space-7` | 3rem (48 px) | Sektionsabstand Mobile |
| `--space-8` | 4rem (64 px) | Sektionsabstand Desktop |
| `--space-9` | 6rem (96 px) | große Zäsuren (vor Nacht-Sektionen) |
| `--gutter` | clamp(1rem, 4vw, 2rem) | Seitenrand |
| `--measure` | 66ch | maximale Textzeilenlänge |
| `--container` | 72rem (1152 px) | maximale Inhaltsbreite |
| `--tap` | 44px | Mindestgröße Touch-Target |

**Typografie-Skala** (fluid, Mobile 360 px → Desktop 1280 px)

| Token | Schrift | Größe (clamp) | Zeilenhöhe | Gewicht | Verwendung |
|---|---|---|---|---|---|
| `--fs-display` | Alegreya | clamp(2.25rem, 1.6rem + 2.8vw, 3.75rem) → 36–60 px | 1.08 | 700 | H1 Startseite |
| `--fs-h1` | Alegreya | clamp(2rem, 1.55rem + 1.9vw, 3rem) → 32–48 px | 1.12 | 700 | H1 Unterseiten |
| `--fs-h2` | Alegreya | clamp(1.625rem, 1.35rem + 1.2vw, 2.25rem) → 26–36 px | 1.18 | 600 | H2 |
| `--fs-h3` | Alegreya | clamp(1.25rem, 1.15rem + 0.45vw, 1.5rem) → 20–24 px | 1.25 | 600 | H3 |
| `--fs-eyebrow` | Alegreya SC | 0.9375rem → 15 px, `letter-spacing: 0.06em` | 1.3 | 500 | Eyebrows (Holz-Farbe) |
| `--fs-lead` | Source Sans 3 | clamp(1.1875rem, 1.1rem + 0.35vw, 1.375rem) → 19–22 px | 1.5 | 400 | Lead-Absätze |
| `--fs-body` | Source Sans 3 | clamp(1.0625rem, 1.03rem + 0.15vw, 1.125rem) → 17–18 px | 1.6 | 400 | Fließtext (Bestand 14 px) |
| `--fs-small` | Source Sans 3 | 0.9375rem → 15 px | 1.5 | 400 | Bildunterschriften, Hinweise (nie kleiner) |
| `--fs-ui` | Source Sans 3 | 1.0625rem → 17 px | 1.2 | 600 | Buttons, Navigation |
| `--fs-input` | Source Sans 3 | 1.0625rem → 17 px (≥ 16 px wegen iOS-Zoom) | 1.4 | 400 | Formularfelder |
| `--fs-date` | Source Sans 3 | clamp(1.75rem, 1.4rem + 1.5vw, 2.75rem) | 1.1 | 700, `tabular-nums lining-nums` | große Datumsangaben |

**Weitere Tokens**

| Token | Wert |
|---|---|
| `--radius-s` | 2px (Chips, Felder) |
| `--radius-m` | 4px (Buttons, Karten) |
| `--radius-l` | 8px (Bilder in Karten) |
| `--shadow-1` | `0 1px 2px rgb(42 33 28 / 0.08), 0 2px 8px rgb(42 33 28 / 0.06)` (nur Karten, nur hell) |
| `--border` | `1px solid var(--c-linie)` |
| `--border-input` | `1.5px solid var(--c-feld-rand)` |
| `--dur-fast` / `--dur` | 120 ms / 180 ms, `ease-out` |
| `--z-header` / `--z-actionbar` / `--z-dialog` | 10 / 20 / 100 |

**Breakpoints:** `--bp-s` 600 px (Tablet), `--bp-m` 960 px (Desktop-Navigation, Zweispalter), `--bp-l` 1280 px (breite Raster). Mobile-first: Media-Queries nur mit `min-width`.

### §6.5 iPhone/Safari-Pflichten

1. `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. Zoom wird **nicht** gesperrt (kein `maximum-scale`, WCAG 1.4.4).
2. Safe-Area: Header `padding-top: env(safe-area-inset-top)`, Aktionsleiste `padding-bottom: max(0.5rem, env(safe-area-inset-bottom))`, seitliche Ränder im Querformat `max(var(--gutter), env(safe-area-inset-left/right))`.
3. Höhenangaben mit `svh`/`dvh` statt `vh` (Safari-Adressleiste). Das Hero-Bild bekommt `max-height: 60svh`.
4. Kein Hover-only-Verhalten: Hover-Stile stehen in `@media (hover: hover) and (pointer: fine)`. Alle Inhalte und Funktionen sind ohne Hover erreichbar.
5. Touch-Targets ≥ 44 × 44 px, auch für Textlinks in Listen (Zeilenhöhe/Padding). Abstand zwischen benachbarten Targets ≥ 8 px.
6. Formularfelder ≥ 16 px Schrift; `autocomplete`, `inputmode`, `enterkeyhint` gesetzt; `type="tel"` für Telefon.
7. `-webkit-tap-highlight-color: transparent` nur zusammen mit eigenem `:active`-Zustand.
8. `<dialog>` (ab iOS 15.4 unterstützt), Scroll-Lock über `overflow: hidden` am `<html>` während das Menü offen ist.
9. `format-detection`: `<meta name="format-detection" content="telephone=no">`, damit Safari nicht wahllos Zahlen (z. B. die UID) zu Telefonlinks macht. Echte Telefonlinks sind explizit gesetzt.
10. Testgeräte: iPhone SE (375 px, kleinster Fall), iPhone 15/16 (393 px), iPhone Pro Max (430 px), iPad Querformat; iOS-Versionen: aktuelle und vorige Hauptversion.

### §6.6 Performance-Budget

| Messgröße | Budget Startseite | Budget Unterseiten | Bestand (Audit) |
|---|---|---|---|
| Gesamtgewicht beim ersten Laden | **≤ 900 KB** (Ziel 600 KB) | ≤ 700 KB | mehrere MB (Bilder bis 2,25 MB je Stück) |
| HTML (Brotli) | ≤ 30 KB | ≤ 25 KB | 166 KB unkomprimiert |
| CSS gesamt (roh / Brotli) | ≤ 50 KB / ≤ 12 KB (Ziel 28 KB roh) | gleiche Datei | 32 CSS-Dateien, `js_composer.css` allein 459 KB |
| JavaScript (Brotli) | ≤ 15 KB | ≤ 15 KB (Reservierung ≤ 20 KB) | 70 JS-Dateien, `rs6.min.js` 416 KB |
| Schriften | ≤ 110 KB (2 Dateien) | gleich, aus Cache | 5 OpenSans + 2 weitere, inkl. eot/svg |
| Bilder | ≤ 600 KB, davon Hero ≤ 120 KB (Mobile) / ≤ 200 KB (Desktop) | ≤ 450 KB | 39,6 MB im Mirror |
| Einzelbild unter dem Fold | ≤ 80 KB (Mobile) / ≤ 150 KB (Desktop) | dto. | — |
| Requests beim ersten Laden | ≤ 20 | ≤ 20 | > 100 |
| Drittanbieter-Domains | **0** | 0 | Google Maps, Facebook-Emoji-CDN |
| TTFB | < 0,3 s | < 0,3 s | 1,93 s |
| LCP (Lab, Lighthouse „Mobile“, simuliert 4G 1,6 Mbit/s, 150 ms RTT) | < 2,0 s | < 2,0 s | — |
| LCP (Lab, „4G“ 9 Mbit/s, 60 ms RTT — Vorgabe) | **< 1,5 s** | < 1,5 s | — |
| CLS | < 0,05 | < 0,05 | — |
| INP (Feld, sobald Daten vorliegen) | < 200 ms | < 200 ms | — |
| Lighthouse Performance / Accessibility / Best Practices / SEO | ≥ 95 / 100 / 100 / 100 | dto. | — |

**Maßnahmen zur Einhaltung**

1. Kritisches CSS ist nicht nötig (eine Datei ≤ 12 KB Brotli, `<link rel="stylesheet">` im Head; bei HTTP/2 parallel zum HTML).
2. Hero-Bild: `<link rel="preload" as="image" imagesrcset=… imagesizes=…>` und `fetchpriority="high"`. Alle anderen Bilder `loading="lazy"` und `decoding="async"`, jeweils mit `width`/`height` gegen CLS.
3. `srcset`-Stufen: 480, 768, 1024, 1440, 1920 w. Formate AVIF (Qualität ≈ 50), WebP (≈ 72), JPEG-Fallback (≈ 75, progressiv). `sizes` exakt pro Komponente gesetzt.
4. Vorkomprimierung beim Build: `.br` (Qualität 11) und `.gz` für HTML/CSS/JS/SVG/ICS. Der Server liefert sie mit `Content-Encoding`.
5. Cache: Assets mit Hash im Dateinamen → `Cache-Control: public, max-age=31536000, immutable`. HTML → `no-cache` (revalidieren per ETag), damit Termine nie veraltet aus dem Cache kommen.
6. Kein JavaScript blockiert das Rendering. Alle Skripte als `type="module"` (automatisch deferred).
7. Budget-Prüfung in CI: Lighthouse CI mit Assertions + eigenes Größenskript, das den Build bei Überschreitung abbricht.

### §6.7 Bildpipeline

1. Originale liegen in `src/assets/img/` (vom Fotografen, max. 3000 px lange Kante, sRGB, ohne GPS-EXIF).
2. Dateinamen beschreibend: `gastgarten-sommer-belegt.jpg`, `kostbar-in-rot-brett.jpg`.
3. `<Picture>`-Komponente von Astro mit Pflichtparametern `alt`, `widths`, `sizes`. Fehlender `alt` lässt den Build scheitern.
4. Metadaten werden beim Export entfernt (EXIF/GPS — Datenschutz der Fotografierten und des Betriebs).
5. OG-Bilder (1200 × 630, JPEG ≤ 200 KB) werden pro Seite aus dem Hero-Bild zugeschnitten, mit Logo-Stempel in der Ecke. Für Veranstaltungen kommen Titel und Datum in Alegreya dazu, gerendert beim Build. Das ist die einzige Stelle, an der Text ins Bild geht, weil WhatsApp-Vorschauen nur das Bild zeigen.

### §6.8 Accessibility-Anforderungen (WCAG 2.1 AA)

| # | Anforderung | WCAG | Umsetzung / Prüfung |
|---|---|---|---|
| 1 | Textkontrast ≥ 4,5:1 (groß ≥ 3:1) | 1.4.3 | Token-Paare aus §1.5, automatischer Kontrastcheck im CI (axe-core) |
| 2 | Nicht-Text-Kontrast ≥ 3:1 (Feldränder, Fokus, Icons) | 1.4.11 | `--c-feld-rand` 4,72:1, Fokus 5,65:1 |
| 3 | Farbe nie alleiniger Informationsträger | 1.4.1 | Status mit Wort, Fehler mit Text + Icon, Links unterstrichen |
| 4 | Ein H1 pro Seite, lückenlose Hierarchie | 1.3.1, 2.4.6 | Build-Check zählt H1 und erkennt Sprünge (Audit: 13 Seiten ohne H1) |
| 5 | Landmarks: `header`, `nav` (mit `aria-label` „Hauptnavigation“), `main`, `footer` | 1.3.1 | Layout-Komponente |
| 6 | Skip-Link | 2.4.1 | G1 |
| 7 | Sichtbarer Fokus auf allen Bedienelementen | 2.4.7 | `:focus-visible`-Ring, nie `outline: none` ohne Ersatz |
| 8 | Vollständige Tastaturbedienung, logische Reihenfolge | 2.1.1, 2.4.3 | Test ohne Maus und mit iOS-Tastatur + VoiceOver |
| 9 | Labels für alle Felder, Pflichtangabe im Text | 1.3.1, 3.3.2 | `FormField`-Komponente (Audit: Platzhalter statt Labels) |
| 10 | Fehler erkennen, beschreiben, Vorschlag machen | 3.3.1, 3.3.3 | Texte §4.8, `aria-invalid`, `aria-describedby`, `ErrorSummary` |
| 11 | `autocomplete` für Personendaten | 1.3.5 | name, tel, email, street-address |
| 12 | Alt-Texte für informative Bilder, `alt=""` für dekorative | 1.1.1 | Pflichtfeld im Schema (Audit: 26 ohne Alt) |
| 13 | Kein Text in Bildern (außer Logo, OG-Bild) | 1.4.5 | Plakatgrafiken werden durch HTML ersetzt |
| 14 | Zoom bis 200 % und Umbruch bei 320 px ohne horizontales Scrollen | 1.4.4, 1.4.10 | `rem`-Typografie, kein Zoom-Lock, Test bei 320 px |
| 15 | Textabstände anpassbar | 1.4.12 | keine fixen Höhen bei Textcontainern |
| 16 | Keine Autoplay-Bewegung > 5 s; `prefers-reduced-motion` | 2.2.2, 2.3.3 (AAA, freiwillig) | kein Slider; Übergänge deaktivierbar |
| 17 | Zielgröße ≥ 44 px | 2.5.5 (AAA, Projektvorgabe) | `--tap`-Token |
| 18 | Sprache `lang="de-AT"`; Dialektwörter ohne eigene Auszeichnung | 3.1.1 | `<html lang="de-AT">` |
| 19 | Eindeutige Linktexte (kein „Hier klicken“, keine 13 × „Zur Tischreservierung“ mit gleichem Ziel und Kontext) | 2.4.4 | Texte §4 |
| 20 | Dialoge: Fokus hinein, Escape schließt, Fokus kehrt zurück | 2.4.3 | natives `<dialog>` |
| 21 | Statusmeldungen ohne Fokuswechsel ansagen (Formular gesendet, Schritt gewechselt) | 4.1.3 | `aria-live="polite"` |
| 22 | Tabellen mit `<th scope>` und `<caption>` | 1.3.1 | Termin-, Prämierungs-, Raumtabelle |
| 23 | Seitentitel eindeutig | 2.4.2 | Muster §7.1 |

**Prüfverfahren:** axe-core in CI (0 Verstöße), Lighthouse A11y 100, manueller Test mit VoiceOver auf iPhone (Safari) für Startseite, Reservierung und Feieranfrage, Tastaturtest am Desktop, Zoom 200 %, 320-px-Ansicht, Graustufenansicht (Farbe als Information).

### §6.9 Qualitätsprüfungen im Build

1. Kein Vorkommen von `localhost`, `joomexp`, `http://` (außer in Rechtstexten zitierten URLs), `wp-content` in der Ausgabe (Audit Befund 6).
2. Jede indexierbare Seite hat Title (≤ 60 Zeichen), Description (120–155 Zeichen), Canonical, OG-Bild, genau ein H1.
3. JSON-LD wird gegen ein Schema validiert. Optional zusätzlich Schema.org-Validator im CI.
4. Linkprüfung (intern 0 Fehler, Anker existieren — wichtig für die 301-Ziele mit `#`).
5. Termin-Logik-Tests (Unit-Tests): Statusleiste für 12 Stichzeitpunkte (vor Öffnung, offen, Sperrstunde Mo–Sa/So, letzter Tag, zwischen Zeiträumen, Jahreswechsel, Zeitumstellung Ende März/Oktober).
6. Größenbudget (§6.6) und Lighthouse CI.
7. Rechtschreibprüfung Deutsch (Österreich) über Inhalte (z. B. Vale/LanguageTool lokal), Wortliste §1.3 als erlaubte Begriffe.

### §6.10 Security-Header und Server

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cross-Origin-Opener-Policy: same-origin
X-Frame-Options: DENY
```

- Das Inline-Skript der Statusleiste wird als externe Datei ausgeliefert. Alternativ bekommt es einen CSP-Hash, damit `'unsafe-inline'` nicht nötig ist.
- HSTS `preload` erst nach 4 Wochen stabilem Betrieb und Prüfung aller Subdomains (Wildcard-Zertifikat vorhanden, Audit §2). Daher erst ohne `preload`.
- `http://` → `https://www.` in einem Sprung (Audit §5.4).
- Formular-Endpunkt: nur POST, Größenlimit 10 KB, Rate-Limit 5 Anfragen/10 min/IP, serverseitige Validierung, keine Speicherung in einer Datenbank (nur Mailversand). Optional ein Mail-Archiv beim Betrieb, Aufbewahrung laut Datenschutzerklärung.
- Mit WordPress entfallen: `/wp-json/wp/v2/users` (User-Enumeration), `readme.html`/`license.txt` (Versionsanzeige), `xmlrpc.php`, Plugin-Lücken.
- `security.txt` unter `/.well-known/security.txt` mit Kontakt-E-Mail.

---

## §7 SEO- und Schema-Spezifikation

### §7.1 Title- und Description-Muster

**Regeln:** Der Title hat höchstens 60 Zeichen, das Wichtigste steht vorn, am Ende die Marke „Heuriger Neumayer“. Die Description hat 120–155 Zeichen, enthält Ort, konkrete Fakten und eine Handlung, aber keine Keyword-Listen. Beide sind Pflichtfelder im Frontmatter, ohne sie bricht der Build ab (Audit Befund 2: 0 von 36 Seiten hatten eine Description).

| Seite | Title | Meta-Description |
|---|---|---|
| `/` | Weinbau & Heuriger Neumayer · Perchtoldsdorf | Familienheuriger in Perchtoldsdorf: eigener Wein, Hausmannskost, Gastgarten und Spielplatz. Achtmal im Jahr ausg'steckt. Jetzt Tisch reservieren. |
| `/termine/` | Ausstecktermine 2026 & 2027 · Heuriger Neumayer | Wann ist ausg'steckt? Alle Termine 2026 und 2027 mit Schmankerlwochen, Öffnungszeiten Mo–Sa 10:30–23:00, So bis 22:30 – auch als Kalenderdatei. |
| `/termine/{slug}/` | {Titel} am {T. Monat} · Heuriger Neumayer | {Datum}: {Kurzbeschreibung, 1 Satz}. {Preis, falls belegt}. Beim Heurigen Neumayer in Perchtoldsdorf – jetzt reservieren. |
| Beispiel Engerl & Bengerl | Engerl & Bengerl am 28. November · Heuriger Neumayer | Sa, 28.11.2026: Abend bei Kerzenschein mit zwei 3-Gänge-Menüs zur Wahl, inkl. Frizzante, € 41. Heuriger Neumayer, Perchtoldsdorf – jetzt reservieren. |
| `/speisen/` | Speisekarte & Schmankerl · Heuriger Neumayer | Backhendl, Schweinsbratenpfandl, Blunz'n und Riesenbrote, dazu Saisonschmankerl und Tagesmenü mit Suppe. Auch vegetarisch und vegan, in Perchtoldsdorf. |
| `/weine/` | Weine aus Perchtoldsdorf · Weinbau Neumayer | Gemischter Satz, Rotgipfler, Zweigelt Barrique & mehr aus eigenem Keller – mehrfach prämiert 2026. Mit KOSTBAR in ROT: vier Rote zum Verkosten. |
| `/ab-hof/` | Ab Hof: Wein, Heurigenbox & 24-h-Automat · Neumayer | Wein rund um die Uhr aus unserem Getränkeautomaten, Spritzer TO GO, Geschenkebox und Heurigenbox ab 5 Personen. Ab Hof in Perchtoldsdorf. |
| `/feiern/` | Feiern beim Heurigen: Hochzeit, Firma, Seminar · Neumayer | Feiern für bis zu 200 Gäste in Stüberl, Gastraum oder Gastgarten – auch wenn nicht ausg'steckt ist. Buffet oder Menü, auf Wunsch mit Fackelwanderung. |
| `/feiern/fackelwanderung/` | Fackelwanderung Perchtoldsdorfer Heide · Neumayer | Mit Fackeln in rund 20 Minuten zu unserem Weingarten auf der Perchtoldsdorfer Heide – oben Erfrischung und Blick über ganz Wien. Für Ihre Feier. |
| `/besuch/` | Anfahrt, Lokal & Kontakt · Heuriger Neumayer | Sonnbergstraße 89, 2380 Perchtoldsdorf. Zwei Ebenen, Stüberl, Gastgarten, Kinderspielplatz. Telefon 0664 211 08 25 – Anfahrt, Team und Kontakt. |
| `/reservierung/` | Tisch reservieren · Heuriger Neumayer Perchtoldsdorf | In drei Schritten einen Tisch für einen unserer Ausstecktage anfragen – oder anrufen: 0664 211 08 25. Ab 11 Personen planen wir Ihre Feier persönlich. |
| `/impressum/` | Impressum · Weinbau & Heuriger Neumayer | Impressum und Offenlegung gemäß ECG und Mediengesetz: Weinbau & Heuriger Neumayer, Inhaber Christian Neumayer, Sonnbergstraße 89, 2380 Perchtoldsdorf. |
| `/datenschutz/` | Datenschutz · Weinbau & Heuriger Neumayer | Wie wir mit Ihren Daten umgehen: keine Cookies, kein Tracking, Formulare nur zur Bearbeitung Ihrer Anfrage. Ihre Rechte nach DSGVO. |
| `/danke/*`, `/404` | „Danke für Ihre Anfrage · Heuriger Neumayer“ / „Seite nicht gefunden · Heuriger Neumayer“ | `noindex, follow`, keine Description nötig |

**Weitere On-Page-Regeln**

- H1 stimmt inhaltlich mit dem Title überein, ist aber nicht identisch (H1 für Menschen, Title für die Ergebnisliste).
- Interne Links mit beschreibenden Ankertexten („Ausstecktermine 2027“, nicht „hier“).
- Bilddateinamen und Alt-Texte beschreibend (§4.9).
- `<html lang="de-AT">`. Kein hreflang, solange es nur Deutsch gibt (Frage 14).
- `sitemap.xml` enthält nur indexierbare Seiten und zukünftige Veranstaltungen, mit `lastmod` aus dem Git-Commit. `robots.txt` mit `Sitemap:`-Zeile.
- Staging läuft unter eigener Subdomain mit `X-Robots-Tag: noindex` **host-basiert** (nicht per Meta-Tag im HTML, damit das beim Go-Live nicht versehentlich mitwandert).

### §7.2 Schema.org (JSON-LD)

**Überblick**

| Seite | Typen |
|---|---|
| alle | `WebSite`, `Restaurant`+`Winery` (per `@id` referenziert, voll nur auf `/` und `/besuch/`) |
| `/` | `Restaurant`+`Winery` vollständig |
| `/termine/` | `Restaurant` (Referenz) + `ItemList` der `FoodEvent`s |
| `/termine/{slug}/` | `FoodEvent`, `BreadcrumbList` |
| `/speisen/` | `Menu` mit `MenuSection`/`MenuItem`, `BreadcrumbList` |
| `/weine/` | `BreadcrumbList` (Produkt-Schema erst mit veröffentlichten Preisen sinnvoll) |
| `/feiern/`, `/feiern/fackelwanderung/`, `/ab-hof/`, `/besuch/` | `BreadcrumbList` (+ `Restaurant` vollständig auf `/besuch/`) |

**Bewusst nicht verwendet:**

- `AggregateRating`/`Review` auf der eigenen Seite: selbst ausgewiesene Bewertungen sind für lokale Unternehmen nicht Rich-Result-fähig und verstoßen gegen die Google-Richtlinien.
- `FAQPage`: Google zeigt FAQ-Rich-Results seit 2023 nur noch für Behörden- und Gesundheitsseiten.
- `Event` für die Aussteckzeiträume selbst: Das sind Öffnungszeiten, keine Veranstaltungen. Sie werden als saisonale `openingHoursSpecification` modelliert.

**Beispiel 1 — Betrieb (Startseite), generiert aus `site.yaml` + `termine.yaml`**

```json
{
  "@context": "https://schema.org",
  "@type": ["Restaurant", "Winery"],
  "@id": "https://www.weinbauneumayer.at/#betrieb",
  "name": "Weinbau & Heuriger Neumayer",
  "alternateName": "Heuriger Neumayer",
  "url": "https://www.weinbauneumayer.at/",
  "logo": "https://www.weinbauneumayer.at/img/logo-neumayer-rot.png",
  "image": [
    "https://www.weinbauneumayer.at/og/start-1200x630.jpg"
  ],
  "description": "Familienheuriger mit eigenem Weinbau in Perchtoldsdorf. Achtmal im Jahr ausg'steckt, mit Gastgarten, Kinderspielplatz und Stüberl für Feiern.",
  "telephone": "+43 664 2110825",
  "email": "christian@weinbauneumayer.at",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Sonnbergstraße 89",
    "postalCode": "2380",
    "addressLocality": "Perchtoldsdorf",
    "addressRegion": "Niederösterreich",
    "addressCountry": "AT"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 48.12844,
    "longitude": 16.25613
  },
  "servesCuisine": ["Heurigenküche", "Österreichische Küche"],
  "acceptsReservations": "https://www.weinbauneumayer.at/reservierung/",
  "hasMenu": "https://www.weinbauneumayer.at/speisen/",
  "amenityFeature": [
    { "@type": "LocationFeatureSpecification", "name": "Gastgarten", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Kinderspielplatz", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Spielecke im Gastraum", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Getränkeautomat, täglich 24 Stunden", "value": true }
  ],
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      "opens": "10:30",
      "closes": "23:00",
      "validFrom": "2026-11-21",
      "validThrough": "2026-12-06"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Sunday",
      "opens": "10:30",
      "closes": "22:30",
      "validFrom": "2026-11-21",
      "validThrough": "2026-12-06"
    }
  ],
  "sameAs": ["https://www.facebook.com/weinbauneumayer"]
}
```

*Hinweise:* Der Generator gibt die `openingHoursSpecification` für **alle zukünftigen** Aussteckzeiträume der nächsten 12 Monate aus (2 Einträge je Zeitraum). Die Geo-Koordinaten stammen aus dem bisherigen Maps-Embed und werden vor Ort verifiziert. `priceRange` bleibt weg, bis Preise vorliegen. Das Logo wird als PNG ≥ 112 px referenziert. **Wichtig:** Die maßgebliche Quelle für Google-Öffnungszeiten ist das Google-Unternehmensprofil. Es muss dieselben Zeiträume als „Sonderöffnungszeiten“ führen (Frage 26), sonst widersprechen sich Website und Maps.

**Beispiel 2 — Veranstaltung**

```json
{
  "@context": "https://schema.org",
  "@type": "FoodEvent",
  "name": "Engerl & Bengerl: ein Abend bei Kerzenschein",
  "startDate": "2026-11-28",
  "endDate": "2026-11-28",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "description": "Abend bei Kerzenschein und leiser Musik mit zwei 3-Gänge-Menüs zur Wahl (Engerl oder Bengerl), inklusive einem Glas Frizzante und Gruß aus der Küche.",
  "image": ["https://www.weinbauneumayer.at/og/engerl-bengerl-2026-1200x630.jpg"],
  "url": "https://www.weinbauneumayer.at/termine/engerl-bengerl-2026/",
  "location": {
    "@type": "Place",
    "name": "Weinbau & Heuriger Neumayer",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Sonnbergstraße 89",
      "postalCode": "2380",
      "addressLocality": "Perchtoldsdorf",
      "addressCountry": "AT"
    }
  },
  "organizer": { "@id": "https://www.weinbauneumayer.at/#betrieb" },
  "offers": {
    "@type": "Offer",
    "price": "41.00",
    "priceCurrency": "EUR",
    "url": "https://www.weinbauneumayer.at/reservierung/?datum=2026-11-28&anlass=engerl-bengerl-2026",
    "availability": "https://schema.org/InStock",
    "description": "Preis pro Menü"
  }
}
```

*Hinweis:* Sobald die Beginnzeit feststeht, wird `startDate` als `2026-11-28T18:00+01:00` [PLATZHALTER] angegeben (Google empfiehlt Uhrzeiten).

**Beispiel 3 — Speisekarte (Auszug)**

```json
{
  "@context": "https://schema.org",
  "@type": "Menu",
  "name": "Speisekarte Heuriger Neumayer",
  "url": "https://www.weinbauneumayer.at/speisen/",
  "inLanguage": "de-AT",
  "hasMenuSection": [
    {
      "@type": "MenuSection",
      "name": "Gebackenes",
      "hasMenuItem": [
        { "@type": "MenuItem", "name": "Backhendlschmaus" },
        { "@type": "MenuItem", "name": "Gebackene Blunz'n mit Sauce Tartare" },
        { "@type": "MenuItem", "name": "Surschnitzel" }
      ]
    },
    {
      "@type": "MenuSection",
      "name": "Vegetarisch & vegan",
      "hasMenuItem": [
        { "@type": "MenuItem", "name": "Gebackener Camembert mit Preiselbeeren",
          "suitableForDiet": "https://schema.org/VegetarianDiet" },
        { "@type": "MenuItem", "name": "Veganes Cevapcici mit Pommes",
          "suitableForDiet": "https://schema.org/VeganDiet" }
      ]
    }
  ]
}
```

Preise (`offers`) werden ergänzt, sobald sie veröffentlicht werden dürfen (Frage 6).

**Beispiel 4 — Breadcrumb**

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Start", "item": "https://www.weinbauneumayer.at/" },
    { "@type": "ListItem", "position": 2, "name": "Feiern", "item": "https://www.weinbauneumayer.at/feiern/" },
    { "@type": "ListItem", "position": 3, "name": "Fackelwanderung", "item": "https://www.weinbauneumayer.at/feiern/fackelwanderung/" }
  ]
}
```

### §7.3 Open Graph und Teilen

Pro Seite: `og:type` (`website`, bei Veranstaltungen `article`), `og:site_name` „Weinbau & Heuriger Neumayer“, `og:locale` `de_AT`, `og:title` (= Title ohne Markenzusatz), `og:description` (= Meta-Description), `og:url` (= Canonical), `og:image` (1200 × 630, absolute URL, mit `og:image:alt`), `twitter:card` `summary_large_image`. Getestet wird die Vorschau in WhatsApp (iOS) und im Facebook-Sharing-Debugger. Nach Go-Live wird der Facebook-Cache der wichtigsten URLs einmal neu abgerufen (Audit Befund 4).

### §7.4 Redirect-Strategie

**Grundsätze**

1. Jede jemals indexierte URL bekommt eine Antwort: 200, 301 auf das inhaltlich passende Ziel, oder 410 bei bewusst entfernten Inhalten. Es gibt keine Massenumleitung auf die Startseite (das würde Google als Soft-404 werten).
2. Es gibt nur **eine** Weiterleitungsstufe (kein A → B → C).
3. Die Redirects liegen als Datei im Repo (`redirects.csv`), werden beim Build in die Serverkonfiguration übersetzt und durch ein Testskript geprüft (jede Zeile: Status + Ziel).
4. Basis ist die URL-Liste aus Crawl (39 URLs), `wp-sitemap.xml` des Bestands und — nach Zugang — dem Search-Console-Bericht „Seiten“ (Frage 10). URLs mit Backlinks oder Impressionen, die bisher nicht erfasst sind, kommen vor dem Go-Live dazu.

**Tabelle (vollständig für alle bekannten URLs)**

| Quelle | Ziel | Status |
|---|---|---|
| `http://weinbauneumayer.at/*`, `http://www.weinbauneumayer.at/*`, `https://weinbauneumayer.at/*` | `https://www.weinbauneumayer.at/*` | 301 (ein Sprung) |
| `/ueber/` | `/besuch/#familie` | 301 |
| `/galerie/` | `/besuch/#lokal` | 301 |
| `/kontakt/` | `/besuch/#kontakt` | 301 |
| `/schmankerl/` | `/speisen/#saison` | 301 |
| `/speisen/tagesmenues/`, `/tagesmenues/` | `/speisen/#tagesmenue` | 301 |
| `/reservierung` (ohne Slash), alle Seiten ohne Slash | mit Slash | 301 |
| `/?p=405`, `/?page_id=405` | `/` | 301 |
| `/?p=406` | `/besuch/#familie` | 301 |
| `/?p=408` | `/speisen/` | 301 |
| `/?p=759` | `/besuch/#kontakt` | 301 |
| `/?p=862` | `/weine/` | 301 |
| `/?p=904` | `/reservierung/` | 301 |
| `/?p=1717` | `/impressum/` | 301 |
| `/?p=1986` | `/feiern/` | 301 |
| `/?p=2036` | `/termine/` | 301 |
| `/?p=2135` | `/speisen/#tagesmenue` | 301 |
| `/?p=2144` | `/speisen/#saison` | 301 |
| `/?p=3238` | `/besuch/#lokal` | 301 |
| `/?p=3312` | `/datenschutz/` | 301 |
| `/pointofsale_category/weine/` | `/weine/` | 301 |
| `/pointofsale_category/essen/` | `/speisen/` | 301 |
| `/pointofsale_category/team/`, `/pointofsale/friendly/` | `/besuch/#familie` | 301 |
| `/wp-content/uploads/2026/09/menueoktober26-1.pdf` | `/speisen/#tagesmenue` | 301 |
| `/feed/`, `/comments/feed/`, `/*/feed/` | — | 410 |
| `/wp-json/*`, `/wp-admin/*`, `/wp-login.php`, `/xmlrpc.php`, `/readme.html`, `/license.txt`, `/wp-includes/*` | — | 410 |
| `/wp-content/uploads/*` (übrige) | — | 410 |
| WooCommerce-/Events-Manager-Seiten (Slugs aus dem WP-Backend, z. B. Warenkorb, Kasse, Mein Konto, Veranstaltungen) [PLATZHALTER: Slugs exportieren] | `/ab-hof/` bzw. `/termine/` | 301 |
| `/termine/{slug}/` vergangener Veranstaltungen | ab Tag + 1: 200 mit `noindex` und Hinweis „Diese Veranstaltung ist vorbei“; ab Tag + 90: 301 auf `/termine/` | 200 → 301 |
| optional `heurigenbox.at/*` (wenn Domain dem Betrieb gehört) | `https://www.weinbauneumayer.at/ab-hof/#heurigenbox` | 301 |

*Anmerkung zu Ankern:* Ziele mit `#` sind zulässig. Der Browser übernimmt den Anker aus dem `Location`-Header, Google ignoriert ihn und wertet die Seite ohne Anker. Die Anker-IDs sind deshalb Teil des Komponentenvertrags (§2.4) und werden im Build geprüft.

**Beispiel Apache (falls der bestehende Host bleibt)**

```apache
RewriteEngine On
# Host und Protokoll in einem Sprung
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\.weinbauneumayer\.at$ [NC]
RewriteRule ^ https://www.weinbauneumayer.at%{REQUEST_URI} [R=301,L,NE]
# WordPress-Shortlinks
RewriteCond %{QUERY_STRING} (?:^|&)(?:p|page_id)=904(?:&|$)
RewriteRule ^$ /reservierung/? [R=301,L]
# zusammengelegte Seiten
RewriteRule ^ueber/?$ /besuch/#familie [R=301,L,NE]
RewriteRule ^schmankerl/?$ /speisen/#saison [R=301,L,NE]
# entfernte WordPress-Pfade
RewriteRule ^(wp-json|wp-admin|wp-includes)(/.*)?$ - [G,L]
RewriteRule ^(xmlrpc\.php|readme\.html|license\.txt|wp-login\.php)$ - [G,L]
```

(Wird aus `redirects.csv` vollständig generiert. Die Caddy-Variante entsteht analog über `redir`/`respond 410`.)

**Go-Live-Reihenfolge (SEO-relevant)**

1. Staging komplett, Redirect-Test grün, Lighthouse/axe grün.
2. Backup des alten WordPress (Dateien + Datenbank) beim Betrieb bzw. bei der Agentur sichern (Frage 10).
3. DNS bzw. Document Root umstellen, TLS prüfen.
4. Direkt nach dem Umstellen: Redirect-Skript gegen Produktion, Stichprobe der 410er, `robots.txt` und `sitemap.xml` prüfen, kein `noindex` auf Produktion.
5. Search Console: neue Sitemap einreichen, alte `wp-sitemap.xml` entfernen und die URL-Prüfung für die 5 Hauptseiten anstoßen.
6. Google-Unternehmensprofil: Website-Link, Öffnungszeiten (Sonderöffnungszeiten je Aussteckzeitraum) und Reservierungslink aktualisieren.
7. 14 Tage tägliches Monitoring der 404 im Serverlog, danach wöchentlich für 3 Monate.

---

## §8 Messung ohne Tracker

**Grundsatz:** Kein Cookie, kein Fingerprinting, kein Analysedienst mit Personenbezug. Damit braucht die Seite weiterhin **kein Cookie-Banner** — das ist eine Stärke des Bestands, die erhalten bleibt (Audit §5.4). Gemessen wird, was für Entscheidungen nötig ist, nicht mehr.

### §8.1 Quellen und was sie beantworten

| Quelle | Was sie misst | Welche Frage sie beantwortet | Aufwand |
|---|---|---|---|
| **Google Search Console** | Impressionen, Klicks, CTR, Position je Suchanfrage und Seite; Indexierungsstatus; Core Web Vitals (Felddaten, sofern genug Chrome-Nutzer); Rich-Result-Status (Events, Breadcrumbs) | Wird der Heurige für „Heuriger Perchtoldsdorf“, „Fackelwanderung Perchtoldsdorf“, „Heurigenbox“ gefunden? Wirken die neuen Descriptions (CTR)? | Verifizierung per DNS-TXT oder Meta-Tag, 1 h |
| **Bing Webmaster Tools** | wie oben für Bing/Ecosia/DuckDuckGo-Anteile | Ergänzung | Import aus GSC, 15 min |
| **Google-Unternehmensprofil (Statistik)** | Anrufe über das Profil, Routenanfragen, Website-Klicks | Wie viele Gäste rufen direkt aus Maps an? (dort fällt ein großer Teil der Anrufe an) | bereits vorhanden? (Frage 26) |
| **Serverlogs** (Webserver, IP gekürzt auf /24 bzw. /48 oder gar nicht gespeichert, Aufbewahrung 14 Tage) | Seitenaufrufe pro URL und Tag, Referrer-Domains (WhatsApp, Facebook, Google), 404-Fehler, Redirect-Treffer, Bot-Anteil | Welche Seiten werden genutzt? Funktionieren die Redirects? Welche alten URLs werden noch aufgerufen? | Auswertung mit GoAccess lokal, als statischer Monatsbericht; 3 h Einrichtung |
| **Formular-Endpunkt (Zähler)** | Anzahl gesendeter Reservierungs-, Feier-, Bestellanfragen pro Tag, Abbruch durch Validierungsfehler (nur Zähler, keine Inhalte) | Steigen die Online-Reservierungen? Welches Feld verursacht Fehler? | im Endpunkt enthalten |
| **Optional: anonymer Ereigniszähler** | `navigator.sendBeacon('/z', 'tel')` bei Tap auf Anrufen, Route, Teilen, Kalender — der Server zählt nur Ereignisname + Datum und speichert kein Log mit IP für diesen Pfad | Wie oft wird von der Website aus angerufen bzw. eine Route geöffnet? | 2 h; im Datenschutztext beschrieben |
| **Betrieb (manuell)** | Frage am Telefon/an der Schank „Wie haben Sie von uns erfahren?“ einen Monat lang auf einer Strichliste; optionales Feld „Wie sind Sie auf uns gekommen?“ in der Feieranfrage | Anteil Website vs. Empfehlung vs. Maps | 0 h Technik |

**Zur Einordnung des optionalen Zählers:** Er liest und speichert nichts auf dem Endgerät (kein Cookie, kein Local Storage). Es wird eine einzige anonyme Anfrage an den eigenen Server gesendet, ohne Kennung. Nach meiner Einschätzung fällt das nicht unter die Einwilligungspflicht nach § 165 Abs. 3 TKG 2021. Das ist eine Einschätzung, keine Rechtsberatung, und vor dem Einsatz kurz prüfen lassen (Frage 17). Empfehlung: einschalten, weil der Anruf der wichtigste Kanal ist und sonst gar nicht sichtbar wird.

### §8.2 Kennzahlen und Zielwerte (Basis = 3 Monate vor Go-Live aus GSC, sobald Zugang besteht)

1. **Organische Klicks** auf die Domain: +30 % in 6 Monaten (Zielwert vorläufig, wird nach Sichtung der GSC-Basis angepasst).
2. **CTR in der Google-Suche** für Marken- und Ortsanfragen („neumayer perchtoldsdorf“, „heuriger perchtoldsdorf“): +2 Prozentpunkte durch Descriptions und Rich Results.
3. **Online-Reservierungsanfragen pro Ausstecken:** Basiswert beim Betrieb erfragen (Redi-Backend), Ziel +25 %.
4. **Feieranfragen pro Quartal:** Basis erfragen; Ziel: jede zweite Anfrage enthält vollständiges Datum + Gästezahl (weniger Rückfragen).
5. **Heurigenbox-Anfragen pro Monat** über `/ab-hof/` (neu, kein Basiswert) — Entscheidungsgrundlage für einen Online-Shop (Frage 5): ab [PLATZHALTER: 10] Anfragen/Monat Shop prüfen.
6. **Technik:** 404-Rate < 0,5 % der Aufrufe nach 4 Wochen; LCP-Felddaten „gut“ für ≥ 90 % (sofern CrUX-Daten vorhanden).

### §8.3 Berichtsrhythmus

Monatlicher Kurzbericht (eine Markdown-Seite im Repo `report/`): 5 Kennzahlen, 3 Auffälligkeiten, 1 Empfehlung. Den Bericht erstellt Hermes aus GSC-Export und Logauswertung, und er geht an Daniel.

---

## §9 Umsetzungsphasen mit Aufwandsschätzung

Die Schätzung gilt für die Umsetzung durch Hermes (Konzept, Code, Inhalte) inklusive Abstimmung. Nicht enthalten sind externe Kosten (Fotograf, Hosting, Domain) und die Arbeitszeit des Betriebs.

| Phase | Inhalt | Ergebnis | Stunden |
|---|---|---|---|
| **P0 Quick Wins am Bestand** (optional, nur wenn der Relaunch später als in 6 Wochen live geht) | gzip/Brotli einschalten, `localhost`-Pfad und Feed-Leaks korrigieren, `tel:`-Links, Öffnungszeiten-Satz korrigieren („achtmal“), 10 größte Bilder komprimieren, 12 Meta-Descriptions | Patch-Liste für die Agentur oder direkte Umsetzung mit WP-Zugang (Audit §7 Prio 1) | 6 |
| **P1 Klärung & Inhalte** | Betreiber-Gespräch zu den offenen Fragen (§10), Fakten einsammeln (Preise, Räume, Fackelwanderung, Erreichbarkeit), Texte aus §4 freigeben, Wortliste und Schreibweise „ausg'steckt“ festlegen | freigegebene Content-Matrix, gefüllte YAML-Dateien | 8 |
| **P2 Bildwelt** | Shotliste finalisieren, Fotograf briefen, Sichtung Bestandsfotos, Auswahl + Bildbearbeitung + Export, Alt-Texte | 40–60 freigegebene Bilder in `src/assets/img/` | 8 (+ extern: Shooting [PLATZHALTER: Kosten, ca. 1 Tag + 1 Abendtermin]) |
| **P3 Design** | Tokens als CSS, Logo-Vektor (falls nötig nachzeichnen), Komponenten-Bibliothek als statische HTML-Seite, Startseite + Termine + Reservierung als klickbarer Prototyp Mobile + Desktop, eine Abstimmungsrunde | freigegebener Prototyp | 24 |
| **P4 Frontend-Build** | Astro-Setup, Content-Schemas, alle Komponenten (§6.3), 11 Seiten + Veranstaltungs-Template, Statuslogik mit Tests, .ics-Generator, statische Karte, OG-Bilder | vollständige Site auf Staging | 44 |
| **P5 Formulare** | Endpunkt (Reservierung, Feier, Bestellung, Kontakt), Validierung, Mail-Templates Betrieb/Gast, Spam-Schutz, Fehlerpfade | funktionierende Formulare auf Staging, Testmails beim Betrieb angekommen | 14 |
| **P6 SEO & Recht** | Titles/Descriptions einpflegen, JSON-LD-Generatoren, Sitemap/robots, `redirects.csv` + Serverregeln + Testskript, Impressum/Datenschutz-Entwurf (juristische Prüfung extern) | Redirect-Test grün, Schema validiert | 8 |
| **P7 QA** | axe/Lighthouse in CI, VoiceOver-Test iPhone, Tastatur, Zoom/320 px, Cross-Browser (Safari iOS, Safari macOS, Chrome Android, Firefox), Termin-Grenzfälle, Korrekturlesen, Bugfixing | Abnahmeprotokoll | 14 |
| **P8 Go-Live** | Hosting/Header, DNS bzw. Umzug, Redirect-Prüfung live, Search Console + Bing, Google-Unternehmensprofil, Facebook-Cache, 14 Tage 404-Monitoring | Site live, Monitoring läuft | 6 |
| **P9 Übergabe** | Kurzanleitung „Termine und Tagesmenü ändern“ (eine Seite), Pflege-Workflow festlegen (Frage 12), erster Monatsbericht | Doku im Repo, Betrieb weiß, wie Änderungen ankommen | 4 |
| **Summe** | | | **136** |
| Puffer 15 % (Abstimmungsschleifen, Inhaltslücken) | | | **20** |
| **Gesamt** | | | **≈ 156 h** |

**Optionale Ausbaustufen (nicht in der Summe)**

1. Bestätigungslink für Reservierungen (Betrieb klickt → Gast erhält automatische Bestätigung): +4 h
2. Git-basiertes CMS (Sveltia/Decap) für Termine, Tagesmenü, Speisen: +10 h
3. Englische Kurzfassung `/en/` (eine Seite mit Kerninfos): +6 h
4. Online-Shop mit Zahlung für Heurigenbox/Wein: eigenes Projekt, +40–60 h plus rechtliche Prüfung
5. PDF-Infoblatt „Feiern“ für Firmen: +4 h

**Reihenfolge und Abhängigkeiten:** P1 → P2 und P3 parallel → P4 (kann mit Platzhalterbildern starten) → P5/P6 → P7 → P8 → P9. **Kritischer Pfad:** Antworten auf die Fragen 1–3 (Öffnungslogik, Reservierungsprozess) und Frage 10 (Zugang zu Hosting/Domain/Agentur). Ohne Hosting-Zugang ist P8 blockiert. Ohne Fotos geht die Seite mit dem besten Bestandsmaterial live — technisch möglich, aber unter dem Anspruch der Bildsprache.

**Realistischer Zeitrahmen:** 5–7 Kalenderwochen ab Freigabe, abhängig von der Verfügbarkeit des Betriebs. Ein guter Go-Live-Zeitpunkt ist **vor den Rindfleischwochen am Mittwoch, 6. Jänner 2027**. Damit startet das neue Jahr mit der neuen Seite, und die Engerl-&-Bengerl- und Pfandlwochen-Kommunikation läuft noch über den Bestand (dafür P0 empfohlen).

---

## §10 Offene Fragen an den Auftraggeber (mit Vorauswahl)

Jede Frage hat eine **Empfehlung (Vorauswahl)**. Wenn Daniel bzw. der Betrieb nicht widerspricht, setze ich die Vorauswahl um.

1. **Öffnungslogik:** Ist es richtig, dass der Heurige nur in den 8 Aussteckzeiträumen geöffnet hat — dann aber täglich ohne Ruhetag, Mo–Sa 10:30–23:00, So 10:30–22:30? Gilt die Sonntagszeit auch an Feiertagen (z. B. 1.11.2027, 6.1.2027)? Gibt es Ausnahmen (24.12. liegt außerhalb, aber z. B. geschlossene Gesellschaften)?
   **Vorauswahl:** Ja, so darstellen. Der Satz „bis zu zehn mal im Jahr“ wird durch „achtmal im Jahr“ ersetzt, Feiertage wie Sonntage. Begründung: deckt sich mit beiden Plakaten 2026/2027 und mit `/termine/`.
2. **Reservierungssystem:** Online-Anfrage mit manueller Bestätigung (neues Formular) oder Weiterbetrieb von Redi Restaurant Reservation (Echtzeit/Warteliste)?
   **Vorauswahl:** Eigenes 3-Schritt-Anfrageformular, Redi kündigen. Begründung: Redi arbeitet heute schon als Anfrage („Wir prüfen die Verfügbarkeit“), bringt Datenverarbeitung bei einem Drittanbieter und schweres JavaScript. Echtzeit-Verfügbarkeit lohnt sich nur bei konsequent gepflegter Tischbelegung.
3. **Bestätigungsprozess:** Wer bestätigt Reservierungen, über welchen Kanal und wie schnell? Bis wann sind Reservierungen für den selben Tag möglich, und wann ist sonntags der letzte Slot?
   **Vorauswahl:** Bestätigung per SMS oder Anruf durch den Betrieb am selben oder nächsten Tag. Online bis 2 Stunden vor Sperrstunde, letzter Slot Mo–Sa 21:00 und So 20:30. Begründung: Bestand bietet 10:30–21:00 an, sonntags ist eine halbe Stunde früher Sperrstunde.
4. **Heurigenbox und heurigenbox.at:** Gehört die Domain dem Betrieb? Sollen Inhalte, Sorten, Fotos und Preise auf `/ab-hof/` übernommen werden?
   **Vorauswahl:** Ja, übernehmen und `heurigenbox.at` per 301 auf `/ab-hof/#heurigenbox` leiten. Begründung: Sitzung bleibt erhalten, Suchsignale werden gebündelt, eine Seite weniger zu pflegen.
5. **Online-Shop (WooCommerce):** Soll es einen echten Shop mit Zahlung geben?
   **Vorauswahl:** Nein in Phase 1, Bestellanfrage-Formular statt Shop. Entscheidung nach 6 Monaten anhand der Anfragezahlen (§8.2). Begründung: Shop bedeutet AGB, Widerruf, Zahlungsanbieter, Altersprüfung, Versand — hoher Aufwand bei unbekannter Nachfrage.
6. **Preise online:** Sollen Speisekarte, Weinpreise (Glas/Flasche/Ab Hof) und Heurigenbox-Preise veröffentlicht werden?
   **Vorauswahl:** Ja, für Ab-Hof-Weine und Heurigenboxen. Für die Speisekarte: ja, wenn der Betrieb eine gepflegte Preisliste liefern kann, sonst ohne Preise wie bisher. Begründung: Firmen und Gastgeber entscheiden nach Preis, veraltete Preise sind aber schlimmer als keine.
7. **Weinliste und Prämierungen:** Pinot Noir (auf der KOSTBAR) und Riesling 2025 (prämiert) stehen nicht auf der Weinliste. Sind sie im Verkauf? Jahrgänge der übrigen Weine? Sind die aus der Grafik transkribierten Prämierungen vollständig und korrekt?
   **Vorauswahl:** Beide in die Weinliste aufnehmen. Prämierungen nur nach Bestätigung veröffentlichen, Jahrgänge aus der aktuellen Preisliste übernehmen.
8. **Fotoshooting:** Wird ein professionelles Shooting beauftragt (Budget, Fotograf)?
   **Vorauswahl:** Ja, in zwei Terminen: (a) ein Halbtag in den Rindfleischwochen im Jänner 2027 für Innenräume, Stüberl, Speisen, Keller und Familie; (b) ein Tag in den Schwammerlwochen im Juni 2027 für Gastgarten, Spielplatz und Weingarten, mit Abendtermin Fackelwanderung. Bis (b) laufen Garten- und Fackelmotive mit den besten Bestandsfotos. Begründung: Die Bildsprache trägt das Konzept, Bestandsfotos sind 8–10 Jahre alt.
9. **Familienfoto:** Ist das Team-Foto von 2019 noch aktuell (Personen, Rollen)?
   **Vorauswahl:** Neu fotografieren beim Shooting, bis dahin das 2019er Foto mit aktueller Namenszeile verwenden.
10. **Zugänge und Agentur:** Wer hat Zugang zu Domain (Registrar), DNS, Hosting, WordPress, Search Console und Google-Unternehmensprofil? Wie ist das Verhältnis zu jeromedia.eu?
    **Vorauswahl:** Betrieb holt sich die Zugänge zur Domain und zum Hosting selbst (Inhaber Christian Neumayer). Die Agentur wird gebeten, ein Backup zu übergeben. Hosting bleibt beim bisherigen Anbieter, wenn dort Brotli und eigene Header möglich sind, sonst Umzug zu einem EU-Webhoster.
11. **E-Mail-Adresse öffentlich:** Darf `christian@weinbauneumayer.at` auf Kontakt- und Feierseite sichtbar stehen (bisher nur im Impressum als `christian[at]…` und auf Plakaten)?
    **Vorauswahl:** Ja, als normaler `mailto:`-Link. Spam wird über den Mailfilter abgefangen, nicht über Verschleierung (Verschleierung ist für Screenreader und Copy/Paste hinderlich). Optional zusätzlich eine eigene Adresse für Feieranfragen [PLATZHALTER].
12. **Pflege von Terminen und Tagesmenü:** Wer pflegt künftig, und wie?
    **Vorauswahl:** Phase 1: Betrieb schickt das Tagesmenü (Foto oder Text) bzw. neue Termine per E-Mail oder WhatsApp an Hermes, die Änderung ist binnen 24 h live. Phase 2 bei Bedarf: Sveltia-CMS-Formular für Selbstpflege. Begründung: Tagesmenüs ändern sich nur 8 × im Jahr für je 3 Wochen, ein CMS rechnet sich erst bei häufiger Selbstpflege.
13. **Newsletter:** Die bestehende Newsletter-Checkbox (MC4WP) — gibt es einen aktiven Newsletter und Abonnenten?
    **Vorauswahl:** In Phase 1 entfernen. Wird ein Newsletter gewünscht, kommt er als eigenes Formular mit Double-Opt-in bei einem EU-Anbieter dazu. Bestehende Abonnenten nur bei nachweisbarer Einwilligung übernehmen.
14. **Sprache:** Nur Deutsch, oder zusätzlich Englisch?
    **Vorauswahl:** Nur Deutsch in Phase 1. Eine englische Kurzseite folgt optional, wenn die Logs relevanten englischsprachigen Traffic zeigen.
15. **Anrede:** „Sie“ oder „ihr“?
    **Vorauswahl:** Durchgehend „Sie“ (§1.3). Begründung: Firmen- und Hochzeitskundschaft. Die Herzlichkeit kommt über Wortwahl und die Familie als Absender.
16. **Barrierefreiheit des Lokals:** Gibt es einen stufenlosen Zugang, ein barrierefreies WC, und welche Ebene ist ohne Stufen erreichbar?
    **Vorauswahl:** Ehrlich angeben, was ist (auch „nicht barrierefrei“). Diese Information ist für Gäste mit Kinderwagen oder Rollstuhl entscheidend und wird oft nachgefragt.
17. **Anonymer Ereigniszähler (§8.1):** einschalten?
    **Vorauswahl:** Ja, nach kurzer rechtlicher Prüfung. Er zählt nur Anrufe/Routen/Teilen, ohne Cookie und ohne IP-Speicherung.
18. **„Seit 40 Jahren“:** In welchem Jahr wurde der Betrieb gegründet?
    **Vorauswahl:** Formulierung „seit {Gründungsjahr}“ verwenden und die Zahl der Jahre automatisch berechnen. So veraltet der Text nicht jedes Jahr.
19. **Schreibweise:** „Ausgsteckt'is“ (Menü Bestand), „Ausgsteckt is`“ (Plakat) oder „Ausg'steckt is“?
    **Vorauswahl:** „Ausg'steckt is“ (Apostroph für das ausgelassene „e“, wie in „g'steckt“) und im Fließtext „ausg'steckt“. Begründung: Es ist die lesbarste Variante. Der Betrieb entscheidet, die Schreibweise wird dann überall einheitlich gesetzt.
20. **Räume und Kapazitäten:** Wie viele Plätze haben Stüberl, die beiden Ebenen und der Gastgarten? Ab wie vielen Personen gilt eine Gruppe als „Feier“?
    **Vorauswahl:** Ab 11 Personen Feieranfrage statt Tischreservierung (entspricht der Bestandsregel „>10“). Platzzahlen pro Raum veröffentlichen.
21. **Fackelwanderung:** Nur als Zusatz zu einer Feier buchbar oder auch einzeln (z. B. für Gruppen ohne Essen)? Preis, Mindestgruppe, Jahreszeit, Ausweichprogramm bei Regen, Dauer?
    **Vorauswahl:** Als Zusatz zu einer Feier, Preis auf Anfrage. Die Seite nennt Ablauf und 20 Minuten Fußweg (belegt) und lässt den Rest offen, bis Fakten vorliegen.
22. **KOSTBAR in ROT, Spritzer TO GO, Geschenkebox:** Gelten der Kostpreis € 6,90 (Grafik ohne Datum), Geschenkebox € 65 (Grafik 01/2025) noch? Was kostet der Spritzer TO GO, und wo gibt es ihn?
    **Vorauswahl:** Preise nur nach Bestätigung zeigen. Bis dahin bleibt die Preiszeile leer, die Komponente unterstützt das.
23. **Logo als Vektor:** Gibt es eine SVG/AI/PDF-Datei des WN-Stempels?
    **Vorauswahl:** Bei Agentur bzw. Etikettendruckerei anfragen. Falls nichts kommt: nachzeichnen (2 h in P3 enthalten).
24. **Credit-Zeile im Footer:** Soll ein Hinweis auf die Umsetzung erscheinen?
    **Vorauswahl:** Nein. Der Footer bleibt beim Betrieb.
25. **Kanalverteilung:** Wie viele Reservierungen kommen heute telefonisch, online (Redi) und persönlich? Wie viele Feieranfragen pro Jahr?
    **Vorauswahl:** Grobe Schätzung des Betriebs genügt. Sie wird die Basis für §8.2. Bis dahin gilt die Annahme „Telefon > Online“.
26. **Google-Unternehmensprofil:** Ist es beansprucht, wer pflegt es, stehen die Aussteckzeiträume als Sonderöffnungszeiten drin?
    **Vorauswahl:** Beanspruchen bzw. Zugang klären. Bei jedem neuen Jahresplan die Sonderöffnungszeiten eintragen (gemeinsam mit `termine.yaml`, 15 min pro Jahr). Begründung: Für „Heuriger Perchtoldsdorf“ ist das Maps-Profil mindestens so wichtig wie die Website.
27. **Öffi-, Park- und Radinfos:** Welche Haltestelle, wie viele Parkplätze, Radabstellplätze?
    **Vorauswahl:** Vom Betrieb einholen und auf `/besuch/#anfahrt` veröffentlichen. Bis dahin steht dort nur die Adresse mit Routenlinks (keine erfundenen Linien).
28. **Zahlungsmittel, Hunde, Allergene:** Kartenzahlung? Hunde im Gastgarten/Lokal? Allergenliste vorhanden?
    **Vorauswahl:** In die FAQ auf `/besuch/` aufnehmen, sobald beantwortet. Allergene: Hinweis „beim Personal erfragen“ (gesetzlich zulässige mündliche Auskunft) bis eine Liste vorliegt.
29. **Gastgarten-Saison:** Von wann bis wann ist der Gastgarten offen?
    **Vorauswahl:** April bis September in der Reservierung als Option anbieten (Annahme, bestätigen).
30. **Quick Wins am Bestand (P0):** Sollen die Sofortmaßnahmen vor dem Relaunch umgesetzt werden?
    **Vorauswahl:** Ja, wenn der Relaunch nicht vor dem 6. Jänner 2027 live ist. Mindestens `tel:`-Links, Kompression und der korrigierte Öffnungszeiten-Satz — das sind ca. 2 h mit großer Wirkung für die Pfandlwochen und Engerl & Bengerl.

---

## Kurzfassung für den Chat (max. 400 Wörter)

**REDESIGN-DRAFT weinbauneumayer.at liegt unter `docs/design-draft/REDESIGN-DRAFT.md`.**

Kern: Relaunch statt Facelift. Astro statisch, kein jQuery, CSS < 50 KB, Startseite < 900 KB, LCP < 1,5 s auf 4G, kein Tracking, kein Cookie-Banner. Alle 10 Top-Befunde des Audits sind einer Maßnahme zugeordnet (§0.1).

**Wichtigste Erkenntnis aus dem Mirror:** Die Aussteckzeiten standen nur als Bild online. Transkribiert: 2026 und 2027 jeweils **achtmal ausg'steckt** (2026: 177 Tage, immer Sa–So). Damit ist der Öffnungszeiten-Widerspruch aus dem Audit lösbar: Mo–Sa 10:30–23:00 und So 10:30–22:30 gelten nur in diesen Zeiträumen. „Bis zu zehn Mal“ ist veraltet.

**Was neu ist:**
1. Navigation 5 statt 10: Termine · Speisen & Wein · Ab Hof · Feiern · Besuch & Kontakt, dazu Button „Tisch reservieren“ und mobile Aktionsleiste (Anrufen · Reservieren · Route).
2. Statusleiste auf jeder Seite („Heute ausg'steckt · offen bis 23:00“ bzw. „Nächstes Mal ab …“), automatisch aus `termine.yaml`.
3. Die Besonderheiten werden sichtbar: eigene Seite Fackelwanderung, neue Rubrik „Ab Hof“ (24-h-Automat, Spritzer TO GO, Geschenkebox, Heurigenbox), KOSTBAR in ROT und Prämierungen auf `/weine/`, eigene teilbare Seiten pro Veranstaltung.
4. Reservierung in 3 Schritten, nur Ausstecktage wählbar, ab 11 Personen direkt zur Feieranfrage. `tel:`-Links überall.
5. Marke: WN-Stempel bleibt, Markenrot #990000 als Signalfarbe auf warmem Papier #FAF6EF, Text #2A211C (14,6:1 statt 3,54:1). Alegreya (Display) + Source Sans 3 (Text), selbst gehostet. Echte Fotos, eine Shotliste mit 20 Motiven, keine Plakatgrafiken mehr als Inhalt.
6. SEO: Titles und Descriptions für alle Seiten ausformuliert, JSON-LD `Restaurant`+`Winery` mit saisonalen Öffnungszeiten, `FoodEvent`, `Menu`, vollständige 301/410-Tabelle inkl. aller `/?p=`-IDs.
7. Messung ohne Tracker: Search Console, Unternehmensprofil, anonymisierte Serverlogs, Formularzähler, optional ein cookiefreier Anrufzähler.

**Aufwand:** 136 h + 15 % Puffer ≈ **156 h**, 5–7 Wochen. Empfohlener Go-Live vor den Rindfleischwochen am 6. Jänner 2027. Bis dahin 2 h Quick Wins am Bestand (tel-Links, Kompression, Öffnungszeiten-Satz).

**30 offene Fragen mit Vorauswahl (§10).** Kritisch sind: (1) Öffnungslogik bestätigen, (2/3) eigenes Anfrageformular statt Redi plus Bestätigungsprozess, (10) Zugänge zu Domain/Hosting/Agentur, (8) Fotoshooting-Budget. Fakten aus Plakatgrafiken (Prämierungen, Kostbar € 6,90, Geschenkebox € 65) sind markiert und müssen vor Veröffentlichung bestätigt werden. Alle fehlenden Fakten stehen als [PLATZHALTER].
