pragma solidity ^0.8.0;

contract VehicleRegistry {
    struct VehicleInfo {
        string vehicleNumber;
        string userName;
        address walletAddress;
    }

    mapping(address => VehicleInfo) public vehicleRecords;

    event VehicleRegistered(address indexed user, string vehicleNumber);

    function registerVehicle(string memory _vehicleNumber, string memory _userName) public {
        vehicleRecords[msg.sender] = VehicleInfo(_vehicleNumber, _userName, msg.sender);
        emit VehicleRegistered(msg.sender, _vehicleNumber);
    }

    function getVehicleInfo(address _user) public view returns (VehicleInfo memory) {
        return vehicleRecords[_user];
    }
}
