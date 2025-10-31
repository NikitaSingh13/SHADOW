import sys
from src.logger import logging


def error_message_detail(error, error_detail: sys):
    """
    Extracts detailed error message:
    - File name
    - Line number
    - Actual error message
    Works for both real and manually raised exceptions.
    """
    exc_info = error_detail.exc_info()
    if exc_info[2] is not None:
        _, _, exc_tb = exc_info
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        # Handles manually raised exceptions (no traceback)
        file_name = "ManualRaise"
        line_number = "N/A"

    return (
        f"Error occurred in python script: [{file_name}] "
        f"at line number [{line_number}] "
        f"with message: [{str(error)}]"
    )


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message


# ✅ Testing
if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        raise CustomException(e, sys)

    # Manual raise test
    # raise CustomException("Something custom failed", sys)
