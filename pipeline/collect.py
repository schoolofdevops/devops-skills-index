import argparse, collections, datetime as dt, hashlib, html, json, math, pathlib, re, subprocess
from semantic import MODEL_NAME, SemanticRoleMatcher

ROOT = pathlib.Path(__file__).resolve().parents[1]
AI_SKILLS = {"MLOps","LLMOps","Agentic systems","LLM / GenAI","RAG / Vector data","AI evaluation & safety","AI infrastructure","AI platform tools","Cloud AI services"}
EXCLUDED_TITLE_PATTERNS = re.compile(r"\b(customer success|account executive|sales|marketing|recruit|talent|research scientist|data scientist|product manager|product owner|project manager|program manager|business analyst|financial analyst|legal|counsel|designer|design engineer|technical services|solutions engineer|information systems|skillbridge|workplace|support intern)\b",re.I)
DIRECT_ROLE_TITLE = re.compile(r"\b(devops|devsecops|site reliability|sre|platform engineer|platform engineering|mlops|llmops|machine learning platform|ai platform|cloud platform engineer|cloud infrastructure engineer)\b",re.I)
ADJACENT_ROLE_TITLE = re.compile(r"\b(reliability|infrastructure|cloud engineer|production engineer|systems engineer|release engineer|build engineer|deployment engineer|developer productivity|developer experience|observability engineer|kubernetes engineer|gpu infrastructure|inference platform|model serving)\b",re.I)
OPERATIONAL_ANCHORS = ["production systems","production infrastructure","on-call","on call","incident response","infrastructure as code","ci/cd","continuous delivery","kubernetes","cloud infrastructure","service reliability","site reliability","devops","deployment automation","platform engineering","model serving","mlops","llmops","gpu infrastructure"]

def fetch(url):
    response=subprocess.run(["curl","--fail","--silent","--show-error","--location","--max-time","60","--user-agent","SchoolOfDevOps-Skills-Research/1.1 (+https://github.com/schoolofdevops/devops-skills-index)",url],check=True,capture_output=True,text=True)
    return json.loads(response.stdout)

def plain(value):
    value=html.unescape(value or ""); value=re.sub(r"<[^>]+>"," ",value)
    return re.sub(r"\s+"," ",html.unescape(value)).strip()

def contains(text, term):
    if term.startswith(" ") or term.endswith(" "): return term.lower() in f" {text.lower()} "
    return re.search(r"(?<![a-z0-9])"+re.escape(term.lower())+r"(?![a-z0-9])",text.lower()) is not None

def title_role(title,taxonomy):
    if EXCLUDED_TITLE_PATTERNS.search(title): return None
    if not DIRECT_ROLE_TITLE.search(title): return None
    for family,terms in taxonomy["role_families"].items():
        if any(contains(title,t) for t in terms): return family
    return None

