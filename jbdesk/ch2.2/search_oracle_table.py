import sys
import cx_Oracle
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGroupBox, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)


class EmployeeSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # EMP Name GroupBox
        self.groupBox = QGroupBox("EMP Name")
        groupBoxLayout = QHBoxLayout()

        self.searchInput = QLineEdit()
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchEmployee)

        groupBoxLayout.addWidget(self.searchInput)
        groupBoxLayout.addWidget(self.searchButton)
        self.groupBox.setLayout(groupBoxLayout)

        # 결과 테이블
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(2)
        self.resultTable.setHorizontalHeaderLabels(["Name", "Job"])

        layout.addWidget(self.groupBox)
        layout.addWidget(self.resultTable)

        self.setLayout(layout)
        self.setWindowTitle("Employee Search")
        self.resize(400, 300)

    def searchEmployee(self):
        emp_name = self.searchInput.text().strip()
        if not emp_name:
            return

        # Oracle DB 연결 정보
        dsn = cx_Oracle.makedsn("192.168.56.10", 1521, service_name="XEPDB1")
        conn = cx_Oracle.connect(user="testuser", password="test1234", dsn=dsn)
        cursor = conn.cursor()

        # EMP 테이블 검색
        query = """
        SELECT ENAME, JOB FROM EMP WHERE ENAME = :ename
        """
        cursor.execute(query, ename=emp_name)

        results = cursor.fetchall()

        # 테이블에 데이터 채우기
        self.resultTable.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            self.resultTable.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
            self.resultTable.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

        cursor.close()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeSearchApp()
    window.show()
    sys.exit(app.exec_())
