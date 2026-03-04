"""
Seed the database with 20+ realistic pre-classified traces
covering all five categories.
"""

import uuid
from datetime import datetime, timedelta, timezone

from models import CategoryEnum, Trace
from sqlalchemy.orm import Session

SEED_TRACES = [
    # === Billing (5) ===
    {
        "user_message": "Hi, I was charged $49.99 but my plan is the $29.99 one. Can you explain the difference?",
        "bot_response": "I'd be happy to look into that for you. It appears the $49.99 charge includes a pro-rated upgrade fee from when your plan was changed on the 15th. I can send you a detailed invoice breakdown if you'd like.",
        "category": CategoryEnum.BILLING,
        "response_time_ms": 845,
    },
    {
        "user_message": "What payment methods do you accept? Can I pay with PayPal?",
        "bot_response": "We currently accept Visa, Mastercard, American Express, and bank transfers. Unfortunately, PayPal is not supported at this time, but we're working on adding it soon.",
        "category": CategoryEnum.BILLING,
        "response_time_ms": 623,
    },
    {
        "user_message": "I need a copy of my invoice from January for tax purposes.",
        "bot_response": "Of course! You can download all past invoices from your Account Settings under the Billing tab. If you need me to email a specific invoice, please share your account email and I'll send it right over.",
        "category": CategoryEnum.BILLING,
        "response_time_ms": 712,
    },
    {
        "user_message": "When is my next billing date? I want to make sure I have funds available.",
        "bot_response": "Your next billing date is March 15th. You'll be charged $29.99 for the Standard plan. We also send a reminder email 3 days before each billing cycle.",
        "category": CategoryEnum.BILLING,
        "response_time_ms": 534,
    },
    {
        "user_message": "Can I switch from monthly to annual billing? Is there a discount?",
        "bot_response": "Yes! Switching to annual billing saves you 20%, bringing your yearly total to $287.90 instead of $359.88. I can make that change for you right now if you'd like.",
        "category": CategoryEnum.BILLING,
        "response_time_ms": 678,
    },
    # === Refund (4) ===
    {
        "user_message": "I was double-charged this month. I need a refund for the extra payment.",
        "bot_response": "I'm sorry about the double charge. I can see the duplicate transaction in our system. I've initiated a refund of $29.99 which should appear in your account within 5-7 business days.",
        "category": CategoryEnum.REFUND,
        "response_time_ms": 921,
    },
    {
        "user_message": "I signed up by accident and was charged immediately. Can I get my money back?",
        "bot_response": "I understand. Since you signed up within the last 24 hours, you're eligible for a full refund under our satisfaction guarantee. I'll process the refund now and you should see it reflected within 3-5 business days.",
        "category": CategoryEnum.REFUND,
        "response_time_ms": 1102,
    },
    {
        "user_message": "The premium features don't work as advertised. I want a refund for this month.",
        "bot_response": "I'm sorry to hear the premium features haven't met your expectations. I'd like to understand which features aren't working so we can fix them. In the meantime, I've submitted a refund request for your current billing period.",
        "category": CategoryEnum.REFUND,
        "response_time_ms": 887,
    },
    {
        "user_message": "I cancelled my subscription last week but was still charged. Please refund me.",
        "bot_response": "I apologize for the inconvenience. I can confirm your cancellation was processed, and the charge was an error. I've issued a full refund of $29.99 to your card on file. You should see it within 5-7 business days.",
        "category": CategoryEnum.REFUND,
        "response_time_ms": 756,
    },
    # === Account Access (4) ===
    {
        "user_message": "I can't log in. It says my password is wrong but I'm sure it's correct.",
        "bot_response": "I'm sorry you're having trouble logging in. Let's try resetting your password — I've sent a password reset link to the email address associated with your account. Please check your inbox and spam folder.",
        "category": CategoryEnum.ACCOUNT_ACCESS,
        "response_time_ms": 645,
    },
    {
        "user_message": "My account is locked after too many login attempts. How do I unlock it?",
        "bot_response": "Your account is temporarily locked for security purposes. It will automatically unlock after 30 minutes. Alternatively, you can reset your password using the 'Forgot Password' link, which will unlock your account immediately.",
        "category": CategoryEnum.ACCOUNT_ACCESS,
        "response_time_ms": 589,
    },
    {
        "user_message": "I lost my phone and can't receive the MFA code. How do I get into my account?",
        "bot_response": "I understand how frustrating that must be. For security, I'll need to verify your identity. Could you please provide the email on your account and answer your security question? Once verified, I can temporarily disable MFA so you can log in.",
        "category": CategoryEnum.ACCOUNT_ACCESS,
        "response_time_ms": 934,
    },
    {
        "user_message": "I never received the verification email when I signed up. Can you resend it?",
        "bot_response": "I've resent the verification email to your address. Please check your spam or junk folder as well. If you still don't receive it within 5 minutes, let me know and we can try an alternative verification method.",
        "category": CategoryEnum.ACCOUNT_ACCESS,
        "response_time_ms": 512,
    },
    # === Cancellation (4) ===
    {
        "user_message": "I want to cancel my subscription. I'm not using the platform anymore.",
        "bot_response": "I'm sorry to see you go. I can process your cancellation right away. Your subscription will remain active until the end of your current billing period on March 15th. Would you like me to proceed?",
        "category": CategoryEnum.CANCELLATION,
        "response_time_ms": 723,
    },
    {
        "user_message": "Can I downgrade from the Pro plan to the Basic plan instead of cancelling entirely?",
        "bot_response": "Absolutely! Downgrading to the Basic plan is a great option. Your new rate would be $9.99/month, and the change will take effect at the start of your next billing cycle. Shall I make the switch?",
        "category": CategoryEnum.CANCELLATION,
        "response_time_ms": 667,
    },
    {
        "user_message": "Please close my account completely. I want all my data deleted.",
        "bot_response": "I understand. I can initiate an account closure and data deletion request. Please note this action is irreversible — all your data will be permanently deleted within 30 days. Would you like to proceed?",
        "category": CategoryEnum.CANCELLATION,
        "response_time_ms": 812,
    },
    {
        "user_message": "I'm switching to a competitor. Cancel my plan effective immediately.",
        "bot_response": "I'm sorry to hear that. I've processed your cancellation effective immediately. You'll receive a confirmation email shortly. If you ever decide to come back, your account can be reactivated within 90 days.",
        "category": CategoryEnum.CANCELLATION,
        "response_time_ms": 698,
    },
    # === General Inquiry (5) ===
    {
        "user_message": "What features are included in the Pro plan?",
        "bot_response": "The Pro plan includes unlimited projects, advanced analytics, priority support, custom integrations, and team collaboration tools for up to 25 members. You can view the full feature comparison on our pricing page.",
        "category": CategoryEnum.GENERAL_INQUIRY,
        "response_time_ms": 543,
    },
    {
        "user_message": "Do you have an API I can use to integrate with my existing tools?",
        "bot_response": "Yes! We offer a RESTful API available on all paid plans. You can find the documentation at docs.billease.com/api. The API supports user management, billing operations, and webhook notifications.",
        "category": CategoryEnum.GENERAL_INQUIRY,
        "response_time_ms": 478,
    },
    {
        "user_message": "Is there a mobile app available for iOS?",
        "bot_response": "We currently offer a web-based platform optimized for mobile browsers. A native iOS app is on our roadmap and expected to launch in Q3. I can add you to the notification list if you'd like to be informed when it's available.",
        "category": CategoryEnum.GENERAL_INQUIRY,
        "response_time_ms": 612,
    },
    {
        "user_message": "How long have you been in business? I want to make sure you're a reliable provider.",
        "bot_response": "BillEase has been serving customers since 2019 and currently supports over 10,000 businesses worldwide. We maintain 99.9% uptime and are SOC 2 Type II certified. Happy to answer any other questions!",
        "category": CategoryEnum.GENERAL_INQUIRY,
        "response_time_ms": 567,
    },
    {
        "user_message": "Can I export my data to CSV? I need it for a report.",
        "bot_response": "Yes, you can export your data in CSV, JSON, or PDF format. Go to Settings > Data Export and select the date range and data types you'd like to include. The export will be emailed to you within a few minutes.",
        "category": CategoryEnum.GENERAL_INQUIRY,
        "response_time_ms": 489,
    },
]


def seed_database(db: Session):
    """Insert seed traces into the database."""
    base_time = datetime.now(timezone.utc) - timedelta(hours=48)

    for i, data in enumerate(SEED_TRACES):
        trace = Trace(
            id=str(uuid.uuid4()),
            user_message=data["user_message"],
            bot_response=data["bot_response"],
            category=data["category"],
            timestamp=base_time + timedelta(minutes=i * 15),
            response_time_ms=data["response_time_ms"],
        )
        db.add(trace)

    db.commit()
    print(f"Seeded {len(SEED_TRACES)} traces into the database.")
