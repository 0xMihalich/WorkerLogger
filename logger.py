from datetime import datetime
from logging import DEBUG, FileHandler, Formatter, Logger, StreamHandler
from os.path import dirname
from sys import stdout
from typing import Optional


__name__    = "WorkerLogger"
__version__ = "0.1"


def root_dir() -> str:
    """Получение директории проекта."""

    import __main__

    return dirname(__main__.__file__)


class WorkerLogger(Logger):
    """Класс логирования событий бота."""

    def __init__(self: "WorkerLogger",
                 name: str,
                 worker: Optional[str] = None,
                 use_console: bool = True,) -> None:
        """Инициализация класса.
           
           Параметры:
           ----------
                - `name`: Имя процесса, для которого ведется лог.
                - `worker`: Опционально можно указать название воркера если в процессе их несколько и логируем каждый по отдельности.
                - `use_console`: Булево, при False ничего не выводит в консоль. По-умолчанию True."""
        
        super().__init__("MainLogger")

        self.name = name
        self.worker = worker
        self.setLevel(DEBUG)

        self.log_path = root_dir()

        formatter = Formatter(fmt=(f"%(asctime)s | %(levelname)-8s | ver {__version__} | "
                                   "%(filename)s-%(funcName)s-%(lineno)04d | %(message)s"),
                              datefmt="%Y-%m-%d %H:%M:%S")
        
        file_handler = FileHandler("{}/{:%Y-%m-%d}_{}.log"
                                  .format(self.log_path, datetime.now(), self.name),
                                   encoding="utf-8")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        if use_console:
            console_handler = StreamHandler(stdout)
            console_handler.setLevel(DEBUG)
            console_handler.setFormatter(formatter)
            self.addHandler(console_handler)

        self.propagate = False
