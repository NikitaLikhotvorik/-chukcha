import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit
import keyword

SCREEN_SIZE = [1200, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = "30.536280"
        self.lat = "59.774005"
        self.mv = 0.1
        self.delta = "9"
        self.map_type = 'map'
        self.map_file = "map.png"
        self.pts = []
        self.pts.append(str(self.lon + ',' + self.lat))
        self.ptsres = '~'.join(self.pts)
        self.initUI()
        self.getImage()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

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

        self.button4 = QPushButton(self)
        self.button4.setText("Искать")
        self.button4.move(950, 50)
        self.button4.clicked.connect(self.search_clicked)

        self.tx = QTextEdit(self)
        self.tx.move(670, 50)

    def getImage(self, delta_type=None, map_type='map'):
        api_server = "http://static-maps.yandex.ru/1.x/?"
        if delta_type is not None and int(self.delta) - 1 >= 0 and delta_type == '-':
            self.delta = str(int(self.delta) - 1)
        elif delta_type is not None and int(self.delta) + 1 <= 17 and delta_type == '+':
            self.delta = str(int(self.delta) + 1)

        self.params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.delta,
            "l": map_type,
            "pt": self.ptsres
        }

        response = requests.get(api_server, params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def button1_clicked(self):
        self.getImage(map_type='map')
        self.map_type = 'map'
        self.update()

    def button2_clicked(self):
        self.getImage(map_type="sat")
        self.map_type = 'sat'
        self.update()

    def button3_clicked(self):
        self.getImage(map_type="skl")
        self.map_type = 'skl'
        self.update()

    def search_clicked(self):
        geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                           f"&geocode={self.tx.toPlainText()}&format=json"

        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.lat = toponym_coodrinates.split()[1]
            self.lon = toponym_coodrinates.split()[0]
            self.params['z'] = 9
            self.pts.append(str(self.lon + ',' + self.lat))
            self.ptsres = '~'.join(self.pts)
            self.params["pt"] = self.ptsres
            print(self.ptsres)
            self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&z={self.params['z']}&l={self.params['l']}" \
                               f"&pt={self.ptsres}"
        response = requests.get(self.map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = 'map.png'
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.getImage(map_type=self.map_type, delta_type='+')
        if event.key() == Qt.Key_PageDown:
            self.getImage(map_type=self.map_type, delta_type='-')
        if event.key() == Qt.Key_S:
            self.lat = float(self.lat) - self.mv
        if event.key() == Qt.Key_W:
            self.lat = float(self.lat) + self.mv
        if event.key() == Qt.Key_D:
            self.lon = float(self.lon) + self.mv
        if event.key() == Qt.Key_A:
            self.lon = float(self.lon) - self.mv
        self.update()
        self.getImage(map_type=self.map_type)
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