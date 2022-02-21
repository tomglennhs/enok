from abc import abstractmethod


class Printer:
    @abstractmethod
    def upload_print(gcode_path: str) -> bool:
        pass
    @abstractmethod
    def start_print(file_name: str) -> bool:
        pass
    @abstractmethod
    def cancel_print() -> bool:
        pass
    @abstractmethod
    def pause_print() -> bool:
        pass
    @abstractmethod
    def resume_print() -> bool:
        pass