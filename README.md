# GAFA(front-end)

## Project Setup

```sh
npm install web3
npm install element-plus
```
please make sure that you have install node.js(version>=18.19.0) and  vue3

### Project Parameter or Variables Adjustment
1. replace the wallet address and private key with yours in the `App.vue`.

     ```js
     const sender = "";
     const privateKey = "";
     ```
    please make sure that your wallet is in sepolia test network and has enough make sepoliaETH for you to send message.

2. replace the contract address in the `config.js` if you deploy them again.

     ```js
     const DEMO_CONTRACT_ADDRESS = "";
     const TOKEN_CONTRACT_ADDRESS = "";
     ```

    please make sure that your smart contract are deployed in sepolia test network.

### Compile and Run Vue

```sh
npm run dev
```

### Test on the Website
open http://localhost:5173/  to test

