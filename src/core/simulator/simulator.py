from typing import List
from scipy import stats
import random as rd


class Simulator:
    def __init__(self,earth_map, sides: List, turns: int, interval: int, time_end, time_beg=0):
        self.earth_map=earth_map
        self.sides=sides
        self.units=[]
        self.time_beg=time_beg
        self.time_end=time_end
        self.interval=interval
        self.turns=turns

        for side in sides:
            units=side.get_units()

            for unit in units:
                self.units.append(unit)

    def event_is_pos(self,unit):
        if unit.life_points<=0: #Saber si la unidad se destruyó según las condiciones del usuario
            return False

        return True

    def get_events(self,moment):
        events={}

        for side in self.sides:
            units=side.get_units()
            for unit in units:
                if self.event_is_pos(unit):
                    print(f"Unidad {unit.id}: {unit.life_points} puntos")
                    events[unit]=0


        for event in events:
            var_time=stats.beta.rvs(1, 3, loc=moment, scale=1, size=1, random_state=None)
                
            var_time=var_time[0]
            events[event]=var_time

        sorted_events = sorted(events.items(), key=lambda x: x[1])
        
        return sorted_events
            
    def simulator_by_turns(self,time_beg,time_end):

        events=self.get_events(rd.randint(time_beg,time_end))

        alive_sides=set()
        for event in events:
            alive_sides.add(event.side)

        if len(alive_sides)<=1:
            self.no_enemies=True
            return

        for event in events:
            if event[1]>self.time_beg and event[1]<self.time_end:
                if self.event_is_pos(event[0]):
                    event[0].turn()
						                       
    def simulating_k_turns(self):
        beg=self.time_beg
        k=self.turns
        for end in range(int(self.time_beg+self.interval),int(self.time_end+self.interval),int(self.interval)):
            if self.no_enemies:
                print("Simulación Finalizada")
                return

            if k==0:
                break

            k-=1
            
            print(f"Turno {self.turns - k}")
            self.simulator_by_turns(beg,end)
            beg=end

			
    
