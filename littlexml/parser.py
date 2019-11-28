import sys

from littlexml.lexer import Lexer
from littlexml.rule import RuleType, RULE_DICT
from littlexml.token import TokenType


class Parser:
    """
    Parses a LittleXML string or stream of lexical tokens.
    :param input_stream: The string or token stream to be parsed
    :param parse_tokens: Whether `input_stream` is a stream of tokens
    :param verbose: Print verbose output
    """

    def __init__(self, input_stream, parse_tokens=False, verbose=False):
        self.input_stream = input_stream
        self.verbose = verbose
        if not parse_tokens:
            self._tokens = Lexer(input_string=input_stream).tokens
        else:
            self._tokens = list(input_stream)
        self._parse()

    def _parse(self):
        """
        Perform syntactic analysis of the token stream.
        :raises ParsingError: If an unexpected token or end of input is
            found in the input stream
        """
        self._position = 0
        self._stack = [RuleType.XML_DOCUMENT, TokenType.END_OF_STRING]
        while self._stack:
            stack_top = self._stack.pop(0)
            stack_next = self._next_rule(stack_top=stack_top)
            self._stack = stack_next + self._stack

    def _next_rule(self, stack_top):
        """
        Analyze token at the current position in the input stream.
        :return: List of elements to push to the stack
        :raises ParsingError: If an unexpected token or end of input is
            found in the input stream
        """
        token = self._get_token()

        if self.verbose:
            print(stack_top, token.token_type, file=sys.stderr)

        if isinstance(stack_top, RuleType):
            state = stack_top, token.token_type
            stack_next = RULE_DICT.get(state, None)
            if stack_next is not None:
                return stack_next

        if isinstance(stack_top, TokenType) and token.token_type == stack_top:
            self._position += 1
            return []

        raise ParsingError(
            f'Invalid token at position {token.start}: '
            f'{token.token_type.value}'
        )

    def _get_token(self):
        """
        Get current token in the input stream.
        :return: The current token
        :raises ParsingError: If end of input is found
        """
        try:
            token = self._tokens[self._position]
        except IndexError:
            raise ParsingError('Unexpected end of input')
        return token


class ParsingError(Exception):
    name = 'Parsing error'
