from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import uvicorn

class UserRegistration(BaseModel):
    name: str
    password: str
    email: str

app = FastAPI()

@app.post("/register")
async def register_user(request: Request, data: UserRegistration):
    # Validate the user registration data
    if not data.name or not data.password or not data.email:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Missing required fields"},
        )

    # Add the user to the database

    # Return a success message
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"message": "User successfully registered"}),
    )




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

