import subprocess
import csv
import time
import requests
import threading
import sys
import argparse

# Declaring Global variables
# {
#     's1': {'count': 0, 'health': 'UP', 'ip': 'IP Address', 'port': 'Port'}
# }
# List of servers in server-farm
server_list = {}
# List of servers up and running
up_servers = {}
# Server load at the beginning of load-balance check duration
base_load = {}


def load_check(feedback_freq, start_time):
    global server_list, up_servers, base_load

    plot_graph = open('plot_server_load.csv', mode='w+')
    writer = csv.writer(plot_graph)
    writer.writerow(['timestamp', 'server_id', 'load'])
    plot_graph.close()

    while True:
        plot_graph = open('plot_server_load.csv', mode='a+')
        writer = csv.writer(plot_graph)
        with open('ip_add_port.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, skipinitialspace=True)

            for row in csv_reader:
                server_id = row['ID']
                server_ip = row['IP_Address']
                server_port = row['Port']

                if server_id not in server_list:
                    server_list[server_id] = {
                        "ip": server_ip,
                        "port": server_port
                    }
                get_server_feedback(server_id)
                time_since_start = time.time() - start_time
                writer.writerow([int(round(time_since_start, 3)), server_id, up_servers[server_id]['load']])
        print(up_servers)
        selected_server = select_server()
        configure_bgp(selected_server)
        plot_graph.close()
        time.sleep(feedback_freq)


def get_server_feedback(server_id):
    global server_list, up_servers, base_load

    try:
        response = requests.get(
            "http://" + server_list[server_id]['ip'] + ":" + server_list[server_id]['port'] + "/status", timeout=2)
        health = 'UP'
        s_list = response.json()


        server_list[s_list['id']]['load'] = s_list['load']
        server_list[server_id]['health'] = health
        up_servers[server_id] = server_list[server_id].copy()
        up_servers[s_list['id']]['load'] = s_list['load'] 

    except Exception as e:
        health = 'DOWN'
        print('Server ' + server_id + ' is down.')
        if server_id in up_servers:
            del up_servers[server_id]
        server_list[server_id]['load'] = 0
        server_list[server_id]['health'] = health


def select_server():
    global server_list, up_servers

    selected_server = min(up_servers.keys(), key=(lambda k: up_servers[k]['load']))
    print('Current server: ' + selected_server)
    return selected_server

# Function for setting bind9 configuration
def configure_bgp(selected_server):
    print(selected_server)
    if selected_server == "S1":
        #Remove BGP prepend for R1 and add BGP prepend for R2 and R3
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"no neighbor 192.168.10.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.11.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.12.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.13.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
    elif selected_server == "S2":
        #Remove BGP prepend for R2 and add BGP prepend for R1 and R3
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.10.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"no neighbor 192.168.11.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.12.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.13.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
    elif selected_server == "S3":
        #Remove BGP prepend for R2 and add BGP prepend for R1 and R3
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.10.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.11.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"no neighbor 192.168.12.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.13.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
    else:
        #Remove BGP prepend for R3 and add BGP prepend for R1 and R2 
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.10.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.11.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"neighbor 192.168.12.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        output = subprocess.Popen("vtysh -c \"config t\" -c \"router bgp 200\" -c \"no neighbor 192.168.13.2 route-map prepend in\"", stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()

def loadbalance_check(loadbalance_verify_freq, loadbalance_tolerarence):
    global up_servers, server_list, base_load

    while True:

        time.sleep(loadbalance_verify_freq)
        min_load_server = min(up_servers.keys(), key=(lambda k: up_servers[k]['load']))
        max_load_server = max(up_servers.keys(), key=(lambda k: up_servers[k]['load']))
        offset = up_servers[max_load_server]['load'] - up_servers[min_load_server]['load']
        if offset <= loadbalance_tolerarence:
            print('============================================')
            print('At the end of ' + str(loadbalance_verify_freq) + ' seconds, load is balanced. Offset: ' + str(offset))
            print('============================================')
        else:
            print('============================================')
            print('At the end of ' + str(loadbalance_verify_freq) + ' seconds, load is not balanced. Offset: ' + str(offset))
            print('============================================')


def get_arguments():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f1', '--feedback_freq', type=float, required=True,
                            help='Feedback frequency (sec), e.g. 60 (secs)')
        parser.add_argument('-f2', '--loadbalance_verify_freq', type=int, required=True,
                            help='Load-balance check frequency (sec), e.g. 3600 (1 hr)')
        parser.add_argument('-t', '--loadbalance_tolerarence', type=float, required=True,
                            help='Threshold for CPU-time loadbalance check(sec) , e.g 30')

        args = parser.parse_args()
        return args
    except Exception as e:
        print(
            "Exiting due to incorrect usage of arguments.\n Usage : python dnsloadbalancer.py {-f1 Feedback_Interval} {-f2 LB_check_interval} {-t LB_Tolerance}")
        sys.exit(0)


def main():
    # Start time of the load-balancer process
    start_time = time.time()

    args = get_arguments()

    load_checkThread = threading.Thread(target=load_check, args=(args.feedback_freq, start_time))
    load_checkThread.start()

    time.sleep(1)

    lb_checkThread = threading.Thread(target=loadbalance_check,
                                      args=(args.loadbalance_verify_freq, args.loadbalance_tolerarence))
    lb_checkThread.start()

    load_checkThread.join()
    lb_checkThread.join()


if __name__ == "__main__":
    main()
 
