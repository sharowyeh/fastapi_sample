from pydantic import BaseModel
from typing import Optional

class NrfBleInitArgs(BaseModel):
    serial_port: str = "COM3"
    baud_rate: int = 10000
    adapter_desc: Optional[str] = None # Optional is no feature in fastapi 

class NrfBleScanArgs(BaseModel):
    interval:float = 200
    window:float = 50
    activated:bool = True
    timeout:int = 0 # 0 will be infinite
