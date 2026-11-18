import csv
from pathlib import Path
from .scoring import score_company

REQUIRED={"company_id","company_name","sector","geography","revenue_usd_m","ebitda_usd_m","revenue_growth_pct","description","website"}
def read_companies(path:str)->list[dict]:
 with open(path,newline="",encoding="utf-8-sig") as f:
  reader=csv.DictReader(f); missing=REQUIRED-set(reader.fieldnames or [])
  if missing: raise ValueError(f"Missing CSV columns: {sorted(missing)}")
  return list(reader)
def run_screen(companies:list[dict],criteria:dict)->list[dict]:
 return sorted((score_company(c,criteria) for c in companies),key=lambda x:(x["fit_score"],x["company_name"].lower()),reverse=True)
def write_outputs(results:list[dict],output:str,roles:list[str])->tuple[Path,Path]:
 dest=Path(output); dest.parent.mkdir(parents=True,exist_ok=True)
 fields=["rank","company_id","company_name","sector","geography","revenue_usd_m","ebitda_usd_m","ebitda_margin_pct","revenue_growth_pct","fit_score","score_sector","score_geography","score_revenue_scale","score_revenue_growth","score_ebitda_margin","website","description","rationale"]
 with dest.open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
  for rank,item in enumerate(results,1): w.writerow({"rank":rank,**{k:item.get(k,"") for k in fields if k!="rank"}})
 contacts=dest.with_name("contact_research_template.csv")
 contact_fields=["company_id","company_name","role_to_research","contact_name","title","profile_url","email","source_name","source_url","verified_on","confidence","analyst_notes"]
 with contacts.open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=contact_fields); w.writeheader()
  for item in results:
   for role in roles: w.writerow({"company_id":item["company_id"],"company_name":item["company_name"],"role_to_research":role,"contact_name":"TO_BE_RESEARCHED","analyst_notes":"Populate only after source verification."})
 return dest,contacts
