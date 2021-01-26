import random

# bubblesort) the random list
def bubblesort(list_unsorted):
    list_len = len(list)
    while list_len != 0:
        j = 0
        #walk through the full list
        while j != list_len - 1:
            # each element is compared in pair
            if list[j + 1] < list[j]:
                temp = list[j + 1]
                # elements are swapped if they are not in order
                list[j + 1] = list[j]
                list[j] = temp
            # moving to the next pair
            j += 1
        # until the end of list
        list_len -= 1
    return list

def get_avg(list):
    # declare all the necessary variables
    total_even = 0
    total_odd = 0
    count_even = 0
    count_odd = 0
    avg_even = 0
    avg_odd = 0
    # check every value
    for i in list:
        if i == 0:
            pass
        # is it even?
        elif i % 2 == 0:
            total_even = total_even + i
            count_even = count_even + 1
        #is it odd?
        elif i % 2 != 0:
            total_odd = total_odd + i
            count_odd = count_odd + 1

    try:
        avg_even = round(total_even / count_even)
    except ZeroDivisionError:
        print("No even values in a list")

    try:
        avg_odd = round(total_odd / count_odd)
    except ZeroDivisionError:
        print("No odd values in a list")

    print("The average for even values is " + str(avg_even), "\r\nThe average for odd values is " + str(avg_odd))
    return avg_even, avg_odd

if __name__ == '__main__':
    # get the list of random numbers in certain range
    list = random.sample(range (0, 1001), 100)
    bubblesort(list)
    get_avg(list)

