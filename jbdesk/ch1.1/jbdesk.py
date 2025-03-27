import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLabel, QGroupBox, QMenuBar, QMenu, QStatusBar
from PyQt5.QtCore import Qt


class JbDeskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 메뉴 바 생성
        self.menu_bar = QMenuBar(self)
        tool_menu = self.menu_bar.addMenu("변환")

        self.action_remove_blank = tool_menu.addAction("공백 줄 제거")
        self.action_to_upper = tool_menu.addAction("대문자로")

        self.action_remove_blank.triggered.connect(lambda: self.set_mode("공백 줄 제거"))
        self.action_to_upper.triggered.connect(lambda: self.set_mode("대문자로"))

        layout.addWidget(self.menu_bar)

        # 첫째 라인: 선택한 Tool 기능 텍스트 표시
        self.tool_label = QLabel("공백 줄 제거", self)
        layout.addWidget(self.tool_label)

        # 둘째 라인: Input GroupBox와 TextEdit
        self.input_groupbox = QGroupBox("입력", self)
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit(self)
        input_layout.addWidget(self.input_text)
        self.input_groupbox.setLayout(input_layout)
        layout.addWidget(self.input_groupbox)

        # 세 번째 라인: 변환 버튼
        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("변환", self)
        self.convert_button.setFixedSize(50, 30)
        self.convert_button.clicked.connect(self.convert_text)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)

        # 다섯째 라인: Output GroupBox와 TextEdit
        self.output_groupbox = QGroupBox("출력", self)
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        self.output_groupbox.setLayout(output_layout)
        layout.addWidget(self.output_groupbox)

        self.set_mode("공백 줄 제거")
        self.setLayout(layout)
        self.setWindowTitle("JbDesk")
        self.setGeometry(300, 300, 1200, 900)

    def set_mode(self, mode):
        self.mode = mode
        self.tool_label.setText(mode)
        self.input_text.clear()
        self.output_text.clear()

    def convert_text(self):
        text = self.input_text.toPlainText()

        if self.mode == "공백 줄 제거":
            result = '\n'.join([line for line in text.splitlines() if line.strip()])
        elif self.mode == "대문자로":
            result = text.upper()
        else:
            result = text

        self.output_text.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JbDeskApp()
    ex.show()
    sys.exit(app.exec_())
