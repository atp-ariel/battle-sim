from numpy.core.fromnumeric import sort, var
import scipy
from scipy import stats
import random as rd

class Side:
    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.no_units=0
        self.no_own_units_defeated=0
        self.no_enemy_units_defeated=0
        self.units=[]

    def add_unit(self,unit):
        unit.side=self
        self.no_units+=1
        self.units.append(unit)

    def remove_unit(self,unit):
        unit.side=None
        self.no_units-=1
        self.units.remove(unit)
            
    def get_units(self):
        return self.units


class Simulator:
    def __init__(self,earth_map,air_map,sides,time_end,time_beg=0):
        self.earth_map=earth_map
        self.air_map=air_map
        self.sides=sides
        self.units=[]
        self.time_beg=time_beg
        self.time_end=time_end

        for side in sides:
            units=side.get_units()

            for unit in units:
                self.units.append(unit)

    def event_is_pos(self,unit):
        if unit.life_points == 0: #Saber si la unidad se destruyó según las condiciones del usuario
            return False

        return True

    def get_events(self,moment):
        events={}

        for side in self.sides:
            units=side.get_units()
            for unit in units:
                events[unit]=0


        for event in events:
            var_time=stats.beta.rvs(1, 3, loc=moment, scale=1, size=1, random_state=None)
                
            var_time=var_time[0]
            events[event]=var_time

        sorted_events = sorted(events.items(), key=lambda x: x[1])
        
        return sorted_events
            
    def simulator_by_turns(self):
        time_beg=int(self.time_beg)
        time_end=int(self.time_end)

        for i in range(time_beg,time_end):
            events=self.get_events(i)
            for event in events:
                if event[1]>self.time_beg and event[1]<self.time_end:
                    if self.event_is_pos(event[0]):
                        event[0].turn()
    