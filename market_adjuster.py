import pandas as pd

#read csv file as a dataframe - contains all listings
tcg_market = pd.read_csv('static\datasets\TCGplayer__Pricing_Custom_Export_20230519_052152.csv')

#show only listings that have a quantity
filter = tcg_market['Total Quantity'] > 0
local_market = tcg_market[filter]

def price_guideline(df_rows):
    '''
        Returns the TCGplayer Marketplace Price whether it was updated or not.
        
        Follows guidelines from readme to update prices to the TCG Marketplace Price column.

        Input: row of dataframe with several columns
        Output: price as numberic value
    '''

local_market['TCG Marketplace Price'] = local_market[['Condition', 'TCG Low Price With Shipping', 'Total Quantity', 'TCG MarketPlace Price']].apply(price_guideline , axis='columns')

local_market.to_csv('static\datasets\out.csv')