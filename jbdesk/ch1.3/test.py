import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QTextEdit,
                             QVBoxLayout, QWidget, QPushButton, QLabel,
                             QGroupBox, QComboBox, QHBoxLayout)
from PyQt5.QtCore import Qt
import pytz
from datetime import datetime


class JbDesk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JbDesk")
        self.setGeometry(100, 100, 600, 400)

        self.selected_function = ""
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.main_layout = QVBoxLayout()

        self.tool_label = QLabel("선택된 기능: ", self)
        self.main_layout.addWidget(self.tool_label)

        self.input_group = QGroupBox("입력")
        self.input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_layout.addWidget(self.input_text)
        self.input_group.setLayout(self.input_layout)
        self.main_layout.addWidget(self.input_group)

        self.convert_button = QPushButton("변환")
        self.convert_button.setFixedWidth(self.convert_button.fontMetrics().width("변환") + 20)
        self.convert_button.clicked.connect(self.perform_conversion)
        self.main_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)

        self.output_group = QGroupBox("출력")
        self.output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_layout.addWidget(self.output_text)
        self.output_group.setLayout(self.output_layout)
        self.main_layout.addWidget(self.output_group)

        self.centralWidget.setLayout(self.main_layout)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        line_menu = menu_bar.addMenu("줄단위")
        line_action = QAction("줄 공백 제거", self)
        line_action.triggered.connect(lambda: self.set_function("줄 공백 제거"))
        line_menu.addAction(line_action)

        notation_menu = menu_bar.addMenu("표기법")
        notations = ["camelCase", "snake_case", "PascalCase", "SCREAMING_SNAKE_CASE", "Train-Case", "dot.notation"]
        for notation in notations:
            action = QAction(notation, self)
            action.triggered.connect(lambda checked, n=notation: self.set_function(n))
            notation_menu.addAction(action)

        timezone_menu = menu_bar.addMenu("TimeZone")
        timezone_action = QAction("로그 TimeZone 변환", self)
        timezone_action.triggered.connect(lambda: self.set_function("로그 TimeZone 변환"))
        timezone_menu.addAction(timezone_action)

    def set_function(self, function):
        self.selected_function = function
        self.tool_label.setText(f"선택된 기능: {function}")

        if function == "로그 TimeZone 변환":
            self.setup_timezone_conversion()
        else:
            self.setup_text_conversion()

    def setup_text_conversion(self):
        self.clear_layout()
        self.main_layout.insertWidget(1, self.input_group)
        self.main_layout.insertWidget(2, self.convert_button, alignment=Qt.AlignCenter)
        self.main_layout.insertWidget(3, self.output_group)

    def setup_timezone_conversion(self):
        self.clear_layout()

        self.timezone_layout = QHBoxLayout()
        self.from_label = QLabel("원본 TimeZone:")
        self.from_timezone = QComboBox()
        self.from_timezone.addItems(["US/Pacific", "Asia/Seoul"])
        self.to_label = QLabel("목표 TimeZone:")
        self.to_timezone = QComboBox()
        self.to_timezone.addItems(["US/Pacific", "Asia/Seoul"])

        self.timezone_layout.addWidget(self.from_label)
        self.timezone_layout.addWidget(self.from_timezone)
        self.timezone_layout.addWidget(self.to_label)
        self.timezone_layout.addWidget(self.to_timezone)
        self.timezone_layout.addWidget(self.convert_button)

        self.main_layout.insertWidget(1, self.input_group)
        self.main_layout.insertLayout(2, self.timezone_layout)
        self.main_layout.insertWidget(3, self.output_group)

    def clear_layout(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().setParent(None)

    def perform_conversion(self):
        text = self.input_text.toPlainText()

        if self.selected_function == "줄 공백 제거":
            result = "\n".join(line.strip() for line in text.split("\n"))
        elif self.selected_function == "camelCase":
            words = re.split(r'\W+', text)
            result = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif self.selected_function == "snake_case":
            result = "_".join(re.split(r'\W+', text)).lower()
        elif self.selected_function == "PascalCase":
            result = "".join(word.capitalize() for word in re.split(r'\W+', text))
        elif self.selected_function == "SCREAMING_SNAKE_CASE":
            result = "_".join(re.split(r'\W+', text)).upper()
        elif self.selected_function == "Train-Case":
            result = "-".join(word.capitalize() for word in re.split(r'\W+', text))
        elif self.selected_function == "dot.notation":
            result = ".".join(re.split(r'\W+', text)).lower()
        elif self.selected_function == "로그 TimeZone 변환":
            try:
                dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
                from_tz = pytz.timezone(self.from_timezone.currentText())
                to_tz = pytz.timezone(self.to_timezone.currentText())
                dt = from_tz.localize(dt).astimezone(to_tz)
                result = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                result = "잘못된 날짜 형식입니다. (예: 2025-03-27 12:30:45)"
        else:
            result = "선택된 기능이 없습니다."

        self.output_text.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JbDesk()
    ex.show()
    sys.exit(app.exec_())
