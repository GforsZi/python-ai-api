from pydantic import BaseModel
from typing import Any
class ApiResponse:
    def __init__(self, message: str, data: Any = None, status_code: int = 200):
        self.message = message
        self.data = data
        self.status_code = status_code

    def _serialize(self, data: Any) -> Any:
        if data is None:
            return None
        if isinstance(data, list):
            return [
                item.model_dump() if isinstance(item, BaseModel) else item
                for item in data
            ]
        if isinstance(data, BaseModel):
            return data.model_dump()
        return data

    def to_dict(self) -> dict:
        return {
            "success": self.status_code < 400,
            "message": self.message,
            "data": self._serialize(self.data),
            "status_code": self.status_code
        }


