import pandas as pd 
import sys
sys.path.append("../")
sys.path.append("../..")

class getData():
    def __init__(self):
        pass
    
    def getFileInput(self, file_name, time_index="timedate"):
        dataset = pd.read_csv(file_name, parse_dates=True, index_col=[time_index])
        return dataset

    def getInfluxInput(self, db_name, ms_name):
        from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
        from KETIPreDataIngestion.data_influx import influx_Client
       
        ##
        DBClient = influx_Client.influxClient(ins.CLUSTDataServer)
        db_list = DBClient.get_DBList() # 나중에 DB 이름 바꾸고 싶을때 여기 체크 가능
        ms_list = DBClient.measurement_list(db_name) # MS 이름 바꾸고 싶을때 여기 체크 가능

        feature_list = DBClient.get_fieldList(db_name, ms_name)
        #full_data = DBClient.get_data(db_name, ms_name)
        full_data = DBClient.get_datafront_by_num("200000", db_name, ms_name)
        print("Data Length:" ,len(full_data))
        #full_data = full_data.set_index('time')

        # 우선 full data 가져오도록 해놨음 db 이름과 ms 이름은 list에서 적당한것 바꿔볼 수 있음
        return full_data


    