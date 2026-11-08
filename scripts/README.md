# Scripts

Scripts om lijsten te printen van verschillende verzamelingen, zoals stripboekenreeksen. Ze printen een tabel (TSV) naar stdout.

## Draaien

Elk script heeft de dependencies als inline metadata ([PEP 723](https://peps.python.org/pep-0723/)) in de kop staan en heeft Python >= 3.14 nodig. Gebruik [uv](https://docs.astral.sh/uv/); die maakt automatisch een omgeving aan en installeert de dependencies:

```bash
uv run asterix.py
```

Er is geen `requirements.txt` of virtualenv nodig.

Sla de uitvoer op met een redirect:

```bash
uv run asterix.py > output/asterix.tsv
```

## Scripts

Zonder argumenten (URL staat in het script):

| Script | Verzameling |
| --- | --- |
| `asterix.py` | Asterix |
| `bessy.py` | Bessy |
| `dirkjan.py` | Dirk Jan |
| `douwedabbert.py` | Douwe Dabbert |
| `kuifje.py` | Kuifje |
| `nicholas_sparks.py` | Nicholas Sparks |
| `robert_en_bertrand.py` | Robert en Bertrand |
| `suskeenwiske.py` | Suske en Wiske |
| `wasgij.py` | Wasgij puzzels |

Met argument:

```bash
uv run stripinfo.py https://stripinfo.be/reeks/strips/<reeks>   # stripinfo.be reeks
uv run lastdodo.py <url>                                        # lastdodo.nl pagina
uv run scrape_wikipedia_tables.py <wikipedia-url>               # tabellen van een Wikipedia-pagina
uv run lego.py [theme_id]                                       # standaard 246 (Harry Potter)
```

`lego.py` leest `sets.csv`, te downloaden van [rebrickable.com](https://rebrickable.com/downloads/), en filtert op thema.

## Item toevoegen

```bash
./add_item.bash <collection_id> '<naam>'
```

Voegt een item toe aan `../web/app.sqlite` (vereist `sqlite3`).
