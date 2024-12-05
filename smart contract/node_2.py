from web3 import Web3
import time
import json
from web3.exceptions import TransactionNotFound

# 连接到 Axiomesh Gemini 测试网的 RPC 端点
web3 = Web3(Web3.HTTPProvider('https://rpc5.gemini.axiomesh.io'))

# 检查连接情况
if web3.is_connected():
    print("成功连接到 Axiomesh Gemini 测试网")
else:
    print("无法连接到 Axiomesh Gemini 测试网")
    exit()

# 从文件加载合约 ABI
with open('demo_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# 合约地址
contract_address = '0xCcD20F5CE97Eb7Ef561BE5C911cbC5c64cAAf8C4'

# 创建合约对象
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# 钱包地址和私钥
WALLET_ADDRESS = "0x2831f51aFE335983f3E4831A27f05Bc605686A31"
USER_PRIVATE_KEY = "25c0c128ba93e734a68611edfeddf268bed7ec48c117f9dd7e85a6ac3f064323"


# 监听事件并获取 questionId
def listen_to_question_asked_event():
    # 创建事件过滤器
    event_filter = contract.events.QuestionAsked.create_filter(from_block='latest')
    print("开始监听 QuestionAsked 事件...")
    while True:
        try:
            # 获取新事件
            for event in event_filter.get_new_entries():
                question_id = event['args']['questionId']
                print("问题已提问，问题 ID 为：", question_id)
                return question_id  # 返回监听到的 questionId
            time.sleep(5)  # 每隔 5 秒检查一次
        except Exception as e:
            print(f"监听事件时发生错误: {e}")
            time.sleep(5)


# 回答问题
def answer_question(question_id, answer_content):
    # 获取当前交易的 nonce
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

    # 构造交易
    transaction = contract.functions.answerQuestion(question_id, answer_content).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': nonce,
        'gas': 2000000,  # 估算的 Gas 限制
        'gasPrice': web3.to_wei('5000', 'gwei')  # Gas 价格
    })

    # 签名交易
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=USER_PRIVATE_KEY)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("回答问题的交易已发送，交易哈希为：", tx_hash.hex())

    # 等待交易确认
    while True:
        try:
            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            if tx_receipt:
                print("交易已确认，区块高度为：", tx_receipt['blockNumber'])
                break
        except TransactionNotFound:
            print("交易未找到，可能尚未被打包，等待 10 秒...")
            time.sleep(10)


# 主程序逻辑
if __name__ == "__main__":
    # Step 1: 监听事件，获取 questionId
    question_id = listen_to_question_asked_event()

    # Step 2: 回答问题
    answer_content = "It is 1.0.0"
    answer_question(question_id, answer_content)