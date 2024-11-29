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
import os
ABI_FILE_PATH = os.path.join(os.path.dirname(__file__), '../../artifacts/contracts/Contract.sol/ParkingFeeSystem.json')


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
    try:
        tx = contract.functions.registerVehicle(vehicle_number, user_name).buildTransaction({
            'from': signer.address,
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 300000,
            'gasPrice': web3.toWei('20', 'gwei'),
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to register vehicle: {str(e)}")

def set_parking_hours(parking_hours: int):
    try:
        tx = contract.functions.setParkingHours(parking_hours).buildTransaction({
            'from': signer.address,
            'nonce': web3.eth.getTransactionCount(signer.address),
            'gas': 300000,
            'gasPrice': web3.toWei('20', 'gwei'),
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.eth.waitForTransactionReceipt(tx_hash)
    except Exception as e:
        raise Exception(f"Failed to set parking hours: {str(e)}")

def get_vehicle_info(user_address: str):
    try:
        return contract.functions.getVehicleInfo(Web3.toChecksumAddress(user_address)).call()
    except Exception as e:
        raise Exception(f"Failed to get vehicle info: {str(e)}")
