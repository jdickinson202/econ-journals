# Economics journals

A short list of 67 leading economics journals, by field, with the IDs you need to look up their articles: OpenAlex, ISSN and RePEc.

It has a top 10 overall and three journals for each JEL field. It's a curated selection, not a complete list or an official ranking.

The list is kept here so the [Economics Discord](http://discord.gg/economics)'s bot, EconGoat and anyone else can read the same one.

## Use it

It's one file, [`journals.csv`](journals.csv), and this address always has the current version:

```
https://raw.githubusercontent.com/jdickinson202/econ-journals/main/journals.csv
```

In Python:

```python
import pandas as pd

journals = pd.read_csv("https://raw.githubusercontent.com/jdickinson202/econ-journals/main/journals.csv")
```

In R:

```r
journals <- read.csv("https://raw.githubusercontent.com/jdickinson202/econ-journals/main/journals.csv")
```

In Stata:

```stata
import delimited "https://raw.githubusercontent.com/jdickinson202/econ-journals/main/journals.csv", clear
```

If a program reads it every day, keep your last good copy to fall back on, in case GitHub is down.

### Finding articles

To get recent articles from [OpenAlex](https://openalex.org), put the IDs in a filter, separated by `|`:

```
https://api.openalex.org/works?filter=primary_location.source.id:S23254222|S203860005,type:article,from_publication_date:2026-01-01&sort=publication_date:desc
```

To see a journal on [IDEAS](https://ideas.repec.org), replace the colon in its RePEc handle with a slash: `aea:aecrev` is at `https://ideas.repec.org/s/aea/aecrev.html`. Article pages there often have JEL codes, which OpenAlex doesn't have.

## Columns

| Column | What it is |
|---|---|
| `openalex_id` | The journal's ID in OpenAlex, such as `S23254222`. |
| `journal` | Its name. |
| `jel` | The JEL field it's listed under, by letter, or `TOP` for the top 10 overall. |
| `field` | That field's name, shortened. |
| `rank` | Its position in that field, starting at 1. |
| `issn` | Its linking ISSN (ISSN-L), from OpenAlex. |
| `repec` | Its RePEc handle, such as `aea:aecrev`. |

Each journal appears once. `jel` says where a journal is listed, not what each of its articles is about: use an article's own JEL codes for that, where it has them.

RePEc's coverage of two journals has stopped, so it won't have their new articles: *History of Political Economy* (its newest there is from 2021) and *National Tax Journal* (2020).

## Change it

To add or correct a journal, open an issue or a pull request.

`check_journals.py` checks the file's format, and asks OpenAlex whether each ID still points at the journal with that ISSN. GitHub runs it on every change and every Monday. To run it yourself:

```
python check_journals.py
```

## Licence

[CC0 1.0](LICENSE): use it for anything, with no need to ask or give credit.
