import pandas as pd
import numpy as np

def data_prep(df):
    #EXTRACT INDEX TO COLUMN
    df.reset_index(inplace=True)

    df.columns = ['Dict_Tree','Value']

    #SPLIT LOGIC
    df_new = df['Dict_Tree'].str.split("_", n = 7, expand = True) # LOGIC FLAW IS ASSUMING 5 "_", should create a count structure

    #RENNAME COLUMNS 
    df_new.columns = ['Level 1', 'Bookmaker', 'Level 2', 'Bet Type', 'Level 3', 'Outcomes','Level 4','Moneyline'] 

    #MERGE SPLIT COLUMNS BACK TO ORIGINAL DATAFRAME
    df = df.join(df_new)

    del df_new


    ####################################################################3
    #CONDITIONAL COUNT LOGIC
    ####################################################################3

    #put columns in list

    colnames = df.columns.tolist()
    #print(colnames)

    dff = df.copy()


    for x in colnames:
        dff[x] = np.where(dff[x].isnull(),0,1)
        


    dff['Full Count']=0
    for x in colnames:
        dff['Full Count'] = dff['Full Count'] + dff[x]


    dff = dff['Full Count']


    df = df.merge(dff.rename('Full Count'), left_index=True, right_index=True)
    del colnames, dff, x

    df['Level 2'] = df['Level 2'].astype(str)


    #print(df['Level 2'])

    ####################################################################3
    #EXTRACT LOGIC
    ####################################################################3

    #PARAMETERS
    Full_Count = df['Full Count']
    Bet_Type = df['Bet Type']
    Outcomes = df['Outcomes']
    MoneyLine = df['Moneyline']
    Level_4 = df['Level 4']

    #LOGIC PARAMETER CONDITIONS
    conditions = [(Full_Count == 6) & (Bet_Type == 'title'),
                (Full_Count == 8) & (Outcomes == 'key'),

                (Full_Count == 10) & (MoneyLine == 'name') & (Level_4 == '0'),
                (Full_Count == 10) & (MoneyLine == 'price') & (Level_4 == '0'),
                (Full_Count == 10) & (MoneyLine == 'point') & (Level_4 == '0'),

                (Full_Count == 10) & (MoneyLine == 'name') & (Level_4 == '1'),
                (Full_Count == 10) & (MoneyLine == 'price') & (Level_4 == '1'),
                (Full_Count == 10) & (MoneyLine == 'point') & (Level_4 == '1')

                ]
    ##### ADD IN TEAM TWO SEPARATION PARAMETER

    #VALUE CHOICE IF CONDITION MET
    choices = [df['Value'],
            df['Value'],
            df['Value'],
            df['Value'],
            df['Value'],
            df['Value'],
            df['Value'],
            df['Value'],
    ]

    #LOGIC FOR METRIC NAMES
    #Create list length of frame with repetitive value
    #Repeat for 
    # 1. Sports Book
    # 2. Bet Type
    # 3. Team
    # 4. Moneyline
    # 5. Spread 


    l = df.shape[0]
    Sports_Book =   ['Sports Book' for i in range(l)]
    Bet_Type =      ['Bet Type' for i in range(l)]

    Team_1 =          ['Team 1' for i in range(l)]
    C_Moneyline_1 =   ['Moneyline 1' for i in range(l)]
    Spread_1 =        ['Spread 1' for i in range(l)]


    Team_2 =          ['Team 2' for i in range(l)]
    C_Moneyline_2 =   ['Moneyline 2' for i in range(l)]
    Spread_2 =        ['Spread 2' for i in range(l)]


    #VALUE CHOICE IF CONDITION MET
    choices2 = [
            Sports_Book,
            Bet_Type,

            Team_1,
            C_Moneyline_1,
            Spread_1,

            Team_2,
            C_Moneyline_2,
            Spread_2
            ]




    # create a new column in the DF based on the conditions
    df["Deal Book"] = np.select(conditions, choices, None)
    df["Metric"] = np.select(conditions, choices2, None)


    #Delete Column in Panda DataFrame
    #del df['Deal Book']
    #del df['ID']

    #ID BRACKET
    df['ID'] = df['Level 1'] + df['Level 2'].astype(str)


    del Bet_Type, Full_Count, MoneyLine, Outcomes, choices, conditions, choices2, Level_4
    del Team_1, Team_2, Spread_1, Spread_2, C_Moneyline_2, C_Moneyline_1
    del Sports_Book, l

    ####################################################################3
    #CROSS TAB LOGIC
    ####################################################################3

    dff = df.copy()
    dff  = dff[['ID','Metric','Deal Book','Level 3','Level 1']]


    #SUBSET THEN DELETE - RENAME COLUMN

    # selecting rows based on condition
    dff_b = dff.loc[dff['Metric'] == 'Bet Type']
    dff_b.columns = ['ID','Metric', 'Bet Type', 'Bet ID', 'Level 1']
    dff_b = dff_b[['ID','Bet Type', 'Bet ID', 'Level 1']]


    #LIVE GAME TAG
    dff_id = df.loc[df['Bookmaker'] == 'id']
    dff_id = dff_id[['Level 1', 'Value']]


    #REMOVE EXTRA FIELD
    dff = dff[['ID','Metric','Deal Book','Level 3']]

    dff_t1 = dff.loc[dff['Metric'] == 'Team 1']
    dff_t1.columns = ['ID','Metric', 'Team 1', 'Bet ID']
    dff_t1 = dff_t1[['ID','Team 1', 'Bet ID']]

    dff_t2 = dff.loc[dff['Metric'] == 'Team 2']
    dff_t2.columns = ['ID','Metric', 'Team 2', 'Bet ID']
    dff_t2 = dff_t2[['ID','Team 2', 'Bet ID']]

    dff_m1 = dff.loc[dff['Metric'] == 'Moneyline 1']
    dff_m1.columns = ['ID','Metric', 'Moneyline 1', 'Bet ID']
    dff_m1 = dff_m1[['ID','Moneyline 1', 'Bet ID']]

    dff_m2 = dff.loc[dff['Metric'] == 'Moneyline 2']
    dff_m2.columns = ['ID','Metric', 'Moneyline 2', 'Bet ID']
    dff_m2 = dff_m2[['ID','Moneyline 2', 'Bet ID']]


    dff_s1 = dff.loc[dff['Metric'] == 'Spread 1']
    dff_s1.columns = ['ID','Metric', 'Spread 1', 'Bet ID']
    dff_s1 = dff_s1[['ID','Spread 1', 'Bet ID']]

    dff_s2 = dff.loc[dff['Metric'] == 'Spread 2']
    dff_s2.columns = ['ID','Metric', 'Spread 2', 'Bet ID']
    dff_s2 = dff_s2[['ID','Spread 2', 'Bet ID']]


    dff_sportsbook = dff.loc[dff['Metric'] == 'Sports Book']
    dff_sportsbook.columns = ['ID','Metric', 'Sports Book', 'Bet ID']
    dff_sportsbook = dff_sportsbook[['ID','Sports Book', 'Bet ID']]



    df2 = pd.merge(dff_b, dff_id,  how='left', left_on=['Level 1'], right_on = ['Level 1'])

    df2 = pd.merge(df2, dff_t1,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])
    df2 = pd.merge(df2, dff_t2,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])

    df2 = pd.merge(df2, dff_m1,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])
    df2 = pd.merge(df2, dff_m2,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])

    df2 = pd.merge(df2, dff_s1,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])
    df2 = pd.merge(df2, dff_s2,  how='left', left_on=['ID','Bet ID'], right_on = ['ID','Bet ID'])

    df2 = pd.merge(df2, dff_sportsbook,  how='left', left_on=['ID'], right_on = ['ID'])

    #print(df2.columns)

    df2 = df2[['Sports Book','ID','Value','Bet ID_x','Bet Type', 'Team 1','Moneyline 1','Spread 1','Team 2','Moneyline 2','Spread 2']]
    return df2


#POST DATA RUN DELETE
#del dff, dff_b, dff_id, dff_m1, dff_m2, dff_s1, dff_s2, dff_sportsbook, dff_t1, dff_t2