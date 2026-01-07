import os
import requests
import base64
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file



# ---------------------------------------------------
# Microsoft Azure App Configuration
# ---------------------------------------------------
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# ---------------------------------------------------
# Load Email Templates
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
# ---------------------------------------------------
# Get Microsoft Graph Access Token
# ---------------------------------------------------
def get_graph_token() -> str:
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# ---------------------------------------------------
# Send Email Function
# ---------------------------------------------------
def send_email(
    to_email: list[str] | str,
    username: str,
    subject: str,
    cc_email: list[str] | None = None,
    bcc_email:list[str] | None = None,
):
    try:
        # Render HTML template
        template = env.get_template("welcome.html")
        html_content = template.render(username=username)

        # Encode logo image
        with open("covalenseglobal_logo.png", "rb") as img:
            image_base64 = base64.b64encode(img.read()).decode("utf-8")

        access_token = get_graph_token()

        email_payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": html_content
                },
                "toRecipients": [
                    {"emailAddress": {"address": to_email}}
                ],
                "attachments": [
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": "logo.png",
                        "contentType": "image/png",
                        "contentBytes": image_base64,
                        "isInline": True,
                        "contentId": "logo_image"
                    }
                ]
            },
            "saveToSentItems": True
        }

        # Add CC recipients if provided
        if cc_email:
            email_payload["message"]["ccRecipients"] = [
                {"emailAddress": {"address": email}}
                for email in cc_email
            ]

        # Add BCC recipients if provided
        if bcc_email:
            email_payload["message"]["bccRecipients"] = [
                {"emailAddress": {"address": email}}
                for email in bcc_email
            ]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        send_url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"

        response = requests.post(send_url, headers=headers, json=email_payload)
        response.raise_for_status()

        print("✅ Welcome email sent successfully")

    except Exception as e:
        print(f"❌ Error sending email: {e}")





if __name__ == "__main__":
    # Test the send_email function
    send_email(
        to_email="rakesh.barthipaka@covalenseglobal.com",
        username="Rakesh",
        # cc_email=["santhosh.ketthe@covalenseglobal.com"],
        # bcc_email=["vamsi.bonamukkala@covalenseglobal.com"],
        subject="Welcome to Mini-CRM ",
    )