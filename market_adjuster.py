
def min_price(price):
    '''
        Returns .49 if lowest listed price with shipping is .49 or lower

        Input: 
        Output: price as number value
    '''
    if price <= .49:
        return .49
    else:
        return price
 


def edition_checker(df_rows):
    '''
        Returns whether an entry has both an unlimited and 1st editon of the same card

        Input: row of dataframe with several columns
        Output: boolean value of weateher or not the card as a different edition
    '''
    filter = ['Ghost Rare', 'Starlight Rare', 'Collector\'s Rare', 'Mosaic Rare', 'Shaterfoil Rare', 'Starfoil Rare', 'Ultimate Rare']

    filter_rarity = (local_market['Rarity'].isin(filter))
    filter_normal_rarity = (~local_market['Rarity'].isin(filter))

    high_rarity = local_market[filter_rarity]
    normal_rarity = local_market[filter_normal_rarity]

    if df_rows['Rarity'] in filter:
        if ('Unlimited' in df_rows['Condition']) and (high_rarity['Product Name'].value_counts()[df_rows['Product Name']] > 1) and (high_rarity['Number'].value_counts()[df_rows['Number']] > 1):
            return True
        else:
            return False
    else:
        if ('Unlimited' in df_rows['Condition']) and (normal_rarity['Number'].value_counts()[df_rows['Number']] > 1) and (normal_rarity['Product Name'].value_counts()[df_rows['Product Name']] > 1):
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
    if df_rows['TCG Low Price With Shipping'] <= .49 :
            return .49
    
    if 'Near Mint' in df_rows['Condition']:
        if (df_rows['TCG Low Price With Shipping'] >= 4) and (df_rows['TCG Low Price With Shipping'] <= 5.49):
            return 5
        elif ((df_rows['TCG Low Price With Shipping'] >= 25) and (df_rows['Total Quantity'] >= 3) and (not (df_rows['ed_bool']))):
            return (round(df_rows['TCG Low Price With Shipping']*4)/4.0 - .01) + 2
        elif ((df_rows['TCG Low Price With Shipping'] >= 25) and (df_rows['Total Quantity'] >= 3) and ((df_rows['ed_bool']))):
            return df_rows['TCG Low Price With Shipping'] + 1.75
        elif (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = (round(df_rows['TCG Low Price With Shipping']*4)/4.0 - .01) - .24
            return min_price(temp)
        elif df_rows['ed_bool']:
            temp = df_rows['TCG Low Price With Shipping'] - .24
            return min_price(temp)
        else :
            return df_rows['TCG Marketplace Price']
    elif 'Lightly Played' in df_rows['Condition']:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = df_rows['TCG Low Price With Shipping'] - .24
            return min_price(temp)
    elif 'Moderately Played' in df_rows['Condition']:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = df_rows['TCG Low Price With Shipping'] - .24
            return min_price(temp)
    elif 'Damaged' in df_rows['Condition']:
        if (df_rows['TCG Low Price With Shipping'] > df_rows['TCG Marketplace Price']):
            temp = df_rows['TCG Low Price With Shipping'] - .24
            return min_price(temp)
    
def price_changer(filename):

    import pandas as pd
    from datetime import datetime
    from pathlib import Path

    #read csv file as a dataframe - contains all listings
    path = 'static\\datasets\\'
    tcg_market = pd.read_csv(Path(path + filename))
    #show only listings that have a quantity
    filter_market = (tcg_market['Total Quantity'] > 0) & (~tcg_market['Rarity'].isin(['Starlight Rare','Collector\'s Rare']))
    global local_market
    local_market = tcg_market[filter_market]

    local_market['ed_bool'] = local_market[['Condition', 'Product Name', 'Number', 'Rarity']].apply(edition_checker, axis='columns')
    local_market['TCG Marketplace Price'] = local_market[['Condition', 'TCG Low Price With Shipping', 'Total Quantity', 'TCG Marketplace Price', 'ed_bool']].apply(price_guideline , axis='columns')

    local_market.drop(columns='ed_bool', inplace=True)

    timestr = datetime.now().strftime("_%Y_%m_%d")
    path_name = r'static\datasets\updated_prices_on'

    local_market.to_csv(path_name + timestr + '.csv')