import math
import random
from abc import ABC,abstractmethod
from .maps.maps import Map

class BSObject(ABC):

    @abstractmethod
    def __init__(self, id: int, life_points: int, defense: int):
        self.id = id
        self.life_points = life_points
        self.defense = defense
        self.map = None
        self.cell = None

    # poner en celda el objeto
    def put_in_cell(self, map: Map, type: str, row: int, col: int):
        if map[row][col].type != type:
            return Exception("Cell is not type of: " + type)
        else:
            if map[row][col].bs_object != None:
                map[row][col].bs_object.map = None
                map[row][col].bs_object.cell = None
            map[row][col].bs_object = self
            self.map = map
            self.cell = map[row][col]

    # tomar danio
    def take_damage(self, attack: float):
        self.life_points -= attack / self.defense
        if self.life_points <= 0:
            self.cell.bs_object = None


class BSStaticObject(BSObject):

    def __init__(self, id: int, life_points: int, defense: int):
        BSObject.__init__(self,id, life_points, defense)

    def put_in_cell(self, map: Map, row: int, col: int):
        BSObject.put_in_cell(map, "earth", row, col)


class BSUnit(BSObject):

    @abstractmethod
    def __init__(self, id, life_points, defense, side, attack, moral, ofensive, min_range, max_range, radio, vision, intelligence, recharge_turns, solidarity,movil):
        BSObject.__init__(self,id, life_points, defense)
        self.side = side
        self.moral = moral
        self.attack = attack
        self.solidarity = solidarity
        self.ofensive = ofensive
        self.min_range = min_range
        self.max_range = max_range
        if not (radio >= 1 and radio <= 9):
            Exception('radio invalido')
        self.radio = radio
        self.vision = vision
        self.intelligence = intelligence
        self.recharge_turns = recharge_turns
        self.turns_recharging = 0
        self.movil = movil
        self.no_defeated_units = 0
        self.visited_cells = set()

    # calcular distancia entre dos celdas
    def calculate_distance(self, cell1, cell2):

        distance_row = abs(cell1.row-cell2.row)
        distance_col = abs(cell1.col-cell2.col)

        return max(distance_row, distance_col)

    # calcular el costo de moverse a la celda
    def move_cost_calculate(self, cell, type):
        
        cost = 0
        
        def nearby_friend():
            for i in range(cell.row-1, cell.row+2):
                if i >= self.map.no_rows:
                    break
                if i < 0:
                    continue
                for j in range(cell.col-1, cell.col+2):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == cell.row and j == cell.col) or (i == self.cell.row and j == self.cell.col):
                        continue
                    if self.map[i][j].bs_object != None and isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side == self.side:
                        return True
            return False

        def enemy_in_range():

            for k in range(self.min_range, self.max_range+1):

                i = cell.row - k
                if i >= 0:
                    for j in range(cell.col-k, cell.col+k+1):
                        if j<0:
                            continue
                        if j>=self.map.no_columns:
                            break
                        if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                            return (True, self.map[i][j])

                i = cell.row + k
                if i < self.map.no_rows:
                    for j in range(cell.col-k, cell.col+k+1):
                        if j<0:
                            continue
                        if j>=self.map.no_columns:
                            break
                        if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                            return (True, self.map[i][j])

                j = cell.col - k
                if j >= 0:
                    for i in range(cell.row-k+1, cell.row+k):
                        if i<0:
                            continue
                        if i>=self.map.no_rows:
                            break
                        if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                            return (True, self.map[i][j])

                j = cell.col + k
                if j < self.map.no_columns:
                    for i in range(cell.row-k+1, cell.row+k):
                        if i<0:
                            continue
                        if i>=self.map.no_rows:
                            break
                        if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                            return (True, self.map[i][j])

            return (False, None)

        def in_range_of_enemy(cost):

            for i in range(cell.row-self.vision, cell.row+self.vision+1):
                if i >= self.map.no_rows:
                    break
                if i < 0:
                    continue
                for j in range(cell.col-1, cell.col+2):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == cell.row and j == cell.col) or (i == self.cell.row and j == self.cell.col):
                        continue
                    if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                        enemy = self.map[i][j].bs_object
                        limits_max_range = (
                            (enemy.cell.row-enemy.max_range,
                             enemy.cell.col-enemy.max_range),
                            (enemy.cell.row+enemy.max_range,
                             enemy.cell.col+enemy.max_range)
                        )
                        limits_min_range = (
                            (enemy.cell.row-enemy.min_range,
                             enemy.cell.col-enemy.min_range),
                            (enemy.cell.row+enemy.min_range,
                             enemy.cell.col+enemy.min_range)
                        )
                        if cell.row >= limits_max_range[0][0] and cell.col >= limits_max_range[0][1] and cell.row <= limits_max_range[1][0] and cell.col <= limits_max_range[1][1]:
                            if cell.row <= limits_min_range[0][0] or cell.row >= limits_min_range[1][0] or cell.col <= limits_min_range[0][1] or cell.col >= limits_min_range[1][1]:
                                cost += 1.1
            return cost

        if cell.passable == 0 or cell.type != type or cell.bs_object != None or abs(cell.heigth-self.cell.heigth) > 0.05:
            return 1000000

        cost = 10-cell.passable/2

        if cell in self.visited_cells:
            cost += cell.passable/3

        if nearby_friend():
            if self.solidarity:
                cost /= 2
            else:
                cost /= math.sqrt(2)

        near_enemy, enemy_cell = enemy_in_range()

        if near_enemy:
            cost -= self.ofensive*1 / \
                math.sqrt(self.calculate_distance(self.cell, enemy_cell)-self.min_range)

        cost=in_range_of_enemy(cost)

        return cost

    # buscar enemigo para atacar
    def enemy_to_attack(self):

        def cost_calculate(enemy):

            estimated_life_points = random.uniform(
                enemy.life_points-10+self.intelligence, enemy.life_points+10-self.intelligence)
            estimated_attack = random.uniform(
                enemy.attack-10+self.intelligence, enemy.attack+10-self.intelligence)
            estimated_defense = random.uniform(
                enemy.defense-10+self.intelligence, enemy.defense+10-self.intelligence)

            return estimated_life_points/(estimated_attack/estimated_defense)

        def friend_in_danger(cell):
            for i in range(self.cell.row-1, self.cell.row+2):
                if i >= self.map.no_rows:
                    break
                if i < 0:
                    continue
                for j in range(cell.col-1, cell.col+2):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == self.cell.row and j == self.cell.col):
                        continue
                    if self.map[i][j].bs_object != None and isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side == self.side:
                        return True
            return False

        cost = -1
        attacked_enemy = None

        for k in range(self.min_range, self.max_range+1):
            i = self.cell.row-k
            if i >= 0:
                for j in range(self.cell.col-k, self.cell.col+k+1):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == self.cell.row and j == self.cell.col):
                        continue
                    if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                        if self.radio > 1 and friend_in_danger(self.map[i][j]):
                            continue
                        new_cost = cost_calculate(self.map[i][j].bs_object)
                        if cost == -1 or cost > new_cost:
                            cost = new_cost
                            attacked_enemy = self.map[i][j].bs_object

            i = self.cell.row+k
            if i < self.map.no_rows:
                for j in range(self.cell.col-k, self.cell.col+k+1):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == self.cell.row and j == self.cell.col):
                        continue
                    if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                        if self.radio > 1 and friend_in_danger(self.map[i][j]):
                            continue
                        new_cost = cost_calculate(self.map[i][j].bs_object)
                        if cost == -1 or cost > new_cost:
                            cost = new_cost
                            attacked_enemy = self.map[i][j].bs_object

            j = self.cell.col-k
            if j >= 0:
                for i in range(self.cell.row-k+1, self.cell.row+k):
                    if i >= self.map.no_rows:
                        break
                    if i < 0:
                        continue
                    if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                        if self.radio > 1 and friend_in_danger(self.map[i][j]):
                            continue
                        new_cost = cost_calculate(self.map[i][j].bs_object)
                        if cost == -1 or cost > new_cost:
                            cost = new_cost
                            attacked_enemy = self.map[i][j].bs_object

            j = self.cell.col+k
            if j < self.map.no_columns:
                for i in range(self.cell.row-k+1, self.cell.row+k):
                    if i >= self.map.no_rows:
                        break
                    if i < 0:
                        continue
                    if isinstance(self.map[i][j].bs_object, BSUnit) and self.map[i][j].bs_object.side != self.side:
                        if self.radio > 1 and friend_in_danger(self.map[i][j]):
                            continue
                        new_cost = cost_calculate(self.map[i][j].bs_object)
                        if cost == -1 or cost > new_cost:
                            cost = new_cost
                            attacked_enemy = self.map[i][j].bs_object

        return attacked_enemy

    def take_damage(self, damage):
        self.life_points -= damage/(self.defense+self.moral)

    # atacar enemigo
    def attack_enemy(self, enemy):

        enemy_distance = self.calculate_distance(self.cell, enemy.cell)
        block_objects = []

        for i in range(enemy.cell.row-1, enemy.cell.row+2):
            if i >= self.map.no_rows:
                break
            if i < 0:
                continue
            for j in range(self.cell.col-1, self.cell.col+2):
                if j >= self.map.no_columns:
                    break
                if j < 0 or (i == self.cell.row and j == self.cell.col):
                    continue
                if self.map[i][j].bs_object != None and self.calculate_distance(self.cell, self.map[i][j]) <= enemy_distance:
                    block_objects.append(self.map[i][j].bs_object)

        precision = random.uniform(0, 1)

        range_enemy = max(abs(enemy.cell.row-self.cell.row),
                          abs(enemy.cell.col-self.cell.col))

        miss_distance = (range_enemy-self.min_range) / \
            (self.max_range-self.min_range+0.1)/10

        positions = [(-1, 1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1)]

        if precision < len(block_objects):

            bs_object = block_objects[int(precision)]
            bs_object.take_damage(self.attack+self.moral)

            if self.radio > 1:
                cells_to_attack = self.radio
                while cells_to_attack:

                    randint = random.randint(0, cells_to_attack)
                    position = positions[randint]
                    positions.pop(randint)

                    if self.map[self.cell.row+ self.eposition[0]][self.cell.col+position[1]].bs_object != None:
                        bs_object = self.map[self.cell.row +
                                             position[0]][self.cell.col+position[1]]
                        bs_object.take_damage((self.attack+self.moral)*4/5)
                        cells_to_attack -= 1

                        if bs_object is BSUnit and bs_object.life_points <= 0:
                            self.no_defeated_units += 1

        elif precision > len(block_objects)+miss_distance:
            enemy.take_damage(self.attack+self.moral)

            if self.radio > 1:
                cells_to_attack = self.radio
                while cells_to_attack:

                    randint = random.randint(0, cells_to_attack)
                    position = positions[randint]
                    positions.pop(randint)

                    if self.map[self.cell.row + self.eposition[0]][self.cell.col+position[1]].bs_object != None:
                        bs_object = self.map[self.cell.row +
                                             position[0]][self.cell.col+position[1]]
                        bs_object.take_damage((self.attack+self.moral)*4/5)
                        cells_to_attack -= 1

                        if bs_object is BSUnit and bs_object.life_points <= 0:
                            self.no_defeated_units += 1

        if enemy.life_points <= 0:
            self.no_defeated_units += 1

    # moverse a una celda
    def move_to_cell(self, cell):
        self.cell = cell
        cell.bs_object = self

    # turno de la unidad
    def turn(self, type):

        enemy = self.enemy_to_attack()
        if enemy != None and self.turns_recharging == 0:
            self.attack_enemy(enemy)
            self.turns_recharging = self.recharge_turns
        else:
            if self.turns_recharging != 0:
                self.turns_recharging -= 1
            cost = 10000
            cell=self.cell
            for i in range(self.cell.row-1, self.cell.row+2):
                if i >= self.map.no_rows:
                    break
                if i < 0:
                    continue
                for j in range(cell.col-1, cell.col+2):
                    if j >= self.map.no_columns:
                        break
                    if j < 0 or (i == self.cell.row and j == self.cell.col):
                        continue
                    new_cost = self.move_cost_calculate(self.map[i][j], type)
                    if new_cost < cost:
                        cost = new_cost
                        cell = self.map[i][j]
            if cost < 10000:
                self.move_to_cell(cell)

