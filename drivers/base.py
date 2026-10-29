from abc import ABC, abstractmethod

class BaseInputController(ABC):
    @abstractmethod
    def move(self, dx: int, dy: int):
        # kontrol mouse
        pass

    @abstractmethod
    def click(self, button: str):
        # Penanda tombol left and right
        pass

    @abstractmethod
    def scroll(self, dy: int):
        # Untuk Scroll
        pass

    @abstractmethod
    def key_press(self, key_name: str):
        # Untuk Key
        pass

    @abstractmethod
    def close(self):
        # Melepas Koneksi
        pass
