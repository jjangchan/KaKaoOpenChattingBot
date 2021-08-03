import csv
from datetime import  datetime

def ReadCSVFile(file_path) :
    with open(file_path, 'r') as file :
        rdr = csv.reader(file)
        list_csv = []
        int_num = 0
        double_open = double_max = double_min = int_total_volume = 0
        for line in reversed(list(rdr)) :
            int_num += 1
            double_high = round(float(line[4]), 2)
            double_low = round(float(line[5]), 2)
            double_min = double_low if double_min == 0 else min(double_min, double_low)
            double_max = max(double_max, double_high)
            double_open = round(float(line[3]), 2) if double_open == 0 else double_open
            int_total_volume += int(float(line[7]))
            int_unix = int(line[0]) / 1000
            int_min = int(datetime.utcfromtimestamp(int_unix).strftime('%M'))

            if int_min%15 == 0 :
                double_close = round(float(line[6]), 2)
                str_day = datetime.utcfromtimestamp(int_unix).strftime('%Y.%m.%d')
                str_hour = datetime.utcfromtimestamp(int_unix).strftime('%H:%M')
                list_temp = [str_day, str_hour, double_open, double_max, double_min, double_close, int_total_volume]
                list_csv.append(list_temp)
                double_open = int_total_volume = double_max = double_min = 0

        WriteCSVFile("BTCUSDT15M.csv", list_csv)

def WriteCSVFile(file_path, list_csv) :
    with open(file_path, 'w', newline='') as file :
        wr = csv.writer(file)
        for i in list_csv :
           wr.writerow(i)

