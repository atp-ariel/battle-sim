from typing import Deque
from ..tokenizer import Tokenizer
from ..parser import Parser, build_parser
from ..code_generation import CodeGenerate
from .bs_grammar import GRAMMAR
from os.path import exists
from json import load


class Compiler:
    def __init__(self):
        parent_path = "./src/language/compiler/"
        action_path = parent_path + "action.json"
        goto_path = parent_path + "go_to.json"

        self.lexer: Tokenizer = Tokenizer()

        if not exists(action_path) or not exists(goto_path):
            build_parser(GRAMMAR, parent_path)

        file = open(action_path)
        action = load(file)
        file.close()

        file = open(goto_path)
        go_to = load(file)
        file.close()

        self.parser = Parser(GRAMMAR,action, go_to)

    def __call__(self, program: str):
        tokens = self.lexer(program)

        program_ast = self.parser.parse(tokens)

        code_program = CodeGenerate().visit(program_ast)
        
        f = open("caca.py", "w")
        f.write(code_program)
        f.close()

        
        