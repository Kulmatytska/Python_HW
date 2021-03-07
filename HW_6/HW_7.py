import datetime
import random
import datefinder
import HW_3_updated as normalization
import sys, os
import csv
import re
from collections import Counter
import json
import xml.etree.ElementTree as ET

sys.path.append('C:\\Users\\Kateryna_Kulmatytska\\PycharmProjects\\Python_HW\\HW_6')


class Article:
    def __init__(self, header, text):
        self.header = header
        self.text = text

    def get_header():
        input_versions = ['News', 'PrivatAdv', 'Consider']
        while True:
            header = input(f"Enter the topic you are interested in: {', '.join(input_versions)}\n")
            if header not in input_versions:
                print('Please select correct topic')
            else:
                break
        return header

    def get_text():
        print("Type your text here. Press Enter twice to exit from text adding mode")
        input_text = ''
        while True:
            new_line = input()
            if new_line != '':
                input_text += new_line + '\n'
            else:
                input_text = input_text[:-1]
                break
        text = normalization.normalization(input_text)
        return text

    def get_file_choise():
        versions = ['json', 'txt', 'xml']
        while True:
            file_choise = input('Choose file type you want to use? Answer: json/txt/xml\n:')
            if file_choise not in versions:
                print('Please select correct file type')
            else:
                break
        return file_choise

    def get_default_file( header, file_choise):
        global default_file
        if file_choise == 'json':
            if header == 'News':
                default_file = 'default_news.json'
            elif header == 'PrivatAdv':
                default_file = 'default_advs.json'
            elif header == 'Consider':
                default_file = 'default_considers.json'
        elif file_choise == 'txt':
            if header == 'News':
                default_file = 'default_news.txt'
            elif header == 'PrivatAdv':
                default_file = 'default_advs.txt'
            elif header == 'Consider':
                default_file = 'default_considers.txt'
        elif file_choise == 'xml':
            if header == 'News':
                default_file = 'default_news.xml'
            elif header == 'PrivatAdv':
                default_file = 'default_advs.xml'
            elif header == 'Consider':
                default_file = 'default_considers.xml'
        return default_file


    def check_path(default_file):
        user_input = input("Enter the path of your file: ")
        if os.path.exists(user_input):
            try:
                file_to_parse = open(user_input, 'r+')
            except:
                print("File is not valid. I'll use mine ")
                file_to_parse = open(default_file, 'r+')
        else:
            print("I did not find the file at, " + str(user_input) + " I'll use mine ")
            file_to_parse = open(default_file, 'r+')
        return file_to_parse


    def parse_file(file_choise, file_to_parse):
        text_list = {}
        if file_choise == 'json':
            parsed_text_json = json.load(file_to_parse)
            for i in parsed_text_json:
                text_list[i["text"]] = i["attrib"]
        elif file_choise == 'txt':
            parsed_text = file_to_parse.read().split('\n\n')
            for i in parsed_text:
                real_text = i.split('Place')
                text_list[real_text[0]] = real_text[1]
            file_to_parse.close()
        elif file_choise == 'xml':
            tree = ET.parse(file_to_parse)
            root = tree.getroot()
            for elem in root:
                text_list[elem.text] = elem.attrib['attrib']
        return text_list

    def print_to_file(self, formatted_text, file_name):
        with open(file_name, "a") as file:
            file.write(formatted_text)
        with open(file_name, "r") as file_updated:
            content = file_updated.read()
            words = re.findall(r"[\w']+", content.lower())
            d = dict()
            for word in words:
                if word.isalpha():
                    if word in d:
                        d[word] = d[word] + 1
                    else:
                        d[word] = 1
            with open('words_count.csv', "w", newline='') as words_count_file:
                for key, value in d.items():
                    writer = csv.writer(words_count_file, delimiter='-')
                    writer.writerow([f'{key}', f'{value}'])

            with open('letters_count.csv', "w", newline='') as letters_count_file:
                headers = ['Letter', 'Count_all', 'Count_uppercase', 'Percentage']
                writer = csv.DictWriter(letters_count_file, fieldnames=headers)
                writer.writeheader()
                letters_lowercase = Counter(letter for line in content
                                            for letter in line.lower()
                                            if letter.isalpha())
                letters_general = Counter(letter for line in content
                                            for letter in line
                                            if letter.isalpha())
                letters_total = len(re.findall("[a-zA-Z]", content))
                for letter, values in letters_lowercase.items():
                    if letters_general.get(letter.upper()) is None:
                        count_upper = 0
                    else: count_upper = letters_general.get(letter.upper())
                    writer.writerow({f'Letter': letter, f'Count_all': letters_lowercase.get(letter),
                                     f'Count_uppercase': count_upper,
                                     f'Percentage': round((letters_lowercase.get(letter) / letters_total * 100),
                                                              2)})


