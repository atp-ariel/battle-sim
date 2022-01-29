from .token import Token
from typing import List
from .lexer import Lexer
from .parser import Parser
from .nfa import NFA, Handler, Match

class Regex:
    def __init__(self, pattern: str):
        self.pattern : str = pattern
        self.nfa : NFA = self.compile()

    def compile(self) -> NFA:
        lex: Lexer = Lexer(self.pattern)
        parser : Parser = Parser(lex)
        tokens : List[Token] = parser()
        handler: Handler = Handler()
        
        nfa_stack : List[NFA]= []
        
        for t in tokens:
            handler.handlers[t.name](t, nfa_stack)
        
        if len(nfa_stack) == 1:
            return nfa_stack.pop() 
        raise Exception("Bad regex!")

    def match(self, string: str) -> bool:
        return self.nfa.match(string)

    def find_all(self, string: str) -> List[Match]:
        return self.nfa.find_all(string)

def compile(regex: str) -> Regex:
    return Regex(regex)

def match(regex: str, word: str) -> bool:
    re = Regex(regex)
    return re.match(word)

def find_all(regex: str, word: str) -> List[Match]:
    re = Regex(regex)
    return re.find_all(word)