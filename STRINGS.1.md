# STRINGS(1)

## NAME
strings - print the strings of printable characters in files

## SYNOPSIS
**strings**
\[-a|--all\]
\[-D|--delimiters STRING\]
\[-e|--encoding CHAR\]
\[-f|--print-file-name\]
\[-h|--help|-?\]
\[-L|--length NUM\]
\[-m|-n|--bytes NUM | -NUM\]
\[-o\]
\[-O|--offset NUM\]
\[-s|--output-separator STRING\]
\[-S|--split-lines\]
\[-t|--radix CHAR\]
\[-v|-V|--version\]
\[-w|--include-all-whitespace\]
\[@file\]
\[--debug\]
\[--\]
\[file ...\]

## DESCRIPTION
For each file specified, the **strings** utility prints contiguous sequences of printable characters that are at least n characters long and are followed by an unprintable character.
The default value of n is 4.
The **strings** utility is mainly used for determining the contents of non-text files.

If no file name is specified as an argument, standard input is read.

### OPTIONS
The following options are available:

Options | Use
------- | ---
-a\|--all|Scan the entire file for printable strings
-D\|--delimiters LIST|Use the ':' separated list of character values as delimiters
-e\|--encoding CHAR|Select the character encoding to be used while searching for strings. Valid values for are:<br><ul><li>s for single 7-bit-byte characters (ASCII, ISO 8859).<li>S for single 8-bit-byte characters.<li>l for 16-bit little-endian.<li>b for 16-bit big-endian.<li>L for 32-bit little-endian.<li>B for 32-bit big-endian.<li>u for 1 to 4 bytes UTF-8 characters.</ul><br>The default is to assume that characters are encoded using a single 7-bit byte
-f\|--print-file-name|Print the name of the file before each string
-h\|--help\|-?|Print a usage summary and exit
-L\|--length NUM|Read NUM bytes from offset
-m\|-n\|--bytes NUM \| -NUM|Print the contiguous character sequence of at least NUM characters long, instead of the default of 4 characters. Argument NUM should specify a positive decimal integer
-o|Equivalent to specifying *-t o*
-O\|--offset NUM|Skip NUM bytes from beginning of file
-s\|--output-separator STRING|By default, output strings are delimited by a new-line. This option allows you to supply any string separator to be used as the output record separator. Useful with *--include-all-whitespace* where strings may contain new-lines internally
-S\|--split-lines|Split long lines in chunks of 70 characters
-t\|--radix CHAR|Print the offset from the start of the file before each string using the specified radix. Valid values are:<br><ul><li>d for decimal<li>o for octal<li>x for hexadecimal</ul>
-v\|-V\|--version|Display a version identifier and exit
-w\|-include-all-whitespace|By default tab and space characters are included in the strings that are displayed, but other whitespace characters, such a new-lines and carriage returns, are not. The *-w* option changes this so that all whitespace characters are considered to be part of a string
@file|Read command-line options from *file*. The options read are inserted in place of the original *@file* option. If *file* does not exist, or cannot be read, then the option will be treated literally, and not removed.<br>Options in *file* are separated by whitespace. A whitespace character may be included in an option by surrounding the entire option in either single or double quotes. Any character (including a backslash) may be included by prefixing the character to be included with a backslash. The file may itself contain additional *@file* options; any such options will be processed recursively
--debug|Enable debug mode
--|Options processing terminator

## ENVIRONMENT
The *STRINGS_DEBUG* environment variable can be set to any value to enable debug mode.

The *FLAVOUR* or *STRINGS_FLAVOUR* environment variables can be set to one of the following values, to implement only the corresponding options and behaviours:
* posix : POSIX [strings](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/strings.html)
* unix | unix:v10 : Unix v10 [strings(1)](http://man.cat-v.org/unix_10th/1/strings)
* bsd | bsd:freebsd : FreeBSD [strings(1)](https://www.freebsd.org/cgi/man.cgi?query=strings)
* gnu | gnu:linux | linux : GNU/Linux [strings(1)](https://man7.org/linux/man-pages/man1/strings.1.html)
* plan9 : Plan 9 [strings(1)](http://man.cat-v.org/plan_9/1/strings)
* inferno : Inferno [strings(1)](http://man.cat-v.org/inferno/1/strings)

However, if the *POSIXLY_CORRECT* environment variable is set to any value, then the POSIX flavour will be selected.

## EXIT STATUS
The **strings** utility exits 0 on success, and >0 if an error occurs.

## EXAMPLES
To display strings in all sections of /bin/ln use:<br>
```$ strings -a /bin/ln```

To display strings in all sections of /bin/cat prefixed with the filename and the offset within the file use:<br>
```$ strings -a -f -t x /bin/cat```

To analyze a Windows malware, looking for embedded VB or JScripts (with CR+LF delimited Unicode strings) use:<br>
```$ strings -D 13 -e u /quarantine/malware.exe```

## SEE ALSO
[ar(1)](https://www.freebsd.org/cgi/man.cgi?query=ar),
[nm(1)](https://www.freebsd.org/cgi/man.cgi?query=nm),
[objdump(1)](https://www.freebsd.org/cgi/man.cgi?query=objdump),
[ranlib(1)](https://www.freebsd.org/cgi/man.cgi?query=ranlib),
[readelf(1)](https://www.freebsd.org/cgi/man.cgi?query=readelf),
[size(1)](https://www.freebsd.org/cgi/man.cgi?query=size),
[strings(3)](https://github.com/HubTou/strings/blob/main/STRINGS.1.md)

## STANDARDS
The **strings** utility is a standard UNIX/POSIX command.

This re-implementation tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

Beyond [Plan 9](https://en.wikipedia.org/wiki/Plan_9_from_Bell_Labs) and [Inferno](https://en.wikipedia.org/wiki/Inferno_(operating_system)), [UTF](https://en.wikipedia.org/wiki/UTF-8)-encoded characters are supported in all (but POSIX and Unix v10) flavours with the *-e|--encoding u* options.

It also adds some non standard options:
* *-D|--delimiters* which can be used to mimic Posix / Unix v10 behaviour with a "0:10" parameter, and help reduce the garbage
* *-S|--split-lines* to mimic Plan 9 / Inferno behaviour
* *-O|--offset* and *-L|--length* to mimic Mark Russinovich's [Windows implementation](https://docs.microsoft.com/en-us/sysinternals/downloads/strings) -o/-b options.

## PORTABILITY
Tested OK under Windows.

## HISTORY
The first strings utility was written by [Bill Joy](https://en.wikipedia.org/wiki/Bill_Joy) on [April 22, 1978](https://minnie.tuhs.org/cgi-bin/utree.pl?file=2BSD/src/strings.c), and appeared in [2BSD](https://en.wikipedia.org/wiki/History_of_the_Berkeley_Software_Distribution#2BSD_(PDP-11)).

This re-implementation was made for the [PNU project](https://github.com/HubTou/PNU).

## LICENSE
It is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

This manual page is based on the one written for [FreeBSD](https://www.freebsd.org/) by S.Sam Arun Raj <samarunraj@gmail.com>.

## CAVEATS
This re-implementation does not support any executable format ([ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format), [a.out](https://en.wikipedia.org/wiki/A.out), [COFF](https://en.wikipedia.org/wiki/COFF), etc.).
All executable files are entirely scanned, regardless of *-a* | *--all* | *-* | *--data* | *-d* | *-t* | *-s* | *-T* | *--target* options.

