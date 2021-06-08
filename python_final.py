import re
import unittest


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


def exam7(list_nums):
    for i in range(0, len(list_nums)-1) :
        index_sub = i;
        for j in range(i+1, len(list_nums)) :
            index_sub = j if list_nums[j] < list_nums[index_sub] else index_sub
        list_nums[i], list_nums[index_sub] = list_nums[index_sub], list_nums[i]
    return list_nums


def exam8(float_r):
    return (float_r**2)*3.14


def exam9(str_pn):
    r = re.compile("(\d{3}[-]\d{4}[-])\d{4}")
    return r.sub("\g<1>####", str_pn)


def exam10(list_nums):
    return sum(list_nums)/len(list_nums)


class TestCUK(unittest.TestCase):

    def setUp(self):
        pass

    def test_exam1(self):
        for i in range(1, 100):
            odd_even = "짝" if i%2 == 0 else "홀"
            self.assertEqual(exam1(i), odd_even)

    def test_exam2(self):
        self.assertCountEqual(exam2([1,2,1,1,1]), [1,2])
        self.assertCountEqual(exam2([3,3,4,5]), [3,4,5])
        self.assertCountEqual(exam2([5,3,3,3,5,5,2,1,5]), [1,2,3,5])
        self.assertCountEqual(exam2([3,3,10,9,2,10,9,9,9,9]), [2,3,9,10])
        self.assertCountEqual(exam2([3,3,1,1,2,3,3,3,4,5,3,4,5,6,10,2,1,1]), [1,2,3,4,5,6,10])

    def test_exam3(self):
        for i in range(2, 10) :
            list_multiple = []
            for j in range(1, 10) :
                list_multiple.append(i*j)
            self.assertEqual(exam3(i), list_multiple)

    def test_exam4(self):
        phones = {"S5": 2014, "S7": 2016, "note8": 2017, "S9": 2018, "S10": 2019}
        for key, value in phones.items():
            self.assertEqual(exam4(key), value)

    def test_exam5(self):
        self.assertEqual(exam5("820327-1022421"), "남성")
        self.assertEqual(exam5("820327-2022421"), "여성")

    def test_exam6(self):
        self.assertEqual(exam6(2), 4)
        self.assertEqual(exam6(3), 9)
        self.assertEqual(exam6(5), 25)

    def test_exam7(self):
        self.assertEqual(exam7([10,3,8,7]), [3,7,8,10])
        self.assertEqual(exam7([4,3,2,1]), [1,2,3,4])
        self.assertEqual(exam7([52,50,100,5,345,20,450,3,121,10,122,2,1]), [1,2,3,5,10,20,50,52,100,121,122,345,450])

    def test_exam8(self):
        self.assertEqual(exam8(2), 12.56)
        self.assertEqual(exam8(3), 28.26)

    def test_exam9(self):
        self.assertEqual(exam9("010-2513-6806"), "010-2513-####")
        self.assertEqual(exam9("010-3222-1234"), "010-3222-####")
        self.assertEqual(exam9("010-1221-0984"), "010-1221-####")

    def test_exam10(self):
        self.assertEqual(exam10([1,2,3,4]), 2.5)
        self.assertEqual(exam10([2,4,6,8,10]), 6.0)

    def tearDown(self):
        pass
