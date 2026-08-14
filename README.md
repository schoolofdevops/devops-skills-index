# DevOps Skills Index

A living, evidence-led view of the roles and skills employers ask for across DevOps, platform engineering, site reliability engineering and AI operations.

## Publication model

The project is designed as a repeatable monthly research publication. It separates:

- job titles from the skills requested inside those jobs;
- required qualifications from preferred qualifications and responsibilities;
- traditional DevOps, SRE and platform engineering from MLOps, LLMOps, AI infrastructure and agentic operations;
- verified findings from illustrative pilot data.

The historical methodology is based on School of DevOps reports published between 2014 and 2023. The next milestone is a representative, audited 2026 benchmark sample.

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

The current website is a product and methodology pilot. Any illustrative 2026 charts are labeled as such and must be replaced by audited market findings before the first public report is announced as research.
