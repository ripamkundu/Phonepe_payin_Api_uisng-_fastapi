from fastapi import APIRouter, HTTPException
from src.model.payapi import PaymentRequest
from src.database.connection import connect
from mysql.connector import Error
from src.security.token import generate_redirect_url 

router = APIRouter(
    prefix="/payapi",
    tags=["payapi"],
)


@router.post("/payment")
async def payment(request: PaymentRequest):
   try:
      conn = connect()
      cursor = conn.cursor()
      insert_query = """
         INSERT INTO payments (merchantId, merchantTransactionId, merchantUserId, amount, redirectUrl, redirectMode, callbackUrl, mobileNumber, paymentInstrumentType) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
      """
      cursor.execute(
         insert_query,
         (
            request.merchantId,
            request.merchantTransactionId,
            request.merchantUserId,
            request.amount,
            request.redirectUrl,
            request.redirectMode,
            request.callbackUrl,
            request.mobileNumber,
            request.paymentInstrument["type"],
         ),
      )
      conn.commit()
      payment_id = cursor.lastrowid
      if not payment_id:
         raise HTTPException(
            status_code=500,
            detail="Error: Failed to insert payment data into the database.",
         )
      redirect_url = generate_redirect_url()
   except Error as e:
      raise HTTPException(status_code=500, detail=f"Error: {e}")
   finally:
      if conn.is_connected():
         cursor.close()
         conn.close()
         
   return {
      "success": True,                                                  
      "code": "PAYMENT_INITIATED",
      "message": "Payment Initiated",
      "data": {
         "merchantId": request.merchantId,
         "merchantTransactionId": request.merchantTransactionId,
         "instrumentResponse": {
            "type": "PAY_PAGE",
            "redirectInfo": {"url": redirect_url, "method": "GET"},
         },
      },
   }
