from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

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

    def __init__(self, symbols: List[Symbol]):
        self.symbols: List[Symbol] = symbols
        self.__head__: NonTerminal = None

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
        self.productions: List[Production] = [] if productions is None else productions
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


class Grammar:
    @property
    def start(self) -> NonTerminal:
        if self.exps:
            return self.exps[0]
        raise ValueError("Grammar has no start expression.")


    def __init__(self, exp: List[NonTerminal] = None):
        self.exps = [ ] if exp is None else exp
        self.exp_dict: Dict[str, NonTerminal] = {e.name: e for e in self.exps}

        self.T: Set[Terminal] = self.get_terminals()
        self.N: Set[NonTerminal] = self.get_non_terminals()
        self.P: List[Production] = self.get_productions()
        self.S: Set[Symbol] = self.T.union(self.N)

    def __getattr__(self, item):
        if item in self.exp_dict:
            return self.exp_dict[item]
        raise AttributeError()
    
    def __iadd__(self, exp: NonTerminal):
        if not isinstance(exp, NonTerminal):
            raise TypeError(f"Expression {exp} must be a non terminal")

        if exp.name in self.exp_dict:
            raise ValueError(f"Grammar expression {exp} already exists.")
        self.exps.append(exp)
        self.exp_dict[exp.name] = exp

        if exp not in self.N:
            self.N.add(exp)
            self.S.add(exp)
        
        for p in exp.productions:
            self.P.append(p)
            for sym in p.symbols:
                if not sym.is_terminal:
                    self.N.add(sym)
                elif sym.name != "EPS":
                    self.T.add(sym)
                else: 
                    continue
                self.S.add(sym)

        return self

    def get_terminals(self) -> Set[Terminal]:
        terminals = set()

        for e in self.exp_dict.values():
            for p in e.productions:
                for sym in p.symbols:
                    if sym.is_terminal and sym.name != "EPS":
                        terminals.add(sym)
        return terminals
    
    def get_productions(self) -> List[Production]:
        prods = []
        for e in self.exps:
            for p in e.productions:
                prods.append(p)
        return prods

    def get_non_terminals(self) -> Set[NonTerminal]:
        non_terminals = set()
        
        for e in self.exp_dict.values():
            non_terminals.add(e)
            for p in e.productions:
                for sym in p.symbols:
                    if not sym.is_terminal:
                        non_terminals.add(sym)
        return non_terminals

    

