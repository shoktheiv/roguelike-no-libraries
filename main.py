import random
import math

game_width = 300
game_height = 150


number_of_rooms = 8
distance = 40

class Vector():
    def __init__(self,  x, y,z=None):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def convert(self):
        centre = Vector(math.floor(game_width/2), math.floor(game_height/2))
        self.x += centre.x
        self.y += centre.y
        return self
    
    def deconvert(self):
        centre = Vector(math.floor(game_width/2), math.floor(game_height/2))
        self.x -= centre.x
        self.y -= centre.y
        return self

    def floor(self):
        return Vector(math.floor(self.x), math.floor(self.y))

    def zero():
        return Vector(0,0)
    
    def copy(self):
        return Vector(self.x, self.y)

class Room():
    def __init__(self, pos, size):
        self.pos = pos
        self.width = size
        self.height = size/2


board=[]
camera_pos = Vector(0,0).convert()
camera_height = 20
camera_width = 40

player_pos = Vector(0,0).convert()

rooms = []

def get_pos(pos):
    y = 0
    for row in board:
        x = 0
        if pos.y == y:
            for col in row:
                if pos.x == x:
                    return col
                x+=1
        y+=1

def set_pos(pos, char):
    y = 0
    for row in board:
        x = 0
        if pos.y == y:
            for col in row:
                if pos.x== x:
                    board[y][x] = char
                x+=1
        y+=1

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n

def create_board():

    global board
    board_temp =[]
    current_row = 0
    while current_row < game_height:
        row = []
        current_columnn = 0
        while current_columnn < game_width:
            row.append("▇")
            current_columnn+=1
        board_temp.append(row)
        current_row +=1
    board = board_temp


def update_board():
    print("\n"*100)
    for i in board:
        row = ''
        for j in i:
            row+=j

def connect_rooms(pos1, pos2):
    #pos1 = pos1.deconvert()
    #pos2 = pos2.deconvert()

    if pos1.y == pos2.y:
        for i in '12':
            row = board[pos1.y]
            n = 0
            for column in row:
                if n > min([pos1.x, pos2.x]) and n < max([pos1.x, pos2.x]):
                    row[n] = ' '
                n+=1
            pos1.y -=1
        
    else:
        dc = pos1.x
        dc = clamp(dc, 0, game_width)
        for i in '123':
            n = 0
            for i in board:
                if(n < max([pos1.y, pos2.y]) and n > min([pos1.y, pos2.y])):
                    i[dc] = ' '
                n +=1
            dc+=1
        
            
def update_scene():
    y = 0
    print('\n' * 100)
    scene = []
    for row in board:
        x = 0
        current_row = ''
        if y > camera_pos.y - camera_height and y < camera_pos.y + camera_height:
            for col in row:
                if x > camera_pos.x - camera_width and x < camera_pos.x + camera_width:
                    current_row += col
                x +=1
            scene.append(current_row)
        y+=1
    for i in scene:
        print(i)

def add_room(pos, size):    
    width = size
    height = size/2

    current_x = math.floor(pos.x - width/2)
    current_y = math.floor(pos.y - height/2)
    
    while (current_y - pos.y) < height:
        while (current_x-pos.x) < width:
            #print(len(board))
            if current_x < 0 or current_x > game_width: return
            if current_y < 0 or current_y > game_height: return

            board[current_y-1][current_x-1] = " "
            current_x += 1
        current_y +=1
        current_x = math.floor(pos.x - width/2)
    rooms.append(Room(pos, size))

def add_player():
    global player_pos
    global camera_pos
    player_pos = rooms[0].pos
    #if get_pos(player_pos) != ' ': return
    print('hi')
    set_pos(player_pos, '●')
    camera_pos = player_pos

def move_player():
    global camera_pos
    global player_pos


    key = input(":::")
    if len(key) >0:
        while key[0] not in ['w', 'a', 's','d']:
            key = input("please enter a proper key:")[0]

    old_pos = player_pos.copy()

    if key == 'w'  : player_pos.y -= 1
    elif key == 's': player_pos.y +=1
    elif key == 'd': player_pos.x +=1
    elif key == 'a': player_pos.x -=1

    if get_pos(player_pos) != ' ':
        player_pos=old_pos
        return

    set_pos(player_pos, '●')
    set_pos(old_pos, ' ')

    camera_pos = player_pos

def check_area(pos, size):

    if(abs(pos.x) > game_width-size):
        return False
    if(abs(pos.y) > game_height-size/2):
        return False

    pos.x = clamp(pos.x, 0, game_width)
    pos.y = clamp(pos.y, 0, game_height)
    if(board[pos.y][pos.x] == " "):
        return False
    
    return True

def create_dungeon():
    max_pos = 3
    current_pos = Vector.zero().convert()
    current_pix = Vector.zero().convert()
    n_rooms = 0

    directions = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
    room_sizes = [16, 20, 24]


    while n_rooms < number_of_rooms:
        dir = random.choice(directions)
        size = random.choice(room_sizes)
        position = current_pos + (dir * Vector(distance, math.floor(distance/2))).floor()

        while(check_area(position, size) is False and (current_pix.x > max_pos or current_pix.y > max_pos)):
            dir = random.choice(directions)
            position = current_pos + (dir * Vector(distance, math.floor(distance/2))).floor()
            size = random.choice(room_sizes)
            
        print(position.x, position.y)
        add_room(position, size)
        if n_rooms > 0: connect_rooms(current_pos, position)
        current_pos = position
        current_pix += dir
        n_rooms+=1
    add_player()
    update_scene()

def game_loop():
    while True:
        move_player()
        update_scene()



create_board()
create_dungeon()
game_loop()
