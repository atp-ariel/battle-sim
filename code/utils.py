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
        if unit.life_points <= 0: #Saber si la unidad se destruyó según las condiciones del usuario
            return False

        return True

    def get_events(self):
        pos_events=[]
        mask=[]
        for side in self.sides:
            units=side.get_units()
            for unit in units:
                pos_events.append(unit)
                mask.append(False)

        cant_events=len(pos_events)
        cant_int=rd.randint(cant_events//2, cant_events-1)

        events={}
        for i in range(cant_int):
            selected_event=rd.randint(0,cant_events-1)

            if mask[selected_event]:
                continue

            mask[selected_event]=True
            var_time=stats.beta.rvs(3, 4, loc=self.time_beg, scale=self.time_end, size=1, random_state=None)
            var_time=var_time[0]
            events[var_time]=pos_events[selected_event]

        key=sorted(events)
        sorted_events={}
        for i in key:
            sorted_events[i]=events[i]
        
        return sorted_events
            
    def simulator_by_turns(self):
        events = self.get_events()

        for time in events.keys():
            if self.event_is_pos(events[time]):
                events[time].turn()

