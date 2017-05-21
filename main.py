import numpy as np
from random import randint
import random
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer
from xml.dom import minidom


class MAP:
    # TODO generowanie mapy DFS
    # TODO generowanie inna metoda
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
    CPU1grave = 13
    CPU2grave = 14
    CPU3grave = 15
    blast = 16
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

    def generateMap(self, player, AI1, AI2, AI3):
        # print(self.gridSize)
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                if (i % 2 == 0) and j % 4 == 0:  # generujemy siatke murów
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

        # pusty lewy gorny rog
        self.currentMap[2, 2] = self.empty
        self.currentMap[2, 3] = self.empty
        self.currentMap[3, 2] = self.empty
        self.currentMap[2, 4] = self.empty
        self.currentMap[4, 2] = self.empty

        # pusty prawy gorny rog
        self.currentMap[2, self.gridSize-2] = self.empty
        self.currentMap[2, self.gridSize-3] = self.empty
        self.currentMap[2, self.gridSize-4] = self.empty
        self.currentMap[3, self.gridSize-2] = self.empty
        self.currentMap[4, self.gridSize-2] = self.empty

        # pusty lewy dolny rog
        self.currentMap[self.gridSize-2, 2] = self.empty
        self.currentMap[self.gridSize-3, 2] = self.empty
        self.currentMap[self.gridSize-4, 2] = self.empty
        self.currentMap[self.gridSize-2, 3] = self.empty
        self.currentMap[self.gridSize-2, 4] = self.empty

        # pusty prawy dolny rog
        self.currentMap[self.gridSize-2, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-3, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-4, self.gridSize-2] = self.empty
        self.currentMap[self.gridSize-2, self.gridSize-3] = self.empty
        self.currentMap[self.gridSize-2, self.gridSize-4] = self.empty

        # 4 graczy w naroznikach
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

    def sterowanie(self, command, currentPlayer, acMap, bomba):  # przekazanie acMap jest do dupy
        # TODO poprawic kierunki
        if command == 'w':
            if self.currentMap[currentPlayer.playerPositionX-1, currentPlayer.playerPositionY] == self.empty:
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
                currentPlayer.playerPositionX -= 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
        elif command == 's':
            if self.currentMap[currentPlayer.playerPositionX+1, currentPlayer.playerPositionY] == self.empty:
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = self.empty
                currentPlayer.playerPositionX += 1
                self.currentMap[currentPlayer.playerPositionX, currentPlayer.playerPositionY] = currentPlayer.id
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
            bomba.timer = 7
        elif command == 'p':
            pass
        else:
            print("Schlecht")
        return self.currentMap


class PLAYER:
    # TODO AI
    playerPositionX = 5
    playerPositionY = 10
    id = 0
    isCPU = 0

    def __init__(self, playerPositionX, playerPositionY, isCPU, id):
        self.playerPositionX = playerPositionX
        self.playerPositionY = playerPositionY
        self.isCPU = isCPU
        self.id = id


