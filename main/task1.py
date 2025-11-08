from web3 import Web3
import json
from config import RPC_URL, CONTRACT_ADDRESS

def load_abi():
    with open("../abis/erc20.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def get_balance(user_address):
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            return "Ошибка подключения к Polygon"

        ERC20_ABI = load_abi()

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=ERC20_ABI
        )

        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()

        raw_balance = contract.functions.balanceOf(
            Web3.to_checksum_address(user_address)
        ).call()

        human_balance = raw_balance / (10 ** decimals)

        return f"{human_balance} {symbol} или {raw_balance}"

    except Exception as e:
        return f"Ошибка: {str(e)}"

# def get_balance_batch(user_input):
#     addresses = user_input.split(" ", 1)[1]
#     results = []
#     for address in addresses.strip("[]").replace('"', '').split(", "):
#         result = get_balance(address)
#         results.append(result)
#     return results

def get_balance_batch(user_input):
    addresses = user_input.split(" ", 1)[1]

    addresses_list = addresses.strip("[]").replace('"', '').split(", ")

    balance = []

    for address in addresses_list:
        result = get_balance(address)
        balance.append(result)
    return balance

def get_top(n, addresses):
    get_addresses = get_balance_batch(addresses)
    sorted_strings = sorted(get_addresses, key=lambda s: float(s.split()[0]), reverse=True)
    result = []
    for i in range(n):
        result.append(sorted_strings[i])
    return result

def main():
    user_input = 'get_balance_batch ["0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d", "0x4830AF4aB9cd9E381602aE50f71AE481a7727f7C"]'
    result = (get_top(2, user_input))
    print(result)
if __name__ == "__main__":
    main()