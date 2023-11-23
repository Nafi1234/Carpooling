from django.core.mail import send_mail
from carpool import settings
def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        return True  # Email sent successfully
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False