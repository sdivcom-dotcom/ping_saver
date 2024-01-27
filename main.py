from pythonping import ping
import argparse
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description="")

parser.add_argument('-address_1', '--address_1',
                    dest='address_1',
                    help='address ping',
                    default="rbc.ru",
                    type=str)

parser.add_argument('-address_2', '--address_2',
                    dest='address_2',
                    help='address ping',
                    default="google.com",
                    type=str)


parser.add_argument('-address_3', '--address_3',
                    dest='address_3',
                    help='address ping',
                    default="ya.ru",
                    type=str)

parser.add_argument('-address_4', '--address_4',
                    dest='address_4',
                    help='address ping',
                    default="bbc.com",
                    type=str)

parser.add_argument('-address_5', '--address_5',
                    dest='address_5',
                    help='address ping',
                    default="reddit.com",
                    type=str)

parser.add_argument('-cycle', '--cycle',
                    dest='cycle',
                    help='cycle',
                    default=1000,
                    type=int)

args = parser.parse_args()
address_1 = args.address_1
address_2 = args.address_2
address_3 = args.address_3
address_4 = args.address_4
address_5 = args.address_5
cycle = args.cycle


def pinger(addr, size, count):
    response_list = ping(addr, size, count)
    response_mass = [response_list.rtt_avg_ms, response_list.rtt_max_ms, response_list.rtt_min_ms, response_list.stats_packets_lost]
    return response_mass


def load_data_from_json(filename):
    filename = filename + ".json"
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def what_day():
    now = datetime.now()
    time_mass = [now.day,now.month,now.year]
    time_mass = str(time_mass)
    time_mass = time_mass.replace("[", "")
    time_mass = time_mass.replace("]", "")
    time_mass = time_mass.replace(" ", "")
    time_mass = time_mass.replace(",", "_")
    return time_mass



def add_data_to_json(filename, avg, max, min, loss, date=None):
    #times = what_day()
    filename = filename + ".json"
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    new_data = {
        "data": date,
        "avg": avg,
        "max": max,
        "min": min,
        "loss": loss,
    }

    existing_data.append(new_data)
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4) 


def plot_data(data, address):
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'])
    plt.figure(figsize=(12, 8))
    plt.plot(df['data'].to_numpy(), df['min'].to_numpy())
    plt.title('min vs. Data')
    plt.xlabel('Date and Time')
    plt.ylabel('min')
    name = address + '_min.png'
    plt.savefig(name)
    plt.clf()
    plt.plot(df['data'].to_numpy(), df['max'].to_numpy())
    plt.title('max vs. Data')
    plt.xlabel('Date and Time')
    plt.ylabel('max')
    plt.savefig('max.png')
    name = address + '_max.png'
    plt.savefig(name)
    plt.clf()
    plt.plot(df['data'].to_numpy(), df['avg'].to_numpy())
    plt.title('avg vs. Data')
    plt.xlabel('Date and Time')
    plt.ylabel('avg')
    name = address + '_avg.png'
    plt.savefig(name)
    plt.clf()
    plt.plot(df['data'].to_numpy(), df['loss'].to_numpy())
    plt.title('loss vs. Data')
    plt.xlabel('Date and Time')
    plt.ylabel('loss')
    name = address + '_loss.png'
    plt.savefig(name)
    plt.clf()


def main(address_1, address_2, address_3, address_4, address_5):
    size = 40
    count = 100
    filename_1 = address_1.replace('.','_')
    filename_2 = address_2.replace('.','_')
    filename_3 = address_3.replace('.','_')
    filename_4 = address_4.replace('.','_')
    filename_5 = address_5.replace('.','_')
    response_mass = pinger(address_1, size, count)
    add_data_to_json(filename_1, response_mass[0], response_mass[1], response_mass[2], response_mass[3], date=None)
    response_mass = pinger(address_2, size, count)
    add_data_to_json(filename_2, response_mass[0], response_mass[1], response_mass[2], response_mass[3], date=None)
    response_mass = pinger(address_3, size, count)
    add_data_to_json(filename_3, response_mass[0], response_mass[1], response_mass[2], response_mass[3], date=None)
    response_mass = pinger(address_4, size, count)
    add_data_to_json(filename_4, response_mass[0], response_mass[1], response_mass[2], response_mass[3], date=None)
    response_mass = pinger(address_5, size, count)
    add_data_to_json(filename_5, response_mass[0], response_mass[1], response_mass[2], response_mass[3], date=None)




i = 0
while i < cycle:
    main(address_1, address_2, address_3, address_4, address_5)
    print(i)
    i = i + 1

filename_1 = address_1.replace('.','_')
data = load_data_from_json(filename_1)
plot_data(data, filename_1)

filename_2 = address_2.replace('.','_')
data = load_data_from_json(filename_2)
plot_data(data, filename_2)

filename_3 = address_3.replace('.','_')
data = load_data_from_json(filename_3)
plot_data(data, filename_3)

filename_4 = address_4.replace('.','_')
data = load_data_from_json(filename_4)
plot_data(data, filename_4)

filename_5 = address_5.replace('.','_')
data = load_data_from_json(filename_5)
plot_data(data, filename_5)