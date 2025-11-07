from web3 import Web3
import json
from config import RPC_URL, CONTRACT_ADDRESS

def load_abi():
    with open("../abis/erc20.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def get_balance(user_address):
    """Получить баланс токена на Polygon"""
    try:
        # Подключение
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


address = "0x6c0E888e4872d4388A726cd245B3F4516A529cDB"
result = get_balance(address)
print(f"Вывод: {result}")