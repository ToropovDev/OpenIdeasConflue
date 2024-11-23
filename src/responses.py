from fastapi.responses import JSONResponse


class OK(JSONResponse):
    status_code: int = 200
