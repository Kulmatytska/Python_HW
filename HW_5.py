import datetime
import random

# input_versions = ('1', '2', '3')
# response = input('Enter the topic you are interested in:\n1 for news\n2 for privat_adv\n3 for consideration \n:')
# while response not in input_versions:
#     print('Please select correct topic:')
#     response = input('news\n privat_adv\n consideration \n:')
#
# print('lets start')
# with open('news.txt', "a") as file:
#     if response == '1':
#         text = input('Describe, what has happened\n: ')
#         news_location = input('Where it has happened\n: ')
#         date = datetime.datetime.today()
#         file.write(f'News -------------------------\n{text}\n{news_location},{date}\n------------------------------\n\n')
#
#     elif response == '2':
#         text = input('Type your adv here\n: ')
#         expiration_date = date(input('Till what date do you want to keep it published?\n: '))
#         date = datetime.datetime.today()
#         file.write(f'Privat_adv -------------------------\n{text}\nActual until{expiration_date},{expiration_date - date}days left\n------------------------------\n\n')

#     else:
#         text = input('Type your consideration here\n: ')
#         score = random.randint(1, 100)
#         file.write(f'Consideration -------------------------\n{text}\nProbability of truth: {score} %\n------------------------------\n\n')

input_versions = ('1', '2', '3')
response = input('Enter the topic you are interested in:\n1 for news\n2 for privat_adv\n3 for consideration \n:')
while response not in input_versions:
    print('Please select correct topic:')
    response = input('\n1 for news\n2 for privat_adv\n3 for consideration \n:')


class News:
    def __init__(self, response):
        self.responce = response

    def get_text(self):
        self.text = text

    def get_news_location(self):
        self.news_location = input('Where it has happened\n: ')

    def get_current_date(self):
        self.current_date = datetime.datetime.today()


class PrivatAdv(News):
    def __init__(self, response):
        News.__init__(self, response=response)

    def get_text(self):
        self.text = input('Type your adv here\n: ')

    def get_expiration_date(self):
        self.expiration_date = datetime.date(input('Till what date do you want to keep it published?\n: '))


class Consideration(News):
    def __init__(self, response):
        News.__init__(self, response=response)

    def get_score(self):
        self.score = random.randint(1, 100)

    def get_text(self):
        self.text = input('What would you like to ask?\n: ')

article = News(response=response)
advertisement = PrivatAdv(response=response)
probability = Consideration(response=response)


with open('news.txt', "a") as file:
    if response == '1':
        file.write(f'News -------------------------\n{article.get_text()}\n{article.get_news_location()},{datetime.datetime.today()}\n------------------------------\n\n')
    elif response == '2':
        file.write(f'Privat_adv -------------------------\n{advertisement.get_text()}\nActual until{advertisement.get_expiration_date()},{advertisement.get_expiration_date() - datetime.datetime.today()}days left\n------------------------------\n\n')
    else:
        file.write(f'Consideration -------------------------\n{probability.get_text()}\nProbability of truth: {probability.get_score()} %\n------------------------------\n\n')
