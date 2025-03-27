import re
import sys

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QGroupBox, QHBoxLayout

import pytz

DATE_PATTERNS = [
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3}', '%Y-%m-%d %H:%M:%S %Z'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '%Y-%m-%d %H:%M:%S'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', '%Y-%m-%d %H:%M'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M:%S %p'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M %p'),
    (r'\d{4}-\d{1,2}-\d{1,2} [APap][Mm] \d{1,2}:\d{1,2}:\d{1,2}', '%Y-%m-%d %p %I:%M:%S'),
    (r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%Y-%m-%d %I:%M:%S %p'),
    (r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [-+]\d{4}', '%d/%b/%Y:%H:%M:%S %z')
]

def convert_log_timezone(log_text: str, source_timezone: str, dest_timezone: str) -> str:
    for pattern, date_format in DATE_PATTERNS:
        match = re.search(pattern, log_text)
        if match:
            datetime_str = match.group()
            try:
                dt = datetime.strptime(datetime_str, date_format)
                if '%z' not in date_format and '%Z' not in date_format:
                    source_tz = pytz.timezone(source_timezone)
                    dt = source_tz.localize(dt)
                dt = dt.astimezone(pytz.timezone(dest_timezone))
                new_datetime_str = dt.strftime(date_format)
                log_text = log_text.replace(datetime_str, new_datetime_str)
            except ValueError:
                continue
    return log_text

def remove_line_spaces(text):
    return '\n'.join([line for line in text.splitlines() if line.strip()])


def to_snake_case(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)  # camelCase -> snake_case
    text = re.sub(r'[-\s]', '_', text)  # kebab-case, space -> snake_case
    return text.lower()


def to_camel_case(text):
    words = to_snake_case(text).split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(text):
    words = to_snake_case(text).split('_')
    return ''.join(word.capitalize() for word in words)


def to_kebab_case(text):
    return to_snake_case(text).replace('_', '-')


def to_screaming_snake_case(text):
    return to_snake_case(text).upper()


def to_train_case(text):
    return '-'.join(word.capitalize() for word in to_snake_case(text).split('_'))


def to_dot_notation(text):
    words = re.split(r'[\s_\-]+', text)
    return ".".join(word.lower() for word in words)


class JbDesk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_option = "줄 공백 제거"  # 기본값
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JbDesk")
        self.setGeometry(300, 300, 1200, 900)

        # 메뉴바 생성
        menubar = self.menuBar()

        # "줄단위" 메뉴
        line_menu = menubar.addMenu("줄단위")
        strip_action = QAction("줄 공백 제거", self)
        strip_action.triggered.connect(lambda: self.set_option("줄 공백 제거"))
        line_menu.addAction(strip_action)

        # "표기법" 메뉴
        format_menu = menubar.addMenu("표기법")
        formats = [
            "camelCase", "snake_case", "PascalCase", "SCREAMING_SNAKE_CASE",
            "kebab-case", "Train-Case", "dot.notation"
        ]
        for fmt in formats:
            action = QAction(fmt, self)
            action.triggered.connect(lambda checked, f=fmt: self.set_option(f))
            format_menu.addAction(action)

        # 메인 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 선택된 기능 표시
        self.option_label = QLabel(f"선택된 기능: {self.selected_option}")
        layout.addWidget(self.option_label)

        # 입력 GroupBox
        input_group = QGroupBox("입력")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 변환 버튼
        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("변환")
        self.convert_button.setFixedSize(50, 30)
        self.convert_button.clicked.connect(self.convert_text)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)

        # 출력 GroupBox
        output_group = QGroupBox("출력")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        central_widget.setLayout(layout)

    def set_option(self, option):
        """메뉴에서 선택된 옵션을 설정"""
        self.selected_option = option
        self.option_label.setText(f"선택된 기능: {self.selected_option}")

    def convert_text(self):
        """선택된 옵션에 따라 입력 텍스트를 변환"""
        text = self.input_text.toPlainText()
        if not text:
            self.output_text.setPlainText("입력 값이 없습니다.")
            return

        if self.selected_option == "줄 공백 제거":
            result = self.remove_line_spaces(text)
        elif self.selected_option == "camelCase":
            result = self.to_camel_case(text)
        elif self.selected_option == "snake_case":
            result = self.to_snake_case(text)
        elif self.selected_option == "PascalCase":
            result = self.to_pascal_case(text)
        elif self.selected_option == "SCREAMING_SNAKE_CASE":
            result = self.to_screaming_snake_case(text)
        elif self.selected_option == "kebab-case":
            result = self.to_kebab_case(text)
        elif self.selected_option == "Train-Case":
            result = self.to_train_case(text)
        elif self.selected_option == "dot.notation":
            result = self.to_dot_notation(text)
        else:
            result = "알 수 없는 변환 옵션입니다."

        self.output_text.setPlainText(result)

    @staticmethod
    def remove_line_spaces(text):
        """줄 공백 제거"""
        return remove_line_spaces(text)

    @staticmethod
    def to_camel_case(text):
        """camelCase 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_camel_case(line) for line in lines])

    @staticmethod
    def to_snake_case(text):
        """snake_case 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_snake_case(line) for line in lines])

    @staticmethod
    def to_pascal_case(text):
        """PascalCase 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_pascal_case(line) for line in lines])

    @staticmethod
    def to_screaming_snake_case(text):
        """SCREAMING_SNAKE_CASE 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_screaming_snake_case(line) for line in lines])

    @staticmethod
    def to_kebab_case(text):
        """kebab-case 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_kebab_case(line) for line in lines])

    @staticmethod
    def to_train_case(text):
        """Train-Case 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_train_case(line) for line in lines])

    @staticmethod
    def to_dot_notation(text):
        """dot.notation 변환"""
        lines = text.strip().split("\n")  # 줄 단위로 분리
        return "\n".join([to_dot_notation(line) for line in lines])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JbDesk()
    window.show()
    sys.exit(app.exec_())