class BOMB:
    # TODO multiple bombs going off
    # TODO blast stops when destroys something
    # TODO player stops when destroyed
    bombPositionX = 5
    bombPositionY = 5
    power = 1  # how far can blast reach
    timer = 5  # how many rounds before bomb goes off
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
        if board.currentMap[self.bombPositionX, self.bombPositionY] == board.bomb:
            board.currentMap[self.bombPositionX, self.bombPositionY] = board.empty
        elif board.currentMap[self.bombPositionX, self.bombPositionY] == board.player:
            board.currentMap[self.bombPositionX, self.bombPositionY] = board.grave
        elif board.currentMap[self.bombPositionX, self.bombPositionY] == board.bombAndPlayer:
            board.currentMap[self.bombPositionX, self.bombPositionY] = board.grave
        j = self.bombPositionY
        i = self.bombPositionX-self.power
        if self.left == 1:
            if board.currentMap[i, j] == board.destructibleWall:
                board.currentMap[i, j] = board.empty
                self.left = 0
            elif board.currentMap[i, j] == board.player:
                board.currentMap[i, j] = board.grave
                self.left = 0
            elif board.currentMap[i, j] == board.CPU1:
                board.currentMap[i, j] = board.graveCPU1
                self.left = 0
            elif board.currentMap[i, j] == board.CPU2:
                board.currentMap[i, j] = board.graveCPU2
                self.left = 0
            elif board.currentMap[i, j] == board.CPU3:
                board.currentMap[i, j] = board.graveCPU3
                self.left = 0
            elif board.currentMap[i, j] == board.bomb:
                board.currentMap[i, j] = board.empty
                self.left = 0
            elif board.currentMap[i, j] == board.bombAndPlayer:
                board.currentMap[i, j] = board.empty
                self.left = 0
        i = self.bombPositionX+self.power
        j = self.bombPositionY
        if self.right == 1:
            if board.currentMap[i, j] == board.destructibleWall:
                board.currentMap[i, j] = board.empty
                self.right = 0
            elif board.currentMap[i, j] == board.player:
                board.currentMap[i, j] = board.grave
                self.right = 0
            elif board.currentMap[i, j] == board.CPU1:
                board.currentMap[i, j] = board.graveCPU1
                self.right = 0
            elif board.currentMap[i, j] == board.CPU2:
                board.currentMap[i, j] = board.graveCPU2
                self.right = 0
            elif board.currentMap[i, j] == board.CPU3:
                board.currentMap[i, j] = board.graveCPU3
                self.right = 0
            elif board.currentMap[i, j] == board.bomb:
                board.currentMap[i, j] = board.empty
                self.right = 0
            elif board.currentMap[i, j] == board.bombAndPlayer:
                board.currentMap[i, j] = board.empty
                self.right = 0
        i = self.bombPositionX
        j = self.bombPositionY + self.power
        if self.up == 1:
            if board.currentMap[i, j] == board.destructibleWall:
                board.currentMap[i, j] = board.empty
                self.up = 0
            elif board.currentMap[i, j] == board.player:
                board.currentMap[i, j] = board.grave
                self.up = 0
            elif board.currentMap[i, j] == board.CPU1:
                board.currentMap[i, j] = board.graveCPU1
                self.up = 0
            elif board.currentMap[i, j] == board.CPU2:
                board.currentMap[i, j] = board.graveCPU2
                self.up = 0
            elif board.currentMap[i, j] == board.CPU3:
                board.currentMap[i, j] = board.graveCPU3
                self.up = 0
            elif board.currentMap[i, j] == board.bomb:
                board.currentMap[i, j] = board.empty
                self.up = 0
            elif board.currentMap[i, j] == board.bombAndPlayer:
                board.currentMap[i, j] = board.empty
                self.up = 0
        i = self.bombPositionX
        j = self.bombPositionY - self.power
        if self.down == 1:
            if board.currentMap[i, j] == board.destructibleWall:
                board.currentMap[i, j] = board.empty
                self.down = 0
            elif board.currentMap[i, j] == board.player:
                board.currentMap[i, j] = board.grave
                self.down = 0
            elif board.currentMap[i, j] == board.CPU1:
                board.currentMap[i, j] = board.graveCPU1
                self.down = 0
            elif board.currentMap[i, j] == board.CPU2:
                board.currentMap[i, j] = board.graveCPU2
                self.down = 0
            elif board.currentMap[i, j] == board.CPU3:
                board.currentMap[i, j] = board.graveCPU3
                self.down = 0
            elif board.currentMap[i, j] == board.bomb:
                board.currentMap[i, j] = board.empty
                self.down = 0
            elif board.currentMap[i, j] == board.bombAndPlayer:
                board.currentMap[i, j] = board.empty
                self.down = 0
        self.active = 0

#  main program code
gracz = PLAYER(0, 0, 2, 0)
AI1 = PLAYER(1, 1, 2, 1)
AI2 = PLAYER(1, 2, 2, 2)
AI3 = PLAYER(1, 3, 8, 3)

mapa = MAP(40)
mapa.generateMap(gracz, AI1, AI2, AI3)


