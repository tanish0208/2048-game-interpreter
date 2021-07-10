from sly import Lexer
from sly import Parser
import random
import game
import sys



class GameLexer(Lexer):

    tokens = {ADD, SUBTRACT, MULTIPLY, DIVIDE, LEFT, RIGHT, UP, DOWN, ASSIGN, TO, VAR, IS, VALUE, IN, ID, DIGIT}

    literals = {',','.'}


    ignore = ' \t'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    DIGIT = r'\d+'


    ID['ADD'] = ADD
    ID['SUBTRACT'] = SUBTRACT
    ID['MULTIPLY'] = MULTIPLY
    ID['DIVIDE'] = DIVIDE
    ID['LEFT'] = LEFT
    ID['RIGHT'] = RIGHT
    ID['UP'] = UP
    ID['DOWN'] = DOWN
    ID['ASSIGN'] = ASSIGN
    ID['TO'] = TO
    ID['VAR'] = VAR
    ID['IS'] = IS
    ID['VALUE'] = VALUE
    ID['IN'] = IN

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1



class GameParser(Parser):

    tokens = GameLexer.tokens

    # Grammar rules
    @_('ADD LEFT "."','SUBTRACT LEFT "."','MULTIPLY LEFT "."','DIVIDE LEFT "."')
    def expr(self, p):
        operation = p[0]
        temp, flag = game.move_left(operation)
        print('Thanks Left move done', end='')
        if(flag):
            game.addRandomTile()
            print(', random tile added', end = '')
        print()
        game.printGrid()



    @_('ADD RIGHT "."','SUBTRACT RIGHT "."','MULTIPLY RIGHT "."','DIVIDE RIGHT "."')
    def expr(self, p):
        operation = p[0]
        temp, flag = game.move_right(operation)
        print('Thanks Right move done', end='')
        if(flag):
            game.addRandomTile()
            print(', random tile added', end = '')
        print()
        game.printGrid()

    @_('ADD UP "."','SUBTRACT UP "."','MULTIPLY UP "."','DIVIDE UP "."')
    def expr(self, p):
        operation = p[0]
        temp, flag = game.move_up(operation)
        print('Thanks Up move done', end='')
        if(flag):
            game.addRandomTile()
            print(', random tile added', end = '')
        print()
        game.printGrid()

    @_('ADD DOWN "."','SUBTRACT DOWN "."','MULTIPLY DOWN "."','DIVIDE DOWN "."')
    def expr(self, p):
        operation = p[0]
        temp, flag = game.move_down(operation)
        print('Thanks Down move done', end='')
        if(flag):
            game.addRandomTile()
            print(', random tile added', end = '')
        print()
        game.printGrid()

    @_('ASSIGN DIGIT TO DIGIT "," DIGIT "."')
    def expr(self, p):
        x = int(p[3])
        y = int(p[5])
        if(x < 1 or x > 4 or y < 1 or y > 4):
            print('coordinates must be in the range of 1-4')
            print('-1', file = sys.stderr)
            return

        global grid
        game.grid[x-1][y-1] = int(p[1])
        print('Thanks, assignment done')
        game.printGrid()


    @_('VAR ID IS DIGIT "," DIGIT "."')
    def expr(self, p):
        x = int(p[3])
        y = int(p[5])
        if(x < 1 or x > 4 or y < 1 or y > 4):
            print('coordinates must be in the range of 1-4')
            print('-1', file = sys.stderr)
            return

        if(game.grid[x-1][y-1]==0):
            print('This tile is empty. Cannot assign variable name')
            print('-1', file = sys.stderr)
            return


        varname = p[1]
        for i in range(16):
            for k in range(len(game.tilename[i])):
                if(game.tilename[i][k]==varname):
                    print('The variable already exists')
                    print('-1', file = sys.stderr)
                    return

        game.tilename[(x-1)*4 + y-1].append(varname)
        print('Thanks, naming done')
        game.printGrid()


    @_('VALUE IN DIGIT "," DIGIT "."')
    def expr(self, p):
        x = int(p[2])
        y = int(p[4])
        if(x < 1 or x > 4 or y < 1 or y > 4):
            print('coordinates must be in the range of 1-4')
            print('-1', file = sys.stderr)
            return

        if(game.grid[x-1][y-1]==0):
            print('The square '+str(x)+","+str(y)+" is empty")
            print('-1', file = sys.stderr)
            return
        else:
            print('The value of tile '+str(x)+","+str(y)+" is : " + str(game.grid[x-1][y-1]))
            game.printGrid()

    @_('VAR ADD IS DIGIT "," DIGIT "."', 'VAR SUBTRACT IS DIGIT "," DIGIT "."', 'VAR MULTIPLY IS DIGIT "," DIGIT "."',
        'VAR DIVIDE IS DIGIT "," DIGIT "."', 'VAR LEFT IS DIGIT "," DIGIT "."', 'VAR RIGHT IS DIGIT "," DIGIT "."',
        'VAR UP IS DIGIT "," DIGIT "."', 'VAR DOWN IS DIGIT "," DIGIT "."', 'VAR ASSIGN IS DIGIT "," DIGIT "."',
        'VAR TO IS DIGIT "," DIGIT "."', 'VAR VAR IS DIGIT "," DIGIT "."', 'VAR IS IS DIGIT "," DIGIT "."',
        'VAR VALUE IS DIGIT "," DIGIT "."', 'VAR IN IS DIGIT "," DIGIT "."')
    def expr(self,p):
        print('Variable name cannot be a keyword')
        print('-1', file = sys.stderr)


    @_('VAR ADD IS DIGIT "," DIGIT', 'VAR SUBTRACT IS DIGIT "," DIGIT', 'VAR MULTIPLY IS DIGIT "," DIGIT',
        'VAR DIVIDE IS DIGIT "," DIGIT', 'VAR LEFT IS DIGIT "," DIGIT', 'VAR RIGHT IS DIGIT "," DIGIT',
        'VAR UP IS DIGIT "," DIGIT', 'VAR DOWN IS DIGIT "," DIGIT', 'VAR ASSIGN IS DIGIT "," DIGIT',
        'VAR TO IS DIGIT "," DIGIT', 'VAR VAR IS DIGIT "," DIGIT', 'VAR IS IS DIGIT "," DIGIT',
        'VAR VALUE IS DIGIT "," DIGIT', 'VAR IN IS DIGIT "," DIGIT', 'VAR ID IS DIGIT "," DIGIT',
        'ASSIGN DIGIT TO DIGIT "," DIGIT', 'ADD DOWN','SUBTRACT DOWN','MULTIPLY DOWN','DIVIDE DOWN',
        'ADD UP','SUBTRACT UP','MULTIPLY UP','DIVIDE UP', 'ADD RIGHT','SUBTRACT RIGHT',
        'MULTIPLY RIGHT','DIVIDE RIGHT', 'ADD LEFT','SUBTRACT LEFT','MULTIPLY LEFT','DIVIDE LEFT',
        'VALUE IN DIGIT "," DIGIT')
    def expr(self,p):
        print('You need to end a command with a full stop')
        print('-1', file = sys.stderr)



    def error(self, p):
        print('There is a syntax error')
        print('-1', file = sys.stderr)


if __name__ == '__main__':

    lexer = GameLexer()
    parser = GameParser()

    game.start_game()
    print('Hi i am the 2048-game engine')
    game.printGrid()


    while True:
        try:
            print('2048> Please type a command')
            text = input('----> ')
            result = parser.parse(lexer.tokenize(text))

        except EOFError:
            break
