import datetime
import random
import datefinder


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
               f"Actual until: {expiration_date},{(expiration_date - datetime.date.today()).days} days left." \
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

    text = input('Type your text here\n:')
    if header == 'News':
        location = input('Enter location \n:')
        story = News(header, text, location)
        story.print_to_file(story.format_text(header, text, location), 'news.txt')
    elif header == 'PrivatAdv':
        expiration_date = list(datefinder.find_dates(input('Till what date we should keep it?\nPlease follow DD-MM-YYYY date version:')))[0].date()
        advertisement = PrivatAdv(header, text, expiration_date)
        advertisement.print_to_file(advertisement.format_text(header, text, expiration_date), 'news.txt')
    elif header == 'Consider':
        score = random.randint(1, 100)
        game = Consider(header, text, score)
        game.print_to_file(game.format_text(header, text, score), 'news.txt')


if __name__ == '__main__':
    # Please don't forget to create a pull request before merging to main
    write_article()
    another_article = input('Do you want to publish something else? Y/N:')
    while another_article != 'N':
        write_article()
        another_article = input('Do you want to publish something else? Y/N:')

