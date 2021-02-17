
import datetime
import random
import datefinder
import HW_3_updated as normalization
import sys, os

sys.path.append('C:\\Users\\Kateryna_Kulmatytska\\PycharmProjects\\Python_HW\\HW_6')


class Article:
    def __init__(self, header, text):
        self.header = header
        self.text = text

    def print_to_file(self, formatted_text, file_name):
        with open(file_name, "a") as file:
            file.write(formatted_text)


class News(Article):
    def __init__(self, header, text, location):
        Article.__init__(self, header=header, text=text)
        self.location = location

    def format_text(self, header, text, location):
        return f"{header}--------------" \
               f"\n{text}\n" \
               f"{location},{datetime.datetime.today().strftime('%d/%m/%Y %H.%M')}" \
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
               f"Probability of truth:{score}%" \
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
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + " I'll use mine")
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
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + "I'll use mine")
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
            user_input = input("Enter the path of your file: ")
            if os.path.exists(user_input):
                input_file = open(user_input, 'r+')
            else:
                print("I did not find the file at, " + str(user_input) + "I'll use mine")
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
