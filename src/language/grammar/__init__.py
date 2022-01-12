from .grammar import Grammar
from pathlib import Path

EXTENSION_GRAMMAR = ".gr"

def get_grammar_from(file_path: Path) -> Grammar:
    if not file_path.exists(): 
        raise FileExistsError()
    if file_path.suffix == EXTENSION_GRAMMAR:
        raise ValueError()

    from .parse_grammar import GrammarParser

    with open(file_path, "r", encoding="utf-8") as gr:
        text = gr.read()
    
    # TODO Tokenizar el archivo
    tokens = []

    gmp = GrammarParser()
    return gmp(tokens)

    