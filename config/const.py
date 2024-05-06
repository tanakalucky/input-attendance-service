import sys
import boto3
from typing import TypeAlias, Literal

ssm = boto3.client("ssm", region_name="ap-northeast-1")

USER_EMAIL = ssm.get_parameter(Name="/input-attendance/user-email")["Parameter"][
    "Value"
]
USER_PASS = ssm.get_parameter(Name="/input-attendance/user-pass")["Parameter"]["Value"]

S3_BUCKET_NAME = ssm.get_parameter(Name="/input-attendance/s3-bucket-name")[
    "Parameter"
]["Value"]
S3_OBJECT_KEY = ssm.get_parameter(Name="/input-attendance/s3-object-key")["Parameter"][
    "Value"
]

Attendance: TypeAlias = Literal["startTime", "endTime", "breakTime"]

try:
    TARGET_YEAR = sys.argv[1]
    TARGET_MONTH = sys.argv[2]
except IndexError:
    print("対象年月を入力してください。")
    sys.exit()
