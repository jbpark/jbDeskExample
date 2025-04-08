import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from fabric import Connection

# 서버 및 로그 정보
LOG_SOURCES = [
    {"host_name": "gateway01", "ip": "192.168.56.40", "log_path": "/home/vagrant/gateway.log"},
    {"host_name": "api01",     "ip": "192.168.56.41", "log_path": "/home/vagrant/api.log"},
    {"host_name": "echo01",    "ip": "192.168.56.42", "log_path": "/home/vagrant/echo.log"},
]

# 고정된 SSH 로그인 정보
SSH_USER = "vagrant"
SSH_PASSWORD = "vagrant"

class LogSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TID 로그 검색기")
        self.setGeometry(100, 100, 1000, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # TID 입력 및 버튼
        input_layout = QHBoxLayout()
        self.tid_input = QLineEdit()
        self.tid_input.setPlaceholderText("검색할 TID 입력")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_logs)

        input_layout.addWidget(QLabel("TID:"))
        input_layout.addWidget(self.tid_input)
        input_layout.addWidget(self.search_button)
        layout.addLayout(input_layout)

        # 결과 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Host", "Log Path", "Message"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def search_logs(self):
        tid = self.tid_input.text().strip()
        if not tid:
            return

        self.table.setRowCount(0)
        all_results = []

        for source in LOG_SOURCES:
            try:
                conn = Connection(
                    host=source["ip"],
                    user=SSH_USER,
                    connect_kwargs={"password": SSH_PASSWORD},
                )
                result = conn.run(f"grep {tid} {source['log_path']}", hide=True, warn=True)
                lines = result.stdout.strip().splitlines()

                for line in lines:
                    all_results.append((source["host_name"], source["log_path"], line))

            except Exception as e:
                all_results.append((source["host_name"], source["log_path"], f"❌ {str(e)}"))

        self.populate_table(all_results)

    def populate_table(self, results):
        self.table.setRowCount(len(results))
        for row, (host, path, message) in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(host))
            self.table.setItem(row, 1, QTableWidgetItem(path))
            msg_item = QTableWidgetItem(message)
            msg_item.setFlags(msg_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 2, msg_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogSearchApp()
    window.show()
    sys.exit(app.exec_())
