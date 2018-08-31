import numpy as np
import gc


# generate random/uniform data, value range [0, 1]
def random_generator(filename, min, max, dimension, count):
    f = open(filename, 'w')
    # f.write(str(dimension) + "\n")
    # f.write(str(count) + "\n")
    for i in range(0, count):
        for j in range(0, dimension):
            # each value is uniform distributed between min and max
            f.write(str(np.random.uniform(min, max)) + " ")
        f.write("\n")
    f.close()


def gen_correlated(dimension):
    array = [0] * dimension
    # compute mean value from uniform distribution
    v = np.mean(np.random.uniform(0, 1, dimension))
    # pick Gaussian/normal distribution as the smaller counter part
    variance = 0
    if v <= 0.5:
        variance = v
    else:
        variance = 1.0 - v
    # for each point each dimension, generate single point
    for j in range(0, dimension):
        value = np.random.normal(0, variance)
        # introduce randomness at neighbor values
        array[j] = v + value
        array[(j + 1) % dimension] = v - value
    return array


# check if element < 0 or element > 1 exists
def check(array, dimension):
    for j in range(0, dimension):
        # enforce points value range [0, 1]
        if array[j] < 0 or array[j] > 1:
            return True
    return False


# generate correlated data, point value range [0, 1]
def correlated_generator(filename, count, dimension):
    f = open(filename, 'w')
    # f.write(str(dimension) + "\n")
    # f.write(str(count) + "\n")
    for i in range(0, count):
        array = gen_correlated(dimension)
        flag = check(array, dimension)
        while flag:
            array = gen_correlated(dimension)
            flag = check(array, dimension)

        for j in range(0, dimension):
            f.write(str(array[j]) + " ")
        f.write("\n")
        gc.collect()
    f.close()


def gen_anti_correlated(dimension):
    array = [0] * dimension
    # get value from Gaussian/normal distribution
    v = np.random.normal(0.5, 0.25)
    # pick Gaussian/normal distribution as the smaller counter part
    variance = 0
    if v <= 0.5:
        variance = v
    else:
        variance = 1.0 - v
    # for each point each dimension, generate single point
    for j in range(0, dimension):
        # add uniform value to the gaussian counter-part
        value = np.random.uniform((-1.0 * variance), variance)
        # introduce randomness at neighbor values
        array[j] = v + value
        array[(j + 1) % dimension] = v - value
    return array


# generate anti-correlated data
def anti_correlated_generator(filename, count, dimension):
    f = open(filename, 'w')
    # f.write(str(dimension) + "\n")
    # f.write(str(count) + "\n")
    for i in range(0, count):
        array = gen_correlated(dimension)
        flag = check(array, dimension)
        while flag:
            array = gen_anti_correlated(dimension)
            flag = check(array, dimension)

        for j in range(0, dimension):
            f.write(str(array[j]) + " ")
        f.write("\n")
        gc.collect()
    f.close()


if __name__ == '__main__':
    point_dimension = 2
    point_min = 0
    point_max = 1
    num_of_point = 1000

    print("generating random distributed data...")
    random_data_file_name = "random_data.txt"
    random_generator(random_data_file_name, point_min, point_max, point_dimension, num_of_point)

    print("generating correlated distributed data...")
    correlated_data_file_name = "correlated_data.txt"
    correlated_generator(correlated_data_file_name, num_of_point, point_dimension)

    print("generating anti-correlated distributed data...")
    anti_correlated_data_file_name = "anticorrelated_data.txt"
    anti_correlated_generator(anti_correlated_data_file_name, num_of_point, point_dimension)
    print('All Done.\n')