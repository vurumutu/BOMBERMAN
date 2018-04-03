import numpy as np
from random import randint
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer
import json
from abc import ABC, abstractmethod

qp = QPainter()


class Block(ABC):
    def __init__(self, _name, _pattern, _caption, _color, _id):
        self.name = _name
        self.pattern = _pattern
        self.caption = _caption
        self.color = _color
        self.id = _id
        self.rect_size = 17

    def change_caption(self, new_caption):
        self.caption = new_caption

    def change_brush(self, new_pattern):
        self.pattern = new_pattern

    def change_color(self, new_color):
        self.color = new_color

    def change_pattern(self, new_color):
        self.color = new_color

    def draw_caption(self, start_point_x, start_point_y):
        qp.drawText(start_point_x, start_point_y, self.caption)

    @abstractmethod
    def draw_block(self, start_point_x, start_point_y):
        pass


class OrdinaryBlock(Block):
    def __init__(self, _name, _pattern, _caption, _color, _id):
        super().__init__(_name, _pattern, _caption, _color, _id)

    def draw_block(self, start_point_x, start_point_y):
        brush = QBrush(self.pattern)
        brush.setColor(self.color)
        qp.setBrush(brush)
        qp.drawRect(start_point_x, start_point_y, self.rect_size, self.rect_size)


class GraveBlock(Block):
    def __init__(self, _name, _pattern, _caption, _color, _id):
        super().__init__(_name, _pattern, _caption, _color, _id)

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
    def __init__(self, _name, _pattern, _caption, _color, _id):
        super().__init__(_name, _pattern, _caption, _color, _id)

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
        'player':               OrdinaryBlock("player", Qt.SolidPattern, "player", QColor(238, 193, 189), 0),
        'CPU1':                 OrdinaryBlock("CPU1", Qt.SolidPattern, "CPU1", QColor(100, 200, 240), 1),
        'CPU2':                 OrdinaryBlock("CPU2", Qt.SolidPattern, "CPU2", QColor(150, 150, 140), 2),
        'CPU3':                 OrdinaryBlock("CPU3", Qt.SolidPattern, "CPU3", QColor(200, 100, 40), 3),
        'solidWall':            OrdinaryBlock("solidWall", Qt.SolidPattern, "solidWall", QColor(200, 200, 20), 4),
        'destructibleWall':     OrdinaryBlock("destructibleWall", Qt.DiagCrossPattern, "destW", QColor(150, 25, 14), 5),
        'empty':                OrdinaryBlock("empty", Qt.Dense1Pattern, "empty", QColor(0, 92, 9), 6),
        'bomb':                 BombBlock("bomb", Qt.SolidPattern, "bomb", QColor(0, 0, 0), 7),
        'grave':                GraveBlock("grave", Qt.SolidPattern, "grave", QColor(238, 193, 189), 8),
        'bombAndPlayer':        OrdinaryBlock("bombAndPlayer", Qt.SolidPattern, "bombandp", QColor(238, 193, 189), 9),
        'blast':                OrdinaryBlock("blast", Qt.SolidPattern, "blast", QColor(255, 255, 255), 9)
    }

    def __init__(self, _grid_size):
        self.gridSize = _grid_size
        self.shape = (self.gridSize, self.gridSize)
        self.current_board = np.empty(self.shape, dtype=object)

    def generate_board(self):
        for i in range(1, self.gridSize):
            for j in range(1, self.gridSize):
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
                    self.board.block_dict['solidWall'].draw_block(10 + i*self.board.block_dict['solidWall'].rect_size,
                                                                  10 + j*self.board.block_dict['solidWall'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['blast']:
                    self.board.block_dict['blast'].draw_block(10 + i*self.board.block_dict['blast'].rect_size,
                                                                  10 + j*self.board.block_dict['blast'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['destructibleWall']:
                    self.board.block_dict['destructibleWall'].draw_block(10 + i*self.board.block_dict['destructibleWall'].rect_size,
                                                                  10 + j*self.board.block_dict['destructibleWall'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['grave']:
                    self.board.block_dict['grave'].draw_block(10 + i*self.board.block_dict['grave'].rect_size,
                                                              10 + j*self.board.block_dict['grave'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['bomb']:
                    self.board.block_dict['bomb'].draw_block(10 + i*self.board.block_dict['bomb'].rect_size,
                                                             10 + j*self.board.block_dict['bomb'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['empty']:
                    self.board.block_dict['empty'].draw_block(10 + i*self.board.block_dict['empty'].rect_size,
                                                              10 + j*self.board.block_dict['empty'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['player']:
                    self.board.block_dict['player'].draw_block(10 + i*self.board.block_dict['player'].rect_size,
                                                              10 + j*self.board.block_dict['player'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['CPU1']:
                    self.board.block_dict['CPU1'].draw_block(10 + i*self.board.block_dict['CPU1'].rect_size,
                                                             10 + j*self.board.block_dict['CPU1'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['CPU2']:
                    self.board.block_dict['CPU2'].draw_block(10 + i*self.board.block_dict['CPU2'].rect_size,
                                                             10 + j*self.board.block_dict['CPU2'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['CPU3']:
                    self.board.block_dict['CPU3'].draw_block(10 + i*self.board.block_dict['CPU3'].rect_size,
                                                             10 + j*self.board.block_dict['CPU3'].rect_size)
                elif self.board.current_board[i, j] == self.board.block_dict['bombAndPlayer']:
                    self.board.block_dict['bombAndPlayer'].draw_block(10 + i*self.board.block_dict['bombAndPlayer'].rect_size,
                                                              10 + j*self.board.block_dict['bombAndPlayer'].rect_size)

        # legend
        i = 20
        for key, value in self.board.block_dict.items():
            value.draw_block(value.rect_size*self.board.gridSize + 20, value.rect_size + i*2)
            value.draw_caption(value.rect_size*self.board.gridSize + 40, value.rect_size + i*2 + 12)
            i += 20

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
