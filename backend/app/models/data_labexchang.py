from pydantic import BaseModel

class InvestmentRequest(BaseModel):
    monthly_investment: float
    years: int

class GasCalculationRequest(BaseModel):
    data: str
    base_fee: float
    priority_fee: float
