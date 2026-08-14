"use client";

import { useMemo, useState } from "react";

const roles = [
  { name: "DevOps Engineer", share: 31, change: -4, tone: "blue" },
  { name: "Platform Engineer", share: 24, change: 7, tone: "violet" },
  { name: "Site Reliability Engineer", share: 21, change: 2, tone: "green" },
  { name: "Cloud / Infrastructure", share: 13, change: -1, tone: "amber" },
  { name: "MLOps / AI Platform", share: 8, change: 11, tone: "pink" },
  { name: "LLMOps / Agentic Ops", share: 3, change: 18, tone: "red" },
];

const skills = [
  ["Kubernetes", "Containers", 64, 4], ["AWS", "Cloud", 61, 1],
  ["Terraform / OpenTofu", "Infrastructure as code", 58, 6], ["Python", "Programming", 52, 8],
  ["CI/CD", "Delivery", 49, -2], ["Linux", "Systems", 47, -3],
  ["Observability", "Reliability", 43, 9], ["GitOps", "Delivery", 31, 7],
  ["Security / policy as code", "DevSecOps", 28, 10], ["LLM serving & evaluation", "AI operations", 17, 22],
] as const;

const months = [42, 47, 45, 53, 58, 61, 64, 68, 72, 75, 82, 89];
const seniority = [
  { level: "Entry", value: 14, note: "Linux, Git, cloud fundamentals, scripting" },
  { level: "Mid-level", value: 43, note: "IaC, containers, CI/CD, observability" },
  { level: "Senior", value: 34, note: "platform design, SLOs, security, cost" },
  { level: "Lead+", value: 9, note: "strategy, developer experience, governance" },
];

const aiRoleShifts = [
  { role: "DevOps Engineer", from: "Automate delivery and infrastructure", to: "Build governed AI-assisted delivery, secure model access and automate agent workflows", signals: ["AI coding assistants", "agent orchestration", "policy & guardrails"] },
  { role: "Platform Engineer", from: "Provide paved roads for application teams", to: "Provide self-service AI platforms for models, prompts, retrieval, evaluation and inference", signals: ["GPU platforms", "model gateways", "vector databases"] },
  { role: "Site Reliability Engineer", from: "Protect availability and latency of services", to: "Define reliability for probabilistic systems: quality, drift, cost, safety and model performance", signals: ["LLM observability", "evaluation", "AI incident response"] },
  { role: "MLOps / LLMOps Engineer", from: "A specialist role adjacent to DevOps", to: "An operational discipline increasingly embedded across platform and reliability teams", signals: ["model lifecycle", "LLM serving", "experiment tracking"] },
];

const aiSkillFamilies = [
  ["AI foundations", "AI, machine learning, generative AI, transformers, embeddings"],
  ["Model operations", "MLOps, model registry, feature store, experiment tracking, drift"],
  ["LLM operations", "LLMOps, prompt management, RAG, vector databases, model gateways"],
  ["Agentic systems", "AI agents, agent orchestration, tool use, MCP, multi-agent workflows"],
  ["AI infrastructure", "GPU scheduling, accelerators, inference serving, Kubernetes operators"],
  ["Quality & safety", "evaluation, tracing, hallucination monitoring, guardrails, red teaming"],
  ["AI platform tools", "MLflow, Kubeflow, Ray, KServe, vLLM, LangChain, LlamaIndex"],
  ["Cloud AI services", "Bedrock, SageMaker, Vertex AI, Azure AI, OpenAI APIs"],
] as const;

const framework = [
  ["01", "Collect", "Capture title, description, company, location, date, salary and source from approved feeds and public career pages."],
  ["02", "Clean", "Canonicalize locations and companies, strip boilerplate, detect reposts, and keep one record per real opening."],
  ["03", "Classify", "Separate role identity from skills mentioned. Assign role family, level, domain, work mode and industry with confidence."],
  ["04", "Extract", "Match a versioned skills dictionary, then use contextual extraction for requirements, preferences and responsibilities."],
  ["05", "Audit", "Human-review a stratified sample, measure precision and recall, document taxonomy changes and publish confidence bands."],
  ["06", "Publish", "Freeze a monthly snapshot, compute weighted trends, publish the living site and preserve every prior edition."],
];

