from abc import abstractmethod


class Printer:
    """Start print. Requires a path to the file."""
    @abstractmethod
    def start_print(gcode_path: str) -> bool:
        pass
    @abstractmethod
    def cancel_print() -> bool:
        pass
    @abstractmethod
    def pause_print():
        pass
    @abstractmethod
    def resume_print():
        pass