# morph

Morph is a batch file renaming library and application written in Python. It is
an attempt to define flexible renaming rules that can be applied to any given
list of files.

## Features

* Renaming patterns include literals and incrementing counters
* Patterns can be chained together
* File list can be modified between pattern applications
* A cli interface demonstration

## Concepts

A `pattern` is a renaming rule. Given a filename, it will produce a new
filename according to the rule. A `pattern` may depend on additional metadata
such as the index of the file within a file list.

A `pattern chain` is a sequence of `patterns`. Each `pattern` is applied in
sequence to a filename to produce a final filename. A `pattern chain` can be
applied to a list of filenames.

There is the additional FilePatternChain which represents file list
manipulations such as reordering, adding, and deleting of files.

A renaming operation requires two inputs: a file list and a list of pattern
chains. Conceptually, the pattern chains are applied in sequence to the file
list. The actual file renaming operation however just tracks filename changes
(including add/move/deletes) and performs a single file rename from the
original filename to the final filename.

## Usage

`morph-cli` is a REPL python script.

Consider the following dir:

    $ ls -1
    file (1).txt
    file (2).txt
    file (3).txt
    file.txt

The user runs in the dir:

    $ PYTHONPATH=/path/to/morph/dir /path/to/morph/bin/morph-cli *

`morph-cli` takes in a list of files as arguments as the initial list of files.

    Morph> files
    0: file (1).txt
    1: file (2).txt
    2: file (3).txt
    3: file.txt

`files` will list the current file list. The file list can then be manipulated:

    Morph> file -m 0 3
    Move file.txt from position 3 to 0? (y/N) y
    0: file.txt
    1: file (1).txt
    2: file (2).txt
    3: file (3).txt

`chains` creates and manages pattern chains

    Morph> chain -n replace statement.2013. ## .txt
    Chain 0:
        Literal (replace, statement.2013.)
        NumericCounter (append, 1, 1, 2)
        Literal (append, .txt)

This command created a new replace type chain with 3 patterns in a sequence. A
`replace` chain will disregard the original file name when applying the
patterns. This is done by making the first pattern a replace pattern and the
rest of the patterns append patterns. A `literal pattern` consists of a single
literal string. A numeric counter is a padded number that starts from a number
and increases for each subsequence file in the file list.

`preview` allows you to see the result of applying the chain.

    Morph> preview 0
    Preview chain 0:
        Literal (replace, statement.2013.)
        NumericCounter (append, 1, 1, 2)
        Literal (append, .txt)
    
    Files:
    0: statement.2013.01.txt
    1: statement.2013.02.txt
    2: statement.2013.03.txt
    3: statement.2013.04.txt
    
`apply` applies the specified pattern to the current file list. You will see
the file list change.

    Morph> apply 0
    Apply chain 0:
        Literal (replace, statement.2013.)
        NumericCounter (append, 1, 1, 2)
        Literal (append, .txt)
    
    file.txt    =>  statement.2013.01.txt
    file (1).txt    => statement.2013.02.txt
    file (2).txt    =>  statement.2013.03.txt
    file (3).txt    =>  statement.2013.04.txt
    Morph> files
    0: statement.2013.01.txt
    1: statement.2013.02.txt
    2: statement.2013.03.txt
    3: statement.2013.04.txt

When you are satisfied with the final `preview`, `commit` the changes to disk.

    Morph> commit
    Morph>
    $ ls -1
    original
    statement.2013.01.txt
    statement.2013.02.txt
    statement.2013.03.txt
    statement.2013.04.txt
    $ ls -1 original/
    file (1).txt
    file (2).txt
    file (3).txt
    file.txt

The original files are automatically backed up.

## Limitations

* Only replace pattern chains can be created
* Only Literal and NumericCounter default patterns can be created using `chain

## Background

This project is inspired by the [1-4a Rename](http://www.1-4a.com/rename/) utility, a Windows freeware application.

The separation of pattern chains and file lists follows the concept of the separation of code and data.

--
milki <milki@rescomp.berkeley.edu>
