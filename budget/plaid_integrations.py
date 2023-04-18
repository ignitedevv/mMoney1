import requests

enviroment_type = 'development'

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


def plaid_get_account_balance(CLIENT_ID, SECRET, token, start_date, end_date):
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
    print(balances)
    print(balances)
    all_account_balances = 0
    for account in balances['accounts']:
        avaliable = account['balances']['available']
        all_account_balances += int(avaliable)

    return all_account_balances
