import unittest
from Searcher import Searcher
import json

class Searcher_tests_No_debug(unittest.TestCase):
    #sample json chunk for testing purposes
    examplejson= """{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}"""
    examplejsondes=json.loads(examplejson)
    
    def testtruenodeb(self):
        search = Searcher.searcher('"SGML" AND "example"')
        self.assertTrue(search.IsMatch(self.examplejsondes))
    
    def testfalsenodeb(self):
        search = Searcher.searcher('"SGML" AND NOT "example"')
        self.assertFalse(search.IsMatch(self.examplejsondes))

    def testsubqueriesnodeb(self):
        search = Searcher.searcher('"SGML" AND ("example" OR "meta")')
        self.assertTrue(search.IsMatch(self.examplejsondes))

    def testsubqueriesfalsenodeb(self):
        search = Searcher.searcher('"SGML" AND NOT ("example" OR "meta")')
        self.assertFalse(search.IsMatch(self.examplejsondes))

    #testing the specific match protocol
    def testtrueSpecnodeb(self):
        search = Searcher.searcher('"Markup" AND "Language"')
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data,list))
        self.assertTrue(isinstance(data[0],str))

    def testtrueregSpecnodeb(self):
        search = Searcher.searcher(' ("Markup" AND "Language") AND R"Stand(a|A)rd"')
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data,list))
        self.assertTrue(isinstance(data[0],str))

    def testfalseSpecnodeb(self):
        search = Searcher.searcher('"Standard" AND "used" AND R"ISO"')
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 0)
        self.assertTrue(isinstance(data,list))        
    
    def testfalseregSpecnodeb(self):
        search = Searcher.searcher('"Standard" AND "used"')
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 0)
        self.assertTrue(isinstance(data,list))

    

class Searcher_tests(unittest.TestCase):

#sample json chunk for testing purposes
    examplejson= """{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}"""
    examplejsondes=json.loads(examplejson)
    
    

    #testing the general match protocol
    def testtrue(self):
        search = Searcher.searcher('"SGML" AND "example"',True)
        self.assertTrue(search.IsMatch(self.examplejsondes))

    def testfalse(self):
        search = Searcher.searcher('"SGML" AND NOT "example"',True)
        self.assertFalse(search.IsMatch(self.examplejsondes))   

    def testsubqueries(self):
        search = Searcher.searcher('"SGML" AND ("example" OR "meta")', True)
        self.assertTrue(search.IsMatch(self.examplejsondes)) 

    def testsubqueriesfalse(self):
        search = Searcher.searcher('"SGML" AND NOT ("example" OR "meta")', True)
        self.assertFalse(search.IsMatch(self.examplejsondes))  
    

    def testregexFalse(self):
        search = Searcher.searcher('"SGML" AND NOT ("example" OR "meta") AND R"Stand(a|A)rd"', True)
        self.assertFalse(search.IsMatch(self.examplejsondes))

    def testregex(self):
        search = Searcher.searcher('"SGML" AND ("example" OR "meta") AND R"Stand(a|A)rd"', True)
        self.assertTrue(search.IsMatch(self.examplejsondes))
    
    #testing the specific match protocol
    def testtrueSpec(self):
        search = Searcher.searcher('"Markup" AND "Language"',True)
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data,list))
        self.assertTrue(isinstance(data[0],str))

    def testtrueregSpec(self):
        search = Searcher.searcher(' ("Markup" AND "Language") AND R"Stand(a|A)rd"',True)
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data,list))
        self.assertTrue(isinstance(data[0],str))

    def testfalseSpec(self):
        search = Searcher.searcher('"Standard" AND "used" AND R"ISO"',True)
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 0)
        self.assertTrue(isinstance(data,list))
        
    
    def testfalseregSpec(self):
        search = Searcher.searcher('"Standard" AND "used"',True)
        data = search.SpecificMatch(self.examplejsondes)
        print(data)
        for item in data:
            print(item)
        self.assertEqual(len(data), 0)
        self.assertTrue(isinstance(data,list))
        


    
if __name__ == '__main__':
    unittest.main()
