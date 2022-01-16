from typing import Callable, Dict, List, Set
from .parser import ParseError


class State:
    def __init__(self, name: str):
        self.epsilon : List[State] = [] # epsilon-closure
        self.transitions : Dict[str, State]= {} 
        self.name : str = name
        self.is_end : bool = False
    
class NFA:
    def __init__(self, start, end):
        self.start : State = start
        self.end : State= end # start and end states
        end.is_end = True
    
    def addstate(self, state: State, state_set: Set[State]) -> None: 
        # add state + recursively add epsilon transitions
        if state in state_set:
            return

        state_set.add(state)
        
        for eps in state.epsilon:
            self.addstate(eps, state_set)
    
    def match(self, string: str) -> bool:
        current_states = set()
        self.addstate(self.start, current_states)
        
        for c in string:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
           
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False

class Handler:
    def __init__(self):
        self.handlers : Dict[str, Callable] = {'CHAR':self.handle_char, 'CONCAT':self.handle_concat,
                         'ALT':self.handle_alt, 'STAR':self.handle_rep,
                         'PLUS':self.handle_rep, 'QMARK':self.handle_qmark}
        self.state_count : int = 0

    def create_state(self) -> State:
        self.state_count += 1
        return State('S_' + str(self.state_count))
    
    def handle_char(self, t, nfa_stack) -> None:
        """
        Build a nfa for a char token

        (s0) -char-> (s1)

        """

        s0 = self.create_state()
        s1 = self.create_state()
        s0.transitions[t.value] = s1
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)
    
    def handle_concat(self, t, nfa_stack) -> None:
        """
        Build a NFA for concat.

        (nfa_1) -e-> (nfa_2)

        """

        n1 : NFA = None
        n2 : NFA = None
        try:
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
        except Exception:
            raise ParseError("Unexpected concatenation.")

        n1.end.is_end = False
        n1.end.epsilon.append(n2.start)
        nfa = NFA(n1.start, n2.end)
        nfa_stack.append(nfa)
    
    def handle_alt(self, t, nfa_stack) -> None:
        """
        Build a NFA for alt.

        s0  -e-> (nfa_1) -e----> s3
            |                /
            |e-> (nfa_2) -e-/

        """ 
        
        n1: NFA = None
        n2: NFA = None
        try:
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
        except Exception:
            raise ParseError("Unexpected '|'.")

        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        s3 = self.create_state()

        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        n1.end.is_end = False
        n2.end.is_end = False

        nfa = NFA(s0, s3)
        nfa_stack.append(nfa)
    
    def handle_rep(self, t, nfa_stack) -> None:
        """
        Build a NFA for repetition token.

        if repetition token is +

            |----e----|           
            V         |                       
        s0 --e-> nfa1 |-e-> s1

        if repetition token is *

            |----e----|           
            V         |                       
        s0 --e-> nfa1 |-e-> s1
            |             ^
            |-------------|
        """

        n1 : NFA = None

        try:
            n1 = nfa_stack.pop()
        except Exception:
            raise ParseError("Unexpected repetition") 

        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]

        if t.name == 'STAR':
            s0.epsilon.append(s1)
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.is_end = False
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)

    def handle_qmark(self, t, nfa_stack) -> None:
        """
        Build a NFA for ?

         |----e----|
         |         |
         |- nfa1 <-|
         
        """
        n1 : NFA = None
        try: 
            n1 = nfa_stack.pop()
        except Exception:
            raise ParseError("Unexpected '?")

        n1.start.epsilon.append(n1.end)
        nfa_stack.append(n1)
