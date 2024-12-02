import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ABI_FILE_PATH = os.path.join(os.path.dirname(__file__), '../../artifacts-zk/contracts/Contract.sol/ParkingFeeSystem.json')

if not RPC_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    raise Exception("Missing required environment variables in .env file.")

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.isConnected():
    raise Exception("Failed to connect to the blockchain network.")

# Load contract ABI
try:
    with open(ABI_FILE_PATH, 'r') as abi_file:
        contract_abi = json.load(abi_file)["abi"]
except Exception as e:
    raise Exception(f"Failed to load contract ABI: {str(e)}")

# Create a signer
signer = Account.from_key(PRIVATE_KEY)

# Initialize contract
contract = web3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=contract_abi)

# Functions to interact with the contract
def register_vehicle(vehicle_number: str, user_name: str):
    """
    Registers a new vehicle for the user.
    """
    try:
        tx = contract.functions.registerVehicle(vehicle_number, user_name).buildTransaction({
            'from': signer.address,
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 500000,
            'gasPrice': web3.toWei('20', 'gwei'),
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to register vehicle: {str(e)}")

def set_parking_hours(vehicle_number: str, parking_hours: int):
    """
    Sets parking hours for a specific vehicle.
    """
    try:
        tx = contract.functions.setParkingHours(vehicle_number, parking_hours).buildTransaction({
            'from': signer.address,
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 500000,
            'gasPrice': web3.toWei('20', 'gwei'),
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to set parking hours for vehicle {vehicle_number}: {str(e)}")

def get_vehicle_info(user_address: str):
    """
    Retrieves all vehicles registered by a user.
    """
    try:
        return contract.functions.getVehicleInfo(Web3.toChecksumAddress(user_address)).call()
    except Exception as e:
        raise Exception(f"Failed to get vehicle info: {str(e)}")

def deposit_balance(amount_in_ether: float):
    """
    Deposits balance to the user's account in the contract.
    """
    try:
        tx = {
            'from': signer.address,
            'to': CONTRACT_ADDRESS,
            'value': web3.toWei(amount_in_ether, 'ether'),
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 500000,
            'gasPrice': web3.toWei('20', 'gwei'),
        }
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to deposit balance: {str(e)}")

def pay_fee(vehicle_number: str):
    """
    Pays the parking fee for a specific vehicle.
    """
    try:
        tx = contract.functions.payFee(vehicle_number).buildTransaction({
            'from': signer.address,
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 500000,
            'gasPrice': web3.toWei('20', 'gwei'),
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to pay fee for vehicle {vehicle_number}: {str(e)}")

# Example Usage
if __name__ == "__main__":
    try:
        # Example: Register a vehicle
        receipt = register_vehicle("ABC123", "John Doe")
        print(f"Vehicle registered: {receipt}")

        # Example: Set parking hours for a specific vehicle
        receipt = set_parking_hours("ABC123", 5)
        print(f"Parking hours set: {receipt}")

        # Example: Get registered vehicles
        vehicles = get_vehicle_info(signer.address)
        print(f"Registered vehicles: {vehicles}")

        # Example: Deposit balance
        receipt = deposit_balance(0.1)  # Deposit 0.1 ETH
        print(f"Balance deposited: {receipt}")

        # Example: Pay parking fee
        receipt = pay_fee("ABC123")
        print(f"Fee paid: {receipt}")

    except Exception as e:
        print(str(e))
