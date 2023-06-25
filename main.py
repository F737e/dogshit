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

        # Connect to Infura API for account validation
        infura_url = "https://mainnet.infura.io/v3/b08d259e4c874edb93d9f0025ffd461e"
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Perform account validation check
        code = w3.eth.get_code(address)
        return bool(code)  # True if account exists, False otherwise
    except ValidationError:
        return False  # Return False if mnemonic is not valid

def check_account_balance(address):
    # Connect to Infura API for balance check
    infura_url = "https://mainnet.infura.io/v3/e1d702d09f394f5096e82c804e3d5c56"
    w3 = Web3(Web3.HTTPProvider(infura_url))

    # Get account balance
    balance = w3.eth.get_balance(address)
    return balance

def save_mnemonic(mnemonic, file_name):
    with open(file_name, "a") as f:
        f.write(mnemonic + "\n")

def main():
    while True:
        # Generate a random mnemonic phrase
        mnemonic = generate_mnemonic()
        print("Generated Mnemonic:", mnemonic)

        # Check if the account associated with the mnemonic exists
        if check_account_validation(mnemonic):
            # Save the mnemonic to a file for further processing
            save_mnemonic(mnemonic, "valid_mnemonics.txt")
            print("Mnemonic saved at valid_mnemonics.txt")

            # Retrieve the account address from the mnemonic
            private_key = Account.from_mnemonic(mnemonic)._private_key
            account = Account.from_key(private_key)
            address = account.address

            # Check the account balance
            balance = check_account_balance(address)
            print("Account Balance:", balance)

            # Save mnemonic to the recovery file if balance is non-zero
            if balance > 0:
                save_mnemonic(mnemonic, "recovery_phase.txt")
                print("Mnemonic saved at recovery_phase.txt")

if __name__ == "__main__":
    main()

