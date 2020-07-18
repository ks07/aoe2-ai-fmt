# Age of Empires 2 AI Rule Formatter

This project provides a script that allows basic syntax checking and formatting of AoE2 .per files.

Note that this tool is currently a work-in-progress. Crucially, it does not yet have full compatibility with .per files built for DE or User Patch versions of the game.

This tool depends on Python 3.6. It has been developed and tested using Ubuntu for Windows, but should work fine in any Linux based environment.

## Dependencies

Building the tool requires [ANTLR v4.8](https://www.antlr.org/), [pipenv](https://pypi.org/project/pipenv/), and GNU Make.

## Installation From Source

Clone the repository, and then use pipenv to create a python virtualenv and install the necessary dependencies within it.

```
pipenv install
```

It is then necessary to build the lexer, parser, and supporting files using antlr4. The provided Makefile can invoke this for you, provided `antlr4` is in your `$PATH`.

```
make
```

Then, simply run the tool from the command line, from within the virtualenv:

```
# ./format.py <path/to/src.per> <path/to/output.per>
# If the output path is provided as '-' then the formatted script will instead be printed to STDOUT.
pipenv run ./format.py examples/multistmt.input.per -
```

Input files may use Windows or Unix style line endings. Output files will always be created with Windows line endings, to match the platform of the game.

## Testing

A small suite of example inputs and their desired pretty printed equivalents are provided in the repo.
A basic test recipe is included in the Makefile to easily run the tool against all inputs, and allow manual inspection of any differences to the desired output.

```
make test
```

## Limitations

As the tool is built using a parser, invalid syntax will cause the formatter to error.

The tool is built based upon the language details provided in the official documentation supplied with The Conquerors.
As this document isn't a formal language specification, some assumptions had to be made, particularly regarding allowed characters in identifiers and whitespace.
It is possible that files accepted by this tool will not be accepted by the game engine, or vice versa.
*Notably, the more advanced actions and facts available in DE and User Patch are not currently supported by the tool, but support for these is in progress.*

Note that **this tool does not check anything more than basic syntax**.
Non-existant facts or actions, incorrect numbers of arguments, undefined constants, and other similar errors will not be detected by this tool.
