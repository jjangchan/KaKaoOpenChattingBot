import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from TwitterBot.Log import Log
from TwitterBot.TwitterClient import TwitterClient
from TwitterBot.TelegramClient import TelegramClient

class Data(object):
    twitter_api = None
    telegram_bot = None
    twitter_consumer_key = ""
    twitter_consumer_secret = ""
    twitter_access_token = ""
    twitter_access_secret = ""
    telegram_token = {}
    set_twitter_account = set()
    dict_twitter_account = {}
    sleep_second = 0
    log_level = "INFO"
    log_file_name = "TwitterBot/twitter_telegram.log"
    log_instance = None
    spreadsheet_url = ""

    def __init__(self, str_file_name):
        self.str_file_name = str_file_name
        self.__LoadJson()
        self.__LoadGspread()
        Data.log_instance = Log.getInstance()
        Data.log_instance.ConfigLog(Data.log_level, Data.log_file_name)
        self.working = True

    def __LoadJson(self):
        try:
            with open(self.str_file_name) as json_file :
                json_data = json.load(json_file)
                Data.twitter_consumer_key = json_data["twitter"]["twitter_consumer_key"]
                Data.twitter_consumer_secret = json_data["twitter"]["twitter_consumer_secret"]
                Data.twitter_access_token = json_data["twitter"]["twitter_access_token"]
                Data.twitter_access_secret = json_data["twitter"]["twitter_access_secret"]
                Data.sleep_second = json_data["sleep_second"]
                Data.spreadsheet_url = json_data["spreadsheet_url"]
                Data.log_file_name = json_data["Log"]["file_name"]
                Data.log_level = json_data["Log"]["log_level"]

        except Exception as e:
            print(e)

    def __LoadGspread(self):
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
            ]

            json_file_name = 'TwitterBot/diesel-skyline-330402-df7cde95ac7a.json'

            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
            gc = gspread.authorize(credentials)

            spreadsheet_url = Data.spreadsheet_url

            # 스프레스시트 문서 가져오기
            doc = gc.open_by_url(spreadsheet_url)

            # 시트 선택하기
            worksheet = doc.worksheet("시트1")

            # 데이터 추출
            name_data = worksheet.col_values(1)
            key_data = worksheet.col_values(2)
            int_count = 0

            for i in range(len(name_data)):
                if name_data[i] == "":
                    break
                Data.telegram_token[name_data[i]] = key_data[i]
                int_count += 1
                twitter_account = worksheet.row_values(int_count)
                for j in range(2, len(twitter_account)):
                    if twitter_account[j] == "":
                        break
                    account = twitter_account[j]
                    Data.set_twitter_account.add(account)
                    if Data.dict_twitter_account.get(account) is None:
                        Data.dict_twitter_account[account] = set()
                    Data.dict_twitter_account[account].add(name_data[i])

        except Exception as e:
            Data.log_instance.logger.error("gspread load error = "+e)


    # 특정 계정 타임라인 새로운 트윗 올라옴 -> 텔레그램 채널방에 뿌리기
    def StartOpperation(self):
        self.working = True;
        twitter_client = TwitterClient(Data.twitter_consumer_key,
                                       Data.twitter_consumer_secret,
                                       Data.twitter_access_token,
                                       Data.twitter_access_secret)
        twitter_client.ConnectTwitter()
        current_time = int(time.time())-(60*60*9) #GMT+0
        dict_time = {account: current_time for account in Data.set_twitter_account}

        dict_telegram_client = {}
        for key, value in Data.telegram_token.items():
            dict_telegram_client[key] = TelegramClient(value, key)
            dict_telegram_client[key].ConnectTelegram()

        while self.working:
            for account in Data.set_twitter_account:
                list_msg = twitter_client.GetTwitterData(account, dict_time)
                if len(list_msg) > 0:
                    for value in Data.dict_twitter_account[account]:
                        dict_telegram_client[value].SendTelegram(list_msg)
                    Data.log_instance.logger.info("["+account+"] send a message through telegram, total number of message = "+str(len(list_msg)))
                else:
                    pass
                    #Data.log_instance.logger.info("["+account+"] empty list_ref")
            time.sleep(Data.sleep_second)

    def StopOpperation(self):
        self.working = False;
