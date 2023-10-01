class Model:

    def __init__(self, max_length: int = 200, repetition_penalty: float = 5.0, top_k: int = 10,
                 top_p: float = 0.95, temperature: float = 1):
        self._tokenizer = None
        self._model = None
        self._mode = False
        self._max_length = max_length
        self._repetition_penalty = repetition_penalty
        self._top_k = top_k
        self._top_p = top_p
        self._temperature = temperature

    def enable(self):
        pass

    def disable(self):
        pass

    def active(self):
        return True

    def generate_text(self, text: str) -> str:
        return "some text"

    def info(self) -> str:
        return f'Максимальная длина текста - {self._max_length}\n' \
               f'Число наиболее вероятных следующих слов - {self._top_k}\n' \
               f'Совокупная вероятность для следующих слов - {self._top_p}\n' \
               f'Вероятность появления слов с большой вероятностью - {self._temperature}\n'

    def set_default(self):
        pass

    def set_top_k(self, new_top_k: int):
        pass

    def set_top_p(self, new_top_p: float):
        pass

    def set_temperature(self, new_temperature: float):
        pass

    def set_max_length(self, new_max_length: int):
        pass
