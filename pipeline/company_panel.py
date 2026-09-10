import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
ALIASES = {
    "intel corporation": "intel",
    "bosch global software technologies": "bosch group",
    "jpmorgan chase co": "jpmorgan chase",
    "amazon web services aws": "amazon",
    "oracle india": "oracle",
    "tech mahindra formerly mahindra satyam": "tech mahindra",
    "wipro digital": "wipro",
}


def company_key(name):
    key = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
    key = re.sub(r"\b(private|pvt|limited|ltd|incorporated|inc|llc)\b", "", key)
    key = re.sub(r"\s+", " ", key).strip()
    return ALIASES.get(key, key)


def map_panel(historical_companies, sources):
    source_by_key = {company_key(source["company"]): source for source in sources}
    connected = []
    unresolved = []
    for historical_company in sorted(historical_companies):
        source = source_by_key.get(company_key(historical_company))
        if source:
            connected.append({
                "historical_company": historical_company,
                "current_company": source["company"],
                "provider": source.get("provider", ""),
            })
        else:
            unresolved.append(historical_company)
    return {
        "historical_company_count": len(historical_companies),
        "connected_count": len(connected),
        "unresolved_count": len(unresolved),
        "connected": connected,
        "unresolved": unresolved,
    }


def main():
    panel = json.loads((ROOT / "data/historical-india-company-panel.json").read_text())
    sources = json.loads((ROOT / "data/sources.json").read_text())
    result = map_panel(panel["companies"], sources)
    (ROOT / "data/company-panel-coverage.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: result[key] for key in ("historical_company_count", "connected_count", "unresolved_count")}))


if __name__ == "__main__":
    main()
