import pandas as pd
import numpy as np

def Calculate_SurvivalProbability(maturity, discountfactor, spread, recoveryRate, is_plot=False):
    
    # subsume list of inputs into a dataframe
    df = pd.DataFrame({'Maturity': maturity, 'Df': discountfactor, 'Spread': spread})
    
    # convert bps to decimal
    df['Spread'] = df['Spread']/10000

    # specify delta_t
    df['Dt'] = df['Maturity'].diff().fillna(0)

    #print(df)

    # loss rate
    L = 1.0 - recoveryRate
    
    # initialize the variables
    term = term1 = term2 = divider = 0
    
    for i in range(0, len(df.index)):
        if i == 0: df.loc[i,'Survival'] = 1
        if i == 1: df.loc[i,'Survival'] = L / (L+df.loc[i,'Dt']*df.loc[i,'Spread'])
        if i > 1:
            terms = 0
            for j in range(1, i):
                term = df.loc[j,'Df']*(L*df.loc[j-1,'Survival'] - \
                                              (L + df.loc[j,'Dt']*df.loc[i,'Spread'])* \
                                              df.loc[j,'Survival'])
                terms = terms + term  
           
            divider = df.loc[i,'Df']*(L+df.loc[i,'Dt']*df.loc[i,'Spread'])
            term1 = terms/divider

            term2 = (L*df.loc[i-1,'Survival']) / (L + (df.loc[i,'Dt'] * df.loc[i,'Spread']))

            df.loc[i,'Survival'] = term1 + term2

    # derive probability of default
    df['Default'] = 1. - df['Survival']
    
    # Calculating Hazard Rates
    for i in range(0,len(df.index)):
        if i == 0 :
            df.loc[i,'Hazard Rate'] = 0
        
        else:
            df.loc[i,'Hazard Rate'] = - np.log(df.loc[i,'Survival']/df.loc[i-1,'Survival'])

        



        
        



    if is_plot:
        # plot survival probability
        df[['Survival', 'Default']].iplot(title='Survival vs Default Probability', 
                                          xTitle='CDS Maturity', 
                                          yTitle='Survival Probability', 
                                          secondary_y = 'Default', 
                                          secondary_y_title='Default Probability')

    return df




