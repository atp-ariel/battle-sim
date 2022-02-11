from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple


class Symbol(metaclass=ABCMeta):
    @property
    def is_terminal(self) -> bool:
        return isinstance(self, Terminal)

    def __init__(self, name: str):
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == str
        return self is other

    @abstractmethod
    def copy(self):
        pass


class Terminal(Symbol):
    def __init__(self, name: str, value: Any = None):
        Symbol.__init__(self, name)
        self.value = value

    def copy(self) -> Symbol:
        return Terminal(self.name, self.value)

    def __repr__(self):
        return f"T({self.__str__()})"


class Production:
    @property
    def head(self):
        if self.__head__ is None:
            raise ValueError("Production head missing.")
        return self.__head__

    @property
    def is_eps(self) -> bool:
        return len(self.symbols) == 1 and self.symbols[0] == "EPS"

    def __init__(self, symbols: List[Symbol], func_ast: Callable = None):
        self.symbols: List[Symbol] = symbols
        self.__head__: NonTerminal = None
        self.id: int = -1
        self.func_ast = func_ast

    def __getitem__(self, index):
        return self.symbols[index]

    def __setitem__(self, index, item):
        self.symbols[index] = item

    def __repr__(self):
        prod_str = "-> " + " ".join(str(symbol) for symbol in self.symbols)
        return prod_str

    def __len__(self):
        return len(self.symbols)

    def __str__(self):
        return self.__repr__()


class NonTerminal(Symbol):
    def __init__(self, name: str, productions: Optional[List[Production]] = None):
        Symbol.__init__(self, name)
        self.productions: List[Production] = [
        ] if productions is None else productions
        for prod in self.productions:
            prod.__head__ = self

    def copy(self) -> Symbol:
        return NonTerminal(self.name, self.productions)

    def __getitem__(self, index):
        return self.productions[index]

    def add(self, prod: Production):
        self.productions.append(prod)
        prod.__head__ = self

    def __iadd__(self, prod: Production):
        if isinstance(prod, Production):
            self.add(prod)
            return self
        raise TypeError(f"Argument {prod} must be a production")

    def __repr__(self):
        return f"NT({self.__str__()})"

    def walk(self, walked_set: Set = None, walked_list: List = None) -> Set['NonTerminal']:
        walked_set = walked_set if walked_set is not None else set()
        walked_list = walked_list if walked_list is not None else []

        if self not in walked_set:
            walked_set.add(self)
            walked_list.append(self)

        for p in self.productions:
            for sym in p.symbols:
                if isinstance(sym, NonTerminal):
                    if not sym in walked_set:
                        walked_set.add(sym)
                        walked_list.append(sym)
                        sym.walk(walked_set, walked_list)

        return walked_list


class Grammar:
    @property
    def start(self) -> NonTerminal:
        if self._s_:
            return self._s_
        raise ValueError("Grammar has no start expression.")

    def __init__(self, start: NonTerminal = None):
        self._s_ = start
        self.T: List[Terminal] = []
        self.N: List[NonTerminal] = []
        self.P: List[Production] = []

        if self._s_ is not None:
            self.T = self.get_terminals()
            self.N = self.get_non_terminals()
            self.P = self.get_productions()

    def get_terminals(self) -> List[Terminal]:
        terminals = []

        for e in self.start.walk():
            for p in e.productions:
                for sym in p.symbols:
                    if sym.is_terminal and sym.name != "EPS":
                        terminals.append(sym)
        return terminals

    def get_productions(self) -> List[Production]:
        prods = []
        for e in self.start.walk():
            for p in e.productions:
                p.id = len(prods)
                prods.append(p)
        return prods

    def get_non_terminals(self) -> List[NonTerminal]:
        return self.start.walk()
