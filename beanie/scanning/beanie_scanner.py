from typing import TextIO, List
import os

from ..utils.beanie_logging import BeanieFileNotFound, BeanieSyntaxError
from .beanie_token import Token, TokenType


class Scanner:
    def __init__(self, input_fn: str):
        """A class for scanning in Tokens

        Args:
            input_fn (str): Filename of the input program file
        """
        self.filename: str = input_fn
        self.file: TextIO

        self.put_back_buffer: str = ""

        self.line_number: int = 1

        self.current_token: Token

        self.initialized: bool = False

    # def __enter__(self: Scanner): -> Scanner:
    def __enter__(self):
        """Opens the program file for scanning

        Raises:
            BeanieFileNotFound: If the program file does not exist
        """
        if os.path.exists(self.filename):
            self.file = open(self.filename, "r")
        else:
            raise BeanieFileNotFound(self.filename)

        self.initialized = True

        return self

    def __exit__(self, _, __, ___):
        """Closes the program file"""
        self.file.close()

    def open(self):
        self.__enter__()

    def close(self):
        self.__exit__(None, None, None)

    def next_character(self) -> str:
        """Get the next character from the input stream

        Returns:
            str: The next character from the input stream
        """
        c: str = ""

        # If we have a character in the putback buffer,
        # we want to read that first, then empty the
        # buffer
        if self.put_back_buffer:
            c = self.put_back_buffer
            self.put_back_buffer = ""
            return c

        # Otherwise, we read a single character from
        # the open input file, and conditionally
        # increment our rudimentary line counter
        c = self.file.read(1)
        if c == "\n":
            self.line_number += 1

        return c

    def skip(self) -> str:
        """Gets the next non-whitespace character from the input stream

        Returns:
            str: The next non-whitespace character from the input stream
        """
        c: str = self.next_character()
        while c.isspace():
            c = self.next_character()
        return c

    def put_back(self, c: str) -> None:
        """Put a character back into the input stream

        Args:
            c (str): Character to put back into the input stream
        """
        
        if len(c) > 1:

            raise TypeError(
                f"put_back() expected a character, but string of length {len(c)} found"
            )

        self.put_back_buffer = c

    def scan_integer_literal(self, c: str) -> int:
        """Scan integer literals into a buffer and parse them into int objects

        Args:
            c (str): Current character from input stream

        Returns:
            int: Scanned integer literal
        """
        in_string: str = ""

        while c.isdigit():
            in_string += c
            c = self.next_character()

        self.put_back(c)

        return int(in_string)

    def scan(self) -> Token:
        """Scan the next token

        Args:
            current_token (Token): Global Token object to scan data into

        Raises:
            BeanieSyntaxError: If an unrecognized Token is reached

        Returns:
            bool: True if a Token was read, False if EOF was reached
        """
        c: str = self.skip()
        self.current_token = Token()
        # Check  for EOF
        if c == "":
            self.current_token.type = TokenType.EOF
            return self.current_token

        possible_token_types: List[TokenType] = []
        for token_type in TokenType:
            if str(token_type)[0] == c:
                possible_token_types.append(token_type)

        if not len(possible_token_types):
            if c.isdigit():
                self.current_token.type = TokenType.INTEGER_LITERAL
                self.current_token.value = self.scan_integer_literal(c)
            else:
                raise BeanieSyntaxError(f'Uncrecognized token "{c}"')
        else:
            if len(c) == 1:
                self.current_token.type = possible_token_types[0]
                return self.current_token
            else:
                pass

        return self.current_token

    def scan_file(self) -> None:
        """Scans a file and prints out its Tokens"""

        while self.scan().type != TokenType.EOF:
            print(self.current_token)
