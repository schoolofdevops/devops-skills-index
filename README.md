# DevOps Skills Index

A living, evidence-led view of the roles and skills employers ask for across DevOps, platform engineering, site reliability engineering and AI operations.

## Publication model

The project is designed as a repeatable monthly research publication. It separates:

- job titles from the skills requested inside those jobs;
- required qualifications from preferred qualifications and responsibilities;
- traditional DevOps, SRE and platform engineering from MLOps, LLMOps, AI infrastructure and agentic operations;
- verified findings from actual but unaudited pilot data.

The historical methodology is based on School of DevOps reports published between 2014 and 2023. The first 2026 pilot contains 1,426 normalized postings from eight public employer job boards. It is deliberately labeled unaudited because the initial source panel is not yet representative.

## Data workflow

`pipeline/collect.py` reads the approved source register in `data/sources.json`, collects public postings, normalizes and deduplicates records, applies the versioned taxonomy, and writes a frozen monthly snapshot. Full job descriptions are not republished; records retain source links, hashes, classification evidence and extracted signals.

The monthly GitHub Action runs on the first day of each month. Each snapshot includes:

- normalized job-level metadata;
- aggregate role, seniority, geography, skill and AI-signal counts;
- source coverage and disclosures;
- a deterministic stratified 10% human-audit queue.

Review workbook: [DevOps Skills Index 2026 — Monthly Data Review](https://docs.google.com/spreadsheets/d/1T37fdasLRmQCO79MsSYJaZoX7keslZdD5ZLclRmqRAA/edit)

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

The current website displays the actual August 2026 pilot and labels it unaudited. Complete the audit queue and broaden the source panel before announcing the snapshot as a representative market report.
