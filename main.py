"""import os
import sys
import pygame
import requests
map_request = "http://static-maps.yandex.ru/1.x/?ll=30.536280%2C59.774005&spn=10,10&l=map"
response = requests.get(map_request)
if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
"""
import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

SCREEN_SIZE = [1200, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = "30.536280"
        self.lat = "59.774005"
        self.mv = 0.1
        self.delta = "9"
        self.getImage()
        self.initUI()

    def getImage(self, delta_type=None, map_type='map'):
        api_server = "http://static-maps.yandex.ru/1.x/"
        if delta_type is not None and int(self.delta) - 1 >= 0 and delta_type == '-':
            self.delta = str(int(self.delta) - 1)
        elif delta_type is not None and int(self.delta) + 1 <= 17 and delta_type == '+':
            self.delta = str(int(self.delta) + 1)

        self.params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.delta,
            "l": map_type
        }
        response = requests.get(api_server, params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def button1_clicked(self):
        self.getImage(map_type='map')
        self.pixmap = QPixmap("map.png")
        self.image.setPixmap(self.pixmap)

    def button2_clicked(self):
        self.getImage(map_type="sat")
        self.pixmap = QPixmap("map.png")
        self.image.setPixmap(self.pixmap)

    def button3_clicked(self):
        self.getImage(map_type="skl")
        self.pixmap = QPixmap("map.png")
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(50, 50)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.button1 = QPushButton(self)
        self.button1.setText("Схема")
        self.button1.move(1050, 50)
        self.button1.clicked.connect(self.button1_clicked)

        self.button2 = QPushButton(self)
        self.button2.setText("Спутник")
        self.button2.move(1050, 150)
        self.button2.clicked.connect(self.button2_clicked)

        self.button3 = QPushButton(self)
        self.button3.setText("Гибрид")
        self.button3.move(1050, 250)
        self.button3.clicked.connect(self.button3_clicked)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.getImage(delta_type='+')
        if event.key() == Qt.Key_PageDown:
            self.getImage(delta_type='-')
        if event.key() == Qt.Key_Down:
            self.lat = float(self.lat) - self.mv
        if event.key() == Qt.Key_Up:
            self.lat = float(self.lat) + self.mv
        if event.key() == Qt.Key_Right:
            self.lon = float(self.lon) + self.mv
        if event.key() == Qt.Key_Left:
            self.lon = float(self.lon) - self.mv
        self.update()
        self.getImage()
        self.pixmap = QPixmap("map.png")
        self.image.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())