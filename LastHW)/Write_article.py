import os
import re
from collections import Counter
from configparser import ConfigParser

import datefinder
import datetime
import random

import json
import csv

import xml.etree.ElementTree as ET
import sqlite3
import HW_3_updated as normalization


# sys.path.append('C:\\Users\\Kateryna_Kulmatytska\\PycharmProjects\\Python_HW\\HW_6')

class Common:
    def __init__(self):
        return

    def get_header(self):
        input_versions = ['News', 'PrivatAdv', 'Consider']
        while True:
            header = input(f"Enter the topic you are interested in: {', '.join(input_versions)}\n")
            if header not in input_versions:
                print('Please select correct topic')
            else:
                break
        return header

    def get_text(self):
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

    def get_attrib(self, header):
        if header == 'News':
            location = input('Enter location \n:')
            return location
        elif header == 'PrivatAdv':
            try:
                expiration_date = list(datefinder.find_dates(
                    input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
            except:
                print('Incorrect date format')
                expiration_date = list(datefinder.find_dates(
                    input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
            return expiration_date
        elif header == 'Consider':
            score = random.randint(1, 100)
            return score

    def get_file_choise(self):
        versions = ['json', 'txt', 'xml']
        while True:
            file_choise = input('Choose file type you want to use? Answer: json/txt/xml\n:')
            if file_choise not in versions:
                print('Please select correct file type')
            else:
                break
        return file_choise

    def check_path(self, header, file_choise):
        user_input = input("Enter the path of your file: ")
        if os.path.exists(user_input):
            try:
                file_to_parse = open(user_input, 'r+')
                return file_to_parse
            except:
                print("File is not valid")
        else:
            print("I'll use default file ")
            config = ConfigParser()
            config.read('config.ini')
            file_to_parse = open((config.get('Defaults', f'default_file_{header}_{file_choise}')), 'r+')
            return file_to_parse

    def parse_file(self, file_choise, file_to_parse):
        text_dict = {}
        if file_choise == 'json':
            parsed_text_json = json.load(file_to_parse)
            for i in parsed_text_json:
                text_dict[i["text"]] = i["attrib"]
        elif file_choise == 'txt':
            parsed_text_txt = file_to_parse.read().split('\n\n')
            for i in parsed_text_txt:
                real_text = i.split('attrib ')
                text_dict[real_text[0]] = real_text[1]
            file_to_parse.close()
        elif file_choise == 'xml':
            tree = ET.parse(file_to_parse)
            root = tree.getroot()
            for elem in root:
                text_dict[elem.text] = elem.attrib['attrib']
        return text_dict


class ConnectDatabase:
    def __init__(self):
        with  sqlite3.connect('database.db') as self.conn:
            self.cursor = self.conn.cursor()
            self.cursor.execute('create table if not exists news (text_news text, location text, UNIQUE (text_news, location))')
            self.cursor.execute('create table if not exists advs (text_advs text, expiration_date date, UNIQUE (text_advs, expiration_date))')
            self.cursor.execute('create table if not exists consider (text_consider text, score int, UNIQUE (text_consider, score))')

    def insert(self, table_name,  column, column1, text, attrib):
        with self.conn:
            self.cursor.execute(f'insert or ignore into {table_name} ({column}, {column1}) values ( ?, ?)', (text, attrib))
        return self.cursor.fetchall()


class Article:
    def __init__(self, header, text):
        self.header = header
        self.text = text

    def print_to_file(self, formatted_text, file_name):
        with open(file_name, "a") as file:
            file.write(formatted_text)


    def words_and_letters_count(self, file_name):
        with open(file_name, "r") as file_updated:
            content = file_updated.read()
            words = re.findall(r"[\w']+", content.lower())
            d = dict()
            for word in words:
                if word.isalpha():
                    if word in d:
                        d[word] += 1
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
                    else:
                        count_upper = letters_general.get(letter.upper())
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
               f"Actual until: {expiration_date}, {((list(datefinder.find_dates(expiration_date))[0].date()) - datetime.date.today()).days} days left." \
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
    a = Common()
    header = a.get_header()
    text = a.get_text()
    text_dict = {}
    print_to_db = ConnectDatabase()
    if len(text) == 0:
        file_choise = a.get_file_choise()
        text_dict = a.parse_file(file_choise, a.check_path(header, file_choise))
    else:
        text_dict[text] = a.get_attrib(header)
    if header == 'News':
        for text, location in text_dict.items():
            story = News(header, text, location)
            story.print_to_file(story.format_text(header, text, location), 'sum_news.txt')
            story.words_and_letters_count('sum_news.txt')
            print_to_db.insert('news', 'text_news', 'location', text, location)
    elif header == 'PrivatAdv':
        for text, expiration_date in text_dict.items():
            advertisement = PrivatAdv(header, text, expiration_date)
            advertisement.print_to_file(advertisement.format_text(header, text, expiration_date), 'sum_news.txt')
            advertisement.words_and_letters_count('sum_news.txt')
            print_to_db.insert('advs', 'text_advs', 'expiration_date', text, expiration_date)
    elif header == 'Consider':
        for text, score in text_dict.items():
            game = Consider(header, text, score)
            game.print_to_file(game.format_text(header, text, score), 'sum_news.txt')
            game.words_and_letters_count('sum_news.txt')
            print_to_db.insert('consider', 'text_consider', 'score', text, score)


if __name__ == '__main__':
    while True:
        user_input = input('Do you want to publish? Y/N:')
        if user_input == 'Y':
            write_article()
        elif user_input == 'N':
            break
        else:
            print("Incorrect input. Please type Y or N\n")
