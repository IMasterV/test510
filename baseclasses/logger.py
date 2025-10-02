import datetime
import os

class Logger:
    file_name = f"/home/root/scripts/logs/_log" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_start_step(cls, method: str):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Start time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Start name method: {method}\n"
        data_to_add += "\n"

        cls.write_log_to_file(data_to_add)

    @classmethod
    def add_end_step(cls, method: str, status: str):

        data_to_add = (
            f"End time: {datetime.datetime.now()}\n"
            f"End name method: {method}\n"
            f"Status: {status}\n"
            "-----\n"
        )

        # data_to_add = f"End time: {str(datetime.datetime.now())}\n"
        # data_to_add += f"End name method: {method}\n"
        # #data_to_add += f"URL: {url}\n"
        # data_to_add += f"\n-----\n"

        cls.write_log_to_file(data_to_add)

    # === Контекстный менеджер ===
    class _Step:
        def __init__(self, method):
            self.method = method
            Logger.add_start_step(method)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                Logger.add_end_step(self.method, status="PASSED")
            else:
                Logger.add_end_step(self.method, status=f"FAILED: {exc_val}")
                return False  # не скрывать исключение

    @classmethod
    def step(cls, method: str):
        """Использовать так: with Logger.step('method'): ..."""
        return cls._Step(method)