# IB Target Intelligence

A transparent target-screening and contact-research workflow for investment banking origination. It scores a synthetic company universe against a configurable mandate, ranks the targets, explains the score and creates a separate contact-research template for analyst completion.

**All companies and contact placeholders are synthetic. No real individuals or contact details are included.**

## Run

Requires Python 3.10+ and no third-party runtime dependencies.

```bash
python -m ib_target_intelligence.cli --companies data/sample_companies.csv --criteria config/sample_mandate.json --output outputs/target_shortlist.csv
```

The command also creates `outputs/contact_research_template.csv`.

## Scoring model

| Dimension | Weight | Sample logic |
|---|---:|---|
| Sector fit | 30% | Exact sector match |
| Geography fit | 15% | Mandate geography match |
| Revenue scale | 25% | Fit against target revenue range |
| Revenue growth | 15% | Linear score from the configured growth floor to target |
| EBITDA margin | 15% | Linear score from the configured margin floor to target |

Each component is scored from 0–100 and combined using configurable weights that must sum to 1.0. This is an illustrative mandate model, not an investment recommendation.

## Workflow and controls

- Criteria live in JSON rather than being hard-coded.
- Component scores and rationale are retained in the shortlist output.
- Target screening and contact discovery are separate stages.
- The contact template records role, name, source, source URL, verification date and confidence. A contact should not be treated as verified until supporting evidence is recorded.
- The demo does not scrape websites, guess personal emails or infer real decision-makers.

## Limitations

No company-data vendor, CRM, web search or contact-enrichment provider is connected. A production workflow would need approved sources, entity resolution, deduplication, contact-level provenance, privacy controls, analyst review and integration testing.
