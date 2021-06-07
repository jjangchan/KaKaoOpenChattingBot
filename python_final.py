import re

def exam1(int_num):
    str_result = "짝" if int_num%2 == 0 else "홀"
    return str_result


def exam2(list_source):
    list_des = []
    for v in list_source:
        if v not in list_des:
            list_des.append(v)
    return list_des


def exam3(int_num):
    list_nums = [i*int_num for i in range(1, 10)]
    return list_nums


def exam4(key):
    phones = {"S5": 2014, "S7": 2016, "note8": 2017, "S9": 2018, "S10": 2019}
    return phones.get(key)


def exam5(str_number):
    int_result = int(str_number.split('-')[1][0])
    str_sex = "여성" if  int_result == 2 else "남성"
    return str_sex


def exam6(int_num):
    return int_num**2;


def exam7(int_nums):
    for i in range(0, len(int_nums)-1) :
        index_sub = i;
        for j in range(i+1, len(int_nums)) :
            index_sub = j if int_nums[j] < int_nums[index_sub] else index_sub
        int_nums[i], int_nums[index_sub] = int_nums[index_sub], int_nums[i]
    return int_nums


def exam8(float_r):
    return (float_r**2)*3.14


def exam9(str_pn):
    r = re.compile("(\d{3}[-]\d{4}[-])\d{4}")
    return r.sub("\g<1>####", str_pn)


def exam10(list_nums):
    return sum(list_nums)/len(list_nums)