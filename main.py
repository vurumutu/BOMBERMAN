import numpy as np
from random import randint
import random
import sys


class MAP:
    # TODO generowanie mapy DFS
    gridSize = 40
    shape = (gridSize, gridSize)
    currentMap = np.ones(shape)
    player = 0
    CPU1 = 1
    CPU2 = 2
    CPU3 = 3
    solidWall = 4
    destructibleWall = 5
    empty = 6
    bomb = 7
    grave = 8
    graveCPU1 = 9
    graveCPU2 = 10
    graveCPU3 = 11
    bombAndPlayer = 12
    playerSign = 'P'
    CPU1Sign = 'c'
    CPU2Sign = 'A'
    CPU3Sign = 'C'
    solidWallSign = 'w'
    bombSign = 'b'
    bombAndPlayerSign = 'b'
    destructibleWallSign = '#'
    graveSign = '+'

    def __init__(self, gridsize):
        self.gridSize = gridsize
        self.shape = (self.gridSize, self.gridSize)
        self.currentMap = np.ones(self.shape)

    def generateMap(self,player, AI1, AI2, AI3):
        print(self.gridSize)
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                if (i % 2 == 0) and j % 4 == 0:#generujemy siatke murów
                    self.currentMap[i, j] = self.solidWall
                else:
                    currentCell = randint(4, 6)  # 2/3 szans na bloczek ktory mozna zniszczyc
                    if currentCell == 4 or currentCell == 5:
                        self.currentMap[i, j] = self.destructibleWall
                    else:
                        self.currentMap[i, j] = self.empty

        for i in range(1, self.gridSize):  # mury dookoła
            self.currentMap[1, i] = self.solidWall
            self.currentMap[self.gridSize-1, i] = self.solidWall
            self.currentMap[i, 1] = self.solidWall
            self.currentMap[i, self.gridSize-1] = self.solidWall

        #pusty lewy gorny rog
        self.currentMap[2, 2] = self.empty
        self.currentMap[2, 3] = self.empty
        self.currentMap[3, 2] = self.empty
        self.currentMap[2, 4] = self.empty
        self.currentMap[4, 2] = self.empty

        #pusty prawy gorny rog
        self.currentMap[2, self.gridSize-2] = self.empty
        self.currentMap[2, self.gridSize-3] = self.empty
        self.currentMap[2, self.gridSize-4] = self.empty
        self.currentMap[3, self.gridSize-2] = self.empty
        self.currentMap[4, self.gridSize-2] = self.empty


        #pusty lewy dolny rog
        self.currentMap[self.gridSize-2, 2] = self.empty
        self.currentMap[self.gridSize-3, 2] = self.empty
        self.currentMap[self.gridSize-4, 2] = self.empty
        self.currentMap[self.gridSize-2, 3] = self.empty
        self.currentMap[self.gridSize-2, 4] = self.empty

        #pusty prawy dolny rog
        self.currentMap[self.gridSize-2, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-3, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-4, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-2, self.gridSize-3] = self.empty
        self.currentMap[self.gridSize-2, self.gridSize-4] = self.empty

        #4 graczy w naroznikach
        self.currentMap[2, 2] = self.player
        player.playerPositionX = 2
        player.playerPositionY = 2
        self.currentMap[2, self.gridSize-2] = self.CPU1
        AI1.playerPositionX = 2
        AI1.playerPositionY = self.gridSize-2
        self.currentMap[self.gridSize-2, 2] = self.CPU2
        AI2.playerPositionX = self.gridSize-2
        AI2.playerPositionY = 2
        self.currentMap[self.gridSize-2, self.gridSize-2] = self.CPU3
        AI3.playerPositionX = self.gridSize-2
        AI3.playerPositionY = self.gridSize-2

        return self.currentMap

    def paintMap(self):
        color = ['\x1b[6;30;42m', '\x1b[7;31;44m', '\x1b[0;30;43m','\x1b[3;35;40m']  # we pick one out of 4 colors in the console

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
                    print('\x1b[6;30;42m' + self.playerSign + '\x1b[0m', end='')
                   # print(self.playerSign, end='')
                elif self.currentMap[i, j] == self.CPU1:
                    #print(self.CPU1Sign, end='')
                    print('\x1b[7;31;44m' + self.playerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.CPU2:
                    # print(self.CPU2Sign, end='')
                    print('\x1b[0;30;43m' + self.playerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.CPU3:
                    # print(self.CPU3Sign, end='')
                    print('\x1b[3;35;40m' + self.playerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.bombAndPlayer:
                    # print(self.CPU3Sign, end='')
                    print('\x1b[6;30;42m' + self.bombAndPlayerSign + '\x1b[0m', end='')
                elif self.currentMap[i, j] == self.grave:
                    print(self.graveSign)
            print("|")
        for i in range(0, self.gridSize):
            print("-", end='')
        print("-")
        print('\x1b[6;30;42m' + "Gracz " + '\x1b[0m')
        print('\x1b[7;31;44m' + "CPU1" + '\x1b[0m')
        print('\x1b[0;30;43m' + "CPU2" + '\x1b[0m')
        print('\x1b[3;35;40m' + "CPU3" + '\x1b[0m')

        # print('Gracz komputerowy 1' + str(self.CPU1Sign))
        # print('Gracz komputerowy 2' + str(self.CPU2Sign))
        # print('Gracz komputerowy 3' + str(self.CPU2Sign))

    def sterowanie(self, command, currentPlayer, acMap, bomba):  # przekazanie acMap jest do dupy
        # print("Przed sterowaniem X: " + str(currentPlayer.playerPositionX))
        # print("Przed sterowaniem Y: " + str(currentPlayer.playerPositionY))
        if command == 'w':
            if self.currentMap[currentPlayer.playerPositionX-1, currentPlayer.playerPositionY] == self.empty:
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
                currentPlayer.playerPositionX -= 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
        elif command == 's':
            if self.currentMap[currentPlayer.playerPositionX+1, currentPlayer.playerPositionY] == self.empty:
               ##print("Płytka na którą wchodzimy: " + str(self.currentMap[currentPlayer.playerPositionX+1, currentPlayer.playerPositionY]))
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
               # print("Płytka na której jestesmy: " + str(self.currentMap[currentPlayer.playerPositionX+1, currentPlayer.playerPositionY]))
                currentPlayer.playerPositionX += 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
               # print("Nowa płytka z graczem: " + str(self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY]))
        elif command == 'd':
            if self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY+1] == self.empty:
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
                currentPlayer.playerPositionY += 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
        elif command == 'a':
            if self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY-1] == self.empty:
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
                currentPlayer.playerPositionY -= 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
        elif command == ' ':
            bomba.active = 1
            self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.bombAndPlayer
            bomba.bombPositionX = currentPlayer.playerPositionX
            bomba.bombPositionY = currentPlayer.playerPositionY
            bomba.timer = 3
        elif command == 'p':
            menuGlowne.end = 1  # brzydkie, do poprawy
            menuGlowne.score(acMap, currentPlayer)
        else:
            print("Schlecht")
            #self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.player
        return self.currentMap


class PLAYER:
    # TODO randomowe sterowanie innymi graczami
    playerPositionX = 5
    playerPositionY = 10
    id = 0
    isCPU = 0
    color = ['\x1b[6;30;42m', '\x1b[7;31;44m', '\x1b[0;30;43m', '\x1b[3;35;40m']  # we pick one out of 4 colors in the console

    def __init__(self, playerPositionX, playerPositionY, isCPU, id):
        self.playerPositionX = playerPositionX
        self.playerPositionY = playerPositionY
        self.isCPU = isCPU
        self.id = id

    def printPlayer(self, number):
        print(self.playerPositionX)
        print(self.playerPositionY)
        print(self.id)
        print(self.isCPU)
        print(self.color[number])



class BOMB:
    # TODO bombs going off
    # TODO multiple bombs going off
    # TODO blast stops when destroys something
    # TODO player stops when destroyed
    bombPositionX = 5
    bombPositionY = 5
    power = 1  # how far can blast reach
    timer = 3  # how many rounds before bomb goes off
    active = 0
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
                elif board.currentMap[i, j] == board.Player:
                    board.currentMap[i, j] = board.gravePlayer
                elif board.currentMap[i, j] == board.CPU1:
                    board.currentMap[i, j] = board.graveCPU1
                elif board.currentMap[i, j] == board.CPU2:
                    board.currentMap[i, j] = board.graveCPU2
                elif board.currentMap[i, j] == board.CPU3:
                    board.currentMap[i, j] = board.graveCPU3
                elif board.currentMap[i, j] == board.bomb:
                    board.currentMap[i, j] = board.empty
                elif board.currentMap[i, j] == board.bombAndPlayer:
                    board.currentMap[i, j] = board.empty
        self.active = 0


# menu class - prompting options
class MENU:
    # TODO scoreboard
    # TODO more options in menu
    mapGenerated = 0  # has map been generated
    end = 0  # if true ends current play and goes to score panel
    points = 0  # points in given round

    def __init__(self):
        pass

    def optionsMenu(self, actualMap, currentPlayer, AI1, AI2, AI3):
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
            actualMap.generateMap(currentPlayer, AI1, AI2, AI3)
            self.optionsMenu(actualMap, currentPlayer, AI1, AI2, AI3)
        elif choice == '2':
            actualMap.generateMap(currentPlayer, AI1, AI2, AI3)
            self.mapGenerated = 1
            self.optionsMenu(actualMap, currentPlayer,AI1,AI2,AI3)
        elif choice == '3':
            self.optionsMenu(actualMap, currentPlayer,AI1,AI2,AI3)
        elif choice == '4':
            self.optionsMenu(actualMap, currentPlayer,AI1,AI2,AI3)
        elif choice == '5':
            self.optionsMenu(actualMap, currentPlayer, AI1, AI2, AI3)
        elif choice == '6':
            self.mainMenu(actualMap, currentPlayer, AI1, AI2, AI3)
        else:
            print("Niepoprawna komenda")
            self.optionsMenu(actualMap, currentPlayer,AI1,AI2,AI3)

    def mainMenu(self, actualMap, currentPlayer, AI1, AI2, AI3):
        losoweSterowanie = ['a', 'w', 's', 'd']
        print("Witamy w super BOMBERMANIE!")
        print("1.Graj")
        print("2.Opcje")
        print("3.Koniec")
        choice = input("Wybierz opcję\n")
        if choice == '1':
            if self.mapGenerated == 0:
                actualMap.generateMap(currentPlayer, AI1, AI2, AI3)
            actualMap.paintMap()
            bomba = BOMB(10, 12, 1)
            while not self.end:
                # sterowanie graczem
                # asd = input("Wybierz opcję:\n")
                asd = sys.stdin.read(1)
                actualMap.currentMap = actualMap.sterowanie(str(asd), currentPlayer, actualMap, bomba)
                # losowe sterowanie duszkami
                asd = random.choice(losoweSterowanie)
                actualMap.currentMap = actualMap.sterowanie(asd, AI1, actualMap)
                asd = random.choice(losoweSterowanie)
                actualMap.currentMap = actualMap.sterowanie(asd, AI2, actualMap)
                asd = random.choice(losoweSterowanie)
                actualMap.currentMap = actualMap.sterowanie(asd, AI3, actualMap)
                if bomba.active == 1:
                    bomba.timer -= 1
                    if bomba.timer == 0:
                        bomba.detonate(actualMap)




                actualMap.paintMap()

                # currentPlayer.printPlayer(0)
                # AI1.printPlayer(1)
                # AI2.printPlayer(2)
                # AI3.printPlayer(3)
        elif choice == '2':
            self.optionsMenu(actualMap, currentPlayer, AI1, AI2, AI3)
        elif choice == '3':
            sys.exit()
        else:
            print("Niepoprawna komenda")
            self.mainMenu(actualMap, currentPlayer,AI1,AI2,AI3)

    def score(self, thisMap, thisPlayer):
        print("Otrzymałeś "+str(self.points)+" punktów!")
        self.end = 0
        input("")
        self.mainMenu(thisMap, thisPlayer, AI1, AI2, AI3)


#  main program code
gracz = PLAYER(0, 0, 2, 0)
AI1 = PLAYER(1, 1, 2, 1)
AI2 = PLAYER(1, 2, 2, 2)
AI3 = PLAYER(1, 3, 8, 3)

mapa = MAP(40)

menuGlowne = MENU()
menuGlowne.mainMenu(mapa, gracz, AI1, AI2, AI3)
