import json
from pathlib import Path
DEFAULT={"sector":0.30,"geography":0.15,"revenue_scale":0.25,"revenue_growth":0.15,"ebitda_margin":0.15}

def load_criteria(path:str)->dict:
 c=json.loads(Path(path).read_text(encoding="utf-8")); w=c.get("weights",DEFAULT)
 if set(w)!=set(DEFAULT): raise ValueError(f"Weights must be exactly: {list(DEFAULT)}")
 w={k:float(v) for k,v in w.items()}
 if any(v<0 for v in w.values()) or abs(sum(w.values())-1)>1e-6: raise ValueError("Weights must be non-negative and sum to 1.0")
 c["weights"]=w; return c

def range_score(value:float,low:float,high:float)->float:
 if low<=value<=high: return 100.0
 gap=(low-value) if value<low else (value-high)
 return max(0.0,100.0-gap/max(high-low,1.0)*100.0)

def progress_score(value:float,floor:float,target:float)->float:
    if target <= floor: raise ValueError("Score target must be greater than its floor")
    return max(0.0,min(100.0,(value-floor)/(target-floor)*100.0))

def score_company(company:dict,criteria:dict)->dict:
 sector=100.0 if company["sector"].lower()==criteria["sector"].lower() else 0.0
 geo=100.0 if criteria.get("geography","Any").lower() in ("any",company["geography"].lower()) else 0.0
 revenue=float(company["revenue_usd_m"]); ebitda=float(company["ebitda_usd_m"]); growth=float(company["revenue_growth_pct"])
 margin=ebitda/revenue*100 if revenue>0 else 0.0
 parts={"sector":sector,"geography":geo,"revenue_scale":range_score(revenue,float(criteria["revenue_min_usd_m"]),float(criteria["revenue_max_usd_m"])),"revenue_growth":progress_score(growth,float(criteria.get("growth_floor_pct",0)),float(criteria.get("growth_target_pct",25))),"ebitda_margin":progress_score(margin,float(criteria.get("ebitda_margin_floor_pct",0)),float(criteria.get("ebitda_margin_target_pct",25)))}
 total=sum(parts[k]*criteria["weights"][k] for k in parts)
 rationale=[f"Sector {'matches' if sector else 'does not match'} mandate",f"Geography {'matches' if geo else 'does not match'} mandate",f"Revenue USD {revenue:.1f}m: {parts['revenue_scale']:.0f}/100",f"Growth {growth:.1f}%: {parts['revenue_growth']:.0f}/100",f"EBITDA margin {margin:.1f}%: {parts['ebitda_margin']:.0f}/100"]
 return {**company,"ebitda_margin_pct":round(margin,2),"fit_score":round(total,2),**{f"score_{k}":round(v,2) for k,v in parts.items()},"rationale":" | ".join(rationale)}
