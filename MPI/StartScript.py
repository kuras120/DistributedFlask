import sys
import math
from Fabric import Fabric


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
        sys.stdout.write('Invalid number of arguments.')
    else:
        data = []
        for elem in split(list(range(1, int(sys.argv[1]))), int(sys.argv[2])):
            data.append(elem)

        zombies = Fabric()

        try:
            brains = zombies.work(data, is_primal)
        except Exception as e:
            sys.exit(e)

        brains.sort(key=lambda x: x[0])

        output = []

        sys.stdout.write('\noutput: ')
        for tissue in brains:
            for neuron in tissue[1]:
                output.append(neuron)
                sys.stdout.write(neuron.__str__() + ' ')
        sys.stdout.write('\n')

        sys.exit(0)
