import time
import shlex
import logging
import subprocess


def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


def mpi_task(directory, resolution, file, task_name):
    logging.getLogger('logger').info('Processing started')
    data = subprocess.Popen(shlex.split('mpiexec -n 4 ' +
                                        '-f Project/Server/MPI/hostfile ' +
                                        'python Project/Server/MPI/StartScript.py ' + directory + ' ' +
                                        resolution[0].__str__() + ' ' + resolution[1].__str__() + ' ' +
                                        '20 ' + file + ' ' +
                                        task_name),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = data.stdout.readline().decode('utf-8').strip()
        if output == '' and data.poll() is not None:
            break
        if output:
            logging.getLogger('logger').info(output)
            print(output)

    if data.returncode == 0:
        logging.getLogger('logger').info('Processing completed')
        return data.returncode
    else:
        logging.getLogger('error-logger').error(data.stderr.read().decode('utf-8'))
        return data.returncode
