import sys
import math
from MPI.Fabric import Fabric


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def is_primal(number):
    if number <= 3:
        return number, True
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return number, False
    return number, True


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid number of arguments.')
    else:
        data = []
        for elem in split(list(range(1, int(sys.argv[1]))), int(sys.argv[2])):
            data.append(elem)

        zombies = Fabric()
        brains = zombies.work(data, is_primal)

        brains.sort(key=lambda x: x[0])

        output = []

        print('output:', end=' ')
        for tissue in brains:
            for neuron in tissue[1]:
                output.append(neuron)
                print(neuron, end=' ')
        print('\n', end='')
        sys.exit(output)
