from ..grammar import Grammar
from typing import Deque
from ..tokenizer import Token


class FinalToken:
    def __init__(self):
        self.name = '$'
        self.lexeme = '$'


class Parser:
    def __init__(self, grammar: Grammar, action, go_to):
        self.grammar = grammar
        self.action = action
        self.go_to = go_to
        self.final = FinalToken()

    def parse(self, secuence: Deque[Token]):
        secuence.append(self.final)

        tokens_stack = []
        states_stack = [0]
        nodes = []

        while len(secuence) > 0:
            token = secuence[0]

            state_action = self.action[states_stack[len(states_stack)-1]]

            if token.name not in state_action:
                raise Exception(
                    f'Unexpected token {token.name} with value {token.lexeme}')

            do = state_action[token.name]

            if do[0] == 'OK':
                return nodes[0]

            if do[0] == 'S':
                states_stack.append(do[1])
                tokens_stack.append(token.lexeme)
                secuence.popleft()
            else:
                prod = self.grammar.P[do[1]]
                if prod.func_ast is not None:
                    prod.func_ast(tokens_stack, nodes)

                out = len(prod)
                while out != 0:
                    tokens_stack.pop()
                    states_stack.pop()
                    out -= 1

                state_go_to = self.go_to[states_stack[len(states_stack)-1]]
                if prod.head.name not in state_go_to:
                    raise Exception(
                        f"Invalid sequence of tokens {prod.head.name}")
                tokens_stack.append(prod.head.name)
                states_stack.append(state_go_to[prod.head.name])
