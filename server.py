import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class EmailRequest(BaseModel):
    role: str
    companyName: str
    userEmail: str

@app.post("/api/generate_email")
async def generate_email_endpoint(request: EmailRequest):
    generated_email = start_email_generation(request.role, request.companyName, request.userEmail)
    return {"generatedEmail": generated_email}

def start_email_generation(role, companyName, userEmail):
    from generate_email import generate_email
    return generate_email(userEmail, role, companyName)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5151)