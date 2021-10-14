import calendar
import json
import time
import datetime

import twitter;
import telegram;

class Data(object) :
    twitter_api = None
    telegram_bot = None
    twitter_consumer_key = ""
    twitter_consumer_secret = ""
    twitter_access_token = ""
    twitter_access_secret = ""
    telegram_token = ""
    str_current_url = ""
    list_account = []
    list_telegram_account = []
    sleep_second = 0

    def __init__(self, str_file_name):
        self.str_file_name = str_file_name
        self.__LoadJson()
        self.ConnectTwitter()
        self.ConnectTelegram()
        current_time = int(time.time())-(60*60*9) #GMT+0
        self.dict_time = {account: current_time for account in Data.list_account}
        self.working = True

    # 트위터 연결
    def ConnectTwitter(self):
        Data.twitter_api = twitter.Api()
        try:
            Data.twitter_api = twitter.Api(consumer_key=self.twitter_consumer_key,
                                           consumer_secret=self.twitter_consumer_secret,
                                           access_token_key=self.twitter_access_token,
                                           access_token_secret=self.twitter_access_secret)
        except Exception as e:
            print("Connect(twitter) error = ", e)

    # 텔레그램 연결
    def ConnectTelegram(self):
        try:
            Data.telegram_bot = telegram.Bot(token=Data.telegram_token)
            #updates = Data.telegram_bot.getUpdates()
            #print(updates)

            #for i in updates:
            #    print(i)
        except Exception as e:
            print("Connect(telegram) error = ", e)

    # 트위터 특정 계정 타임라인 데이터 가져오기
    def GetTwitterData(self, account):
        list_ref = []
        try:
            twitter_status = Data.twitter_api.GetUserTimeline(screen_name=account,
                                                              count=100,
                                                              include_rts=False,
                                                              exclude_replies=True)
            if len(twitter_status) > 0:
                last_time = self.StrToUnixTime(twitter_status[0].created_at)
                if last_time > self.dict_time[account]: # 새로 트윗한글 가져오기
                    for status in twitter_status:
                        current_time = self.StrToUnixTime(status.created_at)
                        if current_time <= self.dict_time[account]:
                            break
                        str_ref = f'https://twitter.com/{account}/status/{status.id_str}'
                        list_ref.append(str_ref)
                    self.dict_time[account] = last_time
        except Exception as e:
            print("GetUserTimeLine error = ", e)
        finally:
            return list_ref

    # 텔레그램에 메시지 보내기
    def SendTelegram(self, list_msg):
        if Data.telegram_bot is None:
            print("Disconnect Telegram")
        else:
            for account in Data.list_telegram_account:
                for msg in list_msg:
                    Data.telegram_bot.sendMessage(chat_id=account, text=msg)

    # 특정 계정 타임라인 새로운 트윗 올라옴 -> 텔레그램 채널방에 뿌리기
    def StartOpperation(self):
        self.working = True;
        while self.working:
            for account in Data.list_account:
                list_msg = self.GetTwitterData(account)
                if len(list_msg) > 0:
                    self.SendTelegram(list_msg)
                    print("["+account+"] send a message through telegram, total number of message = ", len(list_msg))
                else:
                    print("["+account+"] empty list_ref")
            time.sleep(Data.sleep_second)

    def StopOpperation(self):
        self.working = False;


    def __LoadJson(self):
        try:
            with open(self.str_file_name) as json_file :
                json_data = json.load(json_file)
                Data.twitter_consumer_key = json_data["twitter_consumer_key"]
                Data.twitter_consumer_secret = json_data["twitter_consumer_secret"]
                Data.twitter_access_token = json_data["twitter_access_token"]
                Data.twitter_access_secret = json_data["twitter_access_secret"]
                Data.list_account = json_data["parse_account"]
                Data.telegram_token = json_data["telegram_token"]
                Data.list_telegram_account = json_data["telegram_account"]
                Data.sleep_second = json_data["sleep_second"]

        except Exception as e:
            print(e)

    def StrToUnixTime(self, str):
        list_split = str.split()
        str_date = f'{list_split[5]}-{self.MonthToNumber(list_split[1])}-{list_split[2]} {list_split[3]}'
        unixtime = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S').timestamp()
        return int(unixtime)

    def MonthToNumber(self, str_month):
        for index, month in enumerate(calendar.month_abbr):
            if month == str_month:
                return index