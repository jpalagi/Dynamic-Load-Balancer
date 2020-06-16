import os
import sys
import threading
import time
import psutil
from flask import Flask
from flask import jsonify
import random

# Declaring Global variables

server_app_pid = os.getpid()
# User inputs:
# 1. Server ID
server_id = sys.argv[1]

# 2. Server IP address
server_ip = sys.argv[2]

# 3. Server Port
server_port = sys.argv[3]

# 4. Load check frequency (sec), e.g. 60 sec
load_update_freq = int(sys.argv[4])

# 5. Generate load randomly? Y or N
generate_random_load = sys.argv[5]

# Count of Requests
request_count = 0

os.system('mkdir -p /home/fileout')
os.chdir('/home/fileout')
path = os.getcwd()

status = {'id': server_id,
          'load': 0,
          'count': 0}
app = Flask(__name__)


def get_random_file_size():
    global generate_random_load
    if generate_random_load == 'Y':
        r1 = random.randint(10240, 10240000)
    else:
        r1 = 10240000
    return r1


@app.route('/status', methods=['GET'])
def share_status():
    global status
    return jsonify(status)


@app.route('/use-cpu', methods=['GET'])
def use_cpu():
    check_number_of_requests()
    with open(path + '/use-cpu_' + server_id, 'wb') as fileout:
        r1 = get_random_file_size()
        fileout.write(os.urandom(r1))
    out = 'File created with size ' + str(r1) + ' by server ' + server_id + '\n'
    return out


def check_load():
    global status
    global load_update_freq
    global server_app_pid
    while True:
        for p in psutil.process_iter(attrs=['pid', 'cpu_times']):
            if server_app_pid == p.info['pid']:
                current_load = sum(p.info['cpu_times'])
                print('current load: ' + str(current_load))
                status['load'] = current_load

        print('Status: ', status)

        time.sleep(load_update_freq)


def check_number_of_requests():
    global status
    global request_count
    request_count = request_count + 1            #random.randint(1, 3)
    status['count'] = request_count
    print(status['count'])


if __name__ == "__main__":

    loadT = threading.Thread(target=check_load)
    loadT.start()
    app.run(host=server_ip, port=server_port)

    loadT.join()
