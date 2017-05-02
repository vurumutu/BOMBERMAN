import numpy as np
from random import randint


class MAP:
    gridSize = 40
    shape = (gridSize, gridSize)
    currentMap = np.ones(shape)
    solidWall = 4
    destructibleWall = 5
    empty = 6
    bomb = 7
    player = 0
    CPU1 = 1
    CPU2 = 2
    CPU3 = 3
    playerSign = 'P'
    solidWallSign = 'w'
    bombSign = 'b'
    destructibleWallSign = '#'

    def __init__(self, gridsize):
        self.gridSize = gridsize

    def generateMap(self):
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                currentCell = randint(4, 6)#4 sciana, 5 mur,6 pusta przestrzen
                if currentCell == self.solidWall:
                    self.currentMap[i, j] = self.solidWall
                elif currentCell == self.destructibleWall:
                    self.currentMap[i, j] = self.destructibleWall
                else:
                    self.currentMap[i, j] = self.empty
        for i in range(1, self.gridSize):
            self.currentMap[1, i] = self.solidWall
            self.currentMap[self.gridSize-1, i] = self.solidWall
            self.currentMap[i, 1] = self.solidWall
            self.currentMap[i, self.gridSize-1] = self.solidWall

        gracz.playerPositionX = randint(2, self.gridSize-2)#x and y position of a player
        gracz.playerPositionY = randint(2, self.gridSize-2)#2 i minus 2, zeby nie najechac na zewnetrze sciany
        self.currentMap[gracz.playerPositionX, gracz.playerPositionY] = self.player

        AI1.playerPositionX = randint(2, self.gridSize - 2)  # x and y position of a player
        AI1.playerPositionY = randint(2, self.gridSize - 2)  # 2 i minus 2, zeby nie najechac na zewnetrze sciany
        self.currentMap[AI1.playerPositionX, AI1.playerPositionY] = self.CPU1

        AI2.playerPositionX = randint(2, self.gridSize - 2)  # x and y position of a player
        AI2.playerPositionY = randint(2, self.gridSize - 2)  # 2 i minus 2, zeby nie najechac na zewnetrze sciany
        self.currentMap[AI2.playerPositionX, AI2.playerPositionY] = self.CPU2

        AI3.playerPositionX = randint(2, self.gridSize - 2)  # x and y position of a player
        AI3.playerPositionY = randint(2, self.gridSize - 2)  # 2 i minus 2, zeby nie najechac na zewnetrze sciany

        self.currentMap[AI3.playerPositionX, AI3.playerPositionY] = self.CPU3
        return self.currentMap

    def paintMap(self):
        for i in range(0, self.gridSize):
            print("-", end='')
        print("-")
        for i in range(1, self.gridSize):
            print("|", end='')
            for j in range(1, self.gridSize):
                if self.currentMap[i, j] == self.solidWall:
                    print(self.solidWallSign, end='')
                elif self.currentMap[i, j] == self.destructibleWall:
                    print(self.destructibleWallSign, end='')
                elif self.currentMap[i, j] == self.bomb:
                    print(self.bombSign, end='')
                elif self.currentMap[i, j] == self.empty:
                    print(" ", end='')
                elif self.currentMap[i, j] == self.player:
                    print(gracz.color[self.player] + self.playerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.CPU1:
                    print(gracz.color[self.CPU1] + self.playerSign+ '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.CPU2:
                    print(gracz.color[self.CPU2] + self.playerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.CPU3:
                    print(gracz.color[self.CPU3] + self.playerSign + '\x1b[0m', end='')
            print("|")
        for i in range(0, self.gridSize):
            print("-", end='')
        print("-")
        print(gracz.color[self.player] + 'Gracz' + '\x1b[0m')
        print(gracz.color[self.CPU1] + 'Gracz komputerowy 1' + '\x1b[0m')
        print(gracz.color[self.CPU2] + 'Gracz komputerowy 2' + '\x1b[0m')
        print(gracz.color[self.CPU3] + 'Gracz komputerowy 3' + '\x1b[0m')

    def sterowanie(self, command, player):
        if command == 'w':
            if self.currentMap[player.playerPositionX-1, player.playerPositionY] == self.empty:
                self.currentMap[player.playerPositionX, player.playerPositionY] = self.empty
                player.playerPositionX -= 1
        elif command == 's':
            if self.currentMap[player.playerPositionX+1, player.playerPositionY] == self.empty:
                self.currentMap[player.playerPositionX, player.playerPositionY] = self.empty
                player.playerPositionX += 1
        elif command == 'd':
            if self.currentMap[player.playerPositionX, player.playerPositionY+1] == self.empty:
                self.currentMap[player.playerPositionX, player.playerPositionY] = self.empty
                player.playerPositionY += 1
        elif command == 'a':
            if self.currentMap[player.playerPositionX, player.playerPositionY-1] == self.empty:
                self.currentMap[player.playerPositionX, player.playerPositionY] = self.empty
                player.playerPositionY -= 1
        elif command == ' ':
            print("LOL")
        elif command == 'p':
            gracz.end = 1
        else:
            print("Schlecht")
        self.currentMap[player.playerPositionX, player.playerPositionY] = self.player
        return self.currentMap


class PLAYER:
    playerPositionX = 5
    playerPositionY = 10
    id = 0
    isCPU = 0
    end = 0# do przeniesienia gdzies indziej
    color = ['\x1b[6;30;42m', '\x1b[7;31;44m', '\x1b[0;30;43m', '\x1b[3;35;40m']#we pick one out of 4 colors in the console

    def __init__(self, isCPU,id):
        self.isCPU = isCPU
        self.id = id

gracz = PLAYER(0, 0)
AI1 = PLAYER(1, 1)
AI2 = PLAYER(1, 2)
AI3 = PLAYER(1, 3)

mapa = MAP(40)
mapa.currentMap = mapa.generateMap()
mapa.paintMap()
while not gracz.end:
    asd = input("")
    currentMap = mapa.sterowanie(str(asd),gracz)
    mapa.paintMap()
