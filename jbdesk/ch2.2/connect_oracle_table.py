import cx_Oracle

# Oracle Instant Client가 올바르게 설정되었는지 확인
print(cx_Oracle.clientversion())

# Oracle 데이터베이스 연결
dsn = cx_Oracle.makedsn("192.168.56.10", 1521, service_name="XEPDB1")
connection = cx_Oracle.connect(user="testuser", password="test1234", dsn=dsn)

# 커서 생성
cursor = connection.cursor()

# 데이터 조회 예제
cursor.execute("SELECT * FROM EMP")
for row in cursor.fetchall():
    print(row)

# 리소스 해제
cursor.close()
connection.close()
