'''
Created on 26 feb. 2020

@author: imoreno
'''
import unittest
from pydatastudio.caseformatter import CaseFormatter
import re


class Test(unittest.TestCase):


    def testName(self):
        myformatter = CaseFormatter()

        template_str = "normal:{test}, upcase:{test!u}, lowcase:{test!l}, first upcase:{test!c}, first lowcase:{test!f}"
        
        data = {}
        data["test"] = "DiDaDoDu"
        
        output = myformatter.format(template_str, **data)
        
        expected = "normal:DiDaDoDu, upcase:DIDADODU, lowcase:didadodu, first upcase:Didadodu, first lowcase:dIDADODU"
        
        self.assertEqual(output, expected, "Expected: {}, but obtained: {}".format(expected, output))        

    def test_assert_regexp(self):
        
        a = "(.*37, 111, 35.*)|(.*37, 111, 36.*)|(.*37, 111, 38.*)"
        b = "rgb(137, 111, 36)"
        
        assert re.search(a, b), "{} not in {}".format(b, a)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()