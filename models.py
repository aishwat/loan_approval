from pydantic import BaseModel, ValidationError, validator
from typing import Optional

class Customer(BaseModel):
    customerID: int
    dob: str
    income: int
    bureauScore: int
    applicationScore: int
    maxDelL12M: int
    allowedFoir: int
    existingEMI: int
    loanTenure: int
    currentAddress: str
    bureauAddress: str
    # @validator('income')
    # def gt20k(cls, v):
    #     if v < 20000:
    #         raise ValueError('income must be gt 20k')
    #     return v

class Resp:
    approvalStatus: str
    reasonCode: Optional[str]
    addressMatchingScore: float
    loanAmount: Optional[str]
    loanTenure: Optional[str]

# cust = {
#     "customerID": 100000,
#     "dob": "01/01/1977",
#     "income": 25000,
#     "bureauScore": 700,
#     "applicationScore": 750,
#     "maxDelL12M": 0,
#     "allowedFoir": 60,
#     "existingEMI": 2000,
#     "loanTenure": 24,
#     "currentAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037",
#     "bureauAddress": "HOUSE NO 15 2ND CROSS VASANT LAYOUT MARATHALLI NEAR VAGDEVI SCHOOL BANGALORE 560037 KA"
# }