import os
import shlex
import shutil
import zipfile
import subprocess
from mpi4py import MPI


class Fabric:
    def __init__(self, x, y, r, zip_arch, task_name):
        self.__comm = MPI.COMM_WORLD
        self.__size = self.__comm.Get_size()
        self.__rank = self.__comm.Get_rank()
        self.__status = MPI.Status()

        self.x = x
        self.y = y
        self.r = r
        self.zip_arch = zip_arch
        self.task_name = task_name

    def work(self, user_input_path):
        try:
            if self.__rank == 0:
                zipfile.ZipFile(self.zip_arch).extractall(user_input_path)
                folder = os.path.splitext(self.zip_arch)[0]
                folder_cont = os.listdir(folder)
                files = []
                for elem in folder_cont:
                    file = os.path.join(folder, elem)
                    files.append(file)
                return self.create_master(files)
            else:
                self.create_slave()
        except Exception as e:
            raise e

    def create_master(self, queue):
        memory = []
        resource_mark = 0
        for i in range(1, self.__size):
            try:
                if queue:
                    data = queue.pop(0)
                    self.__comm.send([resource_mark, data], dest=i)
                    resource_mark += 1
                else:
                    self.__comm.send([-1, i.__str__() + ' slave was assassinated.\n'], dest=i)
                    self.__size -= 1
            except Exception as e:
                raise 'Error in sending first tasks: ' + i.__str__() + ' ' + e.__str__()

        while queue:
            try:
                output_data = self.__comm.recv(source=MPI.ANY_SOURCE, status=self.__status)
                memory.append(output_data)
                self.__comm.send([resource_mark, queue.pop(0)], dest=self.__status.Get_source())
                resource_mark += 1
            except Exception as e:
                raise 'Error in queuing tasks: ' + e.__str__()

        try:
            for i in range(1, self.__size):
                output_data = self.__comm.recv(source=MPI.ANY_SOURCE)
                memory.append(output_data)

            for i in range(1, self.__size):
                self.__comm.send([-1, i.__str__() + ' slave died suddenly.\n'], dest=i)
        except Exception as e:
            raise 'Error in receiving last tasks: ' + e.__str__()

        try:
            subprocess.run(shlex.split('ffmpeg -r 60 -i ' + os.path.splitext(self.zip_arch)[0] +
                                       '/%d.bmp -c:v libx264 -vf fps=60 -pix_fmt yuv420p ' +
                                       self.task_name + '.mp4'), stdout=subprocess.PIPE)

            shutil.rmtree(os.path.splitext(self.zip_arch)[0])
        except Exception as e:
            raise 'Cannot convert bmps to mp4: ' + e.__str__()

        print(self.__rank.__str__() + ' master thanks, that he could serve you. Farewell, my lord.\n')
        return memory

    def create_slave(self):
        while True:
            try:
                data = self.__comm.recv(source=0)
                if -1 in data:
                    print(data[1])
                    exit()
                else:
                    subprocess.run(shlex.split('./Project/Server/MPI/Raytracing ' + '-x ' + self.x +
                                               ' -y ' + self.y + ' -r ' + self.r + ' -i ' +
                                               data[1]), stdout=subprocess.PIPE)

                    self.__comm.send(data[0], dest=0)
            except Exception as e:
                raise 'Error in processing task: ' + e.__str__()
