import string

from littlexml.token import Token, TokenType, CHARACTER_MAPPING


class Lexer:
    """
    Converts a LittleXML string into a stream of lexical tokens.
    The object can be iterated over, yielding the resulting tokens.
    :param input_string: The string to be tokenized
    """

    def __init__(self, input_string):
        self.input_string = input_string
        self._tokens = None
        self._serialized = None
        self._tokenize()

    def __iter__(self):
        return iter(self._get_tokens())

    @property
    def tokens(self):
        """list of tokens"""
        return self._get_tokens()

    def as_dict(self):
        """
        Get tokens in a serializable format.
        :return: Token stream as list of dicts
        """
        if self._serialized is None:
            tokens = self._get_tokens()
            self._serialized = [token.to_dict() for token in tokens]
        return self._serialized

    def _get_tokens(self):
        if self._tokens is None:
            self._tokenize()
        return self._tokens

    def _tokenize(self):
        """
        Perform lexical analysis of the input string.
        :raises LexicalError: If an unexpected character or end of input is
            found in the input stream
        """
        self._position = 0
        self._tokens = []

        # Repeat until reaching the end of input
        while self._position < len(self.input_string):

            # Get the next tokens in the output stream
            tokens = self._get_token()

            # Add returned tokens to the list of tokens
            if isinstance(tokens, list):
                # Multiple tokens returned
                self._tokens += tokens
            else:
                # A single token returned
                self._tokens.append(tokens)

        # Include the END_OF_STRING token at the end
        end_position = len(self.input_string) + 1
        self._tokens.append(Token(
            token_type=TokenType.END_OF_STRING,
            start=end_position,
        ))

    def _get_token(self):
        """
        Analyze characters at the current position in the input stream and
        find out which token should follow in the output stream.
        :return: The next token (or multiple tokens) in the stream
        :raises LexicalError: If an unexpected character or end of input is
            found in the input stream
        """

        # Get the next character in the input stream
        input_char = self._next_char()

        # If the character is a letter, return a LETTER token
        if input_char in string.ascii_letters:
            return Token(
                token_type=TokenType.LETTER,
                start=self._position,
                value=input_char,
            )

        # If the character is a digit, return a DIGIT token
        if input_char in string.digits:
            return Token(
                token_type=TokenType.DIGIT,
                start=self._position,
                value=input_char,
            )

        # If the character is whitespace, return a SPACE token
        if input_char in string.whitespace:
            self._consume_space()
            return Token(
                token_type=TokenType.SPACE,
                start=self._position,
            )

        # Try to match character using the mapping
        if input_char in CHARACTER_MAPPING:
            if input_char == '>':
                self._consume_space()
            return Token(
                token_type=CHARACTER_MAPPING[input_char],
                start=self._position,
                value=input_char,
            )

        # If the character is a forward slash, try to match a GT_SLASH token
        if input_char == '/':
            self._consume(chars='>')
            self._consume_space()
            return Token(
                token_type=TokenType.GT_SLASH,
                start=self._position,
            )

        # If the character is a less-than sign or a question mark,
        # one of multiple tokens could be possible
        if input_char == '<':
            return self._analyze_lt()
        if input_char == '?':
            return self._analyze_q(input_char=input_char)

        # If no token is returned, raise an exception
        raise LexicalError(
            f'Invalid character at position {self._position}: {input_char}'
        )

    def _analyze_lt(self):
        """
        Analyze characters after a less-than sign in the input stream.
        :return: The next token (or multiple tokens) in the stream
        :raises LexicalError: If an unexpected character or end of input is
            found in the input stream
        """

        # Peek at the next character in the input stream
        next_char = self._peek_char()

        # If the character is a forward slash, return a LT_SLASH token
        if next_char == '/':
            self._next_char()
            return Token(
                token_type=TokenType.LT_SLASH,
                start=self._position,
            )

        # If the character is a question mark,
        # try to match LT_XML and VERSION tokens
        if next_char == '?':
            self._consume(chars='?xml version=')
            lt_xml_token = Token(
                token_type=TokenType.LT_XML,
                start=self._position,
            )
            version_token = Token(
                token_type=TokenType.VERSION,
                start=self._position,
            )
            return [lt_xml_token, version_token]

        # Otherwise return a LESS_THAN token
        return Token(
            token_type=TokenType.LESS_THAN,
            start=self._position,
        )

    def _analyze_q(self, input_char):
        """
        Analyze characters after a question mark in the input stream.
        :return: The next token in the stream
        """

        # Peek at the next character in the input stream
        next_char = self._peek_char()

        # If the character is a greater-than sign, return a GT_XML token
        if next_char == '>':
            self._next_char()
            self._consume_space()
            return Token(
                token_type=TokenType.GT_XML,
                start=self._position,
            )

        # Otherwise return a SIGN token
        return Token(
            token_type=TokenType.SIGN,
            start=self._position,
            value=input_char,
        )

    def _consume(self, chars):
        """
        Move forward in the input stream and check if the characters match.
        :param chars: Characters expected in the input
        :raises LexicalError: If an non-matching character or end of input is
            found in the input stream
        """
        for char in chars:
            input_char = self._next_char()
            if input_char is None:
                raise LexicalError('Unexpected end of input')
            if input_char != char:
                raise LexicalError(
                    f'Invalid character at position {self._position}: '
                    f'{input_char}'
                )

    def _consume_space(self):
        """
        Move forward in the input stream while the characters are whitespace.
        """
        while self._peek_char():
            if self._peek_char() in string.whitespace:
                self._next_char()
            else:
                break

    def _next_char(self):
        """
        Move forward in the input stream by one character.
        :return: The current character, `None` if end of input
        """
        try:
            char = self.input_string[self._position]
        except IndexError:
            return None
        self._position += 1
        return char

    def _peek_char(self):
        """
        Peek at the next character in the input stream.
        :return: The following character, `None` if end of input
        """
        try:
            return self.input_string[self._position]
        except IndexError:
            return None


class LexicalError(Exception):
    name = 'Lexical error'
