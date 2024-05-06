from pathlib import Path
import fitz
import calendar
import sys
from datetime import time
from io import BytesIO


sys.path.append(str(Path("__file__").resolve().parent))
from config.const import *
import boto3


def extract_attendance_data_from_pdf() -> list[dict[Attendance, str]]:
    s3_client = boto3.client("s3")

    obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_KEY)
    fs = obj["Body"].read()
    pdf = fitz.open(stream=BytesIO(fs), filetype="pdf")

    attendance_data_list: list[dict[Attendance, str]] = []
    target_page: fitz.Page = pdf[0]
    target_table = target_page.find_tables()[0].extract()
    target_year = int(TARGET_YEAR)
    target_month = int(TARGET_MONTH)
    day_range = get_day_range(target_year, target_month)

    for data in target_table:
        day = data[0]

        if day not in day_range:
            continue

        target_data: list = data[2:4]
        attendance_data: dict[Attendance, str] = {
            "startTime": target_data[0],
            "endTime": target_data[1],
            "breakTime": "",
        }

        if attendance_data["startTime"] == "":
            attendance_data_list.append(attendance_data)
            continue

        hour = int(attendance_data["endTime"].split(":")[0])
        minute = int(attendance_data["endTime"].split(":")[1])

        rest_start_time = time(11, 30)
        end_time = time(hour, minute)
        fixed_end_time = time(17, 30)

        if end_time <= rest_start_time:
            attendance_data_list.append(attendance_data)
            continue

        if end_time <= fixed_end_time:
            attendance_data["breakTime"] = "00:45"
            attendance_data_list.append(attendance_data)
        else:
            attendance_data["breakTime"] = "01:15"
            attendance_data_list.append(attendance_data)

    pdf.close()

    return attendance_data_list


def get_day_range(target_year, target_month) -> list[str]:
    first_day = 1
    end_day = calendar.monthrange(target_year, target_month)[1]

    return list(map(str, range(first_day, end_day + 1)))
