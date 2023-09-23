import json
import yfinance as yf
import yahoo_fin.stock_info as si
import datetime as dt
import boto3

client = boto3.client('ses', region_name='us-east-2')


def lambda_handler(event, context):
    print("Started code execution at ", get_curr_date())

    # getting current yield on aaa bonds ie y
    aaa = yf.Ticker('AAA')
    y = aaa.info["yield"] * 100

    input = ['MSFT', 'AAPL', 'AMZN', 'GOOG', 'META', 'TSLA', 'ZM', 'DIS', 'JPM', 'NFLX']

    result = []
    data = "{\"obj\":"

    for val in input:
        cv = get_cv(val)
        vstar = get_vstar(get_eps(val), get_g(val), y)
        diff = round(cv - vstar, 2)
        obj = {
            "s": val,
            "c": cv,
            "v": vstar,
            "d": diff
        }
        result.append(obj)

    data = data + str(result) + "}"
    data = data.replace('\'', '\"')

    print(data)




    response = client.send_templated_email(
        Destination={
            'ToAddresses': ['shrutim@uw.edu']
        },
        Source='shrutim@uw.edu',
        Template='DynamicTableTemplate',
        TemplateData=data
    )
    print(response)


    print("Stopped code execution at ", get_curr_date())
    print("-----------------------------------------------------------------------------------------------------------")

    return {
        'statusCode': 200,
        'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
    }



# getting the twelve-month trailing eps(earnings per share) value for a given ticker
def get_eps(ticker):
    symbol = yf.Ticker(ticker)
    eps = symbol.info["trailingEps"]
    return eps


def get_cv(ticker):
    symbol = yf.Ticker(ticker)
    cv = symbol.info["open"]
    return cv


# getting the next 5-year growth estimate for a given ticker
def get_g(ticker):
    ticker_info = si.get_analysts_info(ticker)
    growth_estimates = ticker_info['Growth Estimates']
    g = growth_estimates.iloc[4][ticker]
    g = g.strip('%')
    g = float(g)
    return g


def get_vstar(eps, g, y):
    vstar = (eps * (8.5 + (2 * g)) * 4.4) / y
    vstar = round(vstar, 2)
    return vstar

def get_diff(cv, vstar):
    diff = cv - vstar
    return diff

def get_curr_date():
    # datetime object containing current date and time
    now = dt.datetime.now()
    # dd/mm/YY H:M:S
    dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_str

if __name__ == "__main__":
    lambda_handler(None, None)




