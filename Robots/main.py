import sys
import random
from PyQt5.QtWidgets import *

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

        self.robot_list = QListWidget()
        self.layout.addWidget(self.robot_list)

    def load_robots(self):
        self.robots = [
            Robot(1, 'Robot 1', 'Dostępny', 100, 'Location 1', 'Position 1', 'Magazyn 1', 'Stan 1', 'robot_icon.png'),
            Robot(2, 'Robot 2', 'Niedostępny zajęty', 90, 'Location 2', 'Position 2', 'Magazyn 2', 'Stan 2', 'robot_icon.png'),
            # Add more robots here
        ]
        self.update_robot_list()
        self.robot_selector.addItem('Wszystkie')
        for robot in self.robots:
            self.robot_selector.addItem(robot.name)

    def update_robot_list(self):
        self.robot_list.clear()
        for robot in self.robots:
            self.robot_list.addItem(f'{robot.name} - {robot.status}')

    def on_robot_selected(self, index):
        if index == 0:
            self.selected_robot = None
            self.update_robot_list()
        else:
            self.selected_robot = self.robots[index - 1]
            self.robot_list.clear()
            self.robot_list.addItem(f'{self.selected_robot.name} - {self.selected_robot.status}')

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
            self.update_robot_list()
        else:
            QMessageBox.information(self, 'Info', 'Select a robot to update')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RobotManager()
    mainWin.show()
    sys.exit(app.exec_())
