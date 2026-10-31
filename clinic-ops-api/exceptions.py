from fastapi import Request, status
from fastapi.responses import JSONResponse

class ResourceNotFoundError(Exception):
    def __init__(self, resource_name: str, resource_id: int):
        self.resource_name = resource_name
        self.resource_id = resource_id

async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": f"{exc.resource_name} with ID {exc.resource_id} does not exist."
        },
    )
