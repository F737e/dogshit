import random
from web3 import Web3
from eth_account import Account
from eth_utils.exceptions import ValidationError

# Enable Mnemonic features
Account.enable_unaudited_hdwallet_features()

def generate_mnemonic():
    wordlist_file = "wordlist.txt" 
    with open(wordlist_file, "r") as f:
        wordlist = f.read().splitlines()
    return " ".join(random.sample(wordlist, 12))

def check_account_validation(mnemonic):
    try:
        private_key = Account.from_mnemonic(mnemonic)._private_key
        account = Account.from_key(private_key)
        address = account.address

        # Connect to first Infura API for account validation
        infura_url_account = "https://mainnet.infura.io/v3/b08d259e4c874edb93d9f0025ffd461e"
        w3_account = Web3(Web3.HTTPProvider(infura_url_account))

        # Perform account validation check
        code = w3_account.eth.get_code(address)
        return bool(code)  # True if account exists, False otherwise
    except ValidationError:
        return False  # Return False if mnemonic is not valid

def check_account_balance(mnemonic):
    private_key = Account.from_mnemonic(mnemonic)._private_key
    account = Account.from_key(private_key)
    address = account.address

    # Connect to second Infura API for balance check
    infura_url_balance = "https://mainnet.infura.io/v3/e1d702d09f394f5096e82c804e3d5c56"
    w3_balance = Web3(Web3.HTTPProvider(infura_url_balance))

    # Get account balance
    balance = w3_balance.eth.get_balance(address)
    return balance

def save_mnemonic(mnemonic):
    with open("valid_mnemonics.txt", "a") as f:
        f.write(mnemonic + "\n")

def main():
    while True:
        # Generate a random mnemonic phrase
        mnemonic = generate_mnemonic()
        print("Generated Mnemonic:", mnemonic)

        # Check account validation
        if check_account_validation(mnemonic):
            # Check account balance
            balance = check_account_balance(mnemonic)
            print("Account Balance:", balance)

            # Save mnemonic if account balance is non-zero
            if balance > 0:
                save_mnemonic(mnemonic)
                print("Mnemonic saved.")

if __name__ == "__main__":
    main()
