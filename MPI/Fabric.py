import os
import sys
import shlex
import zipfile
import subprocess
from mpi4py import MPI


class Fabric:
    def __init__(self, x, y, r):
        self.__comm = MPI.COMM_WORLD
        self.__size = self.__comm.Get_size()
        self.__rank = self.__comm.Get_rank()
        self.__status = MPI.Status()

        self.x = x
        self.y = y
        self.r = r

    def work(self, user_input_path, zip_arch):
        try:
            if self.__rank == 0:
                zipp = zipfile.ZipFile(zip_arch)

                data = zipp.extractall(user_input_path)
                folder = os.path.join(user_input_path, 'test/')
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
                    self.__comm.send([-1, i.__str__() + ' slave was assassinated.'], dest=i)
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
                self.__comm.send([-1, i.__str__() + ' slave died suddenly.'], dest=i)
        except Exception as e:
            raise 'Error in receiving last tasks: ' + e.__str__()

        sys.stdout.write(self.__rank.__str__() + ' master thanks, that he could serve you. Farewell, my lord.')
        return memory

    def create_slave(self):
        while True:
            try:
                data = self.__comm.recv(source=0)

                if -1 in data:
                    sys.stdout.write(data[1])
                    exit()
                else:
                    new_data = subprocess.run(shlex.split('./Raytracing ' + '-x ' + self.x + ' -y ' + self.y +
                                                          ' -r ' + self.r + ' -i ' + data[1]),
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    self.__comm.send([data[0], new_data], dest=0)
            except Exception as e:
                raise 'Error in processing task: ' + e.__str__()
