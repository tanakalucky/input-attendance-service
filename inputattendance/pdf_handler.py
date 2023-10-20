from pathlib import Path
import fitz
import calendar
import sys
import tempfile

sys.path.append(str(Path("__file__").resolve().parent))
from config.const import *
import boto3


def extract_attendance_data_from_pdf():
    s3_client = boto3.client("s3")

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        s3_client.download_fileobj(S3_BUCKET_NAME, S3_OBJECT_KEY, tmp_file)
        tmp_file_path = tmp_file.name

    pdf = fitz.open(tmp_file_path)

    attendance_data = []
    for page in range(len(pdf)):
        row_data = pdf[page].get_text().split("\n")

        first_day = 1
        end_day = calendar.monthrange(int(TARGET_YEAR), int(TARGET_MONTH))[1]

        for day in range(first_day, end_day + 1):
            attendance_start_idx = row_data.index(str(day))

            next_day = str(day + 1)
            try:
                attendance_end_idx = (
                    len(row_data) if day == end_day else row_data.index(next_day)
                )
            except ValueError:
                print("勤怠の対象年月が正しいかご確認ください。")
                sys.exit()

            attendance_of_the_day = row_data[attendance_start_idx:attendance_end_idx]
            attendance_data.append(attendance_of_the_day)

    pdf.close()

    return attendance_data
