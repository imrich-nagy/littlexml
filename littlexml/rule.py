from enum import Enum

from littlexml.token import TokenType


class RuleType(Enum):
    XML_DOCUMENT = 'xml_document'
    XML_DECLARATION = 'xml_declaration'
    VERSION_NUMBER = 'version_number'
    ELEMENT = 'element'
    OPEN_TAG = 'open_tag'
    CLOSE_TAG = 'close_tag'
    WORDS = 'words'
    NEXT_WORD = 'next_word'
    NAME = 'name'
    NAME_CHARS = 'name_chars'
    NUMBER = 'number'
    NEXT_DIGIT = 'next_digit'
    WORD = 'word'
    NEXT_CHAR = 'next_char'


RULE_DICT = {
    (RuleType.XML_DOCUMENT, TokenType.LT_XML): [
        RuleType.XML_DECLARATION,
        RuleType.ELEMENT,
    ],
    (RuleType.XML_DOCUMENT, TokenType.LESS_THAN): [
        RuleType.ELEMENT,
    ],
    (RuleType.XML_DECLARATION, TokenType.LT_XML): [
        TokenType.LT_XML,
        TokenType.SPACE,
        TokenType.VERSION,
        RuleType.VERSION_NUMBER,
        TokenType.GT_XML,
    ],
    (RuleType.VERSION_NUMBER, TokenType.DIGIT): [
        RuleType.NUMBER,
        TokenType.DOT,
        RuleType.NUMBER,
    ],
    (RuleType.ELEMENT, TokenType.LESS_THAN): [
        TokenType.LESS_THAN,
        RuleType.NAME,
        RuleType.OPEN_TAG,
    ],
    (RuleType.OPEN_TAG, TokenType.GREATER_THAN): [
        TokenType.GREATER_THAN,
        RuleType.CLOSE_TAG,
    ],
    (RuleType.OPEN_TAG, TokenType.GT_SLASH): [
        TokenType.GT_SLASH,
    ],
    (RuleType.CLOSE_TAG, TokenType.LESS_THAN): [
        RuleType.ELEMENT,
        TokenType.LT_SLASH,
        RuleType.NAME,
        TokenType.GREATER_THAN,
    ],
    (RuleType.CLOSE_TAG, TokenType.LETTER): [
        RuleType.WORDS,
        TokenType.LT_SLASH,
        RuleType.NAME,
        TokenType.GREATER_THAN,
    ],
    (RuleType.CLOSE_TAG, TokenType.DIGIT): [
        RuleType.WORDS,
        TokenType.LT_SLASH,
        RuleType.NAME,
        TokenType.GREATER_THAN,
    ],
    (RuleType.CLOSE_TAG, TokenType.SIGN): [
        RuleType.WORDS,
        TokenType.LT_SLASH,
        RuleType.NAME,
        TokenType.GREATER_THAN,
    ],
    (RuleType.WORDS, TokenType.LETTER): [
        RuleType.WORD,
        RuleType.NEXT_WORD,
    ],
    (RuleType.WORDS, TokenType.DIGIT): [
        RuleType.WORD,
        RuleType.NEXT_WORD,
    ],
    (RuleType.WORDS, TokenType.SIGN): [
        RuleType.WORD,
        RuleType.NEXT_WORD,
    ],
    (RuleType.NEXT_WORD, TokenType.LT_SLASH): [],
    (RuleType.NEXT_WORD, TokenType.SPACE): [
        TokenType.SPACE,
        RuleType.WORDS,
    ],
    (RuleType.NAME, TokenType.UNDERSCORE): [
        TokenType.UNDERSCORE,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME, TokenType.COLON): [
        TokenType.COLON,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME, TokenType.LETTER): [
        TokenType.LETTER,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.DOT): [
        TokenType.DOT,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.GREATER_THAN): [],
    (RuleType.NAME_CHARS, TokenType.GT_SLASH): [],
    (RuleType.NAME_CHARS, TokenType.UNDERSCORE): [
        TokenType.UNDERSCORE,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.COLON): [
        TokenType.COLON,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.HYPHEN): [
        TokenType.HYPHEN,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.LETTER): [
        TokenType.LETTER,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NAME_CHARS, TokenType.DIGIT): [
        TokenType.DIGIT,
        RuleType.NAME_CHARS,
    ],
    (RuleType.NUMBER, TokenType.DIGIT): [
        TokenType.DIGIT,
        RuleType.NEXT_DIGIT,
    ],
    (RuleType.NEXT_DIGIT, TokenType.GT_XML): [],
    (RuleType.NEXT_DIGIT, TokenType.DOT): [],
    (RuleType.NEXT_DIGIT, TokenType.DIGIT): [
        RuleType.NUMBER,
    ],
    (RuleType.WORD, TokenType.LETTER): [
        TokenType.LETTER,
        RuleType.NEXT_CHAR,
    ],
    (RuleType.WORD, TokenType.DIGIT): [
        TokenType.DIGIT,
        RuleType.NEXT_CHAR,
    ],
    (RuleType.WORD, TokenType.SIGN): [
        TokenType.SIGN,
        RuleType.NEXT_CHAR,
    ],
    (RuleType.NEXT_CHAR, TokenType.LT_SLASH): [],
    (RuleType.NEXT_CHAR, TokenType.SPACE): [],
    (RuleType.NEXT_CHAR, TokenType.LETTER): [
        RuleType.WORD,
    ],
    (RuleType.NEXT_CHAR, TokenType.DIGIT): [
        RuleType.WORD,
    ],
    (RuleType.NEXT_CHAR, TokenType.SIGN): [
        RuleType.WORD],
}
