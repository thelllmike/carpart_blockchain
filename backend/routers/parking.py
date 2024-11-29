from fastapi import APIRouter, HTTPException
from model.blockchain import register_vehicle, set_parking_hours, get_vehicle_info

router = APIRouter()

@router.post("/parking/register/")
async def register_vehicle_endpoint(vehicle_number: str, user_name: str):
    """
    Endpoint to register a vehicle on the blockchain.
    """
    try:
        receipt = register_vehicle(vehicle_number, user_name)
        return {
            "status": "success",
            "transactionHash": receipt.transactionHash.hex(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register vehicle: {str(e)}")

@router.post("/parking/set-hours/")
async def set_parking_hours_endpoint(parking_hours: int):
    """
    Endpoint to set parking hours on the blockchain.
    """
    try:
        receipt = set_parking_hours(parking_hours)
        return {
            "status": "success",
            "transactionHash": receipt.transactionHash.hex(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set parking hours: {str(e)}")

@router.get("/parking/info/{user_address}")
async def get_vehicle_info_endpoint(user_address: str):
    """
    Endpoint to get vehicle information from the blockchain.
    """
    try:
        info = get_vehicle_info(user_address)
        return {
            "vehicleNumber": info[0],
            "userName": info[1],
            "walletAddress": info[2],
            "parkingHours": info[3],
            "totalFee": info[4],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vehicle info: {str(e)}")
