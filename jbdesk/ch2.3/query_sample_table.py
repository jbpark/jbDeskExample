import pymysql

# VM 정보 매핑
VM_INFO = {
    "dev_first":    {"ip": "192.168.56.20"},
    "dev_second":   {"ip": "192.168.56.21"},
    "stage_first":  {"ip": "192.168.56.22"},
    "stage_second": {"ip": "192.168.56.23"},
    "live_first":   {"ip": "192.168.56.24"},
    "live_second":  {"ip": "192.168.56.25"},
}

def get_vm_name(environment: str, db_type: str) -> str:
    return f"{environment.lower()}_{db_type.lower()}"

def table_exists(cursor, table_name: str) -> bool:
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None

def query_sample_tables(ip: str, user: str = "root", password: str = "vagrant", db: str = "sample"):
    try:
        conn = pymysql.connect(host=ip, port=3306, user=user, password=password, database=db)
        cursor = conn.cursor()

        if table_exists(cursor, "orders"):
            print("[orders 테이블]")
            cursor.execute("SELECT * FROM orders;")
            for row in cursor.fetchall():
                print(row)
        else:
            print("[orders 테이블 없음]")

        if table_exists(cursor, "products"):
            print("\n[products 테이블]")
            cursor.execute("SELECT * FROM products;")
            for row in cursor.fetchall():
                print(row)
        else:
            print("[products 테이블 없음]")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[!] 접속 실패: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", choices=["dev", "stage", "live"], required=True)
    parser.add_argument("--db_type", choices=["first", "second"], required=True)
    args = parser.parse_args()

    vm_name = get_vm_name(args.environment, args.db_type)
    ip = VM_INFO.get(vm_name, {}).get("ip")

    if not ip:
        print(f"[!] VM 정보 없음: {vm_name}")
    else:
        print(f"[+] {vm_name} ({ip}) 에 접속합니다...")
        query_sample_tables(ip)
