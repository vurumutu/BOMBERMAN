import numpy as np
from random import randint


class MAP:
    # TODO lepsze generowanie mapy
    gridSize = 40
    shape = (gridSize, gridSize)
    currentMap = np.ones(shape)
    solidWall = 4
    destructibleWall = 5
    empty = 6
    bomb = 7
    gravePlayer = 8
    graveCPU1 = 9
    graveCPU2 = 10
    graveCPU3 = 11
    player = 0
    CPU1 = 1
    CPU2 = 2
    CPU3 = 3
    playerSign = 'P'
    solidWallSign = 'w'
    bombSign = 'b'
    destructibleWallSign = '#'
    graveSign = '+'

    def __init__(self, gridsize):
        self.gridSize = gridsize
        self.shape = (self.gridSize, self.gridSize)
        self.currentMap = np.ones(self.shape)

    def generateMap(self):
        print(self.gridSize)
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                currentCell = randint(4, 6)  # 4 sciana, 5 mur,6 pusta przestrzen
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

        gracz.playerPositionX = randint(2, self.gridSize-2)  # x and y position of a player
        gracz.playerPositionY = randint(2, self.gridSize-2)  # 2 i minus 2, zeby nie najechac na zewnetrze sciany
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
                elif self.currentMap[i, j] == self.gravePlayer:
                    print(gracz.color[self.player] + self.graveSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.graveCPU1:
                    print(gracz.color[self.CPU1] + self.graveSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.graveCPU2:
                    print(gracz.color[self.CPU2] + self.graveSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.graveCPU3:
                    print(gracz.color[self.CPU3] + self.graveSign + '\x1b[0m', end='')
            print("|")
        for i in range(0, self.gridSize):
            print("-", end='')
        print("-")
        print(gracz.color[self.player] + 'Gracz' + '\x1b[0m')
        print(gracz.color[self.CPU1] + 'Gracz komputerowy 1' + '\x1b[0m')
        print(gracz.color[self.CPU2] + 'Gracz komputerowy 2' + '\x1b[0m')
        print(gracz.color[self.CPU3] + 'Gracz komputerowy 3' + '\x1b[0m')

    def sterowanie(self, command, player, acMap):  # przekazanie acMap jest do dupy
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
            menuGlowne.end = 1  # brzydkie, do poprawy
            menuGlowne.score(acMap, player)
        else:
            print("Schlecht")
        self.currentMap[player.playerPositionX, player.playerPositionY] = self.player
        return self.currentMap


class PLAYER:
    # TODO randomowe sterowanie innymi grajami
    playerPositionX = 5
    playerPositionY = 10
    id = 0
    isCPU = 0
    color = ['\x1b[6;30;42m', '\x1b[7;31;44m', '\x1b[0;30;43m', '\x1b[3;35;40m']  # we pick one out of 4 colors in the console

    def __init__(self, isCPU,id):
        self.isCPU = isCPU
        self.id = id


class BOMB:
    # TODO bombs going off
    # TODO multiple bombs going off
    # TODO blast stops when destroys something
    # TODO player stops when destroyed
    bombPositionX = 5
    bombPositionY = 5
    power = 1  # how far can blast reach
    timer = 3  # how many rounds before bomb goes off
    left = 1
    right = 1
    up = 1
    down = 1

    def __init__(self, bombPositionX, bombPositionY, power):
        self.bombPositionX = bombPositionX
        self.bombPositionY = bombPositionY
        self.power = power

    # if blast destroys wall it is changed to empty space, if player it is changed into grave
    def detonate(self, board):
        for i in range(self.bombPositionX-self.power, self.bombPositionX+self.power):
            for j in range(self.bombPositionY-self.power, self.bombPositionY + self.power):
                if board.currentMap[i, j] == board.destructibleWall:
                    board.currentMap[i, j] = board.empty
                elif board.currentMap[i, j] == board.gravePlayer:
                    board.currentMap[i, j] = board.gravePlayer
                elif board.currentMap[i, j] == board.graveCPU1:
                    board.currentMap[i, j] = board.graveCPU1
                elif board.currentMap[i, j] == board.graveCPU2:
                    board.currentMap[i, j] = board.graveCPU2
                elif board.currentMap[i, j] == board.graveCPU3:
                    board.currentMap[i, j] = board.graveCPU3


# menu class - prompting options
class MENU:
    # TODO scoreboard
    # TODO more options in menu
    mapGenerated = 0  # has map been generated
    end = 0  # if true ends current play and goes to score panel
    points = 0  # points in given round

    def __init__(self):
        pass

    def optionsMenu(self, actualMap, currentPlayer):
        print("Co chcesz zmienić?")
        print("1.Rozmiar planszy")
        print("2.Losuj planszę")
        print("3.Wczytaj planszę")
        print("4.Kolor gracza")
        print("5.Wczytaj grę")
        print("6.Przejdź do menu głównego")
        choice = input("Wybierz opcję:\n")
        if choice == '1':
            newSize = input("Podaj rozmiar planszy\n")
            actualMap = MAP(int(newSize))
            actualMap.currentMap = actualMap.generateMap()
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '2':
            actualMap.currentMap = actualMap.generateMap()
            self.mapGenerated = 1
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '3':
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '4':
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '5':
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '6':
            self.mainMenu(actualMap, currentPlayer)
        else:
            print("Niepoprawna komenda")
            self.optionsMenu(actualMap, currentPlayer)

    def mainMenu(self, actualMap, currentPlayer):
        print("Witamy w super BOMBERMANIE!")
        print("1.Graj")
        print("2.Opcje")
        print("3.Koniec")
        choice = input("Wybierz opcję\n")
        if choice == '1':
            if self.mapGenerated == 0:
                actualMap.generateMap()
            actualMap.paintMap()
            while not self.end:
                asd = input("Wybierz opcję:\n")
                actualMap.currentMap = actualMap.sterowanie(str(asd), currentPlayer,actualMap)
                actualMap.paintMap()
        elif choice == '2':
            self.optionsMenu(actualMap, currentPlayer)
        elif choice == '3':
            return 0
        else:
            print("Niepoprawna komenda")
            self.mainMenu(actualMap, currentPlayer)

    def score(self, thisMap, thisPlayer):
        print("Otrzymałeś "+str(self.points)+" punktów!")
        self.end = 0
        input("")
        self.mainMenu(thisMap, thisPlayer)


#  main program code
gracz = PLAYER(0, 0)
AI1 = PLAYER(1, 1)
AI2 = PLAYER(1, 2)
AI3 = PLAYER(1, 3)

mapa = MAP(40)

menuGlowne = MENU()
menuGlowne.mainMenu(mapa, gracz)
