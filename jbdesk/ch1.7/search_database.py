from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QHBoxLayout
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# 데이터베이스 설정
DATABASE_URL = "sqlite:///members.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Member 테이블 정의
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


# 데이터베이스 및 테이블 생성 (존재하지 않으면 생성)
if not os.path.exists("members.db"):
    Base.metadata.create_all(engine)


    # 테스트 데이터 추가
    def add_test_data():
        test_members = [
            Member(name="Alice", age=30),
            Member(name="Alice", age=28),
            Member(name="Bob", age=25),
            Member(name="Charlie", age=35),
            Member(name="David", age=40)
        ]
        session.add_all(test_members)
        session.commit()


    add_test_data()


class MemberSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # 첫째 라인: Member Name GroupBox + Search 버튼
        name_layout = QHBoxLayout()
        self.name_group = QGroupBox("Member Name")
        self.name_input = QLineEdit()
        group_layout = QVBoxLayout()
        group_layout.addWidget(self.name_input)
        self.name_group.setLayout(group_layout)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_member)

        name_layout.addWidget(self.name_group)
        name_layout.addWidget(self.search_button)
        main_layout.addLayout(name_layout)

        # 둘째 라인: Grid Table (Name, Age)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Age"])
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.setWindowTitle("Member Search")
        self.setGeometry(100, 100, 400, 300)

    def search_member(self):
        name = self.name_input.text().strip()
        if not name:
            return

        # SQLAlchemy 검색
        stmt = select(Member).where(Member.name == name)
        results = session.execute(stmt).scalars().all()

        self.table.setRowCount(len(results))
        for index, member in enumerate(results):
            self.table.setItem(index, 0, QTableWidgetItem(member.name))
            self.table.setItem(index, 1, QTableWidgetItem(str(member.age)))


if __name__ == "__main__":
    app = QApplication([])
    window = MemberSearchApp()
    window.show()
    app.exec_()