def normalize_source_jobs(src):
    if src["provider"]=="greenhouse":
        payload=fetch(f"https://boards-api.greenhouse.io/v1/boards/{src['token']}/jobs?content=true")
        rows=[{"provider_job_id":str(j.get("id")),"title":plain(j.get("title")),"location":plain((j.get("location") or {}).get("name")),"url":j.get("absolute_url"),"updated_at":j.get("updated_at"),"body":plain(j.get("content"))} for j in payload.get("jobs",[])]
        return rows,len(rows)
    if src["provider"]=="lever":
        payload=fetch(f"https://api.lever.co/v0/postings/{src['token']}?mode=json")
        rows=[]
        for j in payload:
            lists=" ".join(plain(x.get("text"))+" "+plain(x.get("content")) for x in j.get("lists",[]))
            rows.append({"provider_job_id":str(j.get("id")),"title":plain(j.get("text")),"location":plain((j.get("categories") or {}).get("location")),"url":j.get("hostedUrl"),"updated_at":dt.datetime.fromtimestamp((j.get("createdAt") or 0)/1000,dt.timezone.utc).isoformat(),"body":plain(j.get("descriptionPlain"))+" "+lists})
        return rows,len(rows)
    if src["provider"]=="smartrecruiters":
        base=f"https://api.smartrecruiters.com/v1/companies/{src['token']}/postings"
        first=fetch(f"{base}?limit=100&offset=0"); total=first.get("totalFound",0); listings=list(first.get("content",[]))
        for offset in range(100,total,100): listings.extend(fetch(f"{base}?limit=100&offset={offset}").get("content",[]))
        rows=[]
        for listing in listings:
            title=plain(listing.get("name"))
            if EXCLUDED_TITLE_PATTERNS.search(title) or not (DIRECT_ROLE_TITLE.search(title) or ADJACENT_ROLE_TITLE.search(title)): continue
            detail=fetch(f"{base}/{listing['id']}"); sections=((detail.get("jobAd") or {}).get("sections") or {})
            body=" ".join(plain((section or {}).get("text")) for section in sections.values())
            rows.append({"provider_job_id":str(listing.get("id")),"title":title,"location":plain((listing.get("location") or {}).get("fullLocation")),"url":detail.get("postingUrl") or f"https://jobs.smartrecruiters.com/{src['token']}/{listing.get('id')}","updated_at":listing.get("releasedDate"),"body":body})
        return rows,total
    if src["provider"]=="ashby":
        payload=fetch(f"https://api.ashbyhq.com/posting-api/job-board/{src['token']}"); jobs=[j for j in payload.get("jobs",[]) if j.get("isListed",True)]
        rows=[]
        for job in jobs:
            address=((job.get("address") or {}).get("postalAddress") or {})
            location=plain(job.get("location")); country=plain(address.get("addressCountry")); region_name=plain(address.get("addressRegion"))
            if country and country.lower() not in location.lower(): location=", ".join(x for x in [location,region_name,country] if x)
            rows.append({"provider_job_id":str(job.get("id")),"title":plain(job.get("title")),"location":location,"url":job.get("jobUrl"),"updated_at":job.get("publishedAt"),"body":plain(job.get("descriptionPlain") or job.get("descriptionHtml"))})
        return rows,len(rows)
    raise ValueError(f"Unsupported provider: {src['provider']}")

def seniority(title,body):
    text=(title+" "+body[:2500]).lower()
    if re.search(r"\b(intern|graduate|junior|entry.level|associate)\b",text): return "Entry"
    if re.search(r"\b(principal|staff|lead|manager|director|head of|architect)\b",title.lower()): return "Lead+"
    if re.search(r"\b(senior|sr\.?|5\+ years|[6-9]\+ years|10\+ years)\b",text): return "Senior"
    return "Mid-level"

