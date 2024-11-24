// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ParkingFeeSystem {
    struct VehicleInfo {
        string vehicleNumber;
        string userName;
        address walletAddress;
        uint256 entryTime;
        uint256 exitTime;
    }

    mapping(address => VehicleInfo) public vehicleRecords; // Maps wallet addresses to vehicle info
    mapping(address => uint256) public balances;          // User balances to pay parking fees
    address public owner;                                 // Contract owner (admin)
    uint256 public feeRatePerHour;                        // Fee rate per hour in Wei

    event VehicleRegistered(address indexed user, string vehicleNumber);
    event EntryRecorded(address indexed user, uint256 entryTime);
    event ExitRecorded(address indexed user, uint256 exitTime, uint256 fee);
    event BalanceDeposited(address indexed user, uint256 amount);
    event BalanceWithdrawn(address indexed user, uint256 amount);
    event OwnerWithdrawn(uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    modifier userExists() {
        require(bytes(vehicleRecords[msg.sender].vehicleNumber).length > 0, "User not registered");
        _;
    }

    constructor(uint256 _feeRatePerHour) {
        owner = msg.sender; // Set the deployer as the owner
        feeRatePerHour = _feeRatePerHour; // Initialize fee rate in Wei
    }

    /**
     * @notice Register a vehicle for the caller
     * @param _vehicleNumber The vehicle number to register
     * @param _userName The user's name
     */
    function registerVehicle(string memory _vehicleNumber, string memory _userName) public {
        require(bytes(_vehicleNumber).length > 0, "Vehicle number cannot be empty");
        require(bytes(_userName).length > 0, "User name cannot be empty");
        require(bytes(vehicleRecords[msg.sender].vehicleNumber).length == 0, "Vehicle already registered");

        vehicleRecords[msg.sender] = VehicleInfo({
            vehicleNumber: _vehicleNumber,
            userName: _userName,
            walletAddress: msg.sender,
            entryTime: 0,
            exitTime: 0
        });

        emit VehicleRegistered(msg.sender, _vehicleNumber);
    }

    /**
     * @notice Record vehicle entry time
     */
    function recordEntry() public userExists {
        VehicleInfo storage vehicle = vehicleRecords[msg.sender];
        require(vehicle.entryTime == 0, "Vehicle is already parked");

        vehicle.entryTime = block.timestamp;
        emit EntryRecorded(msg.sender, vehicle.entryTime);
    }

    /**
     * @notice Record vehicle exit time and calculate fees
     */
    function recordExit() public userExists {
        VehicleInfo storage vehicle = vehicleRecords[msg.sender];
        require(vehicle.entryTime > 0, "Vehicle has not entered");
        require(vehicle.exitTime == 0, "Vehicle has already exited");

        vehicle.exitTime = block.timestamp;

        // Calculate parking duration in hours and fee
        uint256 parkedDuration = (vehicle.exitTime - vehicle.entryTime) / 3600; // Duration in hours
        uint256 fee = parkedDuration * feeRatePerHour;

        // Ensure the user has enough balance to pay the fee
        require(balances[msg.sender] >= fee, "Insufficient balance to pay parking fee");

        // Deduct fee from user's balance
        balances[msg.sender] -= fee;

        // Reset entry and exit times
        vehicle.entryTime = 0;
        vehicle.exitTime = 0;

        emit ExitRecorded(msg.sender, block.timestamp, fee);
    }

    /**
     * @notice Deposit funds into the user's balance
     */
    function depositBalance() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += msg.value;
        emit BalanceDeposited(msg.sender, msg.value);
    }

    /**
     * @notice Withdraw remaining balance from the user's account
     */
    function withdrawBalance() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance to withdraw");

        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
        emit BalanceWithdrawn(msg.sender, amount);
    }

    /**
     * @notice Admin withdraws collected fees
     */
    function withdrawCollectedFees() public onlyOwner {
        uint256 amount = address(this).balance;
        require(amount > 0, "No fees to withdraw");

        payable(owner).transfer(amount);
        emit OwnerWithdrawn(amount);
    }

    /**
     * @notice Change the hourly fee rate (admin-only)
     * @param _newFeeRate The new fee rate per hour
     */
    function setFeeRate(uint256 _newFeeRate) public onlyOwner {
        feeRatePerHour = _newFeeRate;
    }

    /**
     * @notice Retrieve user's parking info
     */
    function getVehicleInfo(address _user) public view returns (VehicleInfo memory) {
        return vehicleRecords[_user];
    }
}
