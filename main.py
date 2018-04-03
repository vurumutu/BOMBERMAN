import numpy as np
from random import randint
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer


class MAP:
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

    def __init__(self, gridsize):
        self.gridSize = gridsize
        self.shape = (self.gridSize, self.gridSize)
        self.currentMap = np.ones(self.shape)

    def generate_map(self):
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                if (i % 2 == 0) and j % 4 == 0:  # solid walls around the map
                    self.currentMap[i, j] = self.solidWall
                else:
                    current_cell = randint(4, 6)  # 2/3 chances for block that can be destroyed
                    if current_cell == 4 or current_cell == 5:
                        self.currentMap[i, j] = self.destructibleWall
                    else:
                        self.currentMap[i, j] = self.empty

        for i in range(1, self.gridSize):  # mury dookoła
            self.currentMap[1, i] = self.solidWall
            self.currentMap[self.gridSize-1, i] = self.solidWall
            self.currentMap[i, 1] = self.solidWall
            self.currentMap[i, self.gridSize-1] = self.solidWall

        # empty upper left corner
        for i in range(2, 5):
            self.currentMap[2, i] = self.empty
            self.currentMap[i, 2] = self.empty

        # empty upper right corner
        for i in range(2, 5):
            self.currentMap[2, self.gridSize - i] = self.empty
            self.currentMap[i, self.gridSize - 2] = self.empty

        # empty lower left corner
        for i in range(2, 5):
            self.currentMap[self.gridSize-2, i] = self.empty
            self.currentMap[self.gridSize-i, 2] = self.empty

        # empty lower right corner
        for i in range(2, 5):
            self.currentMap[self.gridSize-i, self.gridSize - 2] = self.empty
            self.currentMap[self.gridSize-2, self.gridSize - i] = self.empty

        # 4 players in corners
        self.currentMap[2, 2] = self.player
        self.currentMap[2, self.gridSize-2] = self.CPU1
        self.currentMap[self.gridSize-2, 2] = self.CPU2
        self.currentMap[self.gridSize-2, self.gridSize-2] = self.CPU3

        return self.currentMap


class PLAYER:
    playerPositionX = 5
    playerPositionY = 10
    id = 0
    isCPU = 0

    def __init__(self, _player_position_x, _player_position_y, _is_bot, _id):
        self.playerPositionX = _player_position_x
        self.playerPositionY = _player_position_y
        self.isCPU = _is_bot
        self.id = _id


class BOMB:
    bomb_position_x = 5
    bomb_position_y = 5
    power = 1  # how far can blast reach
    timer = 5  # how many rounds before bomb goes off
    active = 0
    left = 1
    right = 1
    up = 1
    down = 1

    def __init__(self, bomb_position_x, bomb_position_y, power):
        self.bomb_position_x = bomb_position_x
        self.bomb_position_y = bomb_position_y
        self.power = power


#  main program code
gracz = PLAYER(0, 0, 2, 0)
AI1 = PLAYER(1, 1, 2, 1)
AI2 = PLAYER(1, 2, 2, 2)
AI3 = PLAYER(1, 3, 8, 3)

mapa = MAP(40)
mapa.generate_map()


