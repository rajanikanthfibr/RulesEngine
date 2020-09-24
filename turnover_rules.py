hostname = 'lf-prod-replica.cahzexplvjof.eu-west-2.rds.amazonaws.com'
username = 'lf_datascience'
password = 'row9s5s3B0LAP7N21'
database = 'TheSpaceship'
import psycopg2
import pandas.io.sql as sqlio

conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cur = conn.cursor()

sql = "SELECT * FROM bank_transactions limit 10"
dat = sqlio.read_sql_query(sql, conn)


def get_bearer_token():
    '''
    Function to get the Auth bearer token for CATO and CAIS
    '''
    import requests
    url = 'https://uat-uk-api.experian.com/oauth2/v1/token'

    headers = {'client_id': 'UTTHOcuMyOsbKTQ1OezKewKOi3LwGSVL',
               'client_secret': 'wZmP6siY2EmLvpjw',
               'Content-Type': 'application/json',
               'Cookie': 'nlbi_1333066=BgKTaotgBhaQBE6l81NXSQAAAAARF0V2FMVCnDo5hkcaUD9m; visid_incap_1333066=/C46RAKrT9CvAXZB75ZfhW6nGl8AAAAAQUIPAAAAAABNSnmqrMV+qQxPVA16UHWa; incap_ses_873_1333066=ZgDPLc0S1DwWR27b+4 QdDOlca18AAAAAxHu/8anVs8kI0/w8EdlMgg=='}

    data = {'username': 'lendflouat03',
            'password': 'vhM14B14Gys1qy5vc'}

    r = requests.post(url,
                      headers=headers, json=data)
    j = r.json()
    bearer_token = 'Bearer ' + j['access_token']
    return bearer_token


def get_total_turnover(company_no):  # CATO
    '''
    Function to get the total turnover for a company from CATO end point
    '''
    import requests
    url = 'https://uat-uk-api.experian.com/risk/business/v1/cato/' + company_no
    bearer_token = get_bearer_token()
    headers = {'Authorization': bearer_token,
               'Accept': 'application/json',
               'Cookie': 'nlbi_1333066=BgKTaotgBhaQBE6l81NXSQAAAAARF0V2FMVCnDo5hkcaUD9m; visid_incap_1333066=/C4\
             6RAKrT9CvAXZB75ZfhW6nGl8AAAAAQUIPAAAAAABNSnmqrMV+qQxPVA16UHWa; incap_ses_873_1333066=ZgDPLc0S1DwWR2\
             7b+4QdDOlca18AAAAAxHu/8anVs8kI0/w8EdlMgg=='}
    r = requests.get(url,
                     headers=headers)
    j = r.json()
    turnover = 0
    filings = 0
    for doc in j['CATOHistory']:
        temp = doc['CreditTurnover'] if 'CreditTurnover' in doc else 0
        turnover += float(temp) if temp is not None else 0
        filings += 1 if 'CreditTurnover' in doc else 0
    # Added the condition if the number of filings are for more than 10 months and extrapolate the data
    if (filings < 12) and (filings >= 10):
        turnover = turnover * 12 / 10
    return turnover


def get_total_assets(company_no):  # CAIS
    '''
    Function to get the total current assets (TotalCurrentAssets + TotalFixedNonCurrentAssets) for a company from CATO end point
    '''
    import requests
    url = 'https://uat-uk-api.experian.com/risk/business/v1/registeredcompanycredit/' + company_no
    bearer_token = get_bearer_token()
    url = 'https://uat-uk-api.experian.com/risk/business/v1/registeredcompanycredit/07207209'
    headers = {'Authorization': bearer_token,
               'Accept': 'application/json',
               'Cookie': 'nlbi_1333072=c7icapvwvnpO/C0JnfdBTwAAAADoqgfA2IZtWc5Qugtw+U9o; visid_incap_1333072=Dzxv0NIGRTWb \
             8DhasOv9ejs2c14AAAAAQUIPAAAAAADnRVZrtnl7ZSr/kp1uu2is'}
    r = requests.get(url,
                     headers=headers)
    j = r.json()
    temp = j['Financials']['Accounts'][0]['BalanceSheet']['TotalCurrentAssets'] if 'TotalCurrentAssets' in \
                                                                                   j['Financials']['Accounts'][0][
                                                                                       'BalanceSheet'] else 0
    TotalCurrentAssets = float(temp) if temp is not None else 0

    temp = j['Financials']['Accounts'][0]['BalanceSheet'][
        'TotalFixedNonCurrentAssets'] if 'TotalFixedNonCurrentAssets' in j['Financials']['Accounts'][0][
        'BalanceSheet'] else 0
    TotalFixedNonCurrentAssets = float(temp)
    totalassets = TotalCurrentAssets + TotalFixedNonCurrentAssets
    return totalassets

