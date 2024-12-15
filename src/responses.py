from fastapi.responses import JSONResponse


class OK(JSONResponse):
    status_code: int = 200


class ValidationError(JSONResponse):
    status_code: int = 422


class InternalError(JSONResponse):
    status_code: int = 500


class BadRequest(JSONResponse):
    status_code: int = 400