class Example(QWidget):
    rect_size = 17
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
        self.setGeometry(100, 20, 850, 750)
        self.setWindowTitle('Bomberman')
        self.show()

    def do_nothing(self):
        pass

    def rect_brush(self, qp, start_point_x, start_point_y, rect_size, pattern, color):
        self.do_nothing()
        brush = QBrush(pattern)
        brush.setColor(color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, rect_size, rect_size)

    def grave_brush(self, qp, start_point_x, start_point_y, rect_size, current_color):
        self.do_nothing()
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(current_color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, rect_size, rect_size)
        brush.setColor(QColor(0, 0, 0))
        qp.setBrush(brush)
        qp.drawRect(start_point_x+rect_size*0.4, start_point_y, rect_size/5, rect_size)
        qp.drawRect(start_point_x, start_point_y+rect_size*0.3, rect_size, rect_size/5)

    def keyPressEvent(self, e):
        command = e.key()
        if command == Qt.Key_Left or command == Qt.Key_A:
            if mapa.currentMap[gracz.playerPositionX-1, gracz.playerPositionY] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionX -= 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Right or command == Qt.Key_D:
            if mapa.currentMap[gracz.playerPositionX+1, gracz.playerPositionY] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionX += 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Down or command == Qt.Key_S:
            if mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY+1] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionY += 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_Up or command == Qt.Key_W:
            if mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY-1] == mapa.empty:
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = mapa.empty
                gracz.playerPositionY -= 1
                mapa.currentMap[gracz.playerPositionX, gracz.playerPositionY] = gracz.id
        elif command == Qt.Key_P:
            if timer.isActive():
                timer.stop()
            else:
                timer.start(delta_time)
        else:
            print("Somethings wrong.")

    def bomb_brush(self, qp, start_point_x, start_point_y, rect_size, back_color):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(back_color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, rect_size, rect_size)
        brush.setColor(self.bombColor)
        qp.setBrush(brush)
        center = QPoint(start_point_x+rect_size/2, start_point_y+rect_size/2)
        qp.drawEllipse(center, rect_size/2 - 1, rect_size/2 - 1)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for i in range(1, 40):
            for j in range(1, 40):
                if mapa.currentMap[i, j] == mapa.solidWall:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.wallColor)
                elif mapa.currentMap[i, j] == mapa.blast:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.blastColor)
                elif mapa.currentMap[i, j] == mapa.destructibleWall:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.DiagCrossPattern,
                                    self.brickColor)
                elif mapa.currentMap[i, j] == mapa.empty:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.Dense1Pattern,
                                    self.grassColor)
                elif mapa.currentMap[i, j] == mapa.player:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.playerColor)
                elif mapa.currentMap[i, j] == mapa.CPU1:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.CPU1Color)
                elif mapa.currentMap[i, j] == mapa.CPU2:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.CPU2Color)
                elif mapa.currentMap[i, j] == mapa.CPU3:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.CPU3Color)
                elif mapa.currentMap[i, j] == mapa.grave:
                    self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.playerColor)
                elif mapa.currentMap[i, j] == mapa.CPU1grave:
                    self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU1Color)
                elif mapa.currentMap[i, j] == mapa.CPU2grave:
                    self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU2Color)
                elif mapa.currentMap[i, j] == mapa.CPU3grave:
                    self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU3Color)
                elif mapa.currentMap[i, j] == mapa.bomb:
                    self.bomb_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.grassColor)
                elif mapa.currentMap[i, j] == mapa.bombAndPlayer:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.playerColor)
                    self.bomb_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.playerColor)
                else:
                    self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                                    self.wallColor)

        # legend - squares with symbols
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+15, 10, Qt.SolidPattern, self.wallColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+30, 10, Qt.SolidPattern, self.blastColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+45, 10, Qt.DiagCrossPattern, self.brickColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+60, 10, Qt.Dense1Pattern, self.grassColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+75, 10, Qt.SolidPattern, self.playerColor)
        self.grave_brush(qp, self.rect_size * 40 + 20, self.rect_size+90, 10, self.playerColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+105, 10, Qt.SolidPattern, self.playerColor)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+120, 10, Qt.SolidPattern, self.CPU1Color)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+135, 10, Qt.SolidPattern, self.CPU2Color)
        self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+150, 10, Qt.SolidPattern, self.CPU3Color)
        self.bomb_brush(qp, self.rect_size * 40 + 20, self.rect_size+165, 10, self.grassColor)
        self.bomb_brush(qp, self.rect_size * 40 + 20, self.rect_size+180, 10, self.playerColor)

        # legend with captions
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+25, "Niezniszczalna ściana")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+40, "Wybuch")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+55, "Cegły")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+70, "Puste miejsce")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+85, "Gracz")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+100, "Grób gracza")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+115, "Kolor gracza numer 1")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+130, "Kolor gracza numer 2")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+145, "Kolor gracza numer 3")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+160, "Kolor gracza numer 4")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+175, "Bomba")
        qp.drawText(self.rect_size * 40 + 40, self.rect_size+190, "Bomba i gracz")

        qp.end()


if __name__ == '__main__':
    delta_time = 100
    app = QApplication(sys.argv)
    ex = Example()
    ex.repaint()

    timer = QTimer()
    timer.start(delta_time)
    sys.exit(app.exec_())
