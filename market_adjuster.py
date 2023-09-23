
def min_price(price):
    '''
        Returns .49 if lowest listed price with shipping is .49 or lower
        This is the minimum price as per the card shop's guide

        Input: 
        Output: price as number value
    '''
    if price <= .49:
        return .49
    else:
        return price

def price_increment(price):
    '''
        Returns a new price that is in increments of .24, .49, .74, and .99.

        Input: the current price being interated
        Output: the new price for the current item
    ''' 
    if price is not None:
        return (round(price*4)/4.0 - .01)
    else:
         return price


def edition_checker(df_rows):
    '''
        Returns whether an entry has both an unlimited and 1st editon of the same card

        Input: row of dataframe with several columns
        Output: boolean value of wheteher or not the card as a different edition
    '''
    filter = ['Ghost Rare', 'Starlight Rare', 'Collector\'s Rare', 'Mosaic Rare', 'Shaterfoil Rare', 'Starfoil Rare', 'Ultimate Rare'] #excluding these rarities due to normally higher prices

    filter_rarity = (local_market['Rarity'].isin(filter))
    filter_normal_rarity = (~local_market['Rarity'].isin(filter))

    high_rarity = local_market[filter_rarity]
    normal_rarity = local_market[filter_normal_rarity]

    if df_rows['Rarity'] in filter:
        if ('Unlimited' in df_rows['Condition']) and (high_rarity['Product Name'].value_counts()[df_rows['Product Name']] >= 1) and (high_rarity['Number'].value_counts()[df_rows['Number']] >= 1):
            return True
        else:
            return False
    else:
        if ('Unlimited' in df_rows['Condition']) and (normal_rarity['Number'].value_counts()[df_rows['Number']] >= 1) and (normal_rarity['Product Name'].value_counts()[df_rows['Product Name']] >= 1):
            return True
        else:
            return False
                 

def price_guideline(df_rows):
    '''
        Returns the TCGplayer Marketplace Price whether it was updated or not.
        
        Follows guidelines from readme to update prices to the TCG Marketplace Price column.

        Input: row of dataframe with several columns
        Output: price as numberic value
    '''
    nm_condition = ['Near Mint Limited', 'Near Mint 1st Edition', 'Near Mint Unlimited']
    lp_condition = ['Lightly Played Limited', 'Lightly Played 1st Edition', 'Lightly Played Unlimited']
    mp_condition = ['Moderately Played Limited', 'Moderately Played 1st Edition', 'Moderately Played Unlimited']
    d_condition = ['Damaged Limited', 'Damaged 1st Edition', 'Damaged Unlimited']

    if df_rows['TCG Low Price With Shipping'] <= .49 :
            return .49
    
    if (df_rows['TCG Low Price With Shipping'] >= 4) and (df_rows['TCG Low Price With Shipping'] <= 5.49):
            return 5
    
    if ((df_rows['TCG Low Price With Shipping'] >= 25) and (df_rows['Total Quantity'] >= 3) and (not (df_rows['ed_bool']))):
            return price_increment(df_rows['TCG Low Price With Shipping']) + 2
    
    if ((df_rows['TCG Low Price With Shipping'] >= 25) and (df_rows['Total Quantity'] >= 3) and ((df_rows['ed_bool']))):
            return price_increment(df_rows['TCG Low Price With Shipping']) + 1.75
    
    if  df_rows['Condition'] in nm_condition:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = price_increment(df_rows['TCG Low Price With Shipping']) - .25
            return min_price(temp)
        elif df_rows['ed_bool']:
            temp = price_increment(df_rows['TCG Low Price With Shipping']) - .25
            return min_price(temp)
        else :
            return df_rows['TCG Marketplace Price']
    elif df_rows['Condition'] in lp_condition:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = price_increment(df_rows['TCG Low Price With Shipping']) - .25
            return min_price(temp)
    elif df_rows['Condition'] in mp_condition:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = price_increment(df_rows['TCG Low Price With Shipping']) - .25
            return min_price(temp)
    elif df_rows['Condition'] in d_condition:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = price_increment(df_rows['TCG Low Price With Shipping']) - .25
            return min_price(temp)
    
def price_changer(filename):

    import pandas as pd
    import numpy as np
    from datetime import datetime

    #read csv file as a dataframe - contains all listings
    path = r'static\datasets'
    paths = str(path) + '\\' +  str(filename)
    tcg_market = pd.read_csv(paths)
    #show only listings of personal inventory
    filter_market = (tcg_market['Total Quantity'] > 0) & (~tcg_market['Rarity'].isin(['Starlight Rare','Collector\'s Rare'])) & (pd.isnull(tcg_market['Title'])) & (pd.notnull(tcg_market['TCG Low Price With Shipping']))
    global local_market
    local_market = tcg_market[filter_market]

    local_market = local_market.replace([np.nan, -np.inf], 0)

    local_market['ed_bool'] = local_market[['Condition', 'Product Name', 'Number', 'Rarity']].apply(edition_checker, axis='columns')
    local_market['TCG Marketplace Price'] = local_market[['Condition', 'TCG Low Price With Shipping', 'Total Quantity', 'TCG Marketplace Price', 'ed_bool']].apply(price_guideline , axis='columns')

    local_market.drop(columns='ed_bool', inplace=True)

    timestr = datetime.now().strftime("_%Y_%m_%d")
    full_name= r'\updated_prices_on' + timestr

    local_market.to_csv(path + full_name + '.csv')