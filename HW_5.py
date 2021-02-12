import datetime
import random
import datefinder


class Article:
    def __init__(self, header, text):
        self.header = header
        self.text = text

    def print_to_file(self):
        with open('news.txt', "a") as file:
            file.write(f'{self.header} --------------------\n{self.text}\n')
            if self.header == 'News':
                file.write(
                    f'{self.location}, {datetime.datetime.today().strftime("%d/%m/%Y %H.%M")}\n------------------------------\n\n')
            elif self.header == 'PrivatAdv':
                file.write(
                    f'Actual until {self.expiration_date.strftime("%d/%m/%Y")},{(self.expiration_date - datetime.date.today()).days} days left.'
                    f'\n------------------------------\n\n')
            elif self.header == 'Consider':
                file.write(f'Probability of truth: {self.score} %\n------------------------------\n\n')


class News(Article):
    def __init__(self, header, text, location):
        Article.__init__(self, header=header, text=text)
        self.location = location


class PrivatAdv(Article):
    def __init__(self, header, text, expiration_date):
        Article.__init__(self, header=header, text=text)
        self.expiration_date = expiration_date


class Consider(Article):
    def __init__(self, header, text, score):
        Article.__init__(self, header=header, text=text)
        self.score = score


def write_article():
    input_versions = ('News', 'PrivatAdv', 'Consider')
    header = input('Enter the topic you are interested in:\nNews\nPrivatAdv\nConsider\n:')

    while header not in input_versions:
        print('Please select correct topic:')
        header = input('News\nPrivatAdv\nYour version\n:')

    text = input('Type your text here\n:')
    if header == 'News':
        location = input('Enter location \n:')
        story = News(header, text, location)
        story.print_to_file()
    elif header == 'PrivatAdv':
        expiration_date = list(datefinder.find_dates(input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
        advertisement = PrivatAdv(header, text, expiration_date)
        advertisement.print_to_file()
    elif header == 'Consider':
        game = Consider(header, text, random.randint(1, 100))
        game.print_to_file()




if __name__ == '__main__':

    write_article()
    another_article = input('Do you want to publish something else? Y/N:')
    while another_article != 'N':
        write_article()
        another_article = input('Do you want to publish something else? Y/N:')

