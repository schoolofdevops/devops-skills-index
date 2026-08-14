# DevOps Skills Index

A living, evidence-led view of the roles and skills employers ask for across DevOps, platform engineering, site reliability engineering and AI operations.

## Publication model

The project is designed as a repeatable monthly research publication. It separates:

- job titles from the skills requested inside those jobs;
- required qualifications from preferred qualifications and responsibilities;
- traditional DevOps, SRE and platform engineering from MLOps, LLMOps, AI infrastructure and agentic operations;
- verified findings from actual but unaudited pilot data.

The historical methodology is based on School of DevOps reports published between 2014 and 2023. The corrected August 2026 pilot semantically evaluates more than 6,600 active postings from 34 public employer job boards. It is deliberately labeled unaudited because the source panel is not yet representative, particularly for India.

## Data workflow

`pipeline/collect.py` reads the approved source register in `data/sources.json`, collects public postings, normalizes and deduplicates records, and performs hybrid semantic retrieval against positive role definitions and negative occupation examples. A conservative title boundary prevents generic research, customer success, sales and application-development jobs from entering merely because their descriptions mention cloud or infrastructure. Full job descriptions are not republished; records retain source links, hashes, semantic scores, classification evidence and extracted signals.

The monthly GitHub Action runs on the first day of each month. Each snapshot includes:

- normalized job-level metadata;
- aggregate role, seniority, geography, skill and AI-signal counts;
- source coverage and disclosures;
- a deterministic stratified 10% human-audit queue.

Candidate snapshots must pass the versioned gates in `data/coverage-gates.json` before replacing `public/data/latest.json`. The current India publication gate is 500 relevant postings from at least 150 companies; passing the gate still requires a relevance audit.

Supported public ATS adapters: Greenhouse, Lever, SmartRecruiters and Ashby. `data/source-targets.json` tracks priority employers whose career systems still need compliant adapters.

Review workbook: [DevOps Skills Index 2026 — Corrected Semantic Pilot Review](https://docs.google.com/spreadsheets/d/1UmPSeFHqa5jeASbtyBwLz9RrP6G-mvXcUl8zex0Luno/edit)

## Website

The production site is published automatically through GitHub Pages whenever `main` changes.

- Planned custom domain: [skills.schoolofdevops.com](https://skills.schoolofdevops.com)
- GitHub Pages fallback: `https://schoolofdevops.github.io/devops-skills-index/`

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

## Build targets

```bash
npm run build        # Cloudflare/Sites validation build
npm run build:pages  # Static GitHub Pages export to out/
```

## Research status

The current website displays the actual corrected August 2026 pilot and labels it unaudited. The 2023 workbook contained 930 India postings from 376 companies and 3,576 worldwide postings from 1,626 companies; those figures are coverage benchmarks, not directly comparable trend points. Complete the audit queue and broaden the India and services-company source panels before announcing the snapshot as a representative market report.
