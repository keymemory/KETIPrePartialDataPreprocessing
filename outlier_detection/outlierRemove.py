import numpy as np
import pandas as pd

class CertainOutlierRemove():
    # Let Certain Outlier from DataFrame Data to NaN
    # This function makes more Nan according to the data status.

    def __init__(self, data, min_max_limit):
        self.data = data
        self.min_max_limit = min_max_limit
    
    def getDataWitoutCertainOutlier(self):
        #Main Function
        # - Delete duplicated data
        # - Delete Out of range error 

        data_out = self.data.copy()
        data_out = self._duplicate_data_remove(data_out)
        data_out = self._out_of_range_error_remove (data_out, self.min_max_limit)
        anomal_value_list = [99.9, 199.9, 299.9, 9999, -99.9, -199.9, -299.9, -9999]
        # anomal_value_list 관련 향후 수정/업그레이드 해야 함 
        data_out = self._anomal_value_remove(data_out, anomal_value_list)
        return data_out
        
    def _duplicate_data_remove(self, data):
        data = data.sort_index()
        data = data.loc[:, ~data.columns.duplicated()]
        first_idx = data.first_valid_index()
        last_idx = data.last_valid_index()
        valid_data = data.loc[first_idx:last_idx]
           
        return valid_data

    def _out_of_range_error_remove (self, data, min_max_limit):
        data_out = data.copy()
        column_list = data.columns
        max_list = min_max_limit['max_num']
        min_list = min_max_limit['min_num']

        for column_name in column_list:
            print(column_name)
            if column_name in max_list.keys():  
                max_num = max_list[column_name]
                min_num = min_list[column_name]
                print(min_num, max_num)
                mask = data_out[column_name] > max_num
                #merged_result.loc[mask, column_name] = max_num
                data_out[column_name][mask] = np.nan#max_num
                mask = data_out[column_name] < min_num
                #merged_result.loc[mask, column_name] = min_num
                data_out[column_name][mask] = np.nan#min_num
            
        return data_out

    def _anomal_value_remove(self, data, anomal_value_list):
        # 특정 이상치 nan 처리 
        anomal_data = anomal_value_list 
        for index in anomal_data:
            data = data.replace(index, np.NaN)
        return data


class UnCertainOutlierRemove():

    def __init__(self, data):
        self.data = data 
                    
    def getDataWitoutCertainOutlier(self):
        self.data_out = self.IQRDetection(self.data)
        return self.data_out

    def IQRDetection(self, data, weight=1.5):

        # 추가로 하나 더 기능 넣을 예정
        # IQR을 활용한 nan 처리
        for column in data.columns:
            quantile_25 = np.percentile(data[column].values, 25)
            quantile_75 = np.percentile(data[column].values, 75)
            IQR = quantile_75 - quantile_25
            IQR_weight = IQR*weight
            lowest = quantile_25 - IQR_weight
            highest = quantile_75 + IQR_weight
            outlier_idx = data[column][(data[column] < lowest) | (data[column] > highest)].index
            data[data[column][outlier_idx]] = np.nan
        
        return data