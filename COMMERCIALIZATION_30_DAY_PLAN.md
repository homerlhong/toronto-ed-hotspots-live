# REVENGERS | Toronto Emergency Care Intelligence

## 30-day commercialization plan (2026-11-11 to 2026-12-10)

**Status:** Commercial experiment; no paying customers or validated product-market fit yet.

### Customer and offer
- **Initial buyer hypothesis:** small healthcare consultancies, health-services researchers, and market-intelligence teams that need reproducible Ontario emergency-care reporting.
- **Initial product:** Toronto Emergency Care Intelligence — weekly evidence briefing, sourced metrics table, and a dashboard with provenance and missingness indicators.
- **Value proposition:** reduce analyst time spent finding, reconciling, and documenting public emergency-care indicators. Do not position as patient triage or real-time clinical decision support.
- **Pilot price hypothesis:** USD $750–$2,000 for a four-week bespoke reporting pilot; confirm willingness to pay before building subscriptions. This is an experiment, not a market benchmark.

### Weekly milestones
| Window | Deliverable | Acceptance gate |
| --- | --- | --- |
| Nov 11–17 | Publish Pages; source/licence matrix; snapshot-vs-live audit; 1-page sample brief | No misleading LIVE claims; each metric has date, definition, geography, denominator, source and missingness |
| Nov 18–24 | Repeatable Ontario Health/CIHI data ingest; one hospital comparison and historical trend; interview script | 5 buyer interviews; reproducible dataset with audit trail |
| Nov 25–Dec 1 | Prospect outreach; three tailored demos; pilot statement of work | 10 total qualified conversations; >=3 demos requested or completed |
| Dec 2–10 | Offer 4-week paid pilots, collect objections, revise positioning | >=1 signed paid pilot target; otherwise document why and pivot offer |

### Data rights and methodology gates
1. **Ontario Health ED performance:** official monthly metrics, not a live ED feed. Preserve definition, month, hospital, patient group, and missingness. Review access and reuse terms before commercial redistribution.
2. **Toronto Fire active incidents:** official webpage refreshes every five minutes; the current HTML does not fetch it automatically. No exact incident-location claims, ambulance GPS claims, or assumption that fire dispatches equal ED arrivals. Verify permitted reuse/automated collection before implementing ingestion.
3. **ERstat:** free API/data is non-commercial with attribution; live waits/history and commercial reuse require a commercial licence. Do not scrape, embed in a paid product, or rebroadcast unlicensed data.
4. **Comparability:** hospital wait-time indicators are not interchangeable with live posted waits, modeled predictions, or ED length of stay. Do not rank hospitals without indicator definitions and appropriate caveats.
5. **Clinical safety:** research and operational intelligence only. Never advise patients to delay emergency care or choose an ED from this dashboard.

### Sales discovery questions
1. What recurring emergency-care intelligence decision do you make?
2. What data and reporting tools do you use now?
3. How many analyst hours does this cost each month?
4. What indicators, geography and freshness would make a report actionable?
5. What prevents you from trusting or buying an external dashboard?
6. Would you pay for a four-week pilot, and who approves that spend?

### First outreach draft
**Subject:** Ontario emergency-care intelligence — short research interview

Hello [Name],

I'm developing a source-traceable Ontario emergency-care intelligence briefing for healthcare analysts and consulting teams. It brings together official public reporting, clear indicator definitions, historical trends and transparent data-quality notes.

I'm speaking with a small number of potential users to understand where existing reporting workflows are slow or unreliable. Would you be open to a 15-minute conversation? I'm not asking you to purchase anything during the interview.

Best,
Homer

### Metrics and decision rules
- Track: qualified conversations, demo requests, pilot proposals, paid pilots, hours saved, source coverage and data errors.
- **Go:** at least one paying pilot and evidence of recurring need.
- **Revise:** interviews reveal real need but pricing or scope is wrong.
- **Stop/pivot:** no clear buyer, no repeatable problem, or required data cannot be legally/reliably used.

### Current technical baseline
- GitHub repository: https://github.com/homerlhong/toronto-ed-hotspots-live
- Dashboard file: `index.html` (snapshot-oriented, no implemented automated data fetch as of plan creation).
- GitHub Pages deployment status: unverified; enable Pages on `main` / root and verify URL before promoting.
- No authentication, payments, customer accounts or SLA currently exist.

### Source links to verify during build
- Ontario Health ED metrics: https://www.ontariohealth.ca/system/reporting/performance/time-spent-in-emergency-departments
- Toronto Fire active incidents: https://www.toronto.ca/community-people/public-safety-alerts/alerts-notifications/toronto-fire-active-incidents/
- ERstat commercial API/licensing: https://erstat.ca/developers
- CIHI ED indicator: https://www.cihi.ca/en/indicators/emergency-department-wait-time-for-physician-initial-assessment
