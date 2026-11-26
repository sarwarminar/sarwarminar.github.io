import json
from datetime import datetime, timezone
from pathlib import Path
from scholarly import scholarly

SCHOLAR_ID = "fnjyE6wAAAAJ"
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["basics", "indices", "counts"])
required = ["citedby", "citedby5y", "hindex", "hindex5y", "i10index", "i10index5y", "cites_per_year"]
missing = [name for name in required if author.get(name) is None]
if missing:
    raise RuntimeError("Google Scholar returned incomplete data: " + ", ".join(missing))

now = datetime.now(timezone.utc)
# Scholar's recent window is labelled 'Since YEAR' (as on Scholar itself).
since = now.year - 5
annual = {str(y): int(author["cites_per_year"].get(y, 0)) for y in range(min(2019, *(author["cites_per_year"] or {2019:0})), now.year + 1)}
data = {
    "source": "https://scholar.google.com/citations?user=" + SCHOLAR_ID,
    "updated_at": now.isoformat(),
    "since_year": since,
    "citations": {"all": int(author["citedby"]), "recent": int(author["citedby5y"])},
    "h_index": {"all": int(author["hindex"]), "recent": int(author["hindex5y"])},
    "i10_index": {"all": int(author["i10index"]), "recent": int(author["i10index5y"])},
    "citations_per_year": annual,
}
Path("scholar-data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print("Successfully fetched Google Scholar data:", data["citations"])