def region(location):
    low=location.lower()
    if "india" in low or any(c in low for c in ["bengaluru","bangalore","hyderabad","pune","gurugram","mumbai","chennai","noida","delhi","gurgaon"]): return "India"
    if any(c in low for c in ["united states","canada","remote - us","new york","san francisco","boston","austin"]): return "North America"
    if any(c in low for c in ["united kingdom","germany","france","netherlands","spain","ireland","poland","sweden","europe"]): return "Europe"
    if any(c in low for c in ["australia","singapore","japan","south korea","new zealand","indonesia","malaysia","philippines"]): return "Asia-Pacific"
    return "Other / Global"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--month",default=dt.date.today().strftime("%Y-%m")); args=ap.parse_args()
    sources=json.loads((ROOT/"data/sources.json").read_text()); taxonomy=json.loads((ROOT/"data/taxonomy.json").read_text())
    output=ROOT/"data/snapshots"/args.month; output.mkdir(parents=True,exist_ok=True)
    matcher=SemanticRoleMatcher(); raw=[]; coverage=[]
    for src in sources:
        try:
            jobs,active_count=normalize_source_jobs(src)
            for job in jobs: raw.append((src,job))
            coverage.append({"company":src["company"],"company_type":src["company_type"],"target_market":src["target_market"],"provider":src["provider"],"active_postings":active_count,"retrieval_candidates":len(jobs),"relevant_postings":0,"india_relevant_postings":0,"status":"ok"})
        except Exception as exc:
            coverage.append({"company":src["company"],"company_type":src["company_type"],"target_market":src["target_market"],"provider":src["provider"],"active_postings":0,"retrieval_candidates":0,"relevant_postings":0,"india_relevant_postings":0,"status":f"error: {type(exc).__name__}"})
    title_documents=[f"Job role: {j['title']}" for _,j in raw]
    title_matches=[]
    for start in range(0,len(title_documents),512): title_matches.extend(matcher.match_batch(title_documents[start:start+512]))
    candidate_indexes=[]
    for index,((_,job),title_match) in enumerate(zip(raw,title_matches)):
        explicit=title_role(job["title"],taxonomy)
        anchored=any(contains(job["title"]+" "+job["body"][:3000],a) for a in OPERATIONAL_ANCHORS)
        semantic_title=bool(ADJACENT_ROLE_TITLE.search(job["title"])) and title_match["semantic_score"]>=0.52 and title_match["semantic_margin"]>=0.0 and anchored
        if explicit or (not EXCLUDED_TITLE_PATTERNS.search(job["title"]) and semantic_title): candidate_indexes.append(index)
    print(json.dumps({"stage":"candidate_retrieval","active_postings":len(raw),"semantic_candidates":len(candidate_indexes)}),flush=True)
    candidate_documents=[f"Job title: {raw[i][1]['title']}. Role summary: {raw[i][1]['body'][:500]}" for i in candidate_indexes]
    candidate_matches=[]
    for start in range(0,len(candidate_documents),256): candidate_matches.extend(matcher.match_batch(candidate_documents[start:start+256]))
    semantic_by_index=dict(zip(candidate_indexes,candidate_matches))
    coverage_index={c["company"]:c for c in coverage}; records=[]; rejection_reasons=collections.Counter()
    for index,(src,job) in enumerate(raw):
        title=job["title"]; body=job["body"]; explicit=title_role(title,taxonomy)
        match=semantic_by_index.get(index)
        has_anchor=any(contains(title+" "+body[:4000],a) for a in OPERATIONAL_ANCHORS)
        if EXCLUDED_TITLE_PATTERNS.search(title): rejection_reasons["excluded_title"]+=1; continue
        semantic_pass=bool(match) and bool(ADJACENT_ROLE_TITLE.search(title)) and match["semantic_score"]>=0.62 and match["semantic_margin"]>=0.055 and has_anchor
        if not explicit and not semantic_pass: rejection_reasons["below_semantic_threshold"]+=1; continue
        if match is None: match=title_matches[index]
        family=explicit or match["family"]; basis="explicit_title" if explicit else "semantic"
        confidence=0.96 if explicit else min(0.90,round(0.55+match["semantic_margin"]*2.4,2))
        text=title+" "+body; skills=sorted([name for name,terms in taxonomy["skills"].items() if any(contains(text,t) for t in terms)])
        location=job["location"]; job_region=region(location)
        key="|".join([src["company"].lower(),re.sub(r"\W+"," ",title.lower()).strip(),re.sub(r"\W+"," ",location.lower()).strip()])
        records.append({"record_id":hashlib.sha256(key.encode()).hexdigest()[:16],"provider_job_id":job["provider_job_id"],"company":src["company"],"company_type":src["company_type"],"title":title,"location":location,"region":job_region,"source_provider":src["provider"],"source_url":job["url"],"source_updated_at":job["updated_at"],"collected_month":args.month,"role_family":family,"classification_basis":basis,"classification_confidence":confidence,"semantic_model":MODEL_NAME,"semantic_score":match["semantic_score"],"negative_score":match["negative_score"],"semantic_margin":match["semantic_margin"],"seniority":seniority(title,body),"skills":skills,"ai_signals":sorted(set(skills)&AI_SKILLS),"description_sha256":hashlib.sha256(body.encode()).hexdigest(),"description_char_count":len(body),"taxonomy_version":taxonomy["version"]})
        coverage_index[src["company"]]["relevant_postings"]+=1
        if job_region=="India": coverage_index[src["company"]]["india_relevant_postings"]+=1
    records=sorted({r["record_id"]:r for r in records}.values(),key=lambda r:(r["company"],r["title"],r["location"]))
    successful=sum(c["status"]=="ok" for c in coverage)
    if successful==0: raise RuntimeError("All configured sources failed; refusing to publish an empty snapshot")
    def count(field): return dict(collections.Counter(r[field] for r in records).most_common())
    skill_counts=collections.Counter(s for r in records for s in r["skills"]); ai_counts=collections.Counter(s for r in records for s in r["ai_signals"])
    india_count=sum(r["region"]=="India" for r in records); india_companies=len({r["company"] for r in records if r["region"]=="India"})
    gates=json.loads((ROOT/"data/coverage-gates.json").read_text())
    coverage_assessment={"india_relevant_postings":{"actual":india_count,"minimum":gates["india"]["minimum_relevant_postings"],"pass":india_count>=gates["india"]["minimum_relevant_postings"]},"india_companies":{"actual":india_companies,"minimum":gates["india"]["minimum_companies"],"pass":india_companies>=gates["india"]["minimum_companies"]},"company_types":{"actual":len({r["company_type"] for r in records}),"minimum":gates["overall"]["minimum_company_types"],"pass":len({r["company_type"] for r in records})>=gates["overall"]["minimum_company_types"]}}
    summary={"snapshot_month":args.month,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"status":"iteration_2_candidate_unpublished","taxonomy_version":taxonomy["version"],"semantic_model":MODEL_NAME,"semantic_threshold":{"minimum_score":0.62,"minimum_margin":0.055,"operational_anchor_required":True},"total_active_source_postings":sum(c["active_postings"] for c in coverage),"relevant_deduplicated_postings":len(records),"india_relevant_postings":india_count,"india_companies_with_relevant_postings":india_companies,"companies_configured":len(sources),"companies_covered":successful,"companies_with_relevant_postings":len({r["company"] for r in records}),"company_types":count("company_type"),"coverage_assessment":coverage_assessment,"coverage_gate_pass":all(x["pass"] for x in coverage_assessment.values()),"role_families":count("role_family"),"classification_basis":count("classification_basis"),"seniority":count("seniority"),"regions":count("region"),"skills":dict(skill_counts.most_common()),"ai_signals":dict(ai_counts.most_common()),"rejection_reasons":dict(rejection_reasons),"coverage":coverage,"disclosures":["Iteration 2 candidate is not published until coverage and audit gates pass.","The semantic model retrieves operationally similar roles but can still produce false positives and omissions.","The source panel remains limited to employers with compliant public ATS feeds.","Monthly samples may include different employers and openings.","Job descriptions indicate stated demand, not hiring outcomes or actual work performed."]}
    with (output/"jobs.jsonl").open("w") as fh:
        for record in records: fh.write(json.dumps(record,ensure_ascii=False)+"\n")
    audit=[]; grouped=collections.defaultdict(list)
    for record in records: grouped[(record["region"],record["role_family"],record["classification_basis"])].append(record)
    for stratum,stratum_records in sorted(grouped.items()):
        target=max(3,math.ceil(len(stratum_records)*0.10)); ranked=sorted(stratum_records,key=lambda r:hashlib.sha256(f"{args.month}|{r['record_id']}".encode()).hexdigest())
        for record in ranked[:target]: audit.append({**record,"review_status":"Pending","reviewed_relevance":"","reviewed_role_family":"","reviewed_seniority":"","skills_correct":"","ai_signals_correct":"","review_notes":""})
    with (output/"audit_queue.jsonl").open("w") as fh:
        for record in audit: fh.write(json.dumps(record,ensure_ascii=False)+"\n")
    summary["audit_sample_size"]=len(audit); summary["audit_method"]="Deterministic 10% sample stratified by geography, role family and classification basis, with at least three records per populated stratum."
    (output/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    if summary["coverage_gate_pass"]:
        (ROOT/"public/data").mkdir(parents=True,exist_ok=True); (ROOT/"public/data/latest.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"month":args.month,"active":summary["total_active_source_postings"],"relevant":len(records),"india":summary["india_relevant_postings"],"companies":summary["companies_with_relevant_postings"]}))

if __name__=="__main__": main()
