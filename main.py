import numpy as np
from random import randint
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer
import json

qp = QPainter()


class Block:
    rect_size = 17

    def __init__(self, _name, _pattern, _caption, _color, _id):
        self.name = _name
        self.pattern = _pattern
        self.caption = _caption
        self.color = _color
        self.id = _id

    def change_caption(self, new_caption):
        self.caption = new_caption

    def change_brush(self, new_pattern):
        self.pattern = new_pattern

    def change_color(self, new_color):
        self.color = new_color

    def change_pattern(self, new_color):
        self.color = new_color

    def draw_block(self, start_point_x, start_point_y):
        raise NotImplementedError("Please Implement this method")


class OrdinaryBlock(Block):
    def draw_block(self, start_point_x, start_point_y):
        brush = QBrush(self.pattern)
        brush.setColor(self.color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, self.rect_size, self.rect_size)


class GraveBlock(Block):
    def draw_block(self, start_point_x, start_point_y):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, self.rect_size, self.rect_size)
        brush.setColor(QColor(0, 0, 0))
        qp.setBrush(brush)
        qp.drawRect(start_point_x+self.rect_size*0.4, start_point_y, self.rect_size/5, self.rect_size)
        qp.drawRect(start_point_x, start_point_y+self.rect_size*0.3, self.rect_size, self.rect_size/5)


class BombBlock(Block):
    def draw_block(self, start_point_x, start_point_y):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(0, 92, 9))  # empty space color
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, self.rect_size, self.rect_size)
        brush.setColor(self.color)
        qp.setBrush(brush)
        center = QPoint(start_point_x+self.rect_size/2, start_point_y+self.rect_size/2)
        qp.drawEllipse(center, self.rect_size/2 - 1, self.rect_size/2 - 1)


class Board:
    block_dict = {
        'player':               OrdinaryBlock("player", Qt.SolidPattern, "wall", QColor(238, 193, 189), 0),
        'CPU1':                 OrdinaryBlock("CPU1", Qt.SolidPattern, "wall", QColor(100, 200, 240), 1),
        'CPU2':                 OrdinaryBlock("CPU2", Qt.SolidPattern, "wall", QColor(150, 150, 140), 2),
        'CPU3':                 OrdinaryBlock("CPU3", Qt.SolidPattern, "wall", QColor(200, 100, 40), 3),
        'solidWall':            OrdinaryBlock("solidWall", Qt.SolidPattern, "wall", QColor(200, 200, 20), 4),
        'destructibleWall':     OrdinaryBlock("destructibleWall", Qt.DiagCrossPattern, "wall", QColor(150, 25, 14), 5),
        'empty':                OrdinaryBlock("empty", Qt.Dense1Pattern, "wall", QColor(0, 92, 9), 6),
        'bomb':                 BombBlock("bomb", Qt.SolidPattern, "wall", QColor(0, 0, 0), 7),
        'grave':                GraveBlock("grave", Qt.SolidPattern, "wall", QColor(238, 193, 189), 8),
        'bombAndPlayer':        OrdinaryBlock("bombAndPlayer", Qt.SolidPattern, "wall", QColor(238, 193, 189), 9),
        'blast':                OrdinaryBlock("blast", Qt.SolidPattern, "wall", QColor(255, 255, 255), 9)
    }

    def __init__(self, gridsize):
        self.gridSize = gridsize
        self.shape = (self.gridSize, self.gridSize)
        self.current_board = np.empty(self.shape, dtype=object)

    def generate_board(self):
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
                # print(current_map)
                print(i, " ", j)
                if (i % 2 == 0) and j % 4 == 0:  # solid walls inside
                    self.current_board[i, j] = self.block_dict['solidWall']
                else:
                    current_cell = randint(0, 2)  # 2/3 chances for block that can be destroyed
                    if current_cell == 0 or current_cell == 1:
                        self.current_board[i, j] = self.block_dict['destructibleWall']
                    else:
                        self.current_board[i, j] = self.block_dict['empty']

        for i in range(1, self.gridSize):  # solid walls around the map
            self.current_board[1, i] = self.block_dict['solidWall']
            self.current_board[self.gridSize-1, i] = self.block_dict['solidWall']
            self.current_board[i, 1] = self.block_dict['solidWall']
            self.current_board[i, self.gridSize-1] = self.block_dict['solidWall']

        # empty upper left corner
        for i in range(2, 5):
            self.current_board[2, i] = self.block_dict['empty']
            self.current_board[i, 2] = self.block_dict['empty']

        # empty upper right corner
        for i in range(2, 5):
            self.current_board[2, self.gridSize - i] = self.block_dict['empty']
            self.current_board[i, self.gridSize - 2] = self.block_dict['empty']

        # empty lower left corner
        for i in range(2, 5):
            self.current_board[self.gridSize-2, i] = self.block_dict['empty']
            self.current_board[self.gridSize-i, 2] = self.block_dict['empty']

        # empty lower right corner
        for i in range(2, 5):
            self.current_board[self.gridSize-i, self.gridSize - 2] = self.block_dict['empty']
            self.current_board[self.gridSize-2, self.gridSize - i] = self.block_dict['empty']

        # 4 players in corners
        self.current_board[2, 2] = self.block_dict['player']
        self.current_board[2, self.gridSize-2] = self.block_dict['CPU1']
        self.current_board[self.gridSize-2, 2] = self.block_dict['CPU2']
        self.current_board[self.gridSize-2, self.gridSize-2] = self.block_dict['CPU3']

        return self.current_board


