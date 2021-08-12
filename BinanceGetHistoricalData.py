import csv
from datetime import  datetime

def ReadCSVFile(file_path) :
    with open(file_path, 'r') as file :
        rdr = csv.reader(file)
        WriteCSVFile(rdr, "BTCUSDT5M.csv", 5)

def Write1MCSVFile(rdr, file_path) :
    list_csv = []
    for line in reversed(list(rdr)):
        double_open = round(float(line[3]), 2)
        double_high = round(float(line[4]), 2)
        double_low = round(float(line[5]), 2)
        double_close = round(float(line[6]), 2)
        int_volume = int(float(line[7]))
        int_unix = int(line[0]) / 1000
        str_day = datetime.utcfromtimestamp(int_unix).strftime('%Y.%m.%d')
        str_hour = datetime.utcfromtimestamp(int_unix).strftime('%H:%M')
        list_temp = [str_day, str_hour, double_open, double_high, double_low, double_close, int_volume]
        list_csv.append(list_temp)
    with open(file_path, 'w', newline='') as file :
        wr = csv.writer(file)
        for i in list_csv :
            wr.writerow(i)

def WriteCSVFile(rdr, file_path, int_minute) :
    list_csv = []
    double_open = double_max = double_min = int_total_volume = 0
    for line in reversed(list(rdr)):
        int_unix = int(line[0]) / 1000
        int_min = int(datetime.utcfromtimestamp(int_unix).strftime('%M'))
        double_high = round(float(line[4]), 2)
        double_low = round(float(line[5]), 2)
        double_min = double_low if double_min == 0 else min(double_min, double_low)
        double_max = max(double_max, double_high)
        double_open = round(float(line[3]), 2) if double_open == 0 else double_open
        int_total_volume += int(float(line[7]))
        if (int_min+1) % int_minute == 0:
            double_close = round(float(line[6]), 2)
            str_day = datetime.utcfromtimestamp(int_unix-(60*(int_minute-1))).strftime('%Y.%m.%d')
            str_hour = datetime.utcfromtimestamp(int_unix-(60*(int_minute-1))).strftime('%H:%M')
            list_temp = [str_day, str_hour, double_open, double_max, double_min, double_close, int_total_volume]
            list_csv.append(list_temp)
            double_open = int_total_volume = double_max = double_min = 0

    with open(file_path, 'w', newline='') as file :
        wr = csv.writer(file)
        for i in list_csv :
            wr.writerow(i)

