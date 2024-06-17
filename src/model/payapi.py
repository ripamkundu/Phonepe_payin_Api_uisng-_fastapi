from pydantic import BaseModel, Field
from typing import Optional


class PaymentRequest(BaseModel):
   merchantId: str = Field(...)
   merchantTransactionId: str = Field(...)
   merchantUserId: str = Field(...)
   amount: int = Field(...)
   redirectUrl: str = Field(...)
   redirectMode: str = Field(...)
   callbackUrl: str = Field(...)
   mobileNumber: str = Field(None)
   paymentInstrument: dict

class CallbackRequest(BaseModel):
   code: str
   merchantId: str
   transactionId: str
   amount: int
   providerReferenceId: str
   merchantOrderId: str
   param1: Optional[str] = None
   param2: Optional[str] = None
   param3: Optional[str] = None
   param4: Optional[str] = None
   param5: Optional[str] = None
   param6: Optional[str] = None
   param7: Optional[str] = None
   param8: Optional[str] = None
   param9: Optional[str] = None
   param10: Optional[str] = None
   param11: Optional[str] = None
   param12: Optional[str] = None
   param13: Optional[str] = None
   param14: Optional[str] = None
   param15: Optional[str] = None
   param16: Optional[str] = None
   param17: Optional[str] = None
   param18: Optional[str] = None
   param19: Optional[str] = None
   param20: Optional[str] = None
   checksum: str