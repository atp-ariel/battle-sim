from typing import List, Tuple
from .token import Token, TokenType, TokenDefinition
from ..regex import Match


TOKENS: List[TokenDefinition] = [
    TokenDefinition(TokenType.Number, 1),
    TokenDefinition(TokenType.Name, 2),
    TokenDefinition(TokenType.Arrow, 1),
    TokenDefinition(TokenType.Newline, 1),
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
]


class Tokenizer:
    def __call__(self, bs_content_file: str) -> List[Token]:
        tokens: List[Token] = []

        matches = {}
        for token_def in TOKENS:
            matches[token_def] = token_def.type.value.find_all(bs_content_file)
        
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
                token = Token(token_in_i[0][0], token_in_i[0][1].value, token_in_i[0][1].start, token_in_i[0][1].end)
                tokens.append(token)    
                i = token.end

            i += 1
        return tokens           