class News(Article):
    def __init__(self, header, text, location):
        Article.__init__(self, header=header, text=text)
        self.location = location

    def format_text(self, header, text, location):
        return f"{header}--------------" \
               f"\n{text}\n" \
               f"{location}, {datetime.datetime.today().strftime('%d/%m/%Y %H.%M')}" \
               f"\n{'-' * 23}\n\n"


class PrivatAdv(Article):
    def __init__(self, header, text, expiration_date):
        Article.__init__(self, header=header, text=text)
        self.expiration_date = expiration_date

    def format_text(self, header, text, expiration_date):
        return f"{header}----------" \
               f"\n{text}\n" \
               f"Actual until: {expiration_date}, {(expiration_date - datetime.date.today()).days} days left." \
               f"\n{'-' * 23}\n\n"


class Consider(Article):
    def __init__(self, header, text, score):
        Article.__init__(self, header=header, text=text)
        self.score = score

    def format_text(self, header, text, score):
        return f"{header}-------------- " \
               f"\n{text}\n" \
               f"Probability of truth: {score}%" \
               f"\n{'-' * 23}\n\n"


def write_article():
    header = Article.get_header()
    text = Article.get_text()
    if header == 'News':
        if len(text) == 0:
            file_choise = Article.get_file_choise()
            default_file = Article.get_default_file(header, file_choise)
            file_to_parse = Article.check_path(default_file)
            text_list = Article.parse_file(file_choise, file_to_parse)
            for text, location in text_list.items():
                story = News(header, text, location)
                story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
        else:
            location = input('Enter location \n:')
            story = News(header, text, location)
            story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
    elif header == 'PrivatAdv':
        if len(text) == 0:
            file_choise = Article.get_file_choise()
            default_file = Article.get_default_file(header, file_choise)
            file_to_parse = Article.check_path(default_file)
            text_list = Article.parse_file(file_choise, file_to_parse)
            for text, date in text_list.items():
                expiration_date = list(datefinder.find_dates(date))[0].date()
                advertisement = PrivatAdv(header, text, expiration_date)
                advertisement.print_to_file(advertisement.format_text(header, text, expiration_date), 'sum_news.txt')
        else:
            try:
                expiration_date = list(datefinder.find_dates(
                    input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
            except:
                print('Incorrect date format')
                expiration_date = list(datefinder.find_dates(
                    input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
            advertisement = PrivatAdv(header, text, expiration_date)
            advertisement.print_to_file(advertisement.format_text(header, text, expiration_date),'sum_news.txt')
    elif header == 'Consider':
        if len(text) == 0:
            file_choise = Article.get_file_choise()
            default_file = Article.get_default_file(header, file_choise)
            file_to_parse = Article.check_path(default_file)
            text_list = Article.parse_file(file_choise, file_to_parse)
            for text in text_list:
                score = random.randint(1, 100)
                game = Consider(header, text, score)
                game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')
        else:
            score = random.randint(1, 100)
            game = Consider(header, text, score)
            game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')



if __name__ == '__main__':
    while True:
        user_input = input('Do you want to publish? Y/N:')
        if user_input == 'Y':
            write_article()
        elif user_input == 'N':
            break
        else:
            print("Incorrect input. Please type Y or N\n")