class BSLandUnit(BSUnit):
    def __init__(self, id, life_points, defense, side, attack, moral, ofensive,min_range, max_range, radio, vision, intelligence, recharge_turns, solidarity, movil):
        BSUnit.__init__(self,id,life_points,defense,side,attack,moral,ofensive,min_range,max_range,radio,vision,intelligence,recharge_turns,solidarity,movil)

    def put_in_cell(self, map, row, col):
        BSUnit.put_in_cell(self,map, "earth", row, col)

    def turn(self):
        BSUnit.turn(self,'earth')


class BSNavalUnit(BSUnit):
    def __init__(self, id, life_points, defense, side, attack, moral, ofensive,min_range, max_range, radio, vision, intelligence, recharge_turns, solidarity, movil):
        BSUnit.__init__(self,id,life_points,defense,side,attack,moral,ofensive,min_range,max_range,radio,vision,intelligence,recharge_turns,solidarity,movil)

    def put_in_cell(self, map, row, col):
        BSUnit.put_in_cell(self,map, "water", row, col)

    def turn(self):
        BSUnit.turn(self,'earth')


class BSAirUnit(BSUnit):
    def __init__(self, id, life_points, defense, side, attack, moral, ofensive,min_range, max_range, radio, vision, intelligence, recharge_turns, solidarity, movil):
        BSUnit.__init__(self,id,life_points,defense,side,attack,moral,ofensive,min_range,max_range,radio,vision,intelligence,recharge_turns,solidarity,movil)

    def put_in_cell(self, map, row, col):
        BSUnit.put_in_cell(self,map, "air", row, col)