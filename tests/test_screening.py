import tempfile,unittest
from pathlib import Path
from ib_target_intelligence.scoring import load_criteria
from ib_target_intelligence.pipeline import read_companies,run_screen,write_outputs
class TestScreen(unittest.TestCase):
 def test_screen_and_contact_template(self):
  root=Path(__file__).parents[1]; c=load_criteria(str(root/"config/sample_mandate.json")); rows=run_screen(read_companies(str(root/"data/sample_companies.csv")),c)
  self.assertEqual(len(rows),12); self.assertGreaterEqual(rows[0]["fit_score"],rows[-1]["fit_score"]); self.assertEqual(rows[0]["sector"],"Industrial Technology")
  with tempfile.TemporaryDirectory() as d:
   out,contacts=write_outputs(rows,str(Path(d)/"shortlist.csv"),c["contact_roles"]); self.assertTrue(out.exists()); self.assertIn("TO_BE_RESEARCHED",contacts.read_text())
if __name__=="__main__": unittest.main()
