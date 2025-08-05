balances = {}
country_rates = {"+62": 3.20, "+91": 2.50}

def register_user(user_id):
    if user_id not in balances:
        balances[user_id] = 0.0

def get_balance(user_id):
    return balances.get(user_id, 0.0)

def update_balance(user_id, amount):
    balances[user_id] = get_balance(user_id) + amount

def get_country_rates():
    return country_rates

def get_verify_time():
    return 180  # 3 minutes