#!/usr/bin/env python
""" strings - print the strings of printable characters in files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import shlex
import struct
import signal
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: strings - print the strings of printable characters in files v1.1.2 (November 1, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    # File parameters:
    "Encoding": "s", # between "s", "S", "l", "b", "L", "B", "u"
    "Scan entire file": False,
    "Target": "", # "ELF", "a.out", "COFF", etc.
    "Offset": 0,
    "Length": sys.maxsize,

    # String parameters:
    "Include backspaces": False,
    "Include whitespaces": False,
    "String termination": [], # empty list = all unprintable characters
    "Minimum length": 4,

    # Display parameters:
    "Print filename": False,
    "Print offset": "", # blank, "octal", "decimal", "hexadecimal"
    "Split long lines": 1000000000, # a very long line...
    "Output separator": "",

    "Command flavour": "PNU",
}


################################################################################
def _initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def _display_help():
    """Displays usage and help"""
    if parameters["Command flavour"] == "posix":
        print("usage: strings [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-a] [-n NUM] [-t CHAR]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  -------------------------------------------",
            file=sys.stderr
        )
        print("  -a         Scan the entire file for strings", file=sys.stderr)
        print(
            "  -n NUM     Print sequences with NUM or more characters",
            file=sys.stderr
        )
        print(
            "  -t CHAR    Print offsets using the radix named by CHAR",
            file=sys.stderr
        )
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print a help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    elif parameters["Command flavour"] in ("unix", "unix:v10"):
        print("usage: strings [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-a] [-d] [-o] [-s] [-t]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  -------------------------------------------------------------",
            file=sys.stderr
        )
        print("  -a         Look for strings throughout the file", file=sys.stderr)
        print(
            "  -d         Look for strings in the data segment of an object file",
            file=sys.stderr
        )
        print("  -o         Print offsets in octal", file=sys.stderr)
        print(
            "  -s         Look for symbol strings in the symbol table"
            + " of an object file",
            file=sys.stderr
        )
        print(
            "  -t         Look for strings in the text segment of an object file",
            file=sys.stderr
            )
        print(
            "  -number    Ignore strings less than number characters long",
            file=sys.stderr
        )
        print(
            "             (excluding new lines). Default length is 4",
            file=sys.stderr
        )
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print a help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    elif parameters["Command flavour"] in ("bsd", "bsd:freebsd"):
        print("usage: strings [--debug] [-h|--help|-?] [-v|-V|--version]", file=sys.stderr)
        print("       [-a|--all] [-e|--encoding CHAR] [-f|--print-file-name]", file=sys.stderr)
        print("       [-n|--bytes NUM | -NUM] [-o] [-t|--radix CHAR]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ---------------------  -------------------------------------------",
            file=sys.stderr
        )
        print("  -a|--all               Scan the entire file for strings", file=sys.stderr)
        print("  -e|--encoding CHAR     Select the character encoding to use", file=sys.stderr)
        print("  -f|--print-file-name   Print the file name before each string", file=sys.stderr)
        print(
            "  -n|--bytes NUM | -NUM  Print sequences with NUM or more characters",
            file=sys.stderr
        )
        print("  -o                     Print offsets in octal", file=sys.stderr)
        print(
            "  -t|--radix CHAR        Print offsets using the radix named by 'R'",
            file=sys.stderr
        )
        print("  --debug                Enable debug mode", file=sys.stderr)
        print("  -h|--help|-?           Print a help message and exit", file=sys.stderr)
        print("  -v|-V|--version        Print version and exit", file=sys.stderr)
        print("  --                     Options processing terminator", file=sys.stderr)
    elif parameters["Command flavour"] in ("gnu", "gnu:linux", "linux"):
        print("usage: strings [--debug] [-h|--help|-?] [-v|-V|--version]", file=sys.stderr)
        print("       [-a|--all] [-d|--data] [-e|--encoding CHAR]", file=sys.stderr)
        print("       [-f|--print-file-name] [-n|--bytes NUM | -NUM] [-o]", file=sys.stderr)
        print("       [-s|--output-separator STRING] [-t|--radix CHAR]", file=sys.stderr)
        print("       [-T|--target STRING] [-w|--include-all-whitespace]", file=sys.stderr)
        print("       [@file] [--] [file ...]", file=sys.stderr)
        print(
            "  ----------------------------  ---------------------------------------------------------",
            file=sys.stderr
        )
        print("  -a|--all                      Scan the entire file for strings", file=sys.stderr)
        print(
            "  -d|--data                     Only print strings from initialized, loaded data sections",
            file=sys.stderr
        )
        print(
            "  -e|--encoding CHAR            Select the character encoding to use",
            file=sys.stderr
        )
        print(
            "  -f|--print-file-name          Print the file name before each string",
            file=sys.stderr
        )
        print(
            "  -n|--bytes NUM | -NUM         Print sequences with NUM or more characters",
            file=sys.stderr
        )
        print("  -o                            Print offsets in octal", file=sys.stderr)
        print(
            "  -s|--output-separator STRING  Use STRING as the output record separator",
            file=sys.stderr
        )
        print(
            "  -t|--radix CHAR               Print offsets using the radix named by CHAR",
            file=sys.stderr
        )
        print(
            "  -T|--target STRING            Specify an object code format other than",
            file=sys.stderr
        )
        print("                                your system's default format", file=sys.stderr)
        print(
            "  -w|--include-all-whitespace   All whitespace characters are considered",
            file=sys.stderr
        )
        print("                                to be part of a string", file=sys.stderr)
        print("  @file                         Insert command-line options from file", file=sys.stderr)
        print("  --debug                       Enable debug mode", file=sys.stderr)
        print("  -h|--help|-?                  Print a help message and exit", file=sys.stderr)
        print("  -v|-V|--version               Print version and exit", file=sys.stderr)
        print("  --                            Options processing terminator", file=sys.stderr)
    elif parameters["Command flavour"] == "plan9":
        print("usage: strings [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-m NUM]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  -------------------------------------------",
            file=sys.stderr
        )
        print(
            "  -m NUM     Print sequences with NUM or more characters",
            file=sys.stderr
        )
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print a help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    elif parameters["Command flavour"] == "inferno":
        print("usage: strings [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  -----------------------------",
            file=sys.stderr
        )
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print a help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    else: # PNU
        print("usage: strings [--debug] [-h|--help|-?] [-v|-V|--version]", file=sys.stderr)
        print("       [-a|--all] [-D|--delimiters LIST][-e|--encoding CHAR]", file=sys.stderr)
        print("       [-f|--print-file-name] [-L|--length NUM]", file=sys.stderr)
        print("       [-m NUM|-n NUM|--bytes NUM|-NUM] [-o] [-O|--offset NUM]", file=sys.stderr)
        print("       [-s|--output-separator STRING] [-S|--split-lines]", file=sys.stderr)
        print("       [-t|--radix CHAR] [-w|--include-all-whitespace] [@file]", file=sys.stderr)
        print("       [--] [file ...]", file=sys.stderr)
        print(
            "  ----------------------------  ----------------------------------------------",
            file=sys.stderr
        )
        print("  -a|--all                      Scan the entire file for strings", file=sys.stderr)
        print(
            "  -D|--delimiters LIST          Use the ':' separated list of character values",
            file=sys.stderr
        )
        print("                                as delimiters", file=sys.stderr)
        print("  -e|--encoding CHAR            Select the character encoding to use", file=sys.stderr)
        print("  -f|--print-file-name          Print the file name before each string", file=sys.stderr)
        print("  -L|--length NUM               Read NUM bytes from offset", file=sys.stderr)
        print(
            "  -m|-n|--bytes NUM | -NUM      Print sequences with NUM or more characters",
            file=sys.stderr
        )
        print("  -o                            Print offsets in octal", file=sys.stderr)
        print("  -O|--offset NUM               Skip NUM bytes from beginning of file", file=sys.stderr)
        print(
            "  -s|--output-separator STRING  Use STRING as the output record separator",
            file=sys.stderr
        )
        print(
            "  -S|--split-lines              Split long lines in chunks of 70 characters",
            file=sys.stderr
        )
        print(
            "  -t|--radix CHAR               Print offsets using the radix named by CHAR",
            file=sys.stderr
        )
        print(
            "  -w|--include-all-whitespace   All whitespace characters are considered",
            file=sys.stderr
        )
        print("                                to be part of a string", file=sys.stderr)
        print("  @file                         Insert command-line options from file", file=sys.stderr)
        print("  --debug                       Enable debug mode", file=sys.stderr)
        print("  -h|--help|-?                  Print a help message and exit", file=sys.stderr)
        print("  -v|-V|--version               Print version and exit", file=sys.stderr)
        print("  --                            Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def _handle_interrupts(signal_number, current_stack_frame):
    """Prevent SIGINT signals from displaying an ugly stack trace"""
    print(" Interrupted!\n", file=sys.stderr)
    _display_help()
    sys.exit(0)


################################################################################
def _handle_signals():
    """Process signals"""
    signal.signal(signal.SIGINT, _handle_interrupts)


################################################################################
def _process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    if "STRINGS_DEBUG" in os.environ:
        logging.disable(logging.NOTSET)

    if "FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["FLAVOUR"].lower()
    if "STRINGS_FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["STRINGS_FLAVOUR"].lower()

    # From "man environ":
    # POSIXLY_CORRECT
    # When set to any value, this environment variable
    # modifies the behaviour of certain commands to (mostly)
    # execute in a strictly POSIX-compliant manner.
    if "POSIXLY_CORRECT" in os.environ:
        parameters["Command flavour"] = "posix"

    # Command variants supported:
    if parameters["Command flavour"] == "posix":
        parameters["String termination"] = [0, ord('\n')]
    elif parameters["Command flavour"] in ("unix", "unix:v10"):
        parameters["Include backspaces"] = True
        parameters["String termination"] = [0, ord('\n')]
    elif parameters["Command flavour"] in ("plan9", "inferno"):
        parameters["Minimum length"] = 6
        parameters["Print offset"] = "decimal"
        parameters["Encoding"] = "u"
        parameters["Split long lines"] = 70
    elif parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd", "gnu", "gnu:linux", "linux"):
        pass
    else:
        logging.critical("Unimplemented command FLAVOUR: %s", parameters["Command flavour"])
        sys.exit(1)

    logging.debug("_process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def insert_file(part):
    """Return a command line argument with recursively expanded @file options"""
    new_parts = []
    filename = part[1:]
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            for new_part in shlex.split(file.readline()):
                if new_part.startswith('@'):
                    new_parts += insert_file(new_part)
                else:
                    new_parts.append(new_part)
    else:
        new_parts.append(part)

    return new_parts


################################################################################
def _read_option_files(command_line):
    """Return a command line with expanded @file options"""
    new_argv = []
    for part in command_line:
        if part.startswith('@'):
            new_argv += insert_file(part)
        else:
            new_argv.append(part)

    return new_argv


################################################################################
def _process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # @file option handling:
    if parameters["Command flavour"] in ("PNU", "gnu", "gnu:linux", "linux"):
        sys.argv = _read_option_files(sys.argv)

    # Option letters followed by : expect an argument
    # same for option strings followed by =
    if parameters["Command flavour"] == "posix":
        character_options = "an:t:?"
        string_options = [
            "debug",
            "help",
            "version",
        ]
    elif parameters["Command flavour"] in ("unix", "unix:v10"):
        character_options = "1234567890adost?"
        string_options = [
            "debug",
            "help",
            "version",
        ]
    elif parameters["Command flavour"] in ("bsd", "bsd:freebsd"):
        character_options = "1234567890ae:fhn:ot:vV?"
        string_options = [
            "all",
            "bytes=",
            "debug",
            "encoding=",
            "help",
            "print-file-name",
            "radix=",
            "version",
        ]
    elif parameters["Command flavour"] in ("gnu", "gnu:linux", "linux"):
        character_options = "1234567890ade:fhn:os:t:T:vVw?"
        string_options = [
            "all",
            "bytes=",
            "data",
            "debug",
            "encoding=",
            "help",
            "include-all-whitespace",
            "output-separator=",
            "print-file-name",
            "radix=",
            "target=",
            "version",
        ]
    elif parameters["Command flavour"] == "plan9":
        character_options = "m:?"
        string_options = [
            "debug",
            "help",
            "version",
        ]
    elif parameters["Command flavour"] == "inferno":
        character_options = "?"
        string_options = [
            "debug",
            "help",
            "version",
        ]
    else: # PNU
        character_options = "1234567890aD:e:fhL:m:n:oO:s:St:vVw?"
        string_options = [
            "all",
            "bytes=",
            "debug",
            "delimiters=",
            "encoding=",
            "help",
            "include-all-whitespace",
            "length=",
            "offset=",
            "output-separator=",
            "print-file-name",
            "radix=",
            "split-lines",
            "version",
        ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    numeric_option_encountered = False
    for option, argument in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("-a", "--all"):
            parameters["Scan entire file"] = True

        elif option in ("-d", "--data"):
            if parameters["Command flavour"] in ("unix", "unix:v10"):
                logging.critical(
                    "Looking for strings in the data segment of an a.out object file is not implemented"
                )
            elif parameters["Command flavour"] in ("gnu", "gnu:linux", "linux"):
                logging.critical(
                    "Looking for strings in the initialized & loaded data sections of a file is not implemented"
                )
            sys.exit(1)

        elif option in ("-D", "--delimiters"):
            for delimiter in argument.split(":"):
                try:
                    parameters["String termination"].append(int(delimiter))
                except ValueError:
                    logging.critical("Invalid -D argument: list items must be integers")
                    sys.exit(1)

        elif option in ("-e", "--encoding"):
            if argument in ("s", "S", "l", "b", "L", "B", "u"):
                parameters["Encoding"] = argument
            else:
                logging.critical("Invalid -e argument: must be one of {s, S, l, b, L, B, u}")
                sys.exit(1)

        elif option in ("-f", "--print-file-name"):
            parameters["Print filename"] = True

        elif option in ("-h", "--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option in ("-L", "--length"):
            parameters["Scan entire file"] = False
            parameters["Target"] = "part"
            try:
                parameters["Length"] = int(argument)
            except ValueError:
                logging.critical("Invalid -L argument: must be an integer")
                sys.exit(1)
            if parameters["Minimum length"] < 1:
                logging.critical("Invalid -L argument: must be a positive integer")
                sys.exit(1)

        elif option in ("-m", "-n", "--bytes"):
            try:
                parameters["Minimum length"] = int(argument)
            except ValueError:
                logging.critical("Invalid -n argument: must be an integer")
                sys.exit(1)
            if parameters["Minimum length"] < 1:
                logging.critical("Invalid -n argument: must be a positive integer")
                sys.exit(1)

        elif option == "-o":
            parameters["Print offset"] = "octal"

        elif option in ("-O", "--offset"):
            parameters["Scan entire file"] = False
            parameters["Target"] = "part"
            try:
                parameters["Offset"] = int(argument)
            except ValueError:
                logging.critical("Invalid -O argument: must be an integer")
                sys.exit(1)
            if parameters["Minimum length"] < 1:
                logging.critical("Invalid -O argument: must be a positive integer")
                sys.exit(1)

        elif option in ("-s", "--output-separator"):
            if parameters["Command flavour"] in ("unix", "unix:v10"):
                logging.critical(
                    "Looking for symbol strings in the symbol table of an a.out object file is not implemented"
                )
                sys.exit(1)
            else:
                parameters["Output separator"] = argument

        elif option in ("-S", "--split-lines"):
            parameters["Split long lines"] = 70

        elif option in ("-t", "--radix"):
            if parameters["Command flavour"] in ("unix", "unix:v10"):
                logging.critical(
                    "Looking for strings in the text segment of an a.out object file is not implemented"
                )
                sys.exit(1)

            if argument.lower() == "d":
                parameters["Print offset"] = "decimal"
            elif argument.lower() == "o":
                parameters["Print offset"] = "octal"
            elif argument.lower() == "x":
                parameters["Print offset"] = "hexadecimal"
            else:
                logging.critical("Invalid -t argument: must be (d)ecimal, (o)ctal or he(x)adecimal")
                sys.exit(1)

        elif option in ("-T", "--target"):
            # a.out, COFF, ELF
            logging.critical("Specifying an object code format is not implemented")
            sys.exit(1)

        elif option in ("-v", "-V", "--version"):
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option in ("-w", "--include-all-whitespace"):
            parameters["Include whitespaces"] = True

        elif option in ("-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-0"):
            if numeric_option_encountered:
                parameters["Minimum length"] *= 10
                parameters["Minimum length"] += int(option[1])
            else:
                numeric_option_encountered = True
                parameters["Minimum length"] = int(option[1])

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def _is_character_printable(value, encoding, include_backspaces, include_whitespaces):
    """Return true if chr(value) is a printable character according to strings"""
    if value >= 0:
        if value <= 127:
            if chr(value).isprintable() \
            or value == ord("\t") \
            or (include_backspaces and value == ord("\b")) \
            or (include_whitespaces and chr(value) in ('\n', '\v', '\f', '\r', '\b')):
                return True
        elif encoding == "S" and value <= 255 and chr(value).isprintable():
            return True
        elif encoding in ("l", "b", "L", "B", "u") and chr(value).isprintable():
            return True

    return False


################################################################################
def _strings(
    filename,
    encoding,
    minimum_length,
    include_backspaces,
    include_whitespaces,
    string_termination,
    file_offset,
    file_length
):
    """Return a list of strings of printable characters in a file, file segment or input stream"""
    bytes_to_read = 1
    unpack_string = "B"
    if encoding == "l":
        bytes_to_read = 2
        unpack_string = "<H"
    elif encoding == "b":
        bytes_to_read = 2
        unpack_string = ">H"
    elif encoding == "L":
        bytes_to_read = 4
        unpack_string = "<L"
    elif encoding == "B":
        bytes_to_read = 4
        unpack_string = ">L"

    printable_string = ""
    results = []

    if filename:
        try:
            file = open(filename, "rb")
        except:
            return results
    else:
        file = sys.stdin.buffer

    offset = file_offset
    if file_offset != 0:
        file.seek(offset, 1)
    total_extra_bytes = 0
    bytes_buffer = b""
    bytes_read = file.read(bytes_to_read)
    while bytes_read:
        value = struct.unpack(unpack_string, bytes_read)[0]
        extra_bytes = 0
        if encoding == "u":
            if value >= 192 and value <= 223: # 110xxxxx => 2 bytes UTF-8 character
                extra_bytes = 1
            elif value >= 224 and value <= 239: # 1110xxxx => 3 bytes UTF-8 character
                extra_bytes = 2
            elif value >= 240 and value <= 247: # 11110xxx => 4 bytes UTF-8 character
                extra_bytes = 3
            if extra_bytes:
                if bytes_buffer:
                    if extra_bytes <= len(bytes_buffer):
                        bytes = bytes_read + bytes_buffer[:extra_bytes]
                        bytes_buffer = bytes_buffer[extra_bytes:]
                    else:
                        bytes = bytes_read + bytes_buffer + file.read(extra_bytes - len(bytes_buffer))
                        bytes_buffer = b""
                else:
                    bytes = bytes_read + file.read(extra_bytes)
                try:
                    value = ord(bytes.decode("utf-8", "ignore"))
                except TypeError:
                    # The bytes read were not part of an UTF-8 character!
                    if filename:
                        file.seek(- extra_bytes, 1)
                    else:
                        # We can't seek back in a stream
                        # Let's do this painful buffer handling stuff instead...
                        bytes_buffer = bytes[1:]
                    extra_bytes = 0

        if _is_character_printable(value, encoding, include_backspaces, include_whitespaces):
            printable_string += chr(value)
            total_extra_bytes += extra_bytes
        else:
            length = len(printable_string)
            if length >= minimum_length:
                if len(string_termination) == 0 \
                or value in string_termination:
                    logging.debug(
                        "Offset=%d  String=%s  Delimiter=%d",
                        offset - length - total_extra_bytes,
                        printable_string,
                        value
                    )
                    results.append([offset - length - total_extra_bytes, printable_string])
            printable_string = ""
            total_extra_bytes = 0

        offset += bytes_to_read + extra_bytes
        if offset >= file_offset + file_length:
            bytes_read = b""
        elif bytes_buffer:
            bytes_read = bytes_buffer[:1]
            bytes_buffer = bytes_buffer[1:]
        else:
            bytes_read = file.read(bytes_to_read)

    file.close()

    return results


################################################################################
def strings(
    filename="",
    encoding=None,
    minimum_length=None,
    include_backspaces=None,
    include_whitespaces=None,
    string_termination=None,
    scan_entire_file=None,
    target=None,
    file_offset=None,
    file_length=None
):
    """Return a list of strings of printable characters in a file, file segment or input stream"""
    if encoding == None:
        encoding = parameters["Encoding"]
    if minimum_length == None:
        minimum_length = parameters["Minimum length"]
    if include_backspaces == None:
        include_backspaces = parameters["Include backspaces"]
    if include_whitespaces == None:
        include_whitespaces = parameters["Include whitespaces"]
    if string_termination == None:
        string_termination = parameters["String termination"]
    if scan_entire_file == None:
        scan_entire_file = parameters["Scan entire file"]
    if target == None:
        target = parameters["Target"]
    if file_offset == None:
        file_offset = parameters["Offset"]
    if file_length == None:
        file_length = parameters["Length"]

    segments = []
    if not filename or scan_entire_file:
        segments.append([0, sys.maxsize])
    else:
        if not target:
            # TODO Identify file type and set target
            pass

        if target == "part":
            segments.append([file_offset, file_length])
        elif target == "ELF":
            # TODO Process relevant segments of executable
            pass
        elif target == "a.out":
            # TODO Process relevant segments of executable
            pass
        else: # unidentified: scan entire file
            segments.append([0, sys.maxsize])

    all_results = []
    for offset, length in segments:
        all_results += _strings(
            filename,
            encoding,
            minimum_length,
            include_backspaces,
            include_whitespaces,
            string_termination,
            offset,
            length
        )
    return all_results


################################################################################
def _print_string(filename, offset, printable_string):
    """Print the string, eventually splitting long lines"""
    maximum_length = parameters["Split long lines"]
    while len(printable_string):
        if parameters["Print filename"]:
            print("{}: ".format(filename), end="")
        if parameters["Print offset"] == 'decimal':
            print("{:>7d} ".format(offset), end="")
        elif parameters["Print offset"] == 'octal':
            print("{:>7o} ".format(offset), end="")
        elif parameters["Print offset"] == 'hexadecimal':
            print("{:>7x} ".format(offset), end="")
        print(printable_string[:maximum_length], end="")
        if len(printable_string) > maximum_length:
            print("...", end="")
        if parameters["Output separator"]:
            print("\n" + parameters["Output separator"])
        else:
            print()

        printable_string = printable_string[maximum_length:]
        offset += maximum_length


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    _initialize_debugging(program_name)
    _handle_signals()
    _process_environment_variables()
    arguments = _process_command_line()

    exit_status = 0
    if arguments:
        for filename in arguments:
            if os.path.isfile(filename):
                for offset, printable_string in strings(filename):
                    _print_string(filename, offset, printable_string)
            elif filename == "-" \
            and parameters["Command flavour"] in ("posix", "gnu", "gnu:linux", "linux"):
                parameters["Scan entire file"] = True
            else:
                logging.error('"%s" is not a file name', filename)
                exit_status = 1
    else:
        for offset, printable_string in strings():
            _print_string("{standard input}", offset, printable_string)

    sys.exit(exit_status)


if __name__ == "__main__":
    main()
