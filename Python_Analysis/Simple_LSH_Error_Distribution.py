import numpy as np
import matplotlib.pyplot as plt

def compute_s_distribution(successProbability):
    resultset = []
    for i in range(len(successProbability)):
        s = np.cos(np.pi * (1 - successProbability[i]))
        resultset.append(s)
    return resultset


def compute_success_distribution(s):
    return 1-np.arccos(s)/np.pi


def plot_collision_sim(successProbability, sims):
    f = plt.figure()
    plt.plot(successProbability, sims)
    plt.title('similarity vs success probability')
    plt.xlabel('success probability')
    plt.ylabel('similarity')
    plt.show()
    f.savefig('plot.pdf')


if __name__ == '__main__':
    # successProbability_ = [0.3, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    #
    # successProbability_ = [0.2, 0.9]

    # successProbability_ = [0.59698668, 0.66666667, 0.74681669, 0.85643371, 0.95494659, 0.98576356]
    successProbability_ = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.97, 0.98, 0.99]
    similarity_ = compute_s_distribution(successProbability_)
    print("similarity: ", similarity_)

    plot_collision_sim(successProbability_, similarity_)
    # similarity = [0.3, 0.5, 0.7, 0.9, 0.99, 0.999]
    # successProbability = compute_success_distribution(similarity)
    # print("success probability: ", successProbability)