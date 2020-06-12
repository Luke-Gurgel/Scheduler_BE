import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailService:
    def __init__(self):
        """Email service."""
        self.email_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

    def send_invite_email(self, team_name: str, from_email: str, to_emails: [str]):
        invite_msg = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject="Invitation to join a team on Sched",
            plain_text_content=f"You have been invited to join the {team_name} team on Sched!",
        )
        response = self.email_client.send(invite_msg)
        return response
