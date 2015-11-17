import random
import math
import matplotlib.pyplot as plt

__author__ = 'nikita'


def distribution_func(y):
    # return - math.log(1 - y * (1 - math.exp(-1)))
    return math.log(math.log(1 / (1 - y)) / math.log(3)) / math.log(3)


def generate_distribution_array(test_numbers=100):
    distribution_array = []
    for i in xrange(test_numbers):
        distribution_array.append(distribution_func(random.uniform(0, 1)))
    return distribution_array


def write_values(filename, random_numbers):
    test_file = open(filename, 'r+')
    for item in random_numbers:
        print >> test_file, item
    test_file.close()


def max_y_value(random_numbers):
    return 100 * max(random_numbers)


def solution_a(test_one=100, test_two=1000, draw_dots=False):
    random_numbers = generate_distribution_array(test_numbers=test_one)
    # write_values('test_a.txt', random_numbers)

    plt.figure(1)
    plt.title("number of tests: 100")
    plt.hist(random_numbers, 10)
    plt.axis([0, 1, 0, 150])

    if draw_dots:
        plt.figure(3)
        plt.title("number of tests: 100")
        plt.plot(random_numbers, random_numbers, 'ro')

    random_numbers_2 = generate_distribution_array(test_numbers=test_two)
    # write_values('test_a1.txt', random_numbers_2)

    plt.figure(2)
    plt.title("number of tests: 1000")
    plt.hist(random_numbers_2, 10)
    plt.axis([0, 1, 0, 500 * max(random_numbers_2)])

    if draw_dots:
        plt.figure(4)
        plt.title("number of tests: 1000")
        plt.plot(random_numbers, random_numbers_2, 'ro')

    plt.show()


def solution_b(test_number=1000, draw_dots=False):
    distribution_array = []
    for i in xrange(test_number):
        distribution_array.append(sum(generate_distribution_array(test_numbers=30)))
        print i, distribution_array[i]
    # write_values('test_b.txt', distribution_array)

    if draw_dots:
        plt.figure(1)
        plt.title("Task b")
        plt.plot(distribution_array, distribution_array, 'ro')
        plt.show()

    plt.figure(2)
    plt.title("Task b")
    plt.hist(distribution_array, 1000)
    plt.axis([0, 20, 0, 15])
    plt.show()

if __name__ == '__main__':
    solution_a()
    # solution_b(draw_dots=True)
