import argparse
import json
import sys

from littlexml.lexer import Lexer, LexicalError
from littlexml.parser import Parser, ParsingError
from littlexml.token import Token


def parse_args():

    parser = argparse.ArgumentParser(
        prog='littlexml',
        description='Command line tool for parsing LittleXML files',
    )
    parser.set_defaults(handler=print_help)
    subparsers = parser.add_subparsers(
        title='subcommands',
        dest='subcommand',
    )

    validate_parser = subparsers.add_parser(
        name='validate',
        description='Validate LittleXML string',
        help='perform syntactic analysis',
    )
    validate_parser.set_defaults(handler=validate)
    validate_parser.add_argument(
        '-i', '--input-file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='LittleXML file to validate',
        dest='input_file',
    )
    validate_parser.add_argument(
        '-t', '--tokens',
        action='store_true',
        help='read token stream in JSON format',
        dest='tokens',
    )
    validate_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='print top of stack and current token '
             'at each step during parsing',
        dest='verbose',
    )

    tokenize_parser = subparsers.add_parser(
        name='tokenize',
        description='Perform lexical analysis of a LittleXML file',
        help='perform lexical analysis',
    )
    tokenize_parser.set_defaults(handler=tokenize)
    tokenize_parser.add_argument(
        '-i', '--input-file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='file containing string for lexical analysis',
        dest='input_file',
    )
    tokenize_parser.add_argument(
        '-o', '--output-file',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='file for storing the resulting token stream',
        dest='output_file',
    )
    tokenize_parser.add_argument(
        '-s', '--short',
        action='store_true',
        help='output token stream in short format instead of JSON',
        dest='short',
    )

    args = parser.parse_args()
    args.handler(parser=parser, args=args)


def print_help(parser, args):
    parser.print_help()


def tokenize(parser, args):
    lexer = Lexer(input_string=args.input_file.read())
    if args.short:
        for token in lexer:
            print(token, file=args.output_file)
    else:
        json.dump(lexer.as_dict(), args.output_file, indent=2)
        args.output_file.write('\n')


def validate(parser, args):
    if args.tokens:
        token_list = json.load(args.input_file)
        input_stream = Token.from_list(token_list=token_list)
    else:
        input_stream = args.input_file.read()
    try:
        Parser(
            input_stream=input_stream,
            parse_tokens=args.tokens,
            verbose=args.verbose,
        )
    except (LexicalError, ParsingError) as error:
        print(f'{error.name} -- {error}', file=sys.stderr)
        exit(1)
    else:
        print(f'OK', file=sys.stderr)


if __name__ == '__main__':
    parse_args()
