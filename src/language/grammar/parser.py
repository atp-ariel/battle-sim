from grammar import *
from queue import deque

class Item:
    def __init__(self,production:Production,index):
        self.production=production
        self.index=index

class ItemLR1(Item):
    
    def __init__(self, production:Production, index,lookahead:Terminal):
        Item.__init__(self, production,index)
        self.lookahead=lookahead
        self.string=f"{production.head} -> "
        
        for i in range(index):
            self.string+=f"{production[i]} "
            
        self.string+='.'
        
        total=len(production)
        for i in range(index,total):
            self.string+=f" {production[i]}"
            
            
        self.string+=f", {self.lookahead}"
        
        self.hash=hash(self.string)
    
    def __hash__(self):
        return self.hash
    
    def __eq__(self, o):
        if isinstance(o, ItemLR1):
            return self.string==o.string
        return False
    
    def __repr__(self):
        return self.string
    
    def __str__(self):
        return self.string 
        
class State:
    
    def __init__(self,kernel:List[ItemLR1]):
        self.kernel=kernel
        self.string=""
        self.items=set(kernel)
        self.nexts={}
        self.expected_symbols={}
        
        for item in kernel:
            self.string+=f"{item} |"
            
        self.hash=hash(self.string)
    
    def __hash__(self):
        return hash(self.string)
    
    def __eq__(self, o):
        if isinstance(o, State):
            return self.string==o.string
        return False
    
    def __repr__(self):
        return self.string
    
    def __str__(self):
        return self.string 
        
    def add_item(self,item:ItemLR1):
        self.items.add(item)
        
    def build(self,initial_items):
        q=deque(self.kernel)
        
        while len(q)!=0:
            
            item=q.popleft()
            if item.index==len(item.production):
                continue
            sym=item.production[item.index]
            
            if sym in self.expected_symbols:
                self.expected_symbols[sym].add(item)
            else:
                self.expected_symbols[sym]=set([item])
            
            if not sym.is_terminal:
                for i in initial_items[sym]:
                    lookahead=item.lookahead if item.index+1==len(item.production) else item.production[item.index+1]
                    new_item=ItemLR1(i.production, i.index, lookahead)
                    if new_item not in self.items:
                        self.add_item(new_item)
                        q.append(new_item)
                    
    def go_to(self,sym:Symbol,states,q:deque,initial_items):
        new_kernel=[]
        
        for i in self.expected_symbols[sym]:
            new_item=ItemLR1(i.production, i.index+1, i.lookahead)
            new_kernel.append(new_item)
        new_state=State(new_kernel)
        
        if new_state not in states:
            new_state.build(initial_items)
            states.add(new_state)
            q.append(new_state)
        
        self.nexts[sym]=new_state
            
        
class Automaton:
    
    def __init__(self, grammar:Grammar):
        self.grammar=grammar

    def build(self):
        
        s=NonTerminal('S')
        s+=Production([self.grammar.start])
        
        initial_items={s:[ItemLR1(s[0],0,Terminal('$'))]}
        
        for nt in self.grammar.N:
            initial_items[nt]=[]
            for prod in nt.productions:
                initial_items[nt].append(Item(prod,0))
                
        i0=State(initial_items[s])
        
        states=set([i0])
        q=deque([i0])
           
        while len(q)!=0:
            state=q.popleft()
            state.build(initial_items)
            for sym in state.expected_symbols:
                state.go_to(sym, states,q,initial_items)
                
        return states            
                

i=Terminal("i") 
plus=Terminal("+")
eq=Terminal("=")

E=NonTerminal("E")

A=NonTerminal("A") 

E+=Production([A,eq,A])

E+=Production([i])  

A+=Production([i,plus,A])

A+=Production([i])

g=Grammar([E,A])

a=Automaton(g)

print(len(a.build()))