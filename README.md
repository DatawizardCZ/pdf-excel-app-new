# Darvis - PDF Objednávky

Webová aplikace pro převod PDF objednávek (Købsrekvisition) do Excelu.
Frontend je statický HTML/JS, backend jsou dvě Python serverless funkce na Vercelu
(`/api/process` pro PDF→XLSX, `/api/auth` pro login), které znovupoužívají parser
z [`pdf_processor.py`](pdf_processor.py).

## Architektura

```
┌──────────────┐  POST /api/process  ┌─────────────────────┐
│ index.html   │ ─────────────────▶  │ api/process.py      │
│ (drag&drop,  │  multipart/form-data│ Flask + pdfplumber  │
│  fetch, ZIP) │ ◀──────────────── │ → openpyxl XLSX     │
│              │     XLSX bytes      └─────────────────────┘
│              │  GET/POST /api/auth ┌─────────────────────┐
│              │ ─────────────────▶  │ api/auth.py         │
│              │  Bearer / JSON      │ hmac.compare_digest │
│              │ ◀──────────────── │ → 200/401           │
└──────────────┘                     └─────────────────────┘
        ▲
        │  Authorization: Bearer <APP_PASSWORD>
        │  (sdílené heslo z env variable,
        │   sessionStorage v prohlížeči)
```

**Pozor na Vercel routing**: Vercel přiřazuje URL podle souborů v `/api`
(`/api/process` ↔ `api/process.py`, `/api/auth` ↔ `api/auth.py`). Více Flask rout
v jednom souboru by lokálně fungovalo, ale produkce by je nikdy nedostala — proto
je auth ve vlastním souboru.

## Struktura repa

```
.
├── api/
│   ├── process.py        # Vercel funkce: POST /api/process (PDF → XLSX, auth-gated)
│   └── auth.py           # Vercel funkce: GET/POST /api/auth (login)
├── index.html            # Frontend (vanilla HTML+CSS+JS, single file)
├── pdf_processor.py      # PDF parser (sdílený s původní Streamlit verzí)
├── dev_server.py         # Lokální dev server (sjednocuje obě funkce + statiku)
├── requirements.txt      # Python dependencies pro serverless
├── vercel.json           # Vercel konfigurace (memory, maxDuration)
├── .env.example          # Vzor environment variables
├── .devcontainer/        # Devcontainer pro lokální vývoj
└── test_files/           # Vzorová PDF na ruční testy
```

## Formát exportu (XLSX)

Z každého vstupního PDF (`Købsrekvisition <číslo> <zkratka>.pdf`) vznikne jeden
Excel soubor pojmenovaný `<původní_název>_processed.xlsx`. Obsahuje **jeden list**
nazvaný `Objednávka` s následujícími sloupci:

| # | Sloupec            | Popis                                                              |
|---|--------------------|--------------------------------------------------------------------|
| A | `Vendor Item No.`  | Interní katalogové číslo dodavatele (např. `80203`, `15910S`).      |
| B | `Barcode No.`      | EAN/čárový kód, typicky 13 cifer.                                   |
| C | `Description`      | Hlavní popis položky z prvního textového řádku.                     |
| D | `Variant`          | Varianta produktu (nejčastěji prázdné).                             |
| E | `Price` (Cost Price) | Jednotková cena s desetinnou čárkou (např. `1,58`).               |
| F | `Quantity`         | Objednané množství (kolik balení/kusů).                             |
| G | `Kolli Str.`       | Velikost balení (počet kusů v jednom kolli).                        |
| H | `Pieces`           | Celkový počet kusů (`Quantity × Kolli Str.`).                       |
| I | `Specification`    | Druhý popisný řádek z PDF — typicky latinský/biologický název druhu.|

