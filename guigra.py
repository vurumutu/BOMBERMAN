import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt


class Example(QWidget):
    rectSize = 15
    wallColor = QColor(200, 200, 20)
    brickColor = QColor(150, 25, 14)
    grassColor = QColor(0, 92, 9)
    playerColor = QColor(238, 193, 189)
    CPU1Color = QColor(100, 200, 240)
    CPU2Color = QColor(150, 150, 140)
    CPU3Color = QColor(200, 100, 40)
    bombColor = QColor(200, 100, 40)
    blastColor = QColor(255, 255, 255)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 50, 750, 650)
        self.setWindowTitle('Graficzny Bomberman')
        self.show()

    def wallBrush(self, qp, startPointX, startPointY, rectSize):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.wallColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)

    def brickBrush(self, qp, startPointX, startPointY, rectSize):
        brush = QBrush(Qt.DiagCrossPattern)
        brush.setColor(self.brickColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)

    def emptyBrush(self, qp, startPointX, startPointY, rectSize):
        brush = QBrush(Qt.Dense4Pattern)
        brush.setColor(self.grassColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)

    def playerBrush(self, qp, startPointX, startPointY, rectSize, currentColor):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(currentColor)
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

    def blastBrush(self, qp, startPointX, startPointY, rectSize):
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.blastColor)
        qp.setBrush(brush)
        qp.drawRect(startPointX, startPointY, rectSize, rectSize)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for i in range(1, 40):
            for j in range(1, 40):
                if i % 2 == 0 and j % 2 == 0:
                    self.wallBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize)
                elif i % 4 == 0:
                    self.blastBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize)
                elif j % 4 == 0:
                    self.graveBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.playerColor)
                elif i % 2 == 0:
                    self.brickBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize)
                elif j % 2 == 0:
                    self.emptyBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize)
                else:
                    self.playerBrush(qp, 10+i*self.rectSize, 10+j*self.rectSize, self.rectSize, self.CPU1Color)

        # tutaj robimy legendę - bloczki
        self.wallBrush(qp, self.rectSize * 40 + 20, self.rectSize+15, 10)
        self.blastBrush(qp, self.rectSize * 40 + 20, self.rectSize+30, 10)
        self.brickBrush(qp, self.rectSize * 40 + 20, self.rectSize+45, 10)
        self.emptyBrush(qp, self.rectSize * 40 + 20, self.rectSize+60, 10)
        self.playerBrush(qp, self.rectSize * 40 + 20, self.rectSize+75, 10, self.playerColor)
        self.graveBrush(qp, self.rectSize * 40 + 20, self.rectSize+90, 10, self.playerColor)

        self.playerBrush(qp, self.rectSize * 40 + 20, self.rectSize+105, 10, self.playerColor)
        self.playerBrush(qp, self.rectSize * 40 + 20, self.rectSize+120, 10, self.CPU1Color)
        self.playerBrush(qp, self.rectSize * 40 + 20, self.rectSize+135, 10, self.CPU2Color)
        self.playerBrush(qp, self.rectSize * 40 + 20, self.rectSize+150, 10, self.CPU3Color)

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

        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())