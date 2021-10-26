import logging

class Log:
    __instance = None

    def __init__(self):
        self.logger = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Log()
        return cls.__instance

    def ConfigLog(self, log_level, file_name):
        # 로그 생성
        self.logger = logging.getLogger()

        # 로그의 출력 기준 설정
        self.logger.setLevel(log_level)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # log 출력
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # log를 파일에 출력
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
