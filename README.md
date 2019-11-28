# LittleXML

Command line tool for parsing LittleXML files.


## Installation

Make sure you have Python 3 installed.

Use `pip` from the project root to install the package.

```console
$ pip install .
```


## Usage

Use `littlexml` to invoke the tool.

```console
$ littlexml  # display help message
```

Use the `validate` command to parse a LittleXML string and print if its valid or not.

```console
$ littlexml validate
```

By default, the command reads data from standard input.
To specify an input file, use the `-i` flag.

```console
$ littlexml validate -i good-example.littlexml
OK
$ littlexml validate -i bad-example.littlexml
Parsing error -- Invalid token at position 48: lt_slash
```


### Lexical analysis

For lexical analysis, use the `tokenize` command.

```console
$ littlexml tokenize
```

This reads data in LittleXML format and outputs the token stream as a JSON array.

To specify input and output files, use the `-i` and `-o` flags.

```console
$ littlexml tokenize -i example.littlexml -o tokens.json
```

To display the token stream in a shorter human-readable format instead of JSON, use the `-s` flag.

```console
$ littlexml tokenize -i example.littlexml -s
<lt_xml> start=14
<version> start=14
<digit> start=15 value='1'
<dot> start=16 value='.'
...
```


### Syntactic analysis

To perform syntactic analysis only, use `validate` with the `-t` flag.

```console
$ littlexml validate -t
```

This accepts a JSON token stream from standard input and prints whether parsing was successful or not.

Use the `-i` flag to specify an input file.

```console
$ littlexml validate -t -i tokens.json
OK
```

Use the `-v` flag to display the current token and the element currently at the top of the stack at each step during parsing.

```console
$ littlexml validate -i example.littlexml -v
RuleType.XML_DOCUMENT TokenType.LT_XML
RuleType.XML_DECLARATION TokenType.LT_XML
TokenType.LT_XML TokenType.LT_XML
TokenType.VERSION TokenType.VERSION
...
```
