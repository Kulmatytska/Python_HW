
import datetime
import random
import datefinder
import HW_3_updated as normalization
import sys, os
import csv
import re
from collections import Counter
import json

sys.path.append('C:\\Users\\Kateryna_Kulmatytska\\PycharmProjects\\Python_HW\\HW_6')

class Article:
    def __init__(self, header, text):
        self.header = header
        self.text = text

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
                    writer = csv.DictWriter(letters_count_file,  fieldnames=headers)
                    writer.writeheader()
                    letters_lowercase = Counter(letter for line in content
                                      for letter in line.lower()
                                      if letter.isalpha())
                    letters_general = Counter(letter for line in content
                                      for letter in line
                                      if letter.isalpha())
                    letters_total = len(re.findall("[a-zA-Z]", content))
                    for letter, values in letters_lowercase.items():
                        writer.writerow({f'Letter': letter, f'Count_all': letters_lowercase.get(letter), f'Count_uppercase': letters_general.get(letter.upper()),
                                         f'Percentage': round((letters_lowercase.get(letter) / letters_total *100),2)})


class News(Article):
    def __init__(self, header, text, location):
        Article.__init__(self, header=header, text=text)
        self.location = location

    def format_text(self, header, text, location):
        return f"{header}--------------" \
               f"\n{text}\n" \
               f"{location}, {datetime.datetime.today().strftime('%d/%m/%Y %H.%M')}" \
               f"\n-------------------\n\n"


class PrivatAdv(Article):
    def __init__(self, header, text, expiration_date):
        Article.__init__(self, header=header, text=text)
        self.expiration_date = expiration_date

    def format_text(self, header, text, expiration_date):
        return f"{header}----------" \
               f"\n{text}\n" \
               f"Actual until: {expiration_date}, {(expiration_date - datetime.date.today()).days} days left." \
               f"\n-----------------------\n\n"


class Consider(Article):
    def __init__(self, header, text, score):
        Article.__init__(self, header=header, text=text)
        self.score = score

    def format_text(self, header, text, score):
        return f"{header}-------------- " \
               f"\n{text}\n" \
               f"Probability of truth: {score}%" \
               f"\n------------------------------\n\n"


def write_article():
    input_versions = ('News', 'PrivatAdv', 'Consider')
    header = input('Enter the topic you are interested in:\nNews\nPrivatAdv\nConsider\n:')

    while header not in input_versions:
        print('Please select correct topic:')
        header = input('News\nPrivatAdv\nConsider\n:')

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
    if header == 'News':
        if len(text) == 0:
            file_choise = input('Shall I use csv or json file? Answer: json/csv\n:')
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                 input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + " I'll use mine " + file_choise)
            if file_choise == 'json':
                input_file = open('default_news.json', "r")
                parsed_text_json = json.load(input_file)
                for i in parsed_text_json:
                    text = i["text"]
                    location = 'Default location'
                    story = News(header, text, location)
                    story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
            elif file_choise == 'csv':
                input_file = open('default_news.txt', "r")
                parsed_text = input_file.read().split('\n\n')
                for i in parsed_text:
                    text = i[0:]
                    location = 'Default location'
                    story = News(header, text, location)
                    story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
            input_file.close()
            os.remove('default_news.txt')
        else:
            location = input('Enter location \n:')
            story = News(header, text, location)
            story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
    elif header == 'PrivatAdv':
        if len(text) == 0:
            file_choise = input('Shall I use csv or json file? Answer: json/csv\n:')
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + "I'll use mine")
                if file_choise == 'json':
                    input_file = open('default_advs.json', "r")
                    parsed_text_json = json.load(input_file)
                    for i in parsed_text_json:
                        text = i["text"]
                        expiration_date = datetime.date.today()
                        advertisement = PrivatAdv(header, text, expiration_date)
                        advertisement.print_to_file(advertisement.format_text(header, text, expiration_date),
                                                    'sum_news.txt')
                elif file_choise == 'csv':
                    input_file = open('default_advs.txt', "r")
                    parsed_text = input_file.read().split('\n\n')
                    for i in parsed_text:
                        text = i[0:]
                        expiration_date = datetime.date.today()
                        advertisement = PrivatAdv(header, text, expiration_date)
                        advertisement.print_to_file(advertisement.format_text(header, text, expiration_date),
                                                'sum_news.txt')
            input_file.close()
            os.remove('default_advs.txt')
        else:
            expiration_date = list(datefinder.find_dates(
                input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
            advertisement = PrivatAdv(header, text, expiration_date)
            advertisement.print_to_file(advertisement.format_text(header, text, expiration_date), 'sum_news.txt')
    elif header == 'Consider':
        if len(text) == 0:
            file_choise = input('Shall I use csv or json file? Answer: json/csv\n:')
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + "I'll use mine")
                if file_choise == 'json':
                    input_file = open('default_considers.json', "r")
                    parsed_text_json = json.load(input_file)
                    for i in parsed_text_json:
                        text = i["text"]
                        score = random.randint(1, 100)
                        game = Consider(header, text, score)
                        game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')
                if file_choise == 'csv':
                    input_file = open('default_considers.txt', "r")
                    parsed_text = input_file.read().split('\n\n')
                    for i in parsed_text:
                        text = i[0:]
                        score = random.randint(1, 100)
                        game = Consider(header, text, score)
                        game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')
            input_file.close()
            os.remove('default_considers.txt')
        else:
            score = random.randint(1, 100)
            game = Consider(header, text, score)
            game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')


if __name__ == '__main__':
    write_article()
    another_article = input('Do you want to publish something else? Y/N:')
    while another_article != 'N':
        write_article()
        another_article = input('Do you want to publish something else? Y/N:')
