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


class News(Article):
    def __init__(self, header, text, location):
        Article.__init__(self, header=header, text=text )
        self.location = location

    def print_location(self):
        with open('news.txt', "a") as file:
            file.write(f'{self.location}, {datetime.datetime.today().strftime("%d/%m/%Y %H.%M")}\n------------------------------\n\n')


class PrivatAdv(Article):
    def __init__(self, header, text, expiration_date):
        Article.__init__(self, header=header, text=text )
        self.expiration_date = expiration_date

    def print_expiration_date(self):
        with open('news.txt', "a") as file:
            file.write(f'Actual until {self.expiration_date.strftime("%d/%m/%Y")}, {(self.expiration_date - datetime.date.today()).days} days left.\n------------------------------\n\n')

class Consideration(Article):
    def __init__(self, header, text, score):
        Article.__init__(self, header=header, text=text )
        self.score = score

    def print_score(self):
        with open('news.txt', "a") as file:
            file.write(f'Probability of truth: {self.score} %\n------------------------------\n\n')

def write_article():
    input_versions = ('News', 'PrivatAdv', 'Consideration')
    header = input('Enter the topic you are interested in:\nNews\nPrivatAdv\nConsideration\n:')

    while header not in input_versions:
        print('Please select correct topic:')
        header = input('News\nPrivatAdv\nConsideration\n:')
    text = input('Type your text here\n:')

    if header == 'News':
        location = input('Enter location \n:')
        story = News(header, text, location)
        story.print_to_file()
        story.print_location()
    elif header == 'PrivatAdv':
        expiration_date = input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')
        try:
            expiration_date = list(datefinder.find_dates(expiration_date))[0].date()
        except:
            answer = input('Enter correct date\nPlease follow DD-MM-YYYY date version:')
        advertisement = PrivatAdv(header, text, expiration_date)
        advertisement.print_to_file()
        advertisement.print_expiration_date()
    elif header == 'Consideration':
        game = Consideration(header, text, random.randint(1, 100))
        game.print_to_file()
        game.print_score()
    another_article = input('Do you want to publish something else? Y/N:')
    return another_article


if __name__=='__main__':
    another_article = write_article()
    if another_article == 'Y':
        write_article()
    elif another_article == 'N':
        pass


