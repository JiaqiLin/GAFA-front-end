<template>
  <div>
    <div class="index">
      <el-container>
        <el-header>
          <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false">
            <el-menu-item index="0">
              Send-Receive Message on Pig Coin
            </el-menu-item>
          </el-menu></el-header>
        <el-container>
          <el-main>
            <el-row>
              <el-col :span="12">
                <div style="padding-left: 15%;padding-right: 10%;;padding-top: 0%;">
                  <div><el-text style="font-size: larger;" type="primary" size="large" tag="b">User1</el-text></div>
                  <div>token:0xA15ed6A7A64f9c3544E244B9Ca547021c9fAd31f</div>
                  <div style="margin:4% 0 0 0;">Receive Message</div>
                  <div style="margin:2% 0 0 0;"><el-input v-model="user1ReceiveMessage" style="width: 500px" :rows="8"
                      type="textarea" placeholder="listening message in the blockchain......" /></div>
                  <div style="margin: 5% 0 0 0;">Send Message</div>
                  <!-- <div style="margin: 2% 0 0 0;"><el-input v-model="user1SendAddress" style="width: 500px" :rows="1"
                      type="textarea" placeholder="Please input receiver address" /></div> -->
                  <div style="margin: 2% 0 0 0;"><el-input v-model="user1SendQuestionId" style="width: 500px" :rows="1"
                      type="textarea" placeholder="Please input questionId if you want to answer question" /></div>
                  <div style="margin: 2% 0 0 0;"><el-input v-model="user1SendMessage" style="width: 500px" :rows="8"
                      type="textarea" placeholder="Please input message" /></div>
                  <div style="margin:2% 30% 0 30%;"><el-button type="primary" :icon="Message"
                      @click="user1Send">Send</el-button></div>
                </div>
              </el-col>
              <el-col :span="12">
                <div style="padding-left: 10%;padding-right: 15%;;padding-top: 0%;">
                  <div><el-text style="font-size: larger;" type="primary" size="large" tag="b">User2</el-text></div>
                  <div>token:0xf4CB179280020c4ace3BDef35278ed20717dA65c</div>
                  <div style="margin:4% 0 0 0;">Receive Message</div>
                  <div style="margin:2% 0 0 0;"><el-input v-model="user2ReceiveMessage" style="width: 500px" :rows="8"
                      type="textarea" placeholder="listening message in the blockchain......" /></div>
                  <div style="margin: 5% 0 0 0;">Send Message</div>
                  <!-- <div style="margin: 2% 0 0 0;"><el-input v-model="user2SendAddress" style="width: 500px" :rows="1"
                      type="textarea" placeholder="Please input receiver address" /></div> -->
                  <div style="margin: 2% 0 0 0;"><el-input v-model="user2SendQuestionId" style="width: 500px" :rows="1"
                      type="textarea" placeholder="Please input questionId if you want to answer question" /></div>
                  <div style="margin: 2% 0 0 0;"><el-input v-model="user2SendMessage" style="width: 500px" :rows="8"
                      type="textarea" placeholder="Please input message" /></div>
                  <div style="margin:2% 30% 0 30%;"><el-button type="primary" :icon="Message"
                      @click="user2Send">Send</el-button></div>
                </div>
              </el-col>
            </el-row>
          </el-main>
        </el-container>
      </el-container>
    </div>

  </div>
</template>


<script setup lang="ts">
import {
  Menu as IconMenu,
  Message
} from '@element-plus/icons-vue'

import { MetaMaskInpageProvider } from "@metamask/providers";

declare global {
  interface Window {
    ethereum?: MetaMaskInpageProvider;
  }
}

import { ref } from 'vue'


const user1ReceiveMessage = ref('')
const user1SendMessage = ref('')
const user1SendQuestionId = ref('')
const user2ReceiveMessage = ref('')
const user2SendMessage = ref('')
const user2SendQuestionId = ref('')



import { onMounted, onUnmounted } from 'vue'
import { DEMO_CONTRACT_ABI, DEMO_CONTRACT_ADDRESS, TOKEN_CONTRACT_ABI, TOKEN_CONTRACT_ADDRESS } from "./config";
import Web3 from "web3";


let web3 = null; // Web3 实例
let demo_contract = null; // Web3 实例
let token_contract = null; // Web3 实例
let QuestionAskedEvent = null
let QuestionAnsweredEvent = null

// 初始化 Web3 和合约
const initWeb3 = () => {
  //wss://sepolia.infura.io/ws/v3/f2394de6d5274c36b3b4eaded545e9e9
  web3 = new Web3(Web3.givenProvider || 'wss://sepolia.infura.io/ws/v3/f2394de6d5274c36b3b4eaded545e9e9');
  demo_contract = new web3.eth.Contract(DEMO_CONTRACT_ABI, DEMO_CONTRACT_ADDRESS);
  token_contract = new web3.eth.Contract(TOKEN_CONTRACT_ABI, TOKEN_CONTRACT_ADDRESS);
  console.log(web3)
  if (web3.currentProvider) {
    console.log("Web3 提供者已连接:", web3.currentProvider);
  } else {
    console.error("Web3 未连接，请检查提供者设置。");
  }
  web3.eth.getBlockNumber()
    .then((blockNumber) => {
      console.log("成功连接到区块链，当前最新区块号:", blockNumber);
    })
    .catch((error) => {
      console.error("无法连接到区块链:", error);
    });
};

