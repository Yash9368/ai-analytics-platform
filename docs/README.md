# AI Analytics Platform — Documentation

This directory contains project documentation organized by phase.

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Project Foundation | ✅ Complete |
| 2 | Frontend Website | 🔲 Pending |
| 3 | Deploy Frontend | 🔲 Pending |
| 4 | Google Analytics 4 | 🔲 Pending |
| 5 | Google Cloud Setup | 🔲 Pending |
| 6 | FastAPI Backend | 🔲 Pending |
| 7 | Frontend + Backend Integration | 🔲 Pending |
| 8 | Claude MCP Integration | 🔲 Pending |
| 9 | Production Deployment | 🔲 Pending |

## Architecture Decisions

- **Service Account Auth** — Chosen over OAuth2 because it works headlessly (no browser needed) and is ideal for server-to-server communication with GA4 Data API.
- **FastAPI** — Chosen for async support, automatic OpenAPI docs, and Pydantic integration.
- **Next.js** — Chosen for SSR/SSG capabilities, TypeScript support, and excellent developer experience.
- **Claude MCP** — Chosen to give Claude direct, structured access to analytics data for generating AI insights.
