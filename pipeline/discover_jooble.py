import argparse
import datetime as dt
import json
import os
import pathlib
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]


def normalize_job(raw, keywords, location):
    provider_id = str(raw.get("id") or "").strip()
    return {
        "discovery_id": f"jooble:{provider_id}",
        "provider_job_id": provider_id,
        "title": str(raw.get("title") or "").strip(),
        "company": str(raw.get("company") or "").strip(),
        "location": str(raw.get("location") or "").strip(),
        "source_provider": "jooble",
        "source_board": str(raw.get("source") or "").strip(),
        "source_url": str(raw.get("link") or "").strip(),
        "source_updated_at": str(raw.get("updated") or "").strip(),
        "employment_type": str(raw.get("type") or "").strip(),
        "salary_text": str(raw.get("salary") or "").strip(),
        "description_snippet": str(raw.get("snippet") or "").strip(),
        "description_evidence_level": "snippet_only",
        "canonical_status": "unresolved",
        "canonical_url": "",
        "discovery_query": keywords,
        "discovery_location": location,
    }


def collect_discovery_jobs(queries, fetch_page, max_pages=10):
    unique = {}
    results_received = 0
    pages_requested = 0
    for query in queries:
        query_results_received = 0
        for page in range(1, max_pages + 1):
            payload = fetch_page(query, page)
            pages_requested += 1
            rows = payload.get("jobs") or []
            if not rows:
                break
            results_received += len(rows)
            query_results_received += len(rows)
            for raw in rows:
                record = normalize_job(raw, query["keywords"], query["location"])
                if record["provider_job_id"]:
                    unique.setdefault(record["discovery_id"], record)
            if query_results_received >= payload.get("totalCount", 0):
                break
    jobs = sorted(unique.values(), key=lambda row: (row["company"].lower(), row["title"].lower(), row["provider_job_id"]))
    coverage = {
        "queries": len(queries),
        "pages_requested": pages_requested,
        "results_received": results_received,
        "unique_jobs": len(jobs),
        "duplicate_results": results_received - len(jobs),
        "unique_companies": len({row["company"] for row in jobs if row["company"]}),
    }
    return jobs, coverage


def jooble_fetcher(api_key, results_per_page=100):
    endpoint = f"https://jooble.org/api/{api_key}"

    def fetch_page(query, page):
        body = json.dumps({
            "keywords": query["keywords"],
            "location": query["location"],
            "page": str(page),
            "ResultOnPage": str(results_per_page),
            "companysearch": "false",
        }).encode()
        request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json", "User-Agent": "SchoolOfDevOps-Skills-Research/1.1"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)

    return fetch_page


def main():
    parser = argparse.ArgumentParser(description="Discover India DevOps-role candidates through the licensed Jooble API.")
    parser.add_argument("--month", default=dt.date.today().strftime("%Y-%m"))
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()
    api_key = os.environ.get("JOOBLE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("JOOBLE_API_KEY is required. Discovery is disabled without authorized API access.")
    queries = json.loads((ROOT / "data/discovery-queries.json").read_text())
    jobs, coverage = collect_discovery_jobs(queries["jooble"], jooble_fetcher(api_key), args.max_pages)
    output = ROOT / "data/discovery" / args.month
    output.mkdir(parents=True, exist_ok=True)
    with (output / "jooble-candidates.jsonl").open("w") as handle:
        for job in jobs:
            handle.write(json.dumps(job, ensure_ascii=False) + "\n")
    summary = {
        "snapshot_month": args.month,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "discovery_only_unpublished",
        "provider": "jooble",
        **coverage,
        "disclosures": [
            "Jooble results are used for role and employer discovery, not as full-description evidence.",
            "Snippets are not passed to the skills-report publication pipeline.",
            "A posting must be resolved to a permitted canonical employer source before skills are extracted.",
        ],
    }
    (output / "jooble-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
