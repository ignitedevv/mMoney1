import datetime
import plaid
import requests

enviroment_type = 'development'


# For updating link token
def plaid_updpate(CLIENT_ID, SECRET, token, user_id):
    print('update')
    url = f'https://{enviroment_type}.plaid.com/link/token/create'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "client_name": "mMoney",
        "user": {"client_user_id": f"{user_id}"},
        "country_codes": ["US"],
        "language": "en",
        "redirect_uri": "https://127.0.0.1:8000/budget/oauth.html"

    }
    r = requests.post(url, headers=headers, json=data).json()['link_token']


    print(r)
    return r


# Code to get all plaid transactions
def plaid_get_Transactions(CLIENT_ID, SECRET, token, start_date, end_date):
    print('get all transactions ')
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 30,
            "offset": 0
        }
    }
    # Transaction data received
    transaction_data = requests.post(url, headers=headers, json=data).json()
    return transaction_data




# Gets all account balances for a specific access token
def plaid_get_checking_account_balance(CLIENT_ID, SECRET, token, start_date, end_date):
    print('get all transactions ')
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 3,
            "offset": 0
        }
    }

    # Transaction data received
    balances = requests.post(url, headers=headers, json=data).json()

    all_account_balances = 0.0
    for account in balances['accounts']:
        if account['subtype'] == 'checking':
            avaliable = account['balances']['available']
            all_account_balances += float(avaliable)

    return all_account_balances


# Gets all account balances for a specific access token
def plaid_get_savings_account_balance(CLIENT_ID, SECRET, token, start_date, end_date):
    print('get all transactions ')
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 3,
            "offset": 0
        }
    }

    # Transaction data received
    balances = requests.post(url, headers=headers, json=data).json()
    all_account_balances = 0.0
    for account in balances['accounts']:
        if account['subtype'] == 'saving':
            avaliable = account['balances']['available']
            all_account_balances += float(avaliable)

    return all_account_balances


# Gets information on a specific Financial institution
def get_institution(CLIENT_ID, SECRET, ID):
    url = f'https://{enviroment_type}.plaid.com/institutions/get_by_id'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "institution_id": f"{ID}",
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "country_codes": ['USD']
    }

    instution = requests.post(url, headers=headers, json=data).json()
    return instution


# Gets and creates packaged list of all checking accounts with associated information
def get_checking_accounts(CLIENT_ID, SECRET, token, start_date, end_date):
    print('get all transactions ')
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 3,
            "offset": 0
        }
    }

    # Transaction data received
    balances = requests.post(url, headers=headers, json=data).json()
    accounts = []
    all_account_balances = 0
    checking_accounts_list = []
    for account in balances['accounts']:
        if account['subtype'] == 'checking':
            avaliable = account['balances']['available']
            name = account['name']
            official_name = account['official_name']
            subtype = account['subtype']
            int_id = balances['item']['institution_id']
            inst_name = get_institution(CLIENT_ID, SECRET, int_id)['institution']['name']
            last_updated = datetime.datetime.now().time()
            packaged_account = {'name': name, 'official_name': official_name, 'subtype': subtype, 'inst_name': inst_name, 'last_updated': f'{last_updated}', 'avaliable': avaliable}
            checking_accounts_list.append(packaged_account)
            all_account_balances += int(avaliable)


    return checking_accounts_list


# Gets and creates packaged list of all checking accounts with associated information
def get_savings_accounts(CLIENT_ID, SECRET, token, start_date, end_date):
    print('get all transactions ')
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 3,
            "offset": 0
        }
    }

    # Transaction data received
    balances = requests.post(url, headers=headers, json=data).json()
    accounts = []
    all_account_balances = 0
    checking_accounts_list = []
    for account in balances['accounts']:
        if account['subtype'] == 'savings':
            avaliable = account['balances']['available']
            name = account['name']
            official_name = account['official_name']
            subtype = account['subtype']
            int_id = balances['item']['institution_id']
            inst_name = get_institution(CLIENT_ID, SECRET, int_id)['institution']['name']
            last_updated = datetime.datetime.now().time()
            print('324 ' ,last_updated)
            packaged_account = {'name': name, 'official_name': official_name, 'subtype': subtype, 'inst_name': inst_name, 'last_updated': f'{last_updated}', 'avaliable': avaliable}
            checking_accounts_list.append(packaged_account)
            all_account_balances += int(avaliable)

    return checking_accounts_list


def get_investment_account_balances(CLIENT_ID, SECRET, token):
    url = f'https://{enviroment_type}.plaid.com/investments/holdings/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
    }

    investment_holdings = requests.post(url, headers=headers, json=data).json()
    investment_holdings_total = 0.0
    for account in investment_holdings['accounts']:
        current = float(account['balances']['current'])
        investment_holdings_total += current

    return investment_holdings_total


def plaid_get_investment_accounts(CLIENT_ID, SECRET, token):
    url = f'https://{enviroment_type}.plaid.com/investments/holdings/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
    }

    investment_holdings = requests.post(url, headers=headers, json=data).json()

    return investment_holdings['accounts']




# Gets account ids of all accounts for a specific access token
def plaid_get_accounts(CLIENT_ID, SECRET, token, start_date, end_date):
    url = f'https://{enviroment_type}.plaid.com/transactions/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "start_date": f"{start_date}",
        "end_date": f"{end_date}",
        "options": {
            "count": 3,
            "offset": 0
        }
    }

    # Transaction data received
    balances = requests.post(url, headers=headers, json=data).json()

    account_ids = []
    for account in balances['accounts']:
        account_id = account['account_id']
        account_ids.append(account_id)

    return account_ids


# For getting reocurring payments
def plaid_get_rec_payments(CLIENT_ID, SECRET, token, ids_array):
    url = f'https://{enviroment_type}.plaid.com/transactions/recurring/get'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": F"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "access_token": f'{token}',
        "account_ids": ids_array,
        "options": {
            "include_personal_finance_category": False
        }
    }

    r = requests.post(url, headers=headers, json=data).json()

    return r


