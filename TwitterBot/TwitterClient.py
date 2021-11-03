import twitter;
import calendar
import datetime
from TwitterBot.Log import *

class TwitterClient(object):
    log_instance = Log.getInstance()

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.twitter_consumer_key = consumer_key
        self.twitter_consumer_secret = consumer_secret
        self.twitter_access_token = access_token
        self.twitter_access_secret = access_secret
        self.twitter_api = None

    # 트위터 연결
    def ConnectTwitter(self):
        if self.twitter_api is None:
            try:
                self.twitter_api = twitter.Api(consumer_key=self.twitter_consumer_key,
                                               consumer_secret=self.twitter_consumer_secret,
                                               access_token_key=self.twitter_access_token,
                                               access_token_secret=self.twitter_access_secret)
            except Exception as e:
                TwitterClient.log_instance.logger.error("connect_twitter error = ")
        else:
            TwitterClient.log_instance.logger.warn("twitter_connect already exists")

    # 트위터 특정 계정 타임라인 데이터 가져오기
    # 파이썬은 object에 따라 Call by value 또는 Call by reference 가 결정됨
    # mutable => list, dict, set
    # immutable => int, float, str, tuples 등 단일값 이거나, static 속성
    def GetTwitterData(self, account, dict_time):
        list_ref = []
        if self.twitter_api is None:
            print("connect_twitter is None")
            return list_ref
        try:
            twitter_status = self.twitter_api.GetUserTimeline(screen_name=account,
                                                              count=100,
                                                              include_rts=False,
                                                              exclude_replies=True)
            if len(twitter_status) > 0:
                last_time = self.StrToUnixTime(twitter_status[0].created_at)
                if last_time > dict_time[account]: # 새로 트윗한글 가져오기
                    for status in twitter_status:
                        current_time = self.StrToUnixTime(status.created_at)
                        if current_time <= dict_time[account]:
                            break
                        str_ref = f'https://twitter.com/{account}/status/{status.id_str}'
                        list_ref.append(str_ref)
                    dict_time[account] = last_time
        except Exception as e:
            TwitterClient.log_instance.logger.error("GetUserTimeLine error = "+str(e))
        finally:
            return list_ref

    def StrToUnixTime(self, str):
        list_split = str.split()
        str_date = f'{list_split[5]}-{self.MonthToNumber(list_split[1])}-{list_split[2]} {list_split[3]}'
        unixtime = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S').timestamp()
        return int(unixtime)

    def MonthToNumber(self, str_month):
        for index, month in enumerate(calendar.month_abbr):
            if month == str_month:
                return index
