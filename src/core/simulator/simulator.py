from typing import List
from scipy import stats
from .sides import Side
from tabulate import tabulate

class Simulator:
    def __init__(self,earth_map, sides: List, turns: int, interval: int, time_beg=0):
        self.earth_map=earth_map
        self.sides=sides
        self.units=[]
        self.time_beg=time_beg
        self.interval=interval
        self.turns=turns
        self.no_enemies=False

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
                    events[unit]=0

        print("Life points")
        print(tabulate([list(map(lambda x: x.life_points, self.units))], headers=[f"Unit {u.id}" for u in self.units]))
        print("Time - Action")

        for event in events:
            var_time=stats.beta.rvs(1, 3, loc=moment, scale=1, size=1, random_state=None)
                
            var_time=var_time[0]
            events[event]=var_time

        sorted_events = sorted(events.items(), key=lambda x: x[1])
        
        return sorted_events
            
    def simulator_by_turns(self,time_beg,time_end):

        events=self.get_events((time_beg+time_end)//2)

        alive_sides=set()
        for event in events:
            alive_sides.add(event[0].side)

        if len(alive_sides)<=1:
            self.no_enemies=True
            return

        for event in events:
            if event[1]>time_beg and event[1]<time_end:
                if self.event_is_pos(event[0]):
                    print(f"{event[1]}", end=" - ")
                    event[0].turn()
        print()
    def simulating_k_turns(self):
        beg=self.time_beg
        k=self.turns
        while(k>0):
            end=int(beg+self.interval)
            if self.no_enemies:
                print("Simulation Finished!")
                result = [[f"Side {side.id}", side.no_own_units_defeated, side.no_enemy_units_defeated] for side in self.sides]
                print(tabulate(result, headers=["Sides", "Allies Dead", "Enemies Killed"]))

                return

            k-=1
            
            print(f"Turn {self.turns - k}:")
            self.simulator_by_turns(beg,end)
            beg=end

    def start(self):
        self.simulating_k_turns()
