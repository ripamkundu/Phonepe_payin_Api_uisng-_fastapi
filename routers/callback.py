from fastapi import APIRouter, HTTPException, Request
from src.model.payapi import CallbackRequest
from src.database.connection import connect
from src.security.token import verify_checksum
from src.database.settings import salt_key

router = APIRouter(
    prefix="/payapi",
    tags=["payapi"],
)


@router.post("/payment_callback")
async def payment_callback(callback_request: CallbackRequest, request: Request):
    params = callback_request.dict()
    checksum = params.pop("checksum")
    if not checksum or not verify_checksum(params, checksum.split("###")[0], salt_key):
        raise HTTPException(status_code=401, detail="Invalid checksum")

    try:
        conn = connect()
        cursor = conn.cursor()

        columns = ", ".join(params.keys())
        placeholders = ", ".join(["%s"] * len(params))
        values = tuple(params.values())

        insert_query = f"""
            INSERT INTO payment_callbacks ({columns}, checksum)
            VALUES ({placeholders}, %s);
        """

        cursor.execute(insert_query, values + (checksum,))

        conn.commit()
        callback_id = cursor.lastrowid
        if not callback_id:
            raise HTTPException(
                status_code=500,
                detail="Error: Failed to insert callback data into the database.",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return {
        "success": True,
        "message": "Callback received and processed successfully",
    }
