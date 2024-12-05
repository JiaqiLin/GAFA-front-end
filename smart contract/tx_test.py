from web3 import Web3
from eth_account import Account
import json

# 连接到 Axiomesh Gemini 测试网的 RPC 端点
web3 = Web3(Web3.HTTPProvider('https://rpc5.gemini.axiomesh.io'))

# 检查连接情况
if web3.is_connected():
    print("成功连接到 Axiomesh Gemini 测试网")
else:
    print("无法连接到 Axiomesh Gemini 测试网")
    exit()

with open('token_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

WALLET_ADDRESS = "0xa4015233202D1b80EBd200586603C234aB394EB8"
USER_PRIVATE_KEY = "843942065cc117d405c727bbdace2043c861bb13bb35223a3f1d46c5a99cd973"
CHAIN_ID = 23413
RECIPIENT = "0x2831f51aFE335983f3E4831A27f05Bc605686A31"
CONTRACT_ADDRESS = "0x1d0f24eAcE4826174371cf2620F7aa6989fef32a"

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


def transfer_tokens(amount):
    # 构建交易
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

    # 调用转账函数
    transfer_txn = contract.functions.transfer(
        RECIPIENT,
        amount * 10 ** 18  # 考虑代币精度（18位小数）
    ).build_transaction({
        'chainId': CHAIN_ID,  # Goerli测试网络的Chain ID
        'gas': 100000,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
    })

    # 签名交易
    signed_txn = web3.eth.account.sign_transaction(transfer_txn, USER_PRIVATE_KEY)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # 等待交易确认
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt


# 执行转账
try:
    # 转账100个代币
    receipt = transfer_tokens(1000)
    print(f"交易成功! 交易哈希: {receipt['transactionHash'].hex()}")
except Exception as e:
    print(f"交易失败: {str(e)}")