class MainWindow(QWidget):
    def __init__(self, _board, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 20, 850, 750)
        self.setWindowTitle('Bomberman')
        self.board = _board
        self.show()

    def paintEvent(self, e):
        qp.begin(self)
        print("lol")
        for i in range(1, self.board.gridSize):
            for j in range(1, self.board.gridSize):
                if self.board.current_board[i, j] == self.board.block_dict['solidWall']:
                    print(i, j)
                    self.board.block_dict['solidWall'].draw(10, 10)
                # elif mapa.currentMap[i, j] == mapa.blast:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.blastColor)
                # elif mapa.currentMap[i, j] == mapa.destructibleWall:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.DiagCrossPattern,
                #                     self.brickColor)
                # elif mapa.currentMap[i, j] == mapa.empty:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.Dense1Pattern,
                #                     self.grassColor)
                # elif mapa.currentMap[i, j] == mapa.player:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.playerColor)
                # elif mapa.currentMap[i, j] == mapa.CPU1:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.CPU1Color)
                # elif mapa.currentMap[i, j] == mapa.CPU2:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.CPU2Color)
                # elif mapa.currentMap[i, j] == mapa.CPU3:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.CPU3Color)
                # elif mapa.currentMap[i, j] == mapa.grave:
                #     self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.playerColor)
                # elif mapa.currentMap[i, j] == mapa.CPU1grave:
                #     self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU1Color)
                # elif mapa.currentMap[i, j] == mapa.CPU2grave:
                #     self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU2Color)
                # elif mapa.currentMap[i, j] == mapa.CPU3grave:
                #     self.grave_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.CPU3Color)
                # elif mapa.currentMap[i, j] == mapa.bomb:
                #     self.bomb_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.grassColor)
                # elif mapa.currentMap[i, j] == mapa.bombAndPlayer:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.playerColor)
                #     self.bomb_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, self.playerColor)
                # else:
                #     self.rect_brush(qp, 10+i*self.rect_size, 10+j*self.rect_size, self.rect_size, Qt.SolidPattern,
                #                     self.wallColor)

        # # legend - squares with symbols
        # self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+15, 10, Qt.SolidPattern, self.wallColor)
        # self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+30, 10, Qt.SolidPattern, self.blastColor)
        # self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+45, 10, Qt.DiagCrossPattern, self.brickColor)
        # self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+60, 10, Qt.Dense1Pattern, self.grassColor)
        # self.rect_brush(qp, self.rect_size * 40 + 20, self.rect_size+75, 10, Qt.SolidPattern, self.playerColor)
        # self.grave_brush(qp, self.rect_size * 40 + 20, self.rect_size+90, 10, self.playerColor)
        # self.bomb_brush(qp, self.rect_size * 40 + 20, self.rect_size+105, 10, self.grassColor)
        #
        # # legend with captions
        # legend_caption = language_data['game']
        #
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+25, legend_caption['wall'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+40, legend_caption['blast'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+55, legend_caption['destructible_wall'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+70, legend_caption['empty_space'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+85, legend_caption['player'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+100, legend_caption['grave'])
        # qp.drawText(self.rect_size * 40 + 40, self.rect_size+115, legend_caption['bomb'])

        qp.end()


if __name__ == '__main__':
    language_data = json.load(open('./localizations/polish.json'))
    current_board = Board(40)
    current_board.generate_board()

    delta_time = 100
    app = QApplication(sys.argv)
    mw = MainWindow(current_board)
    mw.repaint()

    timer = QTimer()
    timer.start(delta_time)
    sys.exit(app.exec_())