- **Řádek 1** = hlavičky sloupců (zachovány v původním pojmenování z PDF).
- **Řádek 2 a dál** = jedna položka objednávky na řádek.
- Žádný index sloupec, žádné sloučené buňky, žádné formátování — čistá data
  připravená pro další zpracování (filtry, kontingenční tabulky, import jinam).

**Příklad výstupu (řádek 2):**

```
Vendor Item No. | Barcode No.   | Description                | Variant | Price | Quantity | Kolli Str. | Pieces | Specification
80203           | 2521904852390 | Rotte small                |         | 1,58  | 2        | 1          | 2      |
80245           | 2522262405839 | Ildskink M - L             |         | 49,72 | 1        | 1          | 1      | Riopa fernandi
09243           | 2522003664181 | Orange Dværg Hummer        |         | 2,99  | 5        | 1          | 5      | Cambarellus Patzcuarensis Orange
```

Hlavičky se automaticky přizpůsobí jazyku původního PDF (anglické/dánské):
- anglické: `Vendor Item No.`, `Barcode No.`, `Description`, `Cost Price`, `Quantity`, `Kolli Str.`, `Pieces`
- dánské: `Nr.`, `Stregkode`, `Beskrivelse`, `Pris`, `Antal`, `Styk`

## Lokální vývoj

Potřebuješ Python 3.9+.

```bash
pip install -r requirements.txt
APP_PASSWORD=test123 python dev_server.py
```

`dev_server.py` spustí jediný Flask server na `http://localhost:3000`, který:
- servíruje `index.html` na `/`,
- znovuregistruje routy z `api/process.py` (POST `/api/process`),
- znovuregistruje routy z `api/auth.py` (GET/POST `/api/auth`),
- aplikuje stejnou auth gate jako produkce.

Pokud `APP_PASSWORD` nezadáš, app běží v "open" režimu (bez hesla).

Otestuj proti vzorkům (s heslem):

```bash
curl -X POST -H "Authorization: Bearer test123" \
  -F "file=@test_files/Købsrekvisition K0145913 TIL.pdf" \
  http://localhost:3000/api/process -o test.xlsx
```

Případně lze použít `vercel dev` (vyžaduje login do Vercel CLI a `vercel link`),
ale `dev_server.py` je rychlejší a funguje offline.

## Deploy

### Production deploy

Po pushnutí na `main` se spustí auto-deploy (pokud máš v Vercel dashboardu napojený GitHub repo).

Manuálně:

```bash
vercel --prod
```

### Auth (vlastní login)

Aplikace má vlastní jednoduchý login se sdíleným heslem (jedno heslo pro všechny
uživatele). Heslo se nastavuje v environment variable `APP_PASSWORD`.

Bezpečnostní vlastnosti:
- Heslo se na server posílá v `Authorization: Bearer <heslo>` hlavičce přes HTTPS.
- Server používá `hmac.compare_digest` pro porovnání (constant-time, odolné proti timing útokům).
- Frontend si heslo pamatuje v `sessionStorage` — vyprší při zavření tabu.
- Backend ověřuje heslo na **každém** API requestu (frontend pouze schová UI; bez
  hesla nelze API použít ani přes `curl`).
- Pokud je `APP_PASSWORD` prázdné, aplikace běží v "open" režimu bez hesla
  (jen pro lokální vývoj).

Nastavení v produkci:
1. Otevři projekt v Vercel dashboardu
2. Settings → Environment Variables
3. Přidej `APP_PASSWORD` = silné heslo (doporučeno 16+ znaků), zaškrtni všechny
   environments (Production, Preview, Development)
4. Save → Redeploy (jednou, aby si nový env variable vzal)
5. Heslo měníš v dashboardu kdykoli (po změně je třeba redeploy)

## Konfigurace

### `vercel.json`

- `memory: 1024` — 1 GB paměti pro funkci (pdf parsování zvládá s rezervou)
- `maxDuration: 60` — max 60 s na request (vyžaduje Vercel Pro)

### Environment variables