def look_company_id(company_no):
    '''
    Get the company id given a company no
    '''
    sql = """
    select distinct company_id from companies where company_house_no='{}'
    """.format(company_no)
    cur.execute(sql)
    company_id = []
    for data in cur.fetchall():
        company_id.append(data[0])

    return company_id[0] if len(company_id) > 0 else None

def get_trusso_bearer_token():  # Trusso
    '''
    Function to get the authorization token for trusso end point
    '''
    import requests
    url = 'https://uat-uk-api.experian.com/oauth2/v1/token'

    headers = {'client_id': 'dD9ZvaoWncABd8XWUgEn1aEGih7yt2F7',
               'client_secret': '7A5V9dofuYmohQvB',
               'Content-Type': 'application/json',
               'Cookie': 'nlbi_1333066=BgKTaotgBhaQBE6l81NXSQAAAAARF0V2FMVCnDo5hkcaUD9m; visid_incap_1333066=/C46RAKrT9CvAXZB75ZfhW6nGl8AAAAAQUIPAAAAAABNSnmqrMV+qQxPVA16UHWa; incap_ses_873_1333066=ZgDPLc0S1DwWR27b+4 QdDOlca18AAAAAxHu/8anVs8kI0/w8EdlMgg=='}

    data = {'username': 'przemyslaw.winszczyk',
            'password': 'Zb5sFJfGOu4GcNp51lM3MMaI'}

    r = requests.post(url,
                      headers=headers, json=data)
    j = r.json()
    bearer_token = 'Bearer ' + j['access_token']
    return bearer_token

def get_transactions(company_id):
    '''
    Function to get the transaction information from postgres for a given company id
    '''
    sql = """
    select id, data from bank_transactions where company_id='{}'
    """.format(company_id)

    cur.execute(sql)
    transactions = []
    for data in cur.fetchall():
        transactions.append([data[0], data[1]])

    transactions_rev = []
    for transaction_data in transactions:
        transactions_rev.append({
            "accountId": transaction_data[1]['account_id'],
            "amount": abs(transaction_data[1]['amount']),
            "date": transaction_data[1]['transaction_date'],
            "description": transaction_data[1]['description'],
            "transactionClass": 'debit' if transaction_data[1]['amount'] < 0 else 'credit',
            "transactionId": str(transaction_data[0])
        })
    return transactions_rev if len(transactions_rev) > 0 else None

def get_trusso_sales(company_no):  # Trusso
    company_id = look_company_id(company_no)
    transactions = get_transactions(company_id)
    import requests
    bearer_token = get_trusso_bearer_token()
    url = 'https://uat-uk-api.experian.com/ts-categorization-svc/transactions/v4/uk/d2c.json'
    headers = {'Authorization': bearer_token,
               'Accept': 'application/json',
               'Cookie': 'nlbi_1333066=BgKTaotgBhaQBE6l81NXSQAAAAARF0V2FMVCnDo5hkcaUD9m; visid_incap_1333066=/C46RAKrT9CvAXZB75ZfhW6nGl8AAAAAQUIPAAAAAABNSnmqrMV+qQxPVA16UHWa; incap_ses_873_1333066=ZgDPLc0S1DwWR27b+4QdDOlca18AAAAAxHu/8anVs8kI0/w8EdlMgg=='}
    data = {
        "kpis": "none",
        "transactions": transactions
    }
    r = requests.post(url,
                      headers=headers, json=data)
    j = r.json()
    sales = 0
    for doc in j['transactions']:
        if doc['predictedCategory'] in ['INC-I0001', 'INC-I0003']:
            temp = doc['amount'] if 'amount' in doc else 0

            sales += float(temp) if temp is not None else 0
    return sales

def check_turnover(company_id, min_turnover=100000):
    '''
    Check if one of turnover from CATO, totalcurrent assets from CAIS or total transactions of
    INC-I0001,INC-I0003 codes is above the minimum turnover needed
    '''
    return max(get_total_turnover(company_no), get_total_assets(company_no),
               get_trusso_sales(company_no)) > min_turnover