import re
from datetime import datetime
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

# 예제 실행
log_text = '192.168.2.82 - - [27/Mar/2025:00:04:06 -0700] "GET /test HTTP/1.1" 200 - "-" "axios/0.21.4" 73ms "962fff801aa10f24" "a9a7a0fd8e5dd842" "962fff801aa10f24"'
converted_log = convert_log_timezone(log_text, 'US/Pacific', 'Asia/Seoul')
print(converted_log)
