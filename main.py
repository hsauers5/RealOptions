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

        real_option_value_per_share = 0

        for i in range(1, 3):
            # Black-Scholes model
            S = commodity_price
            K = production_cost
            r = prime_rate
            t = 365 * i
            v = 40
            annual_option_value_per_ton = op.black_scholes(St=S, K=K, r=r, t=t, v=v)['value']['option value']
            annual_option_value_to_firm = annual_option_value_per_ton * 4 * max(tons_sold, 2000)
            annual_option_value_per_share = annual_option_value_to_firm / shares_out

            # apply discount rate to option value? Kind of already accounted for in B-S

            real_option_value_per_share += annual_option_value_per_share

        # print(f'{real_option_value_per_share} | {evps}')
        print(real_option_value_per_share)


if __name__ == '__main__':
    main()
