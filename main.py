from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime  # Import datetime module


admission = FastAPI()

# Configure CORS
admission.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your React application's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

class FormData(BaseModel):
    name: str
    phone: str
    score: str
    course: str
    address: str

@admission.post("/submit-form")
async def submit_form(form_data: FormData):
    try:
        sender_email = os.getenv("MAIL_USERNAME")
        password = os.getenv("MAIL_PASSWORD")
        receiver_email = "shivamdeokar9@gmail.com"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        current_date = datetime.now().strftime("%d-%m-%Y")
        message["Subject"] = f"{form_data.name} Registration Form Submitted on {current_date}"

        # HTML formatted email body
        body = f"""
            <html>
            <body>
                <p><b>Name:</b>  {form_data.name}</p>
                <p><b>Score:</b>  {form_data.score}</p>
                <p><b>Address:</b>  {form_data.address}</p>
                <p><b>Phone:</b>  {form_data.phone}</p>
                <p><b>Course:</b>   {form_data.course}</p>
            </body>
            </html>
        """
        message.attach(MIMEText(body, "html"))

        # Connect to SMTP server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return {"message": "Form submitted successfully"}
    except Exception as e:
        print(f"Error in submit_form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

