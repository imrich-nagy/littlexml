import unittest

from littlexml.lexer import LexicalError
from littlexml.parser import Parser, ParsingError


class TestParser(unittest.TestCase):
    VALID_STRINGS = [
        '<?xml version=1.0?><a/>',
        '<?xml version=1.1?><a/>',
        '<?xml version=11.0?><a/>',
        '<?xml version=1.0?><a>1</a>',
        '<a/>',
        '<_/>',
        '<:/>',
        '<xml/>',
        '<_xml/>',
        '<:xml/>',
        '<xml-1.0/>',
        '<__:x:--:m:--:l:__/>',
        '<xml>a</xml>',
        '<_xml>a</_xml>',
        '<:xml>a</:xml>',
        '<xml-1.0>a</xml-1.0>',
        '<nested><xml/></nested>',
        '<nested><xml>a</xml></nested>',
        '<nested1><nested2>a</nested2></nested1>',
        '<nested1><nested2><nested3/></nested2></nested1>',
        '<xml>1</xml>',
        '<xml>?</xml>',
        '<xml>@</xml>',
        '<xml>word</xml>',
        '<xml>word123</xml>',
        '<xml>word another</xml>',
        '<xml>word@ ?words   123 12 3 ?1?2@3@ @ @@ @another??? ? ??</xml>',
        '<nested><xml>a</xml></nested>',
        '<nested><xml>1</xml></nested>',
        '<nested><xml>word words 123 another</xml></nested>',
    ]
    INVALID_STRINGS = [
        '<?xml version=1.0?>',
        '<?xml version=1.0?>a',
        '<?xml?><a/>',
        '<?xml version=?><a/>',
        '<?xml version=1?><a/>',
        '<?xml version=1.?><a/>',
        '<?xml version=1..0?><a/>',
        '<?xml version=1.0.0?><a/>',
        '<?xml versions=1.0?><a/>',
        '<?xmlversion=1.0?><a/>',
        '<?xml version=1.0><a/>',
        '<xml version=1.0?><a/>',
        '<xml version=1.0><a/>',
        '<a/><?xml versions=1.0?><a/>',
        '<a></a><?xml versions=1.0?><a/>',
        '<a>',
        '<1/>',
        '<xml>',
        '<xml/',
        'xml/>',
        '<.xml/>',
        '<-xml/>',
        '<1xml/>',
        '<xml?/>',
        '<?xml/>',
        '<x?ml/>',
        '<xml/></xml>',
        '<xml><xml>',
        '<xml><xml/>',
        '<xml></xml',
        '<.xml></xml>',
        '<-xml></xml>',
        '<1xml></xml>',
        '<xml></.xml>',
        '<xml></-xml>',
        '<xml></1xml>',
        '<?xml></xml>',
        '<xml><?xml>',
        '<xml?></xml>',
        '<xml></xml?>',
        '<nested><xml/>',
        '<nested>xml/></nested<',
        '<nested/><xml/></nested>',
        '<nested><xml></nested>',
        '<nested></xml></nested>',
        '<nested><xml/></xml></nested>',
        '<nested><xml><xml/></nested>',
        '<nested><xml><xml></nested>',
        '<nested>a<xml>word</xml></nested>',
        '<nested1><nested2><nested3></nested2></nested1>',
        '<nested1>nested2><nested3/></nested2></nested1>',
        '<nested1><nested2>nested3/></nested2></nested1>',
        '<nested1><nested2><nested3/></nested2</nested1>',
        '<nested1><nested2>a<nested3/></nested2></nested1>',
        '<nested1><nested2><nested3/>a</nested2></nested1>',
        '<nested1><nested2><nested3></nested2></nested3></nested1>',
    ]

    def test_valid(self):
        for test_string in self.VALID_STRINGS:
            with self.subTest(string=test_string):
                try:
                    Parser(input_stream=test_string)
                except (LexicalError, ParsingError):
                    self.fail()

    def test_invalid(self):
        for test_string in self.INVALID_STRINGS:
            with self.subTest(string=test_string):
                with self.assertRaises((LexicalError, ParsingError)):
                    Parser(input_stream=test_string)