export default function Home() {
  const [region, setRegion] = useState("Worldwide");
  const [view, setView] = useState<"roles" | "skills">("roles");
  const [methodOpen, setMethodOpen] = useState(false);
  const maxMonth = Math.max(...months);
  const filteredSkills = useMemo(() => skills.map((s, i) => ({ ...s, 2: Math.max(8, s[2] + (region === "India" ? [3, -5, 5, 7, 2, 4, -2, 1, -1, -5][i] : 0)) })), [region]);

  return (
    <main>
      <nav className="nav">
        <a className="brand" href="#top"><span className="mark">D/26</span><span>DevOps Skills Index</span></a>
        <div className="navlinks"><a href="#signals">Signals</a><a href="#ai-impact">AI impact</a><a href="#method">Method</a><a href="#roadmap">Roadmap</a></div>
        <button className="outline" onClick={() => setMethodOpen(true)}>Read methodology</button>
      </nav>

      <section className="hero" id="top">
        <div className="eyebrow"><span className="pulse" /> Living report · 2026 pilot</div>
        <h1>What does an operations<br/>engineer need to know <em>now?</em></h1>
        <p className="lede">A monthly, evidence-led view of the roles and skills employers ask for—from cloud and DevOps to platform engineering, SRE and the emerging AI operations stack.</p>
        <div className="heroActions"><a className="primary" href="#signals">Explore the pilot</a><a className="textlink" href="#method">See how it works <span>↘</span></a></div>
        <div className="scope">
          <div><b>4,504</b><span>historical postings examined</span></div>
          <div><b>2 markets</b><span>India + worldwide baseline</span></div>
          <div><b>Monthly</b><span>proposed update cadence</span></div>
          <div><b>Open method</b><span>versioned taxonomy + QA</span></div>
        </div>
        <p className="pilotNote">Pilot numbers below demonstrate the finished experience and are not yet a 2026 market sample. Historical counts come from your 2023 workbook.</p>
      </section>

      <section className="section dark" id="signals">
        <div className="sectionHead inverse"><div><span className="kicker">01 / MARKET SIGNALS</span><h2>The role is fragmenting.<br/>The skill set is converging.</h2></div><div className="controls"><div className="segmented"><button className={region === "Worldwide" ? "active" : ""} onClick={() => setRegion("Worldwide")}>Worldwide</button><button className={region === "India" ? "active" : ""} onClick={() => setRegion("India")}>India</button></div><span className="period">Illustrative 2026 pilot</span></div></div>
        <div className="featureGrid">
          <article className="featureCard"><span className="label">FASTEST-RISING SIGNAL</span><h3>AI operations is becoming a skill layer before it becomes a job title.</h3><p>Track MLOps, LLMOps and agentic operations twice: as dedicated role families and as capabilities requested inside Platform, SRE and DevOps postings.</p><div className="bigStat">+22<span>pt</span></div><small>illustrative growth in AI-operations skill mentions</small></article>
          <article className="chartCard"><div className="cardTop"><span className="label">AI-OPS SIGNAL INDEX</span><span>Jan → Dec</span></div><div className="spark" aria-label="Illustrative upward trend">{months.map((m, i) => <div key={i} className="bar" style={{height: `${(m/maxMonth)*100}%`}}><span>{i === months.length-1 ? m : ""}</span></div>)}</div><div className="axis"><span>Jan</span><span>Apr</span><span>Jul</span><span>Oct</span><span>Dec</span></div></article>
        </div>
        <div className="dataPanel">
          <div className="panelTabs"><button className={view === "roles" ? "active" : ""} onClick={() => setView("roles")}>Role families</button><button className={view === "skills" ? "active" : ""} onClick={() => setView("skills")}>Top skills</button><span>Share of relevant postings · illustrative</span></div>
          {view === "roles" ? <div className="roleRows">{roles.map((role, i) => <div className="roleRow" key={role.name}><span className="rank">{String(i+1).padStart(2,"0")}</span><b>{role.name}</b><div className="track"><i className={role.tone} style={{width: `${role.share*2.5}%`}} /></div><strong>{role.share}%</strong><span className={role.change >= 0 ? "up" : "down"}>{role.change >= 0 ? "↑" : "↓"} {Math.abs(role.change)}pt</span></div>)}</div> : <div className="roleRows">{filteredSkills.map((skill, i) => <div className="roleRow" key={skill[0]}><span className="rank">{String(i+1).padStart(2,"0")}</span><b>{skill[0]}<small>{skill[1]}</small></b><div className="track"><i className="green" style={{width: `${skill[2]*1.35}%`}} /></div><strong>{skill[2]}%</strong><span className={skill[3] >= 0 ? "up" : "down"}>{skill[3] >= 0 ? "↑" : "↓"} {Math.abs(skill[3])}pt</span></div>)}</div>}
        </div>
      </section>

      <section className="section aiImpact" id="ai-impact">
        <div className="sectionHead"><div><span className="kicker">02 / AI IMPACT</span><h2>AI is changing the work<br/>before it changes the title.</h2></div><p>This chapter will measure whether AI creates new operational roles, enters existing roles as a required capability, or changes the responsibilities of the same familiar job titles.</p></div>
        <div className="aiThesis"><article><span className="label">THE QUESTION</span><h3>Is “Agentic DevOps” becoming a role—or a capability inside DevOps?</h3><p>We will report title adoption separately from mentions in job descriptions. A phrase appearing in responsibilities is not evidence that a new occupation exists.</p></article><div className="aiMeasures"><div><b>01</b><span>Dedicated AI-operations roles</span></div><div><b>02</b><span>AI skills inside existing roles</span></div><div><b>03</b><span>Responsibilities being augmented</span></div><div><b>04</b><span>Traditional tasks being displaced</span></div></div></div>
        <div className="aiShiftGrid">{aiRoleShifts.map((item, i) => <article key={item.role}><div className="shiftTop"><span>0{i+1}</span><h3>{item.role}</h3></div><div className="shift"><small>FROM</small><p>{item.from}</p><i>↓</i><small>TOWARD</small><p>{item.to}</p></div><div className="signalTags">{item.signals.map(signal => <span key={signal}>{signal}</span>)}</div></article>)}</div>
        <div className="aiSkillsBlock"><div><span className="kicker">WHAT WE WILL EXTRACT</span><h3>An AI-specific skills dictionary,<br/>measured in context.</h3><p>Each term is classified as required, preferred, responsibility or incidental mention. We will also report co-occurrence—for example, how often Kubernetes appears with vLLM, or SRE appears with model evaluation.</p></div><div className="aiSkillList">{aiSkillFamilies.map((family, i) => <div key={family[0]}><span>{String(i+1).padStart(2,"0")}</span><b>{family[0]}</b><p>{family[1]}</p></div>)}</div></div>
        <div className="monthlyQuestions"><span className="label">QUESTIONS ANSWERED EVERY MONTH</span><div><p>Are MLOps and LLMOps growing as standalone titles?</p><p>Which DevOps roles now require AI or LLM knowledge?</p><p>Is agentic DevOps language moving from experiments to hiring requirements?</p><p>Which traditional skills remain prerequisites for AI operations?</p><p>How do AI requirements differ by seniority, geography and industry?</p><p>Which tools are durable signals versus short-lived product mentions?</p></div></div>
      </section>

      <section className="section" id="roles">
        <div className="sectionHead"><div><span className="kicker">03 / CAREER LENS</span><h2>One market.<br/>Four different ladders.</h2></div><p>Percentages alone hide what candidates need. Every monthly edition should split demand by seniority and distinguish required skills from preferred ones.</p></div>
        <div className="seniority">{seniority.map((s,i)=><article key={s.level}><div className="donut" style={{"--p": `${s.value*3.6}deg`} as React.CSSProperties}><span>{s.value}%</span></div><span className="step">0{i+1}</span><h3>{s.level}</h3><p>{s.note}</p></article>)}</div>
      </section>

      <section className="section paper" id="method">
        <div className="sectionHead"><div><span className="kicker">04 / THE METHOD</span><h2>A repeatable pipeline,<br/>with receipts.</h2></div><p>Your original principle remains the anchor: companies reveal demand in their job descriptions. The 2026 edition adds reproducibility, deduplication, contextual classification and an explicit QA layer.</p></div>
        <div className="framework">{framework.map(item=><article key={item[0]}><span>{item[0]}</span><h3>{item[1]}</h3><p>{item[2]}</p></article>)}</div>
        <div className="methodCallout"><div><span className="label">THE IMPORTANT CHANGE</span><h3>Count postings, not keyword hits.</h3></div><p>A skill counts once per posting. We retain frequency, but also record whether it appears in the title, required qualifications, preferred qualifications or responsibilities. This prevents long descriptions and repeated boilerplate from dominating the report.</p></div>
      </section>

      <section className="section taxonomy">
        <div className="sectionHead inverse"><div><span className="kicker">05 / 2026 TAXONOMY</span><h2>Track the old stack.<br/>Make room for the new one.</h2></div><p>Version the dictionary monthly. Never rewrite history: each snapshot keeps the taxonomy version used to produce it.</p></div>
        <div className="chips"><span>Systems & Linux</span><span>Cloud</span><span>Infrastructure as code</span><span>Containers</span><span>CI/CD</span><span>Observability</span><span>SRE practices</span><span>Platform engineering</span><span>DevSecOps</span><span>FinOps</span><span>Data operations</span><span>MLOps</span><span>LLMOps</span><span>AI infrastructure</span><span>Agentic operations</span><span>Developer experience</span></div>
        <div className="distinctions"><article><b>ROLE</b><h3>What are they hiring?</h3><p>Canonical family plus the employer’s exact title.</p></article><article><b>CAPABILITY</b><h3>What must the person do?</h3><p>Responsibilities and operating practices, independent of tools.</p></article><article><b>SKILL</b><h3>What must they know?</h3><p>Tools, platforms, languages, frameworks and concepts.</p></article></div>
      </section>

      <section className="section" id="roadmap">
        <div className="sectionHead"><div><span className="kicker">06 / DELIVERY PLAN</span><h2>From pilot to a trusted<br/>monthly publication.</h2></div></div>
        <div className="roadmap"><article><span>WEEK 1–2</span><h3>Design the instrument</h3><p>Freeze scope, sources, role families, skills dictionary, sampling rules and QA targets.</p></article><article><span>WEEK 3–4</span><h3>Run the benchmark</h3><p>Collect the first 2026 sample, calibrate classifiers and manually audit a stratified 10% sample.</p></article><article><span>MONTH 2</span><h3>Publish the first edition</h3><p>Release findings, methodology, downloadable tables and a known-limitations note.</p></article><article><span>MONTHLY</span><h3>Refresh and compare</h3><p>Ingest, dedupe, classify, review exceptions, freeze snapshot and show change versus prior month.</p></article></div>
        <div className="footerCta"><span className="mark large">D/26</span><div><h2>Build the evidence base once.<br/>Let the report keep moving.</h2><p>Next milestone: approved sources + a representative 2026 benchmark sample.</p></div><button className="primary" onClick={() => setMethodOpen(true)}>View research specification</button></div>
      </section>

      <footer><span>DevOps Skills Index · 2026 Pilot</span><span>Method inspired by the Initcron / School of DevOps reports, 2014–2023</span><a href="#top">Back to top ↑</a></footer>

      {methodOpen && <div className="modalBackdrop" onClick={() => setMethodOpen(false)}><div className="modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setMethodOpen(false)} aria-label="Close">×</button><span className="kicker">RESEARCH SPECIFICATION · V0.1</span><h2>What the production study will measure</h2><ul><li><b>Universe:</b> Public, active job postings substantially involving software delivery, infrastructure, reliability, cloud platforms or AI system operations.</li><li><b>Sources:</b> Licensed job feeds, compliant public career pages and selected job boards. Source mix reported every month.</li><li><b>Unit:</b> One deduplicated opening. Reposts linked to a canonical job and measured separately as persistence.</li><li><b>Outputs:</b> Role share, skill penetration, co-occurrence, seniority, geography, industry, remote mode, experience, salary coverage and monthly momentum.</li><li><b>QA:</b> Stratified human audit; precision/recall by role and skill family; uncertain records held for review.</li><li><b>Comparability:</b> Frozen monthly snapshots, versioned taxonomy, stable core panels and explicit backfills.</li></ul><button className="primary" onClick={()=>setMethodOpen(false)}>Close specification</button></div></div>}
    </main>
  );
}
