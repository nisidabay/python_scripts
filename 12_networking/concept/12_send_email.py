import smtplib
import ssl
from dataclasses import dataclass
from typing import Any
from decouple import config
from rich.console import Console


@dataclass
class SendMail:
    """Class to send plain text emails"""

    sent_to: str = ""
    subject: str = ""
    body: str = ""
    email_message = f"Subject:{subject}\nTo:{sent_to}\n{body}"
    console: Any = Console()

    def __post_init__(self) -> None:
        """Get default options from config file"""

        self.smtp_server = config("smtp_server")
        self.smtp_port = config("smtp_port")
        self.mail = config("mail")
        self.passw = config("password")

    def send_email(self) -> None:
        """Send a plain text email"""

        with smtplib.SMTP_SSL(self.smtp_server,
                              self.smtp_port,
                              context=ssl.create_default_context()) as email:

            # Credentials
            email.login(self.mail, self.passw)

            # Sending message
            email.sendmail(self.mail, self.sent_to, self.email_message)

            self.console.print(
                f"[green][+] :email: Email sent successfully to: {self.sent_to}[/]"
            )


if __name__ == "__main__":
    mail = SendMail("nisidabay @ gmail.com", "Download completed",
                    "Python full course have been downloaded")
    mail.send_email()
