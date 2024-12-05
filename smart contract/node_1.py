from web3 import Web3
import time
import json
from web3.exceptions import TransactionNotFound
import threading

# 连接到 Axiomesh Gemini 测试网的 RPC 端点
web3 = Web3(Web3.HTTPProvider('https://rpc5.gemini.axiomesh.io'))

# 检查连接情况
if web3.is_connected():
    print("成功连接到 Axiomesh Gemini 测试网")
else:
    print("无法连接到 Axiomesh Gemini 测试网")
    exit()

with open('demo_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# 合约地址
CONTRACT_ADDRESS = '0xCcD20F5CE97Eb7Ef561BE5C911cbC5c64cAAf8C4'
TOKEN_ADDRESS = '0x1d0f24eAcE4826174371cf2620F7aa6989fef32a'
# 创建合约对象
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# 钱包地址 私钥  链ID
WALLET_ADDRESS = "0xa4015233202D1b80EBd200586603C234aB394EB8"
USER_PRIVATE_KEY = "843942065cc117d405c727bbdace2043c861bb13bb35223a3f1d46c5a99cd973"
CHAIN_ID = 23413
RECIPIENT = "0x2831f51aFE335983f3E4831A27f05Bc605686A31"

# 监听事件的函数
def listen_to_events():
    # 创建事件过滤器
    event_filter = contract.events.QuestionAnswered.create_filter(from_block='latest')

    print("开始监听 QuestionAnswered 事件...")
    while True:
        try:
            # 获取新事件
            for event in event_filter.get_new_entries():
                print("问题已回答，问题 ID 为：", event['args']['questionId'])
                print("问题已回答，回答者地址为：", event['args']['answerer'])
                print("问题已回答，回答内容为：", event['args']['answerContent'])
                # 退出监听线程（如果需要可以去掉 exit()，改为持续监听）
                return
            time.sleep(5)  # 每隔 5 秒检查一次
        except Exception as e:
            print(f"监听事件时发生错误: {e}")
            time.sleep(5)


# 在单独线程中启动事件监听
event_listener_thread = threading.Thread(target=listen_to_events)
event_listener_thread.daemon = True  # 设置为守护线程，主线程退出时自动终止
event_listener_thread.start()

question_content = "What is the firmware version?"

# 获取当前交易的 nonce
nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
transaction = contract.functions.askQuestion(question_content).build_transaction({
    'from': WALLET_ADDRESS,
    'nonce': nonce,
    'gas': 2000000,  # 估算的 Gas 限制
    'gasPrice': web3.to_wei('5000', 'gwei')  # Gas 价格
})

# 签名交易
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=USER_PRIVATE_KEY)

# 发送交易
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

print("交易已发送，交易哈希为：", tx_hash.hex())

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
event_listener_thread.join()


