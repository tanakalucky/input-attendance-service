from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pathlib import Path
import sys

sys.path.append(str(Path("__file__").resolve().parent))
from config.const import *


class BrowserHandler:
    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        prefs = {}
        options.experimental_options["prefs"] = prefs
        prefs["profile.default_content_settings"] = {"images": 2}

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        driver.implicitly_wait(5)

        self.driver = driver

    def login(self):
        driver = self.driver

        driver.get("https://id.jobcan.jp/users/sign_in")

        login_uid = driver.find_element(By.XPATH, "//*[@id='user_email']")
        login_uid.send_keys(USER_EMAIL)

        login_pw = driver.find_element(By.XPATH, "//*[@id='user_password']")
        login_pw.send_keys(USER_PASS)

        login_btn = driver.find_element(By.XPATH, "//*[@id='login_button']")
        login_btn.click()

        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    def move_to_input_attendance_page(self):
        driver = self.driver

        # headlessモードだと、タブ切り替えができない
        jobcan_attendance_url = driver.find_element(
            By.XPATH, "/html/body/div[1]/header/nav/div/div[2]/ul/li[3]/a"
        ).get_attribute("href")
        driver.get(jobcan_attendance_url)

        fix_attendance_btn = driver.find_element(
            By.XPATH, "/html/body/div/div/nav/div[2]/div/div[1]/a"
        )
        fix_attendance_btn.click()

        fix_month_attendance_btn = driver.find_element(
            By.XPATH, "/html/body/div/div/nav/div[2]/div/div[1]/div/a[2]"
        )
        fix_month_attendance_btn.click()

        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    def select_year_and_month(self):
        driver = self.driver

        select = Select(
            driver.find_element(
                By.XPATH,
                "/html/body/div/div/div[2]/main/div/div/div/h5/div/form/div/div[2]/select[1]",
            )
        )
        select.select_by_value(TARGET_YEAR)

        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

        select = Select(
            driver.find_element(
                By.XPATH,
                "/html/body/div/div/div[2]/main/div/div/div/h5/div/form/div/div[2]/select[2]",
            )
        )
        select.select_by_value(TARGET_MONTH)

        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    def clear_attendance(self):
        driver = self.driver

        time_inputs = driver.find_elements(By.CLASS_NAME, "form-type-time")
        for input in time_inputs:
            input.clear()

    def input_attendance(self, attendance_data_list: list[dict[Attendance, str]]):
        driver = self.driver

        time_inputs = driver.find_elements(By.CLASS_NAME, "form-type-time")

        for idx, data in enumerate(attendance_data_list):
            # 1日につき3つのインプット要素
            time_input_idx = idx * 3

            time_inputs[time_input_idx].send_keys(data["startTime"])
            time_inputs[time_input_idx + 1].send_keys(data["endTime"])
            time_inputs[time_input_idx + 2].send_keys(data["breakTime"])

    def save_attendance(self):
        driver = self.driver

        save_btn = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[2]/main/div/div/div/div[2]/form/div[1]/div[2]/div[1]",
        )
        driver.execute_script("arguments[0].click();", save_btn)

        alert = driver.switch_to.alert
        alert.accept()

    def close(self):
        self.driver.close()
