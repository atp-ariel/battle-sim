from typing import List
from .token import Token


class Tokenizer:


        
    def __call__(self, bs_content_file: str) -> List[Token]:
        tokens : List[Token] = []
        remaining_txt : str = bs_content_file

        if not (remaining_txt or remaining_txt.isspace()):
            match : TokenMatch = self.find_match(remaining_txt)
            if match.is_match:
                tokens.append(Token(match.))
        return tokens