class Example(QWidget):
    rectSize = 17
    wallColor = QColor(200, 200, 20)
    brickColor = QColor(150, 25, 14)
    grassColor = QColor(0, 92, 9)
    playerColor = QColor(238, 193, 189)
    CPU1Color = QColor(100, 200, 240)
    CPU2Color = QColor(150, 150, 140)
    CPU3Color = QColor(200, 100, 40)
    blastColor = QColor(255, 255, 255)
    bombColor = QColor(0, 0, 0)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 20, 850, 750)
        self.setWindowTitle('Graficzny Bomberman')
        self.show()

    def rectBrush(self, qp, startPointX, startPointY, rectSize, pattern, color):
        brush = QBrush(pattern)
        brush.setColor(color)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)

    def graveBrush(self, qp, startPointX, startPointY, rectSize, currentColor):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(currentColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)
        brush.setColor(QColor(0, 0, 0))
        qp.setBrush(brush)
        qp.drawRect(startPointX+rectSize*0.4, startPointY, rectSize/5, rectSize)
        qp.drawRect(startPointX, startPointY+rectSize*0.3, rectSize, rectSize/5)

    def keyPressEvent(self, e):
        command = e.key()
        if command == Qt.Key_Left or command == Qt.Key_A:
            playerMovements.append(str(chr(command+32)))
            if mapa.currentMap[gracz.playerPositionX-1, gracz.playerPositionY] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionX -= 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Right or command == Qt.Key_D:
            playerMovements.append(str(chr(command+32)))
            if mapa.currentMap[gracz.playerPositionX+1, gracz.playerPositionY] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionX += 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Down or command == Qt.Key_S:
            playerMovements.append(str(chr(command+32)))
            if mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY+1] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionY += 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Up or command == Qt.Key_W:
            playerMovements.append(str(chr(command+32)))
            if mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY-1] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionY -= 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Space:
            playerMovements.append(str(chr(command)))
            bomba.active = 1
            mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.bombAndPlayer
            bomba.bombPositionX = gracz.playerPositionX
            bomba.bombPositionY = gracz.playerPositionY
            bomba.timer = 7
        elif command == Qt.Key_Z:
            saveMovements(playerMovements, CPU1Movements, CPU2Movements, CPU3Movements)
        elif command == Qt.Key_L:
            load()
            timer.stop()
        elif command == Qt.Key_R:
            global replay
            replay = not replay
        elif command == Qt.Key_P:
            if timer.isActive():
                timer.stop()
            else:
                timer.start(timertime)
        else:
            print("Schlecht")

    def bombBrush(self, qp, startPointX, startPointY, rectSize, backColor):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(backColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)
        brush.setColor(self.bombColor)
        qp.setBrush(brush)
        center = QPoint(startPointX+rectSize/2, startPointY+rectSize/2)
        qp.drawEllipse(center, rectSize/2 - 1, rectSize/2 - 1)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for i in range(1, 40):
            for j in range(1, 40):
                if mapa.currentMap[i, j] == mapa.solidWall:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.wallColor)
                elif mapa.currentMap[i, j] == mapa.blast:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.blastColor)
                elif mapa.currentMap[i, j] == mapa.destructibleWall:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.DiagCrossPattern,
                                   self.brickColor)
                elif mapa.currentMap[i, j] == mapa.empty:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.Dense1Pattern,
                                   self.grassColor)
                elif mapa.currentMap[i, j] == mapa.player:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.playerColor)
                elif mapa.currentMap[i, j] == mapa.CPU1:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.CPU1Color)
                elif mapa.currentMap[i, j] == mapa.CPU2:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.CPU2Color)
                elif mapa.currentMap[i, j] == mapa.CPU3:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.CPU3Color)
                elif mapa.currentMap[i, j] == mapa.grave:
                    self.graveBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.playerColor)
                elif mapa.currentMap[i, j] == mapa.CPU1grave:
                    self.graveBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.CPU1Color)
                elif mapa.currentMap[i, j] == mapa.CPU2grave:
                    self.graveBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.CPU2Color)
                elif mapa.currentMap[i, j] == mapa.CPU3grave:
                    self.graveBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.CPU3Color)
                elif mapa.currentMap[i, j] == mapa.bomb:
                    self.bombBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.grassColor)
                elif mapa.currentMap[i, j] == mapa.bombAndPlayer:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.playerColor)
                    self.bombBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.playerColor)
                else:
                    self.rectBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, Qt.SolidPattern,
                                   self.wallColor)

        # tutaj robimy legendę - bloczki
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+15, 10, Qt.SolidPattern, self.wallColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+30, 10, Qt.SolidPattern, self.blastColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+45, 10, Qt.DiagCrossPattern, self.brickColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+60, 10, Qt.Dense1Pattern, self.grassColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+75, 10, Qt.SolidPattern, self.playerColor)
        self.graveBrush(qp, self.rectSize * 40 + 20, self.rectSize+90, 10, self.playerColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+105, 10, Qt.SolidPattern, self.playerColor)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+120, 10, Qt.SolidPattern, self.CPU1Color)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+135, 10, Qt.SolidPattern, self.CPU2Color)
        self.rectBrush(qp, self.rectSize * 40 + 20, self.rectSize+150, 10, Qt.SolidPattern, self.CPU3Color)
        self.bombBrush(qp, self.rectSize * 40 + 20, self.rectSize+165, 10, self.grassColor)
        self.bombBrush(qp, self.rectSize * 40 + 20, self.rectSize+180, 10, self.playerColor)

        # tutaj robimy legendę - podpisy
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+25, "Niezniszczalna ściana")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+40, "Wybuch")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+55, "Cegły")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+70, "Puste miejsce")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+85, "Gracz")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+100, "Grób gracza")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+115, "Kolor gracza numer 1")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+130, "Kolor gracza numer 2")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+145, "Kolor gracza numer 3")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+160, "Kolor gracza numer 4")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+175, "Bomba")
        qp.drawText(self.rectSize * 40 + 40, self.rectSize+190, "Bomba i gracz")

        qp.end()


