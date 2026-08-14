#!/usr/bin/env python3
import argparse, collections, datetime as dt, hashlib, html, json, math, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
AI_SKILLS = {"MLOps","LLMOps","Agentic systems","LLM / GenAI","RAG / Vector data","AI evaluation & safety","AI infrastructure","AI platform tools","Cloud AI services"}

def fetch(url):
    response=subprocess.run(["curl","--fail","--silent","--show-error","--location","--max-time","45","--user-agent","SchoolOfDevOps-Skills-Research/1.0 (+https://github.com/schoolofdevops/devops-skills-index)",url],check=True,capture_output=True,text=True)
    return json.loads(response.stdout)

def plain(value):
    value=html.unescape(value or "")
    value=re.sub(r"<[^>]+>"," ",value)
    return re.sub(r"\s+"," ",html.unescape(value)).strip()

def contains(text, term):
    if term.startswith(" ") or term.endswith(" "): return term.lower() in f" {text.lower()} "
    return re.search(r"(?<![a-z0-9])"+re.escape(term.lower())+r"(?![a-z0-9])",text.lower()) is not None

def classify_role(title, body, taxonomy):
    low=title.lower()
    for family, terms in taxonomy["role_families"].items():
        if any(contains(low,t) for t in terms): return family,"title"
    context=(title+" "+body[:5000]).lower()
    operational=any(contains(context,t) for t in ["infrastructure","kubernetes","cloud platform","reliability","devops","ci/cd","mlops","model serving","production systems"])
    if not operational: return None,None
    for family, terms in taxonomy["role_families"].items():
        if any(contains(context,t) for t in terms): return family,"description"
    return "Cloud / Infrastructure","description"

def seniority(title,body):
    text=(title+" "+body[:2500]).lower()
    if re.search(r"\b(intern|graduate|junior|entry.level|associate)\b",text): return "Entry"
    if re.search(r"\b(principal|staff|lead|manager|director|head of|architect)\b",title.lower()): return "Lead+"
    if re.search(r"\b(senior|sr\.?|5\+ years|[6-9]\+ years|10\+ years)\b",text): return "Senior"
    return "Mid-level"

def region(location):
    low=location.lower()
    if "india" in low or any(c in low for c in ["bengaluru","bangalore","hyderabad","pune","gurugram","mumbai","chennai","noida"]): return "India"
    if any(c in low for c in ["united states","canada","remote - us","new york","san francisco","boston","austin"]): return "North America"
    if any(c in low for c in ["united kingdom","germany","france","netherlands","spain","ireland","poland","sweden","europe"]): return "Europe"
    if any(c in low for c in ["australia","singapore","japan","south korea","new zealand"]): return "Asia-Pacific"
    return "Other / Global"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--month",default=dt.date.today().strftime("%Y-%m")); args=ap.parse_args()
    sources=json.loads((ROOT/"data/sources.json").read_text()); taxonomy=json.loads((ROOT/"data/taxonomy.json").read_text())
    output=ROOT/"data/snapshots"/args.month; output.mkdir(parents=True,exist_ok=True)
    records=[]; coverage=[]
    for src in sources:
        try:
            payload=fetch(f"https://boards-api.greenhouse.io/v1/boards/{src['token']}/jobs?content=true")
            jobs=payload.get("jobs",[]); relevant=0
            for job in jobs:
                body=plain(job.get("content")); title=plain(job.get("title")); location=plain((job.get("location") or {}).get("name"))
                family,basis=classify_role(title,body,taxonomy)
                if not family: continue
                relevant+=1; text=title+" "+body
                skills=sorted([name for name,terms in taxonomy["skills"].items() if any(contains(text,t) for t in terms)])
                key="|".join([src["company"].lower(),re.sub(r"\W+"," ",title.lower()).strip(),re.sub(r"\W+"," ",location.lower()).strip()])
                confidence=0.92 if basis=="title" else 0.62
                records.append({"record_id":hashlib.sha256(key.encode()).hexdigest()[:16],"provider_job_id":str(job.get("id")),"company":src["company"],"title":title,"location":location,"region":region(location),"source_provider":"Greenhouse","source_url":job.get("absolute_url"),"source_updated_at":job.get("updated_at"),"collected_month":args.month,"role_family":family,"classification_basis":basis,"classification_confidence":confidence,"seniority":seniority(title,body),"skills":skills,"ai_signals":sorted(set(skills)&AI_SKILLS),"description_sha256":hashlib.sha256(body.encode()).hexdigest(),"description_char_count":len(body),"taxonomy_version":taxonomy["version"]})
            coverage.append({"company":src["company"],"provider":"Greenhouse","active_postings":len(jobs),"relevant_postings":relevant,"status":"ok"})
        except Exception as exc: coverage.append({"company":src["company"],"provider":"Greenhouse","active_postings":0,"relevant_postings":0,"status":f"error: {type(exc).__name__}"})
    unique={r["record_id"]:r for r in records}; records=sorted(unique.values(),key=lambda r:(r["company"],r["title"],r["location"]))
    successful=sum(c["status"]=="ok" for c in coverage)
    if successful==0: raise RuntimeError("All configured sources failed; refusing to publish an empty snapshot")
    def count(field): return dict(collections.Counter(r[field] for r in records).most_common())
    skill_counts=collections.Counter(s for r in records for s in r["skills"]); ai_counts=collections.Counter(s for r in records for s in r["ai_signals"])
    summary={"snapshot_month":args.month,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"status":"pilot_unaudited","taxonomy_version":taxonomy["version"],"total_active_source_postings":sum(c["active_postings"] for c in coverage),"relevant_deduplicated_postings":len(records),"companies_covered":successful,"role_families":count("role_family"),"seniority":count("seniority"),"regions":count("region"),"skills":dict(skill_counts.most_common()),"ai_signals":dict(ai_counts.most_common()),"coverage":coverage,"disclosures":["Pilot is not yet human-audited.","Source panel is concentrated in technology companies using public Greenhouse boards.","Monthly samples may include different employers and openings.","Job descriptions indicate stated demand, not hiring outcomes or actual work performed."]}
    with (output/"jobs.jsonl").open("w") as fh:
        for record in records: fh.write(json.dumps(record,ensure_ascii=False)+"\n")
    audit=[]
    grouped=collections.defaultdict(list)
    for record in records: grouped[record["role_family"]].append(record)
    for family, family_records in sorted(grouped.items()):
        target=max(10,math.ceil(len(family_records)*0.10))
        ranked=sorted(family_records,key=lambda r:hashlib.sha256(f"{args.month}|{r['record_id']}".encode()).hexdigest())
        for record in ranked[:target]:
            audit.append({**record,"review_status":"Pending","reviewed_role_family":"","reviewed_seniority":"","skills_correct":"","ai_signals_correct":"","review_notes":""})
    with (output/"audit_queue.jsonl").open("w") as fh:
        for record in audit: fh.write(json.dumps(record,ensure_ascii=False)+"\n")
    summary["audit_sample_size"]=len(audit)
    summary["audit_method"]="Deterministic stratified 10% sample by role family, with at least 10 records per family."
    (output/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    (ROOT/"public/data").mkdir(parents=True,exist_ok=True); (ROOT/"public/data/latest.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"month":args.month,"active":summary["total_active_source_postings"],"relevant":len(records),"companies":summary["companies_covered"]}))

if __name__=="__main__": main()
