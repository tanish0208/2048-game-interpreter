import random
import sys

grid = []
tilename = []
def start_game():

    global grid,tilename
    for i in range(4):
        grid.append([0] * 4)


    for i in range(16):
        tilename.append([])
    addRandomTile()
    return grid

def addRandomTile():

    global grid
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    n = random.randint(0,1)

    while(grid[row][col] != 0):
        row = random.randint(0, 3)
        col = random.randint(0, 3)

    if(n==0):
        grid[row][col] = 2
    else:
        grid[row][col] = 4

def squeeze():

    global grid,tilename
    changed = False


    new_grid = []


    for i in range(4):
        new_grid.append([0] * 4)

    for i in range(4):
        pos = 0

        for j in range(4):
            if(grid[i][j] != 0):

                new_grid[i][pos] = grid[i][j]
                temp = tilename[i*4 + j]
                tilename[i*4 + j] = []
                tilename[i*4 + pos] = temp

                if(j != pos):
                    changed = True
                pos += 1


    return new_grid, changed


def merge(operation):

    global grid,tilename
    changed = False
    
    for i in range(4):
        for j in range(3):

            if(grid[i][j] == grid[i][j + 1] and grid[i][j] != 0):

                if(operation=="ADD"):
                    grid[i][j] = grid[i][j] * 2
                elif(operation=="SUBTRACT"):
                    grid[i][j] = 0
                elif(operation=="MULTIPLY"):
                    grid[i][j] = grid[i][j]*grid[i][j]
                elif(operation=="DIVIDE"):
                    grid[i][j] = 1

                grid[i][j + 1] = 0
                for k in range(len(tilename[i*4 + j + 1])):
                    tilename[i*4 + j].append(tilename[i*4 + j + 1][k])
                tilename[i*4 + j + 1] = []

                changed = True

    return grid, changed



def reverse():
    new_grid =[]
    new_tilename = []
    for i in range(16):
        new_tilename.append([])
    for i in range(4):
        new_grid.append([])
        for j in range(4):
            new_grid[i].append(grid[i][3 - j])
            new_tilename[i*4 + j] = tilename[i*4 + 3-j]
    return new_grid, new_tilename


def rotate():
    new_grid = []
    new_tilename = []
    for i in range(16):
        new_tilename.append([])
    for i in range(4):
        new_grid.append([])
        for j in range(4):
            new_grid[i].append(grid[j][i])
            new_tilename[i*4 + j] = tilename[j*4 + i]

    return new_grid, new_tilename


def move_left(operation):

    # print('yo')
    global grid
    grid, changed1 = squeeze()


    grid, changed2 = merge(operation)

    changed = changed1 or changed2

    grid, temp = squeeze()

    return grid, changed

def move_right(operation):

    global grid,tilename
    grid,tilename = reverse()
    grid, changed = move_left(operation)

    grid,tilename = reverse()

    return grid, changed



def move_up(operation):

    global grid,tilename
    grid,tilename = rotate()

    grid, changed = move_left(operation)

    grid,tilename = rotate()
    return grid, changed

def move_down(operation):

    global grid
    grid,tilename = rotate()
    grid, changed = move_right(operation)

    grid,tilename = rotate()
    return grid, changed


def printGrid():
    print('The current state is : ')
    print('-----------------')
    for i in range(4):
        print('|',end = '')
        for j in range(4):
            if(grid[i][j]==0):
                print('   |',end='')
            else:
                print(' '+str(grid[i][j]) + ' |', end = '')
        print('\n-----------------')

    output = ""
    sqList = []
    for i in range(4):
        for j in range(4):
            sqList.append(str(grid[i][j]))

    joined = "\40".join(sqList)
    output+=joined


    for i in range(4):
        for j in range(4):
            if(len(tilename[i*4 + j])>0):
                temp = []
                output+="\40"+str(i+1)+","+str(j+1)

                for k in range(len(tilename[i*4 + j])):
                    temp.append(tilename[i*4 + j][k])
                tile = ",".join(temp)
                output+=tile


    print(output,file = sys.stderr)