def saveMovements(movPlayer, movCPU1, movCPU2, movCPU3):
    doc = minidom.Document()

    doc.appendChild(doc.createComment("Replay Bomberman"))

    book = doc.createElement('players')
    doc.appendChild(book)

    print(movPlayer)
    print(movCPU1)
    print(movCPU2)
    print(movCPU3)

    if len(movPlayer) != len(movCPU1):
        # wypielnia stringa do dlugosci movCPU1 zerami
        movPlayer = movPlayer + ['n'] * (len(movCPU1) - len(movPlayer))

    humanPlayer = doc.createElement('Czlowiek')
    book.appendChild(humanPlayer)
    movements = doc.createElement('movements')
    humanPlayer.appendChild(movements)
    movements.appendChild(doc.createTextNode(''.join(movPlayer)))

    CPU1Player = doc.createElement('CPU1')
    book.appendChild(CPU1Player)
    movements = doc.createElement('movements')
    CPU1Player.appendChild(movements)
    movements.appendChild(doc.createTextNode(''.join(movCPU1)))

    CPU2Player = doc.createElement('CPU2')
    book.appendChild(CPU2Player)
    movements = doc.createElement('movements')
    CPU2Player.appendChild(movements)
    movements.appendChild(doc.createTextNode(''.join(movCPU2)))

    CPU3Player = doc.createElement('CPU3')
    book.appendChild(CPU3Player)
    movements = doc.createElement('movements')
    CPU3Player.appendChild(movements)
    movements.appendChild(doc.createTextNode(''.join(movCPU3)))

    file_handle = open("saveFile.xml", "w")
    doc.writexml(file_handle)
    file_handle.close()


def load():
        xmldoc = minidom.parse('saveFile.xml')
        itemlist = xmldoc.getElementsByTagName('movements')
        for s in itemlist:
            print(s.childNodes[0].nodeValue)
        global playerMovements, CPU1Movements, CPU2Movements, CPU3Movements
        playerMovements = list(itemlist[0].childNodes[0].nodeValue)
        CPU1Movements = list(itemlist[1].childNodes[0].nodeValue)
        CPU2Movements = list(itemlist[2].childNodes[0].nodeValue)
        CPU3Movements = list(itemlist[3].childNodes[0].nodeValue)
        print(playerMovements)


if __name__ == '__main__':
    timertime = 100
    replay = 0
    replayround = 0
    app = QApplication(sys.argv)
    ex = Example()
    losoweSterowanie = ['a', 'w', 's', 'd']
    bomba = BOMB(10, 12, 1)
    # losowe sterowanie duszkami
    playerMovements = []
    CPU1Movements = []
    CPU2Movements = []
    CPU3Movements = []


    def tick():
        global replay
        if replay == 0:
            asd = random.choice(losoweSterowanie)
            mapa.currentMap = mapa.sterowanie(asd, AI1, mapa, bomba)
            CPU1Movements.append(asd)
            asd = random.choice(losoweSterowanie)
            mapa.currentMap = mapa.sterowanie(asd, AI2, mapa, bomba)
            CPU2Movements.append(asd)
            asd = random.choice(losoweSterowanie)
            mapa.currentMap = mapa.sterowanie(asd, AI3, mapa, bomba)
            CPU3Movements.append(asd)
        else:
            global replayround
            mapa.currentMap = mapa.sterowanie(playerMovements[replayround], AI1, mapa, bomba)
            mapa.currentMap = mapa.sterowanie(CPU1Movements[replayround], AI1, mapa, bomba)
            mapa.currentMap = mapa.sterowanie(CPU2Movements[replayround], AI2, mapa, bomba)
            mapa.currentMap = mapa.sterowanie(CPU3Movements[replayround], AI3, mapa, bomba)
            if replayround < len(CPU1Movements)-1:
                print("rr: "+str(replayround)+" dlugosc: "+str(len(CPU1Movements)))
                replayround += 1
            else:
                replay = not replay
                replayround = 0
                print("Koncze replay")
        ex.repaint()


    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(timertime)

    sys.exit(app.exec_())
