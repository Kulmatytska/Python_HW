import random
import string

def get_the_list():
    uni_list = []
    # get the number of key/values in a dict + dicts quantity
    quantity = random.randint(2,10)
    for i in range(quantity):
        # generate lists for keys and values
        keys = random.sample(string.ascii_lowercase, quantity)
        values = random.sample(range (0, 100), quantity)
        # combine them into dict
        my_dict = dict(zip(keys, values))
        # append new dict to a list
        uni_list.append(my_dict)
    print(uni_list)
    return uni_list

 def create_common_dict(uni_list):
    common_dict = {}
    i = 0
    for dictionary in uni_list:
        for key, value in dictionary.items():
            if key not in common_dict:
                common_dict.update({key : value})
            else:
                if dictionary.get(key) < common_dict.get(key):
                    continue
                else:
                    common_dict.update({key + '_' + str(i) : value})
        i += 1

    print(common_dict)
    return common_dict


if __name__  ==  '__main__' :
    uni_list = get_the_list()
    create_common_dict(uni_list)