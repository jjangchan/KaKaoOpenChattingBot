from TwitterBot import DataRepo

if __name__ == '__main__':
    data = DataRepo.Data('TwitterBot/twitter_config.json')
    data.StartOpperation()