import os
import sys
import math
import shlex
import zipfile
import subprocess

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
    if len(sys.argv) != 6:
        sys.stdout.write('Invalid number of arguments.')
    else:
        user_input_path = sys.argv[1]
        x = sys.argv[2]
        y = sys.argv[3]
        r = sys.argv[4]
        zip_arch = os.path.join(user_input_path, sys.argv[5])

        zipp = zipfile.ZipFile(zip_arch)

        data = zipp.extractall(user_input_path)
        folder = os.path.join(user_input_path, 'test/')
        folder_cont = os.listdir(folder)

        files = []
        for elem in folder_cont:
            file = os.path.join(folder, elem)
            files.append(file)

        zombies = Fabric(x, y, r)

        try:
            brains = zombies.work(files)
            subprocess.run(shlex.split('ffmpeg -r 4 -i ' + folder + '/%d.bmp -c:v libx264 -vf fps=60 -pix_fmt yuv420p '
                                       + os.path.join(user_input_path, '../OUTPUT') + '/out.mp4'),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sys.exit(0)
        except Exception as e:
            sys.exit(e)
