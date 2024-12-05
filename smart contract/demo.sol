// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// 假设你已经有一个 ERC-20 代币合约
interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}

contract Demo {

    IERC20 public token;  // 自定义 ERC-20 代币的合约接口

    // 定义结构体来存储设备的基本信息
    struct Device {
        uint256 deviceId;        // 设备号
        string ipAddress;        // IP 地址
        string firmwareUrl;      // 固件地址
        string deviceName;       // 设备名称
        AddressInfo location;    // 设备的位置信息（嵌套结构体）
        address walletAddress;   // 设备关联的钱包地址
    }

    struct Question {
        uint256 questionId;
        address questioner;
        address answerer;
        uint256 time;
        string questionContent;
        string answerContent;
    }

    // 定义结构体来存储设备的具体位置信息
    struct AddressInfo {
        string country;          // 国家
        string city;             // 城市
        string street;           // 街道
        string postalCode;       // 邮政编码
    }

    // 按设备号存储设备信息
    mapping(uint256 => Device) public devices;
    // 按钱包地址存储设备信息
    mapping(address => uint256) public deviceByWallet;

    // 当节点提问时触发的事件
    event QuestionAsked(
        uint256 indexed questionId,
        address indexed questioner,
        string questionContent,
        uint256 timestamp
    );

    // 存储提问和回答
    mapping(uint256 => Question) public questions;
    uint256 public questionCounter;

    // 当节点回答问题时触发的事件
    event QuestionAnswered(
        uint256 indexed questionId,
        address indexed questioner,
        address indexed answerer,
        string questionContent,
        string answerContent,
        uint256 timestamp
    );

    // 节点转账事件
    event TokenTransferred(
        address indexed sender, 
        address indexed recipient, 
        uint256 amount);

    // 构造函数，初始化自定义代币合约地址
    constructor(address _tokenAddress) {
        token = IERC20(_tokenAddress);  // 传入自定义 ERC-20 代币的合约地址
    }

    // 注册设备
    function registerDevice(
        uint256 _deviceId,
        string memory _ipAddress,
        string memory _firmwareUrl,
        string memory _deviceName,
        string memory _country,
        string memory _city,
        string memory _street,
        string memory _postalCode,
        address _walletAddress  // 设备关联的钱包地址
    ) public {
        // 创建AddressInfo结构体
        AddressInfo memory newAddressInfo = AddressInfo({
            country: _country,
            city: _city,
            street: _street,
            postalCode: _postalCode
        });

        // 创建Device结构体并存储到devices映射中
        devices[_deviceId] = Device({
            deviceId: _deviceId,
            ipAddress: _ipAddress,
            firmwareUrl: _firmwareUrl,
            deviceName: _deviceName,
            location: newAddressInfo,
            walletAddress: _walletAddress
        });

        // 将设备的钱包地址映射到设备ID
        deviceByWallet[_walletAddress] = _deviceId;
    }

    // 根据钱包地址查找设备信息
    function getDeviceByWallet(address _walletAddress) public view returns (Device memory) {
        uint256 deviceId = deviceByWallet[_walletAddress];
        // require(deviceId != 0, "Device not found for the given wallet address");
        return devices[deviceId];
    }

    // 查询设备钱包地址的代币余额
    function getDeviceTokenBalance(uint256 _deviceId) public view returns (uint256) {
        Device memory device = devices[_deviceId];
        return token.balanceOf(device.walletAddress);  // 查询设备钱包的代币余额
    }

    
    function transferTokens(address _recipient, uint256 _amount) public {
        require(token.balanceOf(msg.sender) >= _amount, "Insufficient balance");
        require(_recipient != address(0), "Invalid recipient address");
        require(token.transfer(_recipient, _amount), "Token transfer failed");
    }
    
        
    function askQuestion(string memory _questionContent) public {
        // 增加问题计数器
        questionCounter++;

        // 创建一个新的问题并存储
        questions[questionCounter] = Question({
            questionId: questionCounter,
            questioner: msg.sender,
            answerer: address(0), // 初始值为空地址
            time: block.timestamp,
            questionContent: _questionContent,
            answerContent: ""
        });

        // 触发提问事件
        emit QuestionAsked(
            questionCounter,
            msg.sender,
            _questionContent,
            block.timestamp
        );
    }

    // 回答函数
    function answerQuestion(uint256 _questionId, string memory _answerContent) public {
        Question storage question = questions[_questionId];

        require(question.questionId != 0, "Question does not exist");
        require(bytes(question.answerContent).length == 0, "Question already answered");

        // 更新问题的回答内容和回答者
        question.answerer = msg.sender;
        question.answerContent = _answerContent;

        // 触发回答事件
        emit QuestionAnswered(
            question.questionId,
            question.questioner,
            msg.sender,
            question.questionContent,
            _answerContent,
            block.timestamp
        );
    }

    function transferBetweenAccounts(
        address sender,
        address recipient,
        uint256 amount
    ) public returns (bool) {
        require(sender != address(0), "Sender address cannot be zero");
        require(recipient != address(0), "Recipient address cannot be zero");
        require(amount > 0, "Transfer amount must be greater than zero");

        uint256 senderBalance = token.balanceOf(sender);
        require(senderBalance >= amount, "Sender has insufficient balance");

        bool success = token.transferFrom(sender, recipient, amount);
        require(success, "Token transfer failed");

        emit TokenTransferred(sender, recipient, amount); // 记录事件

        return true;
    }

}