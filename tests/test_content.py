import copy,json,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from content_model import check_collection,quality
from validate import validate
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ContentTests(unittest.TestCase):
    def setUp(self):self.pages=json.loads((ROOT/'content/pages.json').read_text())
    def test_published_collection(self):check_collection(self.pages)
    def test_draft_cannot_be_indexed(self):
        p=copy.deepcopy(self.pages[0]);p['status']='draft';self.assertFalse(quality(p)['passed'])
    def test_research_requires_real_proof(self):
        p=copy.deepcopy(self.pages[0]);p['pageType']='research';self.assertFalse(quality(p)['passed'])
    def test_duplicate_paragraph_rejected(self):
        p=copy.deepcopy(self.pages);p[1]['sections'][0]=p[0]['sections'][0]
        with self.assertRaises(ValueError):check_collection(p)
    def test_missing_local_evidence_rejected(self):
        p=copy.deepcopy(next(x for x in self.pages if x['pageType']=='location'));p['sources']=[];self.assertFalse(quality(p)['passed'])
    def test_generated_routes(self):validate()
if __name__=='__main__':unittest.main()
