# STRINGS(3)

## NAME
strings - return the strings of printable characters in files

## SYNOPSIS
**import strings**

*List*
strings.**strings**(String *filename*, char *encoding*, Int *minimum_length*, Boolean *include_backspaces*, Boolean *include_whitespaces*, String *string_termination*, Boolean *scan_entire_file*, String *target*, Integer *file_offset*, Integer *file_length*)

## DESCRIPTION
The **strings** function returns a list of (offset, printable strings) tuples contained in the *filename* file or the standard input stream if empty.

All the other parameters also have default values and thus are optional.

The *encoding* parameter sets the character encoding to be used while searching for strings.
Valid values are:
* *s* for single 7-bit-byte characters (ASCII, ISO 8859). The default value.
* *S* for single 8-bit-byte characters.
* *l* for 16-bit little-endian.
* *b* for 16-bit big-endian.
* *L* for 32-bit little-endian.
* *B* for 32-bit big-endian.
* *u* for 1 to 4 bytes UTF-8 characters.

The *minimum_length* parameter defines the minimum number of contiguous characters in strings.
The default value is 4.

If True, the *include_backspaces* parameter allows backspace characters in strings.
The default value is False.

If True, the *include_whitespaces* parameter allows backspace, new line, vertical tab, form feed and carriage return characters in strings.
The default value is False.

The *string_termination* parameter expects a comma separated string of the integer values of allowed string ending characters.
The default value is a blank string, which means any unprintable character.
It is common to use "0:10" to allow only null or new line characters, which is often relevant for binary and text files respectively.

If True, the *scan_entire_file* parameter sets a full file scan.
The default value is False, though without any executable file formats supported (yet) it also falls back to a full scan.

The *target* parameter allows the selection of a specific executable file format (potentially different from the system's default), though none are currently supported.
It must be set to "part" if you want to use the *file_offset* or *file_length* parameters.
The default value is a blank string.

The *file_offset* parameter defines the number of bytes to skip from the beginning of the file to scan.
The default value is 0.

The *file_length* parameter defines the number of bytes to read from the *file_offset* of the file to scan.
The default value is all.

## ENVIRONMENT
The *STRINGS_DEBUG* environment variable can be set to any value to enable debug mode.

## SEE ALSO
[ident(1)](https://github.com/HubTou/what/blob/main/IDENT.1.md),
[strings(1)](https://github.com/HubTou/strings/blob/main/STRINGS.1.md),
[what(1)](https://github.com/HubTou/what/blob/main/WHAT.1.md)

## STANDARDS
The **strings** library tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## HISTORY
This library was made for the [PNU project](https://github.com/HubTou/PNU).

## LICENSE
It is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

## CAVEATS
This library does not (yet) support any executable format ([ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format), [a.out](https://en.wikipedia.org/wiki/A.out), [COFF](https://en.wikipedia.org/wiki/COFF), etc.).
All executable files are entirely scanned regardless of the *target* parameter, with the exception of the "part" value.

