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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

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

    def getImage(self, delta_type=None):
        api_server = "http://static-maps.yandex.ru/1.x/"
        if delta_type is not None and int(self.delta) - 1 >= 0 and delta_type == '-':
            self.delta = str(int(self.delta) - 1)
        elif delta_type is not None and int(self.delta) + 1 <= 17 and delta_type == '+':
            self.delta = str(int(self.delta) + 1)

        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.delta,
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(50, 50)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.getImage(delta_type='+')
            self.pixmap = QPixmap("map.png")
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_PageDown:
            self.getImage(delta_type='-')
            self.pixmap = QPixmap("map.png")
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_Down:
            self.lon = int(self.lon) + self.mv
        if event.key() == Qt.Key_Up:
            self.lon = int(self.lon) - self.mv
        if event.key() == Qt.Key_Right:
            self.lat = int(self.lat) + self.mv
        if event.key() == Qt.Key_Left:
            self.lat = int(self.lat) - self.mv
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())