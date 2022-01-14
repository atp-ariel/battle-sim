from typing import List
from .tokens import *
from numpy import array, append


class Lexer:
    def __init__(self):
        self.__digits__ = '0123456789'

    def is_digit(self, c: str):
        return self.__digits__.find(c) > -1

    def __call__(self, re: str) -> List[Token]:
        tokens = array([])

        def add(item):
            nonlocal tokens

            tokens = append(tokens, item) 

        i = 0
        escape_found = False
        while i < len(re):
            c = re[i]
            if escape_found:
                if c == 't':
                    add(ElementToken("\t"))
                elif c == 's':
                    add(SpaceToken(c))
                else:
                    add(ElementToken(c))

            token = Token.get_token_class(c)()  

            if isinstance(token, Escape):
                escape_found = True
                i += 1
                continue

            add(token)
            
            if isinstance(token, LeftCurlyBrace):
                i += 1
                while i < len(re):
                    if c == ',':
                        append(Comma())
                    elif self.__is_digit__(c):
                        append(ElementToken(c))
                    elif c == '}':
                        append(RightCurlyBrace())
                        break
                    else:
                        raise Exception('Bad token at index ${}.'.format(i))
                    i += 1
            
            escape_found = False
            i += 1
            
        return list(tokens)