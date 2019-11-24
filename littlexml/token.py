from enum import Enum


class Token:

    def __init__(self, token_type, start, value=None):
        self.token_type = token_type
        self.start = start
        self.value = value

    def __repr__(self):
        identifier = f'Token [{self.token_type.value} {self.start}]'
        if self.value is not None:
            return f'<{identifier}: {repr(self.value)}>'
        return f'<{identifier}>'

    def __str__(self):
        identifier = f'<{self.token_type.value}> start={self.start}'
        if self.value is not None:
            return f'{identifier} value={repr(self.value)}'
        return identifier

    def to_dict(self):
        token_dict = {
            'type': self.token_type.value,
            'start': self.start,
        }
        if self.value is not None:
            token_dict['value'] = self.value
        return token_dict

    @classmethod
    def from_dict(cls, token_dict):
        return Token(
            token_type=TokenType(token_dict['type']),
            start=token_dict['start'],
            value=token_dict.get('value', None),
        )


class TokenType(Enum):
    LETTER = 'letter'
    DIGIT = 'digit'
    SPACE = 'space'
    HYPHEN = 'hyphen'
    DOT = 'dot'
    COLON = 'colon'
    LESS_THAN = 'less_than'
    LT_SLASH = 'lt_slash'
    LT_XML = 'lt_xml'
    GREATER_THAN = 'greater_than'
    GT_SLASH = 'gt_slash'
    GT_XML = 'gt_xml'
    SIGN = 'sign'
    UNDERSCORE = 'underscore'
    VERSION = 'version'
    END_OF_STRING = 'end_of_string'


CHARACTER_MAPPING = {
    '-': TokenType.HYPHEN,
    '.': TokenType.DOT,
    ':': TokenType.COLON,
    '>': TokenType.GREATER_THAN,
    '@': TokenType.SIGN,
    '_': TokenType.UNDERSCORE,
}
