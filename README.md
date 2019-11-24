# LittleXML

Command line tool for parsing LittleXML files.

## Usage

Use Python to invoke the command.

```shell script
python -m littlexml  # display help message
```

## Lexical analysis

```shell script
python -m littlexml tokenize
```

This reads data in LittleXML format from stdin and outputs the token stream to stdout in JSON format.

To specify input and output files, use the `-i` and `-o` flags.

```shell script
python -m littlexml -i example.littlexml -o tokens.json
```

To display the token stream in a shorter human-readable format instead of JSON, use the `-s` flag.

```shell script
python -m littlexml -s
```