Nastavují se v Vercel dashboardu (Project Settings → Environment Variables).
Lokálně je předáš inline (`APP_PASSWORD=... python dev_server.py`) nebo přes
`.env.local` (vytvoř kopii z `.env.example` a načti přes `set -a; source .env.local; set +a`).

| Proměnná | Default | Význam |
|---|---|---|
| `APP_PASSWORD` | _prázdné_ | Sdílené heslo pro vstup. Prázdné = open režim (bez hesla, jen pro lokální vývoj). V produkci VŽDY nastavte silné heslo. |
| `DEBUG_MODE` | `false` | Pokud `true`, API vrací v chybové odpovědi i Python traceback. |

## Limity

- **Upload max ~4.5 MB** — Vercel limit na request body. Pro typické objednávkové PDF výrazně víc, než je potřeba.
- **Timeout 60 s** — když je PDF hodně velké/složité, může vypršet čas. V praxi se objednávky parsují pod 5 s.
- **Function size limit 250 MB** (rozbalená velikost). pandas + pdfplumber + openpyxl + Flask se vejde s rezervou.

## Logy

Vercel Functions Logs v dashboardu (Deployments → poslední → Function Logs).
Každé volání `/api/process` tam má záznam včetně délky trvání a paměti.

## Update parsing logiky

Editovat `pdf_processor.py` → push na `main` → auto-deploy. Frontend ani API
wrapper se kvůli změně parseru nemění.

## Změny oproti původní Streamlit verzi

- ❌ Streamlit + `app_secure.py` (UI vrstva, login, session management) → nahrazeno staticem + jednoduchým loginem v Pythonu/JS
- ❌ `config.py` (rate limit, file size limit, logging do souboru) → odstraněno (rate limit řeší Vercel infrastruktura, file size limit Vercel platforma, logy Vercel Functions Logs)
- ❌ `tabula-py` → nepotřeboval se, parser používá jen pdfplumber
- ❌ `python-dotenv` → Vercel injektuje env variables přímo
- ✅ `pdf_processor.py` (547 řádků parsingu) zachováno **1:1**, bonusový bugfix (viz níže)
- ✅ Auth: vlastní login se sdíleným heslem (`APP_PASSWORD` env), HTTPS přes Vercel, constant-time porovnání
- ✅ Hromadné stažení Excelů jako ZIP (nově)

### Regresní ověření migrace

Při migraci byl XLSX výstup nového stacku porovnán proti původní Streamlit verzi
nad všemi 8 vzorovými PDF v `test_files/`. Iniciální porovnání (před bugfixem
níže) ukázalo **identický výstup ve všech 1 035 buňkách napříč 8 soubory**.

Důvod: [`api/process.py`](api/process.py) používá pro zápis Excelu naprosto
stejné volání jako původní Streamlit (`pd.ExcelWriter` + `engine='openpyxl'`
+ `sheet_name='Objednávka'`), a parser [`pdf_processor.py`](pdf_processor.py)
zůstal beze změn (kromě bugfixu níže).

### Bugfix při migraci: phantom adresní řádek

Během testování se ukázalo, že u PDF s druhou stranou (např.
[`test_files/Købsrekvisition K0145958 AAL.pdf`](test_files/Købsrekvisition%20K0145958%20AAL.pdf))
parser zařadil do tabulky i část adresy příjemce — řádek
`27204 Kladno 9200 Aalborg SV` se ocitl v Excelu jako falešná položka
s Vendor Item No. `27204` a textem adresy v poli `Description`.

Tenhle bug existoval i v původní Streamlit verzi (parser je sdílený). V rámci
migrace byl opraven přidáním validačního filtru v
[`pdf_processor.py`](pdf_processor.py): řádek je zařazen do výstupu pouze
pokud má buď platný čárový kód (≥ 10 cifer), nebo cenu s desetinnou částí.
Adresní řádky obojí postrádají, takže propadnou filtrem.
