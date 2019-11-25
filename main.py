import sys
from PySide2 import QtCore, QtWidgets, QtGui
from trivia import solver

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setFixedSize(QtCore.QSize(640,450))
        self.setWindowTitle('Solver')

        self.button = QtWidgets.QPushButton("Solve")
        self.text = QtWidgets.QLabel("This will be a 3 column graph and maybe a small preview of the screenshot")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(solver.run)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    widget = Window()
    widget.show()

    sys.exit(app.exec_())