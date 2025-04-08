import argparse
from fabric import Connection
from invoke.exceptions import UnexpectedExit

def get_os_info(host_name: str, user_name: str, password: str) -> str:
    """
    SSH로 접속해서 OS 이름과 버전을 반환합니다.
    """
    try:
        conn = Connection(
            host=host_name,
            user=user_name,
            connect_kwargs={"password": password}
        )

        try:
            result = conn.run("cat /etc/os-release", hide=True)
            lines = result.stdout.strip().splitlines()
            info = {}
            for line in lines:
                if "=" in line:
                    key, value = line.split("=", 1)
                    info[key.strip()] = value.strip().strip('"')
            return f"{info.get('NAME', 'Unknown OS')} {info.get('VERSION', '')}"

        except UnexpectedExit:
            # /etc/os-release가 없는 경우 (예: CentOS 6)
            result = conn.run("cat /etc/redhat-release", hide=True)
            return result.stdout.strip()

    except Exception as e:
        return f"❌ 접속 실패: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Fabric을 사용하여 원격 서버 OS 정보를 가져옵니다.")
    parser.add_argument("-host_name", required=True, help="호스트 이름 또는 IP")
    parser.add_argument("-user_name", required=True, help="SSH 사용자 이름")
    parser.add_argument("-password", required=True, help="SSH 비밀번호")

    args = parser.parse_args()

    os_info = get_os_info(args.host_name, args.user_name, args.password)
    print("✅ OS 정보:", os_info)

if __name__ == "__main__":
    main()
