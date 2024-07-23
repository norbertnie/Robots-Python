import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, \
    QHBoxLayout, QGridLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt


class Robot:
    def __init__(self, id, name, status, battery_level, lokalizacja, pozycja, magazyn, stan, image_path):
        self.id = id
        self.name = name
        self.status = status
        self.battery_level = battery_level
        self.lokalizacja = lokalizacja
        self.pozycja = pozycja
        self.magazyn = magazyn
        self.stan = stan
        self.image_path = image_path


class RobotManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Robot Manager')
        self.setGeometry(100, 100, 800, 600)

        self.robots = []
        self.selected_robot = None
        self.statuses = [
            "W trakcie akcji",
            "Dostępny",
            "Niedostępny zajęty",
            "Niedostępny Potrzebny asystent"
        ]

        self.status_to_image = {
            "Dostępny": os.path.abspath("./.venv/images/check.png"),
            "W trakcie akcji": os.path.abspath("./.venv/images/arrows.png"),
            "Niedostępny zajęty": os.path.abspath("./.venv/images/warning.png"),
            "Niedostępny Potrzebny asystent": os.path.abspath("./.venv/images/error.png")
        }

        self.status_to_color = {
            "Dostępny": "green",
            "W trakcie akcji": "blue",
            "Niedostępny zajęty": "orange",
            "Niedostępny Potrzebny asystent": "red"
        }

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        self.label = QLabel('Robot')
        self.top_layout.addWidget(self.label)

        self.prev_button = QPushButton('<')
        self.prev_button.clicked.connect(self.select_previous_robot)
        self.top_layout.addWidget(self.prev_button)

        self.robot_selector = QComboBox()
        self.robot_selector.currentIndexChanged.connect(self.on_robot_selected)
        self.top_layout.addWidget(self.robot_selector)

        self.next_button = QPushButton('>')
        self.next_button.clicked.connect(self.select_next_robot)
        self.top_layout.addWidget(self.next_button)

        self.load_button = QPushButton('Load Robots')
        self.load_button.clicked.connect(self.load_robots)
        self.top_layout.addWidget(self.load_button)

        self.update_button = QPushButton('Update Robot')
        self.update_button.clicked.connect(self.update_robot)
        self.top_layout.addWidget(self.update_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def load_robots(self):
        self.robots = [
            Robot(1, 'Robot 1', 'Dostępny', 100, 'Location 1', 'Position 1', 'Magazyn 1', 'Stan 1',
                  os.path.abspath("./.venv/images/robot_1_black.png")),
            Robot(2, 'Robot 2', 'Niedostępny zajęty', 90, 'Location 2', 'Position 2', 'Magazyn 2', 'Stan 2',
                  os.path.abspath("./.venv/images/robot_2_black.png")),
            Robot(3, 'Robot 3', 'Niedostępny Potrzebny asystent', 80, 'Location 3', 'Position 3', 'Magazyn 3', 'Stan 3',
                  os.path.abspath("./.venv/images/robot_3_black.png")),
            # Add more robots here
        ]
        self.update_robot_selector()
        self.update_robot_tiles()

    def update_robot_selector(self):
        self.robot_selector.clear()
        self.robot_selector.addItem('Wszystkie')
        for robot in self.robots:
            self.robot_selector.addItem(robot.name)

    def update_robot_tiles(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        robots_to_display = self.robots if self.selected_robot is None else [self.selected_robot]

        for i, robot in enumerate(robots_to_display):
            tile = self.create_robot_tile(robot)
            self.scroll_layout.addWidget(tile, i // 2, i % 2)

    def create_robot_tile(self, robot):
        tile = QFrame()
        tile.setFrameShape(QFrame.Box)
        tile.setLineWidth(2)
        layout = QVBoxLayout(tile)
        layout.setAlignment(Qt.AlignTop)

        border_color = self.status_to_color.get(robot.status, "black")
        tile.setStyleSheet(f"QFrame {{ border: 2px solid {border_color}; }}")

        image_label = QLabel()
        pixmap = QPixmap(robot.image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
        layout.addWidget(image_label, alignment=Qt.AlignCenter)

        name_label = QLabel(f'Name: {robot.name}')
        layout.addWidget(name_label)

        status_label = QLabel(f'Status: {robot.status}')
        layout.addWidget(status_label)

        status_image_label = QLabel()
        status_pixmap = QPixmap(self.status_to_image.get(robot.status))
        if not status_pixmap.isNull():
            status_image_label.setPixmap(status_pixmap.scaled(20, 20, Qt.KeepAspectRatio))
        layout.addWidget(status_image_label, alignment=Qt.AlignCenter)

        battery_label = QLabel(f'Battery Level: {robot.battery_level}%')
        layout.addWidget(battery_label)

        location_label = QLabel(f'Lokalizacja: {robot.lokalizacja}')
        layout.addWidget(location_label)

        position_label = QLabel(f'Pozycja: {robot.pozycja}')
        layout.addWidget(position_label)

        magazyn_label = QLabel(f'Magazyn: {robot.magazyn}')
        layout.addWidget(magazyn_label)

        stan_label = QLabel(f'Stan: {robot.stan}')
        layout.addWidget(stan_label)

        return tile

    def on_robot_selected(self, index):
        if index == 0:
            self.selected_robot = None
        else:
            self.selected_robot = self.robots[index - 1]
        self.update_robot_tiles()

    def select_previous_robot(self):
        current_index = self.robot_selector.currentIndex()
        if current_index > 0:
            self.robot_selector.setCurrentIndex(current_index - 1)

    def select_next_robot(self):
        current_index = self.robot_selector.currentIndex()
        if current_index < self.robot_selector.count() - 1:
            self.robot_selector.setCurrentIndex(current_index + 1)

    def update_robot(self):
        if self.selected_robot:
            new_statuses = [status for status in self.statuses if status != self.selected_robot.status]
            self.selected_robot.status = random.choice(new_statuses)
            self.selected_robot.battery_level = max(0, self.selected_robot.battery_level - 10)
            self.selected_robot.lokalizacja = 'Updated Location'
            self.selected_robot.pozycja = 'Updated Position'
            self.selected_robot.magazyn = 'Updated Magazyn'
            self.selected_robot.stan = 'Updated Stan'
            self.update_robot_tiles()
        else:
            for robot in self.robots:
                new_statuses = [status for status in self.statuses if status != robot.status]
                robot.status = random.choice(new_statuses)
                robot.battery_level = max(0, robot.battery_level - 10)
                robot.lokalizacja = 'Updated Location'
                robot.pozycja = 'Updated Position'
                robot.magazyn = 'Updated Magazyn'
                robot.stan = 'Updated Stan'
            self.update_robot_tiles()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RobotManager()
    mainWin.show()
    sys.exit(app.exec_())
