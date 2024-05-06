from .browser_handler import BrowserHandler
from .pdf_handler import extract_attendance_data_from_pdf


def main():
    bh = BrowserHandler()

    bh.login()

    bh.move_to_input_attendance_page()

    bh.select_year_and_month()

    bh.clear_attendance()

    attendance_data_list = extract_attendance_data_from_pdf()
    bh.input_attendance(attendance_data_list)

    bh.save_attendance()

    bh.close()


if __name__ == "__main__":
    main()
