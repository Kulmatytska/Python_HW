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
    common_dict = {'0': 0}
    i = 0
    for dictionary in uni_list:
        for key, value in dictionary.items():
            firsts = [w[0] for w in list(common_dict)]
            if key not in firsts:
                common_dict.update({key: value})
            else:
                for k in list(common_dict.keys()):
                    if k[0] == key:
                        if dictionary.get(key) > common_dict.get(k):
                            common_dict.update({key + '_' + str(i): value})
                            del common_dict[k]
                        else:
                            common_dict.update({key + '_' + str([i for i, d in enumerate(uni_list) if d.get(key) == common_dict.get(k)]): common_dict.get(k)})
                            del common_dict[k]
        i += 1
    del common_dict['0']
    print(common_dict)
    return common_dict


if __name__=='__main__':
    uni_list = get_the_list()
    common_dict = create_common_dict(uni_list)