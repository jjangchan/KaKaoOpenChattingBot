import telegram
from TwitterBot.Log import Log

class TelegramClient(object):
    #log_instance = Log.getInstance()

    def __init__(self, str_token, str_account):
        self.connect_telegram = None
        self.telegram_token = str_token
        self.telegram_account = str_account


    # 텔레그램 연결
    def ConnectTelegram(self):
        if self.connect_telegram is None:
            try:
                self.connect_telegram = telegram.Bot(token=self.telegram_token)
                # updates = Data.telegram_bot.getUpdates()
                # print(updates)

                # for i in updates:
                #    print(i)
            except Exception as e:
                pass
                #TelegramClient.log_instance.logger.error("connect_telegram error = ", e)
        else:
            pass
            #TelegramClient.log_instance.logger.warn("connect_telegram already exists")

    # 텔레그램에 메시지 보내기
    def SendTelegram(self, list_msg):
        if self.connect_telegram is None:
            print("Disconnect Telegram")
        else:
            try:
                for msg in list_msg:
                    self.connect_telegram.sendMessage(chat_id=self.telegram_account, text=msg)
            except Exception as e:
                TelegramClient.log_instance.logger.error("telegram send msg error = "+e)

