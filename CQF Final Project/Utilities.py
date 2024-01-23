import numpy as np
from math import *


### Y Finance Section

import yfinance as yf

def getHistLogReturn(tickers, period):

    ###Initialize DataFrame
    dic_histLogReturn = {}

    for i in range(0,len(tickers)):
        #print(tickers[i])
        #print(period)
        yfticker = yf.Ticker(tickers[i])
        arr_histPrice = np.array(yfticker.history(period = period)['Close'])
        #print(np.shape(arr_histPrice))

        #Calculate Log Return
        arr_histLogReturn = np.diff(np.log(arr_histPrice))

        #Store in Dictionary
        dic_histLogReturn[tickers[i]] = arr_histLogReturn
    return dic_histLogReturn


def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)




def get_timeToDefault(arr_x,input_array):
    
    def nearestValue(x):
        
        
        for i in range(0,len(input_array)-1):
            if x > np.max(input_array):
                index = len(input_array)-1
            elif x > input_array[i] and x <= input_array[i+1]:
                index = i + 0.5

            
            

        return index

    index = np.array(list(map(nearestValue,arr_x)))

    return index


def find_nth_smallest_proper_way(a, n):
    return np.partition(a, n-1)[n-1]


def kth_timetoDefault(dist, k):
    return np.sort(np.partition(dist, k-1, axis = 1)[:, k-1])



def logpdf_t_copula(x,mu,Sigma,df,d):
    '''
    Multivariate t-student density:
    output:
        the density of the given element
    input:
        x = parameter (d dimensional numpy array or scalar)
        mu = mean (d dimensional numpy array or scalar)
        Sigma = scale matrix (dxd numpy array)
        df = degrees of freedom
        d: dimension
    '''
    Num = gamma(1. * (d+df)/2)
    Denom = ( gamma(1.*df/2) * pow(df*pi,1.*d/2) * pow(np.linalg.det(Sigma),1./2) * pow(1 + (1./df)*np.dot(np.dot((x - mu),np.linalg.inv(Sigma)), (x - mu)),1.* (d+df)/2))
    d = 1. * Num / Denom 
    return log(d)