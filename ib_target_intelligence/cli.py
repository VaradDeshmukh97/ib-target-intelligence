import argparse
from .scoring import load_criteria
from .pipeline import read_companies,run_screen,write_outputs
def main():
 p=argparse.ArgumentParser(description="IB target screening demo"); p.add_argument("--companies",required=True); p.add_argument("--criteria",required=True); p.add_argument("--output",required=True); a=p.parse_args()
 c=load_criteria(a.criteria); rows=run_screen(read_companies(a.companies),c); shortlist,contacts=write_outputs(rows,a.output,c.get("contact_roles",["Chief Executive Officer","Chief Financial Officer"]))
 print(f"Screened {len(rows)} companies.\nShortlist: {shortlist}\nContact template: {contacts}\nTop targets:")
 for x in rows[:5]: print(f"{x['fit_score']:5.1f}  {x['company_name']}")
if __name__=="__main__": main()
