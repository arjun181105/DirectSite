import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from monitoring import check,summary
class MonitoringTests(unittest.TestCase):
    def test_unmeasured_not_zero(self):self.assertIsNone(summary([])['ChatGPT Search']['mentionRate'])
    def test_evidence_required(self):
        with self.assertRaises(ValueError):check({'promptId':'geo-01','platform':'ChatGPT Search','date':'2026-09-12','status':'observed','directSiteMentioned':True})
    def test_unavailable_not_negative(self):
        with self.assertRaises(ValueError):check({'promptId':'geo-01','platform':'ChatGPT Search','date':'2026-09-12','status':'unavailable','directSiteMentioned':False,'evidenceFile':'manual.txt','location':'Australia'})
