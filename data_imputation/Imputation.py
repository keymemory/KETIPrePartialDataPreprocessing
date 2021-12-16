import numpy as np
import pandas as pd
  
class SerialImputation():
    def __init__ (self):
        self.ScikitLearnMethods =['KNN','MICE']
        self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
        self.fillNAMethods = ['bfill','ffill']
        self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
        self.orderIntMethods = [ 'polynomial', 'spline']
        self.deepMethods = ['brits']
 
    def get_dataWithSerialImputationMethods(self, data, imputation_param):
        result = data.copy()
        imputation_method = imputation_param['imputation_method']
        totalNanLimit = imputation_param['totalNanLimit']
        # if total column NaN number is less tan limit, Impute it according to the parameter  
        result= result.dropna(thresh=totalNanLimit, axis=1)
        result = self.dfImputation(result, imputation_param)
        for column in data.columns:
            if column in result.columns:
                data.loc[:, column] = result[column]
        return data

    def printNaNDataSummary(self, data):
        nan_data_summary = round(data.isna().sum()/len(data), 2)
        print("===== NaN data Ratio summary ======")
        print(nan_data_summary)


    def dfImputation(self, data, imputation_param):
        imputation_method = imputation_param['imputation_method']
        totalNanLimit = imputation_param['totalNanLimit']
        self.printNaNDataSummary(data)

        DataWithMaskedNaN = data.copy()
        for method_set in imputation_method:
            max_limit =method_set['max']
            from KETIPrePartialDataPreprocessing.data_imputation import nanMasking
            NaNInfoOverThresh= nanMasking.getConsecutiveNaNInfoOverThresh(data, max_limit)
            # Missing Data Imputation
            data = self.imputeDataByMethod(method_set, data)
            DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(data, NaNInfoOverThresh, max_limit)
        self.printNaNDataSummary(DataWithMaskedNaN)
        return DataWithMaskedNaN

    def imputeDataByMethod(self, method_set, data):
        
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        parameter = method_set['parameter']

        from KETIPrePartialDataPreprocessing.data_imputation import basicMethod 
        from KETIPrePartialDataPreprocessing.data_imputation.DL import deepLearningImputation 
        basicImpute = basicMethod.BasicImputation(data, method, max_limit)
        if method in self.ScikitLearnMethods:
            result = basicImpute.ScikitLearnMethod()       
        elif method in self.simpleMethods:
            result = basicImpute.simpleMethod()
        elif method in self.simpleIntMethods:
            result = basicImpute.simpleIntMethod()
        elif method in self.fillNAMethods:
            result = basicImpute.fillNAMethod()
        elif method in self.orderIntMethods:
            result = basicImpute.orderIntMethod()
        elif method in self.deepMethods:
            result = deepLearningImputation.DLImputation(data, method, parameter).getResult()
        else:
            result = data.copy()
            print("Couldn't find a proper imputation method.")
        return result        