from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QMainWindow, QLabel


class AnimationWindow(QMainWindow):
    def __init__(self, gate, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("Gate animation")
        self.setFixedSize(500, 500)

        self.gif_label = QLabel(self)
        self.gif_label.setFixedSize(500, 500)

        self.gif_path = gate

        self.__display_gif()

    def __display_gif(self):
        movie = QMovie(self.gif_path)
        self.gif_label.setMovie(movie)
        movie.start()