def Calculate_kthtodefault(DiscountFactorFunc,TimetoKthDefaultMatrix,RecoveryRate,K):

    #First To Default
    #print(type(TimetoKthDefaultMatrix))
    def DefaultLeg(DiscountFactorFunc,TimetoKthDefaultMatrix,RecoveryRate,K):
        
        DefaultLegPV= []

        for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):
            if TimetoKthDefaultMatrix[i][K-1] == 5 :
                #print('Default Ran here')
                DefaultLegPV.append(0) #No Default Case                    
            elif TimetoKthDefaultMatrix[i][K-1] < 5:
                #print('Default Ran here 2')
                DefaultLegPV.append((1-RecoveryRate)*DiscountFactorFunc(TimetoKthDefaultMatrix[i][K-1])*(1/5))
            else:
                print(i, TimetoKthDefaultMatrix[i][K],'Something Wrong')
         

        #print(DefaultLegPV) 
        #print('DefaultLegPV',np.mean(DefaultLegPV))

        return np.mean(DefaultLegPV),DefaultLegPV
    



    def PremiumLeg(DiscountFactorFunc,TimetoKthDefaultMatrix,RecoveryRate,K):

        PremiumLegPV = []

        if K == 1:

            for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):

                if TimetoKthDefaultMatrix[i][K-1] == 5 :
                    
                    PremiumLegPV.append(np.sum(1*[DiscountFactorFunc(x) for x in range(1,6)])) #No Default Case - Full Payment                   
                elif TimetoKthDefaultMatrix[i][K-1] < 5:
                    #print('Test Here',type(TimetoKthDefaultMatrix[i][K-1]),type(int(np.ceil(TimetoKthDefaultMatrix[i][K-1]))),TimetoKthDefaultMatrix[i][K-1],int(np.ceil(TimetoKthDefaultMatrix[i][K-1])))
                    PremiumReceivedPV_1 = 1 * TimetoKthDefaultMatrix[i][0]* DiscountFactorFunc(TimetoKthDefaultMatrix[i][0])
                    PremiumLegPV.append(PremiumReceivedPV_1)
                    #print('Default Happened at ',TimetoKthDefaultMatrix[i][K-1], 'For Iteration', i)
                else:
                    print(i,TimetoKthDefaultMatrix[i][K-1],'Something Wrong at PremiumLeg')
        
        elif K == 2:

            for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):
                if TimetoKthDefaultMatrix[i][1] == 5 :
                    #print('RAN HERE')
                    PremiumLegPV.append(np.sum(1*[DiscountFactorFunc(x) for x in range(1,6)])) #No Default Case - Full Payment     
                elif TimetoKthDefaultMatrix[i][1] < 5:
                    #print('Test Here',type(TimetoKthDefaultMatrix[i][K-1]),type(int(np.ceil(TimetoKthDefaultMatrix[i][K-1]))),TimetoKthDefaultMatrix[i][K-1],int(np.ceil(TimetoKthDefaultMatrix[i][K-1])))
                    PremiumReceivedPV_1 = 1 * TimetoKthDefaultMatrix[i][0]* DiscountFactorFunc(TimetoKthDefaultMatrix[i][0])
                    PremiumReceivedPV_2 = (4/5) * (TimetoKthDefaultMatrix[i][1]-TimetoKthDefaultMatrix[i][0])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][1])
                    PremiumLegPV.append(PremiumReceivedPV_1 + PremiumReceivedPV_2)
                    #print('Default Happened at ',TimetoKthDefaultMatrix[i][K-1], 'For Iteration', i)
                else:
                    print(i,TimetoKthDefaultMatrix[i][0],'Something Wrong at PremiumLeg for K = ',K)

        elif K == 3:
             for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):
                if TimetoKthDefaultMatrix[i][1] == 5 :
                    #print('RAN HERE')
                    PremiumLegPV.append(np.sum(1*[DiscountFactorFunc(x) for x in range(1,6)])) #No Default Case - Full Payment     
                elif TimetoKthDefaultMatrix[i][1] < 5:
                    #print('Test Here',type(TimetoKthDefaultMatrix[i][K-1]),type(int(np.ceil(TimetoKthDefaultMatrix[i][K-1]))),TimetoKthDefaultMatrix[i][K-1],int(np.ceil(TimetoKthDefaultMatrix[i][K-1])))
                    PremiumReceivedPV_1 = 1 * TimetoKthDefaultMatrix[i][0]* DiscountFactorFunc(TimetoKthDefaultMatrix[i][0])
                    PremiumReceivedPV_2 = (4/5) * (TimetoKthDefaultMatrix[i][1]-TimetoKthDefaultMatrix[i][0])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][1])
                    PremiumReceivedPV_3 = (3/5) * (TimetoKthDefaultMatrix[i][2]-TimetoKthDefaultMatrix[i][1])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][2])
                    PremiumLegPV.append(PremiumReceivedPV_1 + PremiumReceivedPV_2 + PremiumReceivedPV_3)
                    #print('Default Happened at ',TimetoKthDefaultMatrix[i][K-1], 'For Iteration', i)
                else:
                    print(i,TimetoKthDefaultMatrix[i][0],'Something Wrong at PremiumLeg for K = ',K)

        elif K == 4:
            for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):
                if TimetoKthDefaultMatrix[i][1] == 5 :
                    #print('RAN HERE')
                    PremiumLegPV.append(np.sum(1*[DiscountFactorFunc(x) for x in range(1,6)])) #No Default Case - Full Payment     
                elif TimetoKthDefaultMatrix[i][1] < 5:
                    #print('Test Here',type(TimetoKthDefaultMatrix[i][K-1]),type(int(np.ceil(TimetoKthDefaultMatrix[i][K-1]))),TimetoKthDefaultMatrix[i][K-1],int(np.ceil(TimetoKthDefaultMatrix[i][K-1])))
                    PremiumReceivedPV_1 = 1 * TimetoKthDefaultMatrix[i][0]* DiscountFactorFunc(TimetoKthDefaultMatrix[i][0])
                    PremiumReceivedPV_2 = (4/5) * (TimetoKthDefaultMatrix[i][1]-TimetoKthDefaultMatrix[i][0])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][1])
                    PremiumReceivedPV_3 = (3/5) * (TimetoKthDefaultMatrix[i][2]-TimetoKthDefaultMatrix[i][1])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][2])
                    PremiumReceivedPV_4 = (2/5) * (TimetoKthDefaultMatrix[i][3]-TimetoKthDefaultMatrix[i][2])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][3])
                    PremiumLegPV.append(PremiumReceivedPV_1 + PremiumReceivedPV_2 + PremiumReceivedPV_3 + PremiumReceivedPV_4)
                    #print('Default Happened at ',TimetoKthDefaultMatrix[i][K-1], 'For Iteration', i)
                else:
                    print(i,TimetoKthDefaultMatrix[i][0],'Something Wrong at PremiumLeg for K = ',K)


        elif K == 5:
            for i in range(0,np.shape(TimetoKthDefaultMatrix)[0]):
                if TimetoKthDefaultMatrix[i][1] == 5 :
                    #print('RAN HERE')
                    PremiumLegPV.append(np.sum(1*[DiscountFactorFunc(x) for x in range(1,6)])) #No Default Case - Full Payment     
                elif TimetoKthDefaultMatrix[i][1] < 5:
                    #print('Test Here',type(TimetoKthDefaultMatrix[i][K-1]),type(int(np.ceil(TimetoKthDefaultMatrix[i][K-1]))),TimetoKthDefaultMatrix[i][K-1],int(np.ceil(TimetoKthDefaultMatrix[i][K-1])))
                    PremiumReceivedPV_1 = 1 * TimetoKthDefaultMatrix[i][0]* DiscountFactorFunc(TimetoKthDefaultMatrix[i][0])
                    PremiumReceivedPV_2 = (4/5) * (TimetoKthDefaultMatrix[i][1]-TimetoKthDefaultMatrix[i][0])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][1])
                    PremiumReceivedPV_3 = (3/5) * (TimetoKthDefaultMatrix[i][2]-TimetoKthDefaultMatrix[i][1])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][2])
                    PremiumReceivedPV_4 = (2/5) * (TimetoKthDefaultMatrix[i][3]-TimetoKthDefaultMatrix[i][2])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][3])
                    PremiumReceivedPV_5 = (1/5) * (TimetoKthDefaultMatrix[i][4]-TimetoKthDefaultMatrix[i][3])*DiscountFactorFunc(TimetoKthDefaultMatrix[i][4])
                    PremiumLegPV.append(PremiumReceivedPV_1 + PremiumReceivedPV_2 + PremiumReceivedPV_3 + PremiumReceivedPV_4 + PremiumReceivedPV_5)
                    #print('Default Happened at ',TimetoKthDefaultMatrix[i][K-1], 'For Iteration', i)
                else:
                    print(i,TimetoKthDefaultMatrix[i][0],'Something Wrong at PremiumLeg for K = ',K)


        else:
            print(K, "Is not a valid Kth Value")

        #print('PremiumLegPV',np.mean(PremiumLegPV))

        return np.mean(PremiumLegPV),PremiumLegPV
    
    


    PremiumLegPV = PremiumLeg(DiscountFactorFunc,TimetoKthDefaultMatrix,RecoveryRate,K)
    DefaultLegPV = DefaultLeg(DiscountFactorFunc,TimetoKthDefaultMatrix,RecoveryRate,K)



    return DefaultLegPV[0]/PremiumLegPV[0],PremiumLegPV,DefaultLegPV
    #Second To Default


    #3rd To Default


    #4th To Default


    #5th To Default

