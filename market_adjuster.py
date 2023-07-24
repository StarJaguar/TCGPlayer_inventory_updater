import pandas as pd

#read csv file as a dataframe - contains all listings
tcg_market = pd.read_csv('static\datasets\TCGplayer__Pricing_Custom_Export_20230519_052152.csv')

#show only listings that have a quantity
filter = (tcg_market['Total Quantity'] > 0) & (tcg_market['Rarity'] != 'Starlight Rare')
local_market = tcg_market[filter]

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
        Returns weather a there is both an unlimited and 1st editon of the same card

        Input: row of dataframe with several columns
        Output: boolean value of weateher or not the card as a different edition
    '''
    if ('Unlimited' in df_rows['Condition']) and (local_market['Product Name'].value_counts()[df_rows['Product Name']]> 1) and (local_market['Number'].value_counts()[df_rows['Number']]> 1):
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
    elif (df_rows['TCG Low Price With Shipping'] >= 4) and (df_rows['TCG Low Price With Shipping'] <= 5.49) and (not (df_rows['ed_bool'])):
        return 5
    elif ((df_rows['TCG Low Price With Shipping'] >= 25) and (df_rows['Total Quantity'] >= 3) and (not (df_rows['ed_bool']))):
        return df_rows['TCG Low Price With Shipping'] + 2
    else :
        return df_rows['TCG Marketplace Price']

local_market['ed_bool'] = local_market[['Condition', 'Product Name', 'Number']].apply(edition_checker, axis='columns')
local_market['TCG Marketplace Price'] = local_market[['Condition', 'TCG Low Price With Shipping', 'Total Quantity', 'TCG Marketplace Price', 'ed_bool']].apply(price_guideline , axis='columns')

#local_market.drop(columns='ed_bool', inplace=True)

local_market.to_csv('static\datasets\out.csv')