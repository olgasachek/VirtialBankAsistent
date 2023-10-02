from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch import Tensor

class Model:

    def __init__(self, max_length: int = 200, repetition_penalty: float = 5.0, top_k: int = 10,
                 top_p: float = 0.95, temperature: float = 1):
        self.__tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained("C:/Users/Lenovo/PycharmProjects/VirtualBankAssistant/bank_model4")
        self.__model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained("C:/Users/Lenovo/PycharmProjects/VirtualBankAssistant/bank_model4")
        self.__mode = False
        self.__max_length = max_length
        self.__repetition_penalty = repetition_penalty
        self.__top_k = top_k
        self.__top_p = top_p
        self.__temperature = temperature

    def enable(self):
        pass

    def disable(self):
        pass

    def active(self):
        return True

    def generate_text(self, text: str) -> str:
        input_token: Tensor = self.__tokenizer.encode(text, return_tensors="pt", )
        output_text: Tensor = self.__model.generate(input_token, max_length=200, do_sample=True,
                                                    repetition_penalty=self.__repetition_penalty, top_k=self.__top_k,
                                                    top_p=self.__top_p, temperature=self.__temperature)
        output_text: str = self.__tokenizer.decode(output_text[0]).replace('\xa0—', ' ').replace('\n', ' ')

        return output_text

    def info(self) -> str:
        return f'Максимальная длина текста - {self.__max_length}\n' \
               f'Число наиболее вероятных следующих слов - {self.__top_k}\n' \
               f'Совокупная вероятность для следующих слов - {self.__top_p}\n' \
               f'Вероятность появления слов с большой вероятностью - {self.__temperature}\n'

    def set_default(self):
        self.__max_length = 200
        self.__top_k = 10
        self.__top_p = 0.95
        self.__temperature = 1

    def set_top_k(self, new_top_k: int):
        self.__top_k = new_top_k

    def set_top_p(self, new_top_p: float):
        self.__top_p = new_top_p

    def set_temperature(self, new_temperature: float):
        self.__temperature = new_temperature

    def set_max_length(self, new_max_length: int):
        self.__max_length = new_max_length
