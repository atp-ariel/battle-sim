from typing import  Iterable, List, Tuple
from .token import Token, TokenType, TokenDefinition
from ..regex import Match
from queue import deque


TOKENS: List[TokenDefinition] = [
    TokenDefinition(TokenType.EOF, 1),
    TokenDefinition(TokenType.Comma, 1),
    TokenDefinition(TokenType.Number, 1),
    TokenDefinition(TokenType.Name, 2),
    TokenDefinition(TokenType.Arrow, 1),
    TokenDefinition(TokenType.Semicolon, 1),
    TokenDefinition(TokenType.Break, 1),
    TokenDefinition(TokenType.Continue, 1),
    TokenDefinition(TokenType.Def_Func, 1),
    TokenDefinition(TokenType.LeftParent, 1),
    TokenDefinition(TokenType.RightParent, 1),
    TokenDefinition(TokenType.If, 1),
    TokenDefinition(TokenType.Elif, 1),
    TokenDefinition(TokenType.Else, 1),
    TokenDefinition(TokenType.Class, 1),
    TokenDefinition(TokenType.Is, 1),
    TokenDefinition(TokenType.TNumber, 1),
    TokenDefinition(TokenType.Assign, 1),
    TokenDefinition(TokenType.Return, 1),
    TokenDefinition(TokenType.LeftCurly, 1),
    TokenDefinition(TokenType.RightCurly, 1),
    TokenDefinition(TokenType.Or, 1),
    TokenDefinition(TokenType.And, 1),
    TokenDefinition(TokenType.Not, 1),
    TokenDefinition(TokenType.Equal, 1),
    TokenDefinition(TokenType.Neq, 1),
    TokenDefinition(TokenType.Lte, 1),
    TokenDefinition(TokenType.Lt, 1),
    TokenDefinition(TokenType.Gte, 1),
    TokenDefinition(TokenType.Gt, 1),
    TokenDefinition(TokenType.Plus, 1),
    TokenDefinition(TokenType.Minus, 1),
    TokenDefinition(TokenType.Mul, 1),
    TokenDefinition(TokenType.Div, 1),
    TokenDefinition(TokenType.Pow, 1),
    TokenDefinition(TokenType.Mod, 1),
    TokenDefinition(TokenType.Dot, 1),
    TokenDefinition(TokenType.true, 1),
    TokenDefinition(TokenType.false, 1),
    TokenDefinition(TokenType.none, 1),
    TokenDefinition(TokenType.void, 1),
    TokenDefinition(TokenType.Constructor, 1),
    TokenDefinition(TokenType.This, 1),
    TokenDefinition(TokenType.OAnd, 1),
    TokenDefinition(TokenType.While, 1),
    TokenDefinition(TokenType.LeftBracket, 1),
    TokenDefinition(TokenType.RightBracket, 1),
    TokenDefinition(TokenType.Bool, 1)
    
]


class Tokenizer:
    def __call__(self, bs_content_file: str) -> Iterable[Token]:
        tokens: List[Token] = []

        matches = {}
        for token_def in TOKENS:
            matches[token_def] = token_def.type.value[0].find_all(bs_content_file)
        
        i = 0
        while i < len(bs_content_file):
            token_in_i: List[Tuple[TokenDefinition, Match]] = []

            # Get all matches
            for k, v in matches.items():
                for t in v:
                    if t.start == i:
                        token_in_i.append((k, t))
                    
            # Get match with highest precedence
            if len(token_in_i):
                token_in_i = sorted(token_in_i, key=lambda tup: tup[0].precendece)
                token = Token(token_in_i[0][0].type, token_in_i[0][1].value, token_in_i[0][1].start, token_in_i[0][1].end)
                tokens.append(token)    
                i = token.end

            i += 1
        tokens.append(Token(TokenType.EOF, "EOF", tokens[-1].end + 1, tokens[-1].end + 4))
        return deque(tokens)          
