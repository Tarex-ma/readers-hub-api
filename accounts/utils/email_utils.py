from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import jwt
from datetime import datetime, timedelta

def generate_verification_token(user):
    """Generate JWT token for email verification"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'type': 'email_verification'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def send_verification_email(user):
    """Send email verification link"""
    token = generate_verification_token(user)
    verification_url = f"{settings.FRONTEND_URL}/verify-email/?token={token}"
    
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'Reader\'s Hub'
    }
    
    html_message = render_to_string('emails/verify_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='Verify your email - Reader\'s Hub',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_welcome_email(user):
    """Send welcome email with book recommendations"""
    context = {
        'user': user,
        'site_name': 'Reader\'s Hub',
        'login_url': f"{settings.FRONTEND_URL}/login"
    }
    
    html_message = render_to_string('emails/welcome_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='Welcome to Reader\'s Hub!',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_password_reset_email(user, token):
    """Send password reset link"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
    
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'Reader\'s Hub'
    }
    
    html_message = render_to_string('emails/password_reset.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='Reset your password - Reader\'s Hub',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_follow_notification(follower, followed):
    """Notify user when someone follows them"""
    context = {
        'follower': follower,
        'followed': followed,
        'profile_url': f"{settings.FRONTEND_URL}/users/{follower.id}",
        'site_name': 'Reader\'s Hub'
    }
    
    html_message = render_to_string('emails/follow_notification.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=f"{follower.username} started following you!",
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[followed.email],
        html_message=html_message,
        fail_silently=False,
    )