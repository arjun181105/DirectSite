import pathlib,sys,unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from benchmark import summarise,public_url,AuditHTML
class BenchmarkTests(unittest.TestCase):
    def test_empty_sample_is_unknown(self):
        s=summarise([]);self.assertEqual(s['n'],0);self.assertIsNone(s['medianHtmlBytes']);self.assertFalse(s['publishable'])
    def test_private_addresses_rejected(self):
        with patch('socket.getaddrinfo',return_value=[(None,None,None,None,('127.0.0.1',443))]):
            with self.assertRaises(ValueError):public_url('https://example.com/')
    def test_non_https_rejected(self):
        with self.assertRaises(ValueError):public_url('http://example.com/')
    def test_static_presence_not_visibility(self):
        p=AuditHTML();p.feed('<title>Example</title><a href="tel:123" hidden>Call</a><form></form>');self.assertEqual(p.tel,1);self.assertEqual(p.forms,1)
