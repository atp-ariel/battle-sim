from ..tokenizer import Tokenizer
from ..parser import Parser, build_parser
from ..code_generation import CodeGenerate
from ..semantic_analysis import *
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

        self.parser = Parser(GRAMMAR, action, go_to)

    def __call__(self, program: str) -> str:
        # Tokenize
        tokens = self.lexer(program)

        # Parse
        program_ast = self.parser.parse(tokens)

        # Semantic analysis
        # context = Context()
        # bst = battle_sim_typing(program_ast, Type_Collector(context), Type_Builder(context), Type_Checker(context), context)
        # bst()

        # Code Generate
        code_program = CodeGenerate().visit(program_ast)

        return code_program
