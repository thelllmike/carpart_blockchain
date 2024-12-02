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
async def set_parking_hours_endpoint(vehicle_number: str, parking_hours: int):
    """
    Endpoint to set parking hours for a specific vehicle on the blockchain.
    """
    try:
        receipt = set_parking_hours(vehicle_number, parking_hours)
        return {
            "status": "success",
            "transactionHash": receipt.transactionHash.hex(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set parking hours for vehicle {vehicle_number}: {str(e)}")

@router.get("/parking/info/{user_address}")
async def get_vehicle_info_endpoint(user_address: str):
    """
    Endpoint to get all vehicles information for a user from the blockchain.
    """
    try:
        vehicles = get_vehicle_info(user_address)
        # Format the response to include all registered vehicles
        formatted_vehicles = [
            {
                "vehicleNumber": vehicle[0],
                "userName": vehicle[1],
                "walletAddress": vehicle[2],
                "parkingHours": vehicle[3],
                "totalFee": vehicle[4],
            }
            for vehicle in vehicles
        ]
        return {"status": "success", "vehicles": formatted_vehicles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vehicle info: {str(e)}")
