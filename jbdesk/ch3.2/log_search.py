from fabric import Connection
import sys

# VM 정보 (각 호스트 이름과 IP)
hosts = {
    "gateway01": "192.168.56.40",
    "api01": "192.168.56.41",
    "echo01": "192.168.56.42"
}

# VM 로그 파일 경로
log_paths = {
    "gateway01": "/home/vagrant/gateway.log",
    "api01": "/home/vagrant/api.log",
    "echo01": "/home/vagrant/echo.log"
}

# 공통 사용자 및 비밀번호
user = "vagrant"
password = "vagrant"

def search_tid(tid):
    for name, ip in hosts.items():
        log_file = log_paths[name]
        print(f"\n🔍 Searching TID={tid} in {name} ({ip})...")
        try:
            conn = Connection(
                host=ip,
                user=user,
                connect_kwargs={"password": password}
            )
            result = conn.run(f"grep {tid} {log_file}", hide=True, warn=True)
            if result.stdout.strip():
                print(result.stdout.strip())
            else:
                print("❌ No log found.")
        except Exception as e:
            print(f"⚠️ Error connecting to {name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python log_search.py <TID>")
        sys.exit(1)

    tid = sys.argv[1]
    search_tid(tid)
