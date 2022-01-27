from grammar import *
from queue import deque
import json
from typing import Deque

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
        self.number=0
        
        for item in kernel:
            self.string+=f"{item} |"
            
        self.hash=hash(self.string)
    
    def __hash__(self):
        return self.hash
    
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
                    
    def go_to(self,sym:Symbol,states_dict,state_list,q:deque,initial_items):
        new_kernel=[]
        
        for i in self.expected_symbols[sym]:
            new_item=ItemLR1(i.production, i.index+1, i.lookahead)
            new_kernel.append(new_item)
        new_state=State(new_kernel)
        
        if new_state not in states_dict:
            new_state.number=len(states_dict)
            new_state.build(initial_items)
            states_dict[new_state]=new_state
            state_list.append(new_state)
            q.append(new_state)
        else:
            new_state=states_dict[new_state]
        
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
        
        states_list=[i0]
        states_dict={i0:i0}
        q=deque(states_list)
           
        while len(q)!=0:
            state=q.popleft()
            state.build(initial_items)
            for sym in state.expected_symbols:
                state.go_to(sym, states_dict,states_list,q,initial_items)
                
        return states_list            
                

class TableActionGoTo:
    def __init__(self,grammar:Grammar):
        self.grammar=grammar
        
    def build(self):
        
        states=Automaton(self.grammar).build()
        
        action=[]
        go_to=[]
        
        for state in states:
            state_action={}
            state_go_to={}
            
            for n in state.nexts:
                if n.is_terminal:
                    state_action[n.name]=('S',state.nexts[n].number)
                else:
                    state_go_to[n.name]=state.nexts[n].number
            
            lookahead_item={}
            for i in state.items:
                if i.index==len(i.production):
                    if i.lookahead in lookahead_item:
                        raise Exception('Conflicto Reduce-Reduce')
                    lookahead_item[i.lookahead]=i
                    
            for l in lookahead_item:
                if l in state_action:
                    raise Exception('Conflicto Shift-Reduce')
                state_action[l.name]=('R',lookahead_item[l].production.id)
                if l.name=='$' and lookahead_item[l].production.head.name=='S':
                    state_action[l.name]=('OK',)
                    
                
            action.append(state_action)
            go_to.append(state_go_to)
        
        with open('action.json','w') as fout:
            json.dump(action, fout)
            
        with open('go_to.json','w') as fout:
            json.dump(go_to, fout)
            
class Parser:
    def __init__(self,grammar:Grammar,action,go_to):
        self.grammar=grammar
        self.action=action
        self.go_to=go_to
        
    def parse(self,secuence:Deque[Terminal]):
        
        tokens_stack=[]
        states_stack=[0]
        nodes=[]
        
        while len(secuence)>0 or len(tokens_stack)>0:
            
            token=secuence[0]
            
            state_action=action[states_stack[len(states_stack)-1]]
            
            if token.name not in state_action:
                raise Exception('cadena invalida')
            
            do=state_action[token.name]
            
            if do[0]=='OK':
                print('Cadena valida')
                return

            if do[0]=='S':
                states_stack.append(do[1])
                tokens_stack.append(token.name)
                secuence.popleft()
            else:
                prod=self.grammar.P[do[1]]
                if prod.func_ast is not None:
                    prod.func_ast(tokens_stack,nodes)
                out=len(prod)                
                while out!=0:
                    tokens_stack.pop()
                    states_stack.pop()
                    out-=1
                
                
                state_go_to=go_to[states_stack[len(states_stack)-1]]
                if prod.head.name not in state_go_to:
                    raise Exception('Cadena invalida')
                tokens_stack.append(prod.head.name)
                states_stack.append(state_go_to[prod.head.name])
                    
                        
                    
i=Terminal("int") 
plus=Terminal("+")
pi=Terminal("(")
pd=Terminal(")")
mult=Terminal("*")

E=NonTerminal("E")

T=NonTerminal("T") 

F=NonTerminal("F") 

E+=Production([E,plus,T])

E+=Production([T])

T+=Production([T,mult,F])  

T+=Production([F])

F+=Production([pi,E,pd])

F+=Production([i])

g=Grammar([E,T,F])

table=TableActionGoTo(g)

table.build()

file=open("action.json")
action=json.load(file)
file.close()

file=open("go_to.json")
go_to=json.load(file)
file.close()

parser=Parser(g,action, go_to)

secuence=deque([Terminal('int'),Terminal('+'),Terminal('int'),Terminal('*'),Terminal('int'),Terminal('$')])

parser.parse(secuence)