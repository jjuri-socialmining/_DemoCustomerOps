# Links cortos — registro y convención

Acortador propio sobre GitHub Pages. Cada código es una carpeta
`web/go/<codigo>/` con un redirect instantáneo a la página real con sus UTM;
el tracker (`web/assets/track.js`) captura fuente, campaña y contenido en cada visita.

**No editar los stubs a mano** — la fuente de verdad es `links.json`;
este README y `docs-4b8e2d1.html` se regeneran con el tool.

## Convención de códigos

`<fuente>[-cliente]-<pagina>` — ej. `r-ds`, `li-rag`, `w-acme-ds`

| Clave | Fuente (`utm_source` / `utm_medium`) |
|---|---|
| `r` | Resume — `resume` / `pdf` |
| `w` | WhatsApp — `whatsapp` / `chat` |
| `li` | LinkedIn — `linkedin` / `social` |
| `web` | Internet/otro — `web` / `referral` |
| `em` | Email — `email` / `email` |

| Clave | Página (`utm_content`) |
|---|---|
| `ds` | Dashboard SIGMA — `Dashboard_GemeloDigital_SIGMA.html` (`dashboard-sigma`) |
| `ds-en` | Dashboard SIGMA (EN) — `Dashboard_DigitalTwin_SIGMA.html` (`dashboard-sigma-en`) |
| `rag` | Evidencia RAG — `projects/rag-pipeline-evidence.html` (`rag-evidence`) |
| `svc` | Portafolio de servicios (EN) — `pages/sigma-services-en.html` (`services-en`) |
| `home` | Landing SIGMA (EN) — `index-en.html` (`home-en`) |
| `kpi` | Landing KPI (ES) — `(raíz)` (`kpi-panel`) |
| `gh` | Perfil GitHub (externo) — `https://github.com/jjuri-socialmining` (`sin UTM`) |
| `lin` | Perfil LinkedIn (externo) — `https://linkedin.com/in/jjuri-CI-vancouver` (`sin UTM`) |
| `3d` | Demo 3D CIC (externo, sin tracker) — `https://jjuri-socialmining.github.io/miningops-capsule-demo/cic-adsorption-circuit-demo-v2.html` (`sin UTM`) |

## Links activos

| Código | Link corto | Fuente | Página | Campaña |
|---|---|---|---|---|
| `li-ds` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/li-ds | LinkedIn | Dashboard SIGMA | general |
| `li-ds-en` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/li-ds-en | LinkedIn | Dashboard SIGMA (EN) | general |
| `li-home` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/li-home | LinkedIn | Landing SIGMA (EN) | general |
| `li-rag` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/li-rag | LinkedIn | Evidencia RAG | general |
| `li-svc` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/li-svc | LinkedIn | Portafolio de servicios (EN) | general |
| `r-aijobs-3d` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-3d | Resume | Demo 3D CIC (externo, sin tracker) | ai-job-search |
| `r-aijobs-ds` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-ds | Resume | Dashboard SIGMA | ai-job-search |
| `r-aijobs-gh` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-gh | Resume | Perfil GitHub (externo) | ai-job-search |
| `r-aijobs-home` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-home | Resume | Landing SIGMA (EN) | ai-job-search |
| `r-aijobs-kpi` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-kpi | Resume | Landing KPI (ES) | ai-job-search |
| `r-aijobs-lin` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-lin | Resume | Perfil LinkedIn (externo) | ai-job-search |
| `r-aijobs-rag` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-rag | Resume | Evidencia RAG | ai-job-search |
| `r-aijobs-svc` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-aijobs-svc | Resume | Portafolio de servicios (EN) | ai-job-search |
| `r-ds` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-ds | Resume | Dashboard SIGMA | general |
| `r-ds-en` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-ds-en | Resume | Dashboard SIGMA (EN) | general |
| `r-home` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-home | Resume | Landing SIGMA (EN) | general |
| `r-rag` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-rag | Resume | Evidencia RAG | general |
| `r-svc` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/r-svc | Resume | Portafolio de servicios (EN) | general |
| `w-ds` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/w-ds | WhatsApp | Dashboard SIGMA | general |
| `w-ds-en` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/w-ds-en | WhatsApp | Dashboard SIGMA (EN) | general |
| `w-home` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/w-home | WhatsApp | Landing SIGMA (EN) | general |
| `w-rag` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/w-rag | WhatsApp | Evidencia RAG | general |
| `w-svc` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/w-svc | WhatsApp | Portafolio de servicios (EN) | general |
| `web-ds` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/web-ds | Internet/otro | Dashboard SIGMA | general |
| `web-ds-en` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/web-ds-en | Internet/otro | Dashboard SIGMA (EN) | general |
| `web-home` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/web-home | Internet/otro | Landing SIGMA (EN) | general |
| `web-rag` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/web-rag | Internet/otro | Evidencia RAG | general |
| `web-svc` | https://jjuri-socialmining.github.io/_DemoCustomerOps/go/web-svc | Internet/otro | Portafolio de servicios (EN) | general |

## Uso del tool

```bash
python3 tools/make_shortlink.py add w-acme-ds --source w --page ds --client acme
python3 tools/make_shortlink.py list
python3 tools/make_shortlink.py rebuild   # regenera stubs + docs desde links.json
```
