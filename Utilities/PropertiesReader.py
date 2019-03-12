import logging
from enum import Enum


class Method(Enum):
    Automatic = 0
    Manual_dictionary = 1
    Manual_properties = 2


class PropertiesReader:
    def __init__(self, file):
        self.__dict_properties = {}
        self.__file_dict = {}

        self.load(file)
        self.__logger = logging.getLogger('logger')

    def load(self, file):
        file = open(file)
        lines = file.readlines()

        keys = {}
        values = {}
        for line in lines:
            stripped = line.strip()
            if stripped:
                splitted = stripped.split('=')
                splitted = [splitted[0]] + splitted[1].split(',')
                for i in range(splitted.__len__()):
                    splitted[i] = splitted[i].strip()
                if 'key' in splitted[0]:
                    keys[splitted[0]] = splitted[1:]
                else:
                    if 'question' or 'answer' in splitted[0]:
                        values[splitted[0]] = splitted[1]

        self.__file_dict['keys'] = keys
        self.__file_dict['values'] = values

        file.close()

    def read(self, key, method=Method.Automatic):
        if method == Method.Automatic:
            if key in self.__dict_properties:
                self.__logger.info('Key was found in local storage.')
                return self.__dict_properties[key]
            else:
                self.__logger.info('Finding key in properties file...')
                return self.__read_from_source(key)

        elif method == Method.Manual_dictionary:
            if key in self.__dict_properties:
                return self.__dict_properties[key]
            else:
                self.__logger.error('Data with specific key doesn\'t exist.')

        elif method == Method.Manual_properties:
            return self.__read_from_source(key)

    def __read_from_source(self, key):
        for key_d, values in self.__file_dict['keys'].items():
            if key in key_d:
                self.__logger.info('Key was found.')
                return self.__read_key_source(key, values)
        self.__logger.error('Questionnaire data cannot be found.')

    def __read_key_source(self, key, properties):
        new_dict = []
        question, answers = [], []
        for element in properties:
            if 'question' in element:
                if question:
                    if not answers:
                        self.__logger.warning('No answers for question: "' + question[0] + '". Possible error.')
                    question.append(answers)
                    new_dict.append(question)
                    question, answers = [], []
                question.append(self.__file_dict['values'][element])
            elif 'answer' in element:
                if question:
                    answers.append(self.__file_dict['values'][element])
                else:
                    self.__logger.error('No question for answer: ' + element + '.')

        question.append(answers)
        new_dict.append(question)

        self.__dict_properties[key] = new_dict
        return new_dict
