import sys
from PySide2 import QtCore, QtWidgets, QtGui
from pyqtgraph import BarGraphItem, plot, PlotWidget
from trivia import solver
import csv

class Window(QtWidgets.QWidget):
    """
    The Window class is in charge of drawing a GUI, receiving the data from the actual
    solver, and display it.
    """

    with open('config.csv') as csv_file:
        configurations = list(csv.reader(csv_file, delimiter=','))

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setFixedSize(QtCore.QSize(640, 450))
        self.setWindowTitle('Trivia Solver')

        self.solve_button = QtWidgets.QPushButton("Solve")
        self.solve_button.setDefault(True)
        self.save_button = QtWidgets.QPushButton('Save to samples')
        self.clear_button = QtWidgets.QPushButton('Clear')
        self.screenshot = QtWidgets.QLabel()
        self.screenshot.setWordWrap(True)
        self.screenshot.setAlignment(QtCore.Qt.AlignCenter)

        text_recognition_form = QtWidgets.QFormLayout()
        text_recognition_form.setAlignment(QtCore.Qt.AlignTop)
        self.configuration_combobox = QtWidgets.QComboBox()
        self.load_configurations()
        self.configuration_combobox.currentIndexChanged.connect(self.config_changed)
        text_recognition_form.addRow(self.configuration_combobox)
        self.question_text = QtWidgets.QTextEdit()
        self.question_text.setReadOnly(True)
        self.question_text.setMaximumHeight(100)
        text_recognition_form.addRow('Question', self.question_text)
        self.answer1_text = QtWidgets.QLineEdit()
        self.answer1_text.setReadOnly(True)
        text_recognition_form.addRow('Answer 1', self.answer1_text)
        self.answer2_text = QtWidgets.QLineEdit()
        self.answer2_text.setReadOnly(True)
        text_recognition_form.addRow('Answer 2', self.answer2_text)
        self.answer3_text = QtWidgets.QLineEdit()
        self.answer3_text.setReadOnly(True)
        text_recognition_form.addRow('Answer 3', self.answer3_text)

        results_layout = QtWidgets.QVBoxLayout()
        results_layout.addLayout(text_recognition_form)

        self.chart = PlotWidget()

        results_layout.addWidget(QtWidgets.QFrame())
        results_layout.addWidget(self.chart)

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.addWidget(self.screenshot)
        content_layout.addLayout(results_layout)

        layout = QtWidgets.QVBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximumHeight(20)
        layout.addWidget(self.progress_bar)
        layout.addLayout(content_layout)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.show_screenshot = QtWidgets.QCheckBox('Show Screenshot')
        buttons_layout.addWidget(self.show_screenshot)
        buttons_layout.addWidget(self.solve_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.setAlignment(QtCore.Qt.AlignRight)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Actions performed:
        self.solve_button.clicked.connect(self.run_solver)
        self.save_button.clicked.connect(self.save_to_samples)
        self.clear_button.clicked.connect(self.clear_outputs)

        self.config_changed()
        
        self.s = None
        self.r = solver.Reader()

    def config_changed(self):
        index = self.configuration_combobox.currentIndex()
        self.r.set_configuration(self.configurations[index+1])

    def clear_outputs(self):
        self.screenshot.clear()
        self.progress_bar.setValue(0)
        self.chart.clear()
        self.question_text.clear()
        self.answer1_text.clear()
        self.answer2_text.clear()
        self.answer3_text.clear()

    def run_solver(self):
        self.clear_outputs()

        self.s = solver.ScreenManager()
        self.progress_bar.setValue(5)

        self.s.shot()
        self.progress_bar.setValue(30)

        recognition = self.r.read(self.s.filepath)

        # Show the results in the GUI
        self.question_text.setText(recognition['q'])
        self.answer1_text.setText(recognition['a1'])
        self.answer2_text.setText(recognition['a2'])
        self.answer3_text.setText(recognition['a3'])
        self.progress_bar.setValue(35)

        self.progress_bar.setValue(60)

        # Show the screenshot in display
        if self.show_screenshot.isChecked():
            pixmap = QtGui.QPixmap(self.s.filepath)
            pixmap = pixmap.scaledToHeight(370, aspectMode=QtCore.Qt.KeepAspectRatio)
            self.screenshot.setPixmap(pixmap)
        self.progress_bar.setValue(65)

        # Scrap the internet
        self.progress_bar.setValue(90)

        # Display the results
        self.plot()
        self.progress_bar.setValue(100)

    def save_to_samples(self):
        if self.s is not None:
            self.s.save_to_samples()

    def plot(self):
        y = [100, 400, 240]
        x = [1, 2, 3]
        bars = BarGraphItem(x=x, height=y, width=0.6)
        self.chart.addItem(bars)

    def closeEvent(self, event):
        # clear screenshots not saved in samples
        if self.s is not None:
            self.s.clear_screenshot_dir()

        self.close()

    def load_configurations(self):
        for c in self.configurations[1:]:
                self.configuration_combobox.addItem(f'{c[0]} [{c[1]}] ({c[2]})')

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    widget = Window()  # No input args??
    widget.show()

    sys.exit(app.exec_())