// 监听合约事件
const listenToContractEvents = () => {
  QuestionAskedEvent = demo_contract.events.QuestionAsked({ filter: {}, fromBlock: 'latest' });
  console.log(QuestionAskedEvent);
  QuestionAskedEvent.on('data', (event: any) => {
    console.log(event);
    const time = new Date(Number(event.returnValues.timestamp.toString())).toLocaleDateString().replace(/\//g, "-") + " " + new Date(Number(event.returnValues.timestamp.toString())).toTimeString().substr(0, 8);

    user2ReceiveMessage.value = `question ${event.returnValues.questionId.toString()}:${event.returnValues.questionContent} \nquestioner:${event.returnValues.questioner}\n`;

  });
  QuestionAskedEvent.on('error', (error: any) => {
    console.error("事件监听失败:", error);
  });


  QuestionAnsweredEvent = demo_contract.events.QuestionAnswered({ filter: {}, fromBlock: 'latest' });
  console.log(QuestionAnsweredEvent);
  QuestionAnsweredEvent.on('data', (event: any) => {
    console.log(event);
    const time = new Date(Number(event.returnValues.timestamp.toString())).toLocaleDateString().replace(/\//g, "-") + " " + new Date(Number(event.returnValues.timestamp.toString())).toTimeString().substr(0, 8);

    user1ReceiveMessage.value = `question ${event.returnValues.questionId.toString()}:${event.returnValues.questionContent} \n\nanswer:${event.returnValues.answerContent}\nanswerer:${event.returnValues.answerer}`;

  });
  QuestionAskedEvent.on('error', (error: any) => {
    console.error("事件监听失败:", error);
  });
};

// 取消订阅
const unsubscribeEvents = () => {
  if (QuestionAskedEvent.value) {
    QuestionAskedEvent.value.unsubscribe((error, success) => {
      if (success) console.log("成功取消合约事件监听");
    });
  }
};

// 生命周期钩子
onMounted(() => {
  initWeb3();
  //createAccount();
  listenToContractEvents();
});

onUnmounted(() => {
  unsubscribeEvents();
});

//发送问题
// 写入方法：发送交易
const user1Send = async () => {
  if (user1SendMessage.value == '') {
    alert("请输入有效的信息！");
    return;
  }

  const sender = "0xA15ed6A7A64f9c3544E244B9Ca547021c9fAd31f"; // 发送方地址
  const privateKey = ''

  // 构造交易数据
  const data = demo_contract.methods.askQuestion(user1SendMessage.value).encodeABI();

  const tx = {
    to: DEMO_CONTRACT_ADDRESS,
    data: data,
    gas: 3000000, // 根据需求调整 Gas Limit，
    nonce: await web3.eth.getTransactionCount(sender),
    //gasPrice: web3.utils.toWei('5000', 'gwei'),
    maxPriorityFeePerGas: web3.utils.toWei('2', 'gwei'),
    maxFeePerGas: web3.utils.toWei('50', 'gwei'),
  };


  // 手动签名交易
  const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);

  // 发送签名后的交易
  web3.eth.sendSignedTransaction(signedTx.rawTransaction)
    .on('transactionHash', (hash) => {
      console.log('Transaction Hash:', hash);
    })
    .on('receipt', (receipt) => {
      console.log('Transaction Receipt:', receipt);
    })
    .on('error', (error) => {
      console.error('Transaction Error:', error);
      console.error('Transaction Error message:', error.message)
    });
};

//回答问题
const user2Send = async () => {
  if (user2SendMessage.value == '') {
    alert("请输入有效的回答！");
    return;
  }
  if (user2SendQuestionId.value == '') {
    alert("请输入有效的问题Id！");
    return;
  }

  const sender = "0xf4CB179280020c4ace3BDef35278ed20717dA65c"; // 发送方地址
  const privateKey = ''

  // 构造交易数据
  const data = demo_contract.methods.answerQuestion(user2SendQuestionId.value, user2SendMessage.value).encodeABI();

  const tx = {
    to: DEMO_CONTRACT_ADDRESS,
    data: data,
    gas: 3000000, // 根据需求调整 Gas Limit，
    nonce: await web3.eth.getTransactionCount(sender), // 获取交易的 nonce 值
    //gasPrice: web3.utils.toWei('5000', 'gwei'),
    maxPriorityFeePerGas: web3.utils.toWei('2', 'gwei'),
    maxFeePerGas: web3.utils.toWei('50', 'gwei'),
  };



  // 手动签名交易
  const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);

  // 发送签名后的交易
  web3.eth.sendSignedTransaction(signedTx.rawTransaction)
    .on('transactionHash', (hash) => {
      console.log('Transaction Hash:', hash);
    })
    .on('receipt', (receipt) => {
      console.log('Transaction Receipt:', receipt);
    })
    .on('error', (error) => {
      console.error('Transaction Error:', error);
      console.error('Transaction Error message:', error.message)
    });
};


</script>



<style scoped>
.el-menu--horizontal>.el-menu-item:nth-child(1) {
  margin-right: auto;
}



.index {
  padding: 0px;
  margin: 0px;
  height: calc(92vh);
  width: 100%;
}

.el-container {
  height: 100%;
  width: 100%;
}
</style>
