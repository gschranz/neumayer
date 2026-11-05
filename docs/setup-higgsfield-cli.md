# Higgsfield CLI auf einem Headless-Host anmelden

**Problem:** `higgsfield auth login` startet einen OAuth-2.0-PKCE-Flow mit `redirect_uri=http://localhost:8765/callback`. Der Browser, in dem man sich anmeldet, ist aber ein **anderes Gerät** als der Host, auf dem die CLI läuft. Nach dem Login landet der Browser auf `localhost:8765` des *eigenen* Rechners → Verbindungsfehler → der Login schlägt scheinbar fehl.

**Lösung:** Der Authorization-Code steckt in der URL, auf der der Browser strandet. Diese URL reicht man an den lokalen Listener weiter — der PKCE-Verifier liegt beim CLI-Prozess, also tauscht er den Code selbst gegen das Token.

## Ablauf

```bash
# 1. Login im Hintergrund starten (muss laufen bleiben!)
export HOME=/data/.hermes/home
higgsfield auth login
```

```bash
# 2. Authorize-URL aus der erzeugten sign-in.html ziehen
D=$(ls -dt /data/.hermes/home/higgsfield-auth-* | head -1)
python3 - "$D" <<'EOF'
import sys, re, os
h = open(os.path.join(sys.argv[1], "sign-in.html")).read()
m = re.search(r'https://clerk\.higgsfield\.ai/oauth/authorize\?[^"]+', h)
print(m.group(0).replace("&amp;", "&"))
EOF
```

3. Diese URL an die Person schicken, die sich anmelden soll. Sie öffnet sie im eigenen Browser, meldet sich an und landet auf einer Fehlerseite („localhost:8765 nicht erreichbar"). **Das ist erwartet.**

4. Sie kopiert die vollständige URL aus der Adresszeile (`http://localhost:8765/callback?code=…&state=…`) und schickt sie zurück.

```bash
# 5. Callback lokal an den wartenden Listener reichen
curl -s "http://localhost:8765/callback?code=<CODE>&iss=https%3A%2F%2Fclerk.higgsfield.ai&state=<STATE>" | head -5
# -> HTML mit "Device authorized - Higgsfield CLI"
```

```bash
# 6. Verifizieren
higgsfield auth token          # muss oat_… liefern
higgsfield workspace list      # ID + Plan + Credits
higgsfield workspace set <ID>  # ohne Auswahl: "Error: No workspace selected."
higgsfield account status      # E-Mail, Plan, Credits
```

## Fallstricke

- **Code ist einmalig und kurzlebig** (~1–2 Min). Abgelaufen → Login neu starten, neuen Link ziehen. Nicht den alten Link wiederverwenden.
- **`state` muss exakt passen.** Immer die komplette Callback-URL verwenden, nichts wegkürzen.
- **Ohne Workspace geht nichts:** `higgsfield model list` bricht mit `Error: No workspace selected` ab. Erst `workspace set`.
- **Kein API-Key-Env-Pfad.** Die CLI kennt nur OAuth (`auth login | logout | token`); es gibt keine `HIGGSFIELD_*`-Variable und kein `--token`-Flag. Wer headless ohne Browser arbeiten will, braucht die REST-API (`open.higgsfield.ai`, `Authorization: Key <id>:<secret>`) — separates Produkt, separates USD-Guthaben.
- **Abrechnung:** CLI/MCP verbrauchen **Plan-Credits**; „Unlimited"-Modelle gelten nur auf der Website, nicht über CLI. Kein Ausgaben-Limit eingebaut.

## Kosten-Orientierung (Stand 2026-11)

| Modell | Credits pro Bild |
|---|---|
| `nano_banana_2_1` | 1,5 |
| `nano_banana_pro` (2k, 16:9) | 2 |
| `gpt_image_2_5` (high, 2k) | 2,75 |

Kosten vorher abfragen: `higgsfield generate cost <model> --prompt "…"`.
