from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch import Tensor

class Model:

    def __init__(self, max_length: int = 50,
                 repetition_penalty: float = 5.0,
                 num_beams = 1,
                 top_k: int = 1,
                 top_p: float = 0.95,
                 temperature: float = 0.1):
        self.__tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained("./bank_model")
        self.__model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained("./bank_model")
        self.__mode = False
        self.__max_length = max_length
        self.__repetition_penalty = repetition_penalty
        self.__num_beams = num_beams
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
        output_text: Tensor = self.__model.generate(input_token,
                                                    max_length=self.__max_length,
                                                    do_sample=True,
                                                    repetition_penalty=self.__repetition_penalty,
                                                    num_beams=1,
                                                    top_k=self.__top_k,
                                                    top_p=self.__top_p,
                                                    temperature=self.__temperature)
        output_text: str = self.__tokenizer.decode(output_text[0]).replace('\xa0—', ' ').replace('\n', ' ')

        return output_text

    def info(self) -> str:
        return f'Максимальная длина текста - {self.__max_length}\n' \
               f'Число разветвлений путей генерации для каждого шага - {self.__num_beams}\n' \
               f'Число наиболее вероятных следующих слов - {self.__top_k}\n' \
               f'Совокупная вероятность для следующих слов - {self.__top_p}\n' \
               f'Вероятность появления слов с большой вероятностью - {self.__temperature}\n'

    def set_default(self):
        self.__max_length = 50
        self.__num_beams = 1,
        self.__top_k = 1
        self.__top_p = 0.95
        self.__temperature = 0.1

    def set_num_beams(self, new_num_beams: int):
        self.__num_beams = new_num_beams

    def set_top_k(self, new_top_k: int):
        self.__top_k = new_top_k

    def set_top_p(self, new_top_p: float):
        self.__top_p = new_top_p

    def set_temperature(self, new_temperature: float):
        self.__temperature = new_temperature

    def set_max_length(self, new_max_length: int):
        self.__max_length = new_max_length
