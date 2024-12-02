// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ParkingFeeSystem {
    struct VehicleInfo {
        string vehicleNumber;
        string userName;
        address walletAddress;
        uint256 parkingHours; // Parking hours for this vehicle
        uint256 totalFee;     // Total calculated fee for parking
    }

    mapping(address => VehicleInfo[]) public userVehicles; // User's multiple vehicles
    mapping(address => uint256) public balances;           // User balances for parking fees
    address public owner;                                  // Contract owner (admin)
    uint256 public feeRatePerHour;                         // Fee rate per hour in Wei

    event VehicleRegistered(address indexed user, string vehicleNumber);
    event ParkingHoursSet(address indexed user, string vehicleNumber, uint256 parkingHours, uint256 fee);
    event FeePaid(address indexed user, string vehicleNumber, uint256 amount);
    event BalanceDeposited(address indexed user, uint256 amount);
    event BalanceWithdrawn(address indexed user, uint256 amount);
    event OwnerWithdrawn(uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
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

        // Check if the vehicle number is already registered for this user
        for (uint256 i = 0; i < userVehicles[msg.sender].length; i++) {
            require(
                keccak256(bytes(userVehicles[msg.sender][i].vehicleNumber)) != keccak256(bytes(_vehicleNumber)),
                "Vehicle already registered"
            );
        }

        // Add a new vehicle to the user's list
        userVehicles[msg.sender].push(
            VehicleInfo({
                vehicleNumber: _vehicleNumber,
                userName: _userName,
                walletAddress: msg.sender,
                parkingHours: 0,
                totalFee: 0
            })
        );

        emit VehicleRegistered(msg.sender, _vehicleNumber);
    }

    /**
     * @notice Set parking hours for a specific vehicle
     * @param _vehicleNumber The vehicle number
     * @param parkingHours The number of hours the vehicle will be parked
     */
    function setParkingHours(string memory _vehicleNumber, uint256 parkingHours) public {
        require(parkingHours > 0, "Parking hours must be greater than zero");

        // Find the vehicle by its number
        VehicleInfo[] storage vehicles = userVehicles[msg.sender];
        bool vehicleFound = false;

        for (uint256 i = 0; i < vehicles.length; i++) {
            if (keccak256(bytes(vehicles[i].vehicleNumber)) == keccak256(bytes(_vehicleNumber))) {
                vehicles[i].parkingHours = parkingHours;
                vehicles[i].totalFee = parkingHours * feeRatePerHour; // Calculate the total fee
                vehicleFound = true;

                emit ParkingHoursSet(msg.sender, _vehicleNumber, parkingHours, vehicles[i].totalFee);
                break;
            }
        }

        require(vehicleFound, "Vehicle not found");
    }

    /**
     * @notice Pay the parking fee for a specific vehicle
     * @param _vehicleNumber The vehicle number
     */
    function payFee(string memory _vehicleNumber) public {
        VehicleInfo[] storage vehicles = userVehicles[msg.sender];
        bool vehicleFound = false;

        for (uint256 i = 0; i < vehicles.length; i++) {
            if (keccak256(bytes(vehicles[i].vehicleNumber)) == keccak256(bytes(_vehicleNumber))) {
                require(vehicles[i].totalFee > 0, "No fee to pay");
                require(balances[msg.sender] >= vehicles[i].totalFee, "Insufficient balance to pay the fee");

                // Deduct the fee from the user's balance
                balances[msg.sender] -= vehicles[i].totalFee;

                // Reset parking hours and fee after payment
                vehicles[i].parkingHours = 0;
                vehicles[i].totalFee = 0;

                vehicleFound = true;

                emit FeePaid(msg.sender, _vehicleNumber, vehicles[i].totalFee);
                break;
            }
        }

        require(vehicleFound, "Vehicle not found");
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
     * @notice Retrieve user's parking info for all vehicles
     * @param _user The address of the user
     */
    function getVehicleInfo(address _user) public view returns (VehicleInfo[] memory) {
        return userVehicles[_user];
    }
}
