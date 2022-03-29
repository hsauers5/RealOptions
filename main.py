import pandas as pd
import opstrat as op

def main():
    # read data
    data = pd.read_csv('data.csv')
    print(data)

    # for each row/period, do B-S model using historical volatility
        # also figure out implied gamma of real option
    for index, row in data.iterrows():
        # print(row['Period'])
        commodity_price = float(row['CommodityPrice'])
        evps = float(row['TEVperShare'])
        tons_sold = float(row['TonsSold'])
        production_cost = float(row['ProductionCost'])
        prime_rate = float(row['PrimeRate'])
        shares_out = float(row['SharesOut'])

        # Black-Scholes model
        S = commodity_price
        K = production_cost
        r = prime_rate
        t = 365
        v = 48.5
        annual_option_value_per_ton = op.black_scholes(St=S, K=K, r=r, t=t, v=v)['value']['option value']
        annual_option_value_to_firm = annual_option_value_per_ton * tons_sold
        annual_option_value_per_share = annual_option_value_to_firm / shares_out

        # take annual value, discount at prime rate for ten years, get approx. real option value
        real_option_value_per_share = 0
        discount_rate = prime_rate/100
        for i in range(1, 11):
            real_option_value_per_share += annual_option_value_per_share / ((1+discount_rate)**i)

        # print(f'{real_option_value_per_share} | {evps}')
        print(real_option_value_per_share)


if __name__ == '__main__':
    main()