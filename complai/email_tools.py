from agents import function_tool
from messenger import send_email


@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """Send the selected ComplAI sales email to configured sales recipients.

    Args:
        subject: The email subject.
        text_body: The plain-text email body.
        html_body: The HTML email body.
    """
    return send_email(subject, text_body, html_body)
