from datetime import datetime, timedelta
import binascii
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.core.signing import (
    TimestampSigner,
    b64_encode,
    b64_decode,
    SignatureExpired,
    BadSignature,
)
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from shop import settings


class UserRegistrationMixin:
    """Миксин с функционалом для регистрации пользователя"""

    EMAIL_FIELD = 'email'

    def get_email(self):
        return getattr(self, self.EMAIL_FIELD)

    def get_verification_code(self):
        signer = TimestampSigner()
        signature = signer.sign(self.get_email())
        return b64_encode(signature.encode('utf-8')).decode('utf-8')

    def send_verification_mail(self):
        verification_code = self.get_verification_code()
        context = {
            'user': self,
            'settings': settings,
            'code': verification_code,
            'link_valid_until': datetime.today() + timedelta(days=settings.VERIFICATION_CODE_EXPIRED),
        }

        msg = EmailMessage(
            subject=render_to_string('auth/mail/verification_subject.txt', context),
            body=render_to_string('auth/mail/verification_body.html', context),
            to=[self.get_email()],
        )
        msg.content_subtype = 'html'
        msg.send()

    @classmethod
    def verify_by_code(cls, code):
        if code:
            UserModel = get_user_model()
            signer = TimestampSigner()
            try:
                max_age = timedelta(days=settings.VERIFICATION_CODE_EXPIRED).total_seconds()
                signature = b64_decode(force_bytes(code)).decode('utf-8')
                username = signer.unsign(signature, max_age=max_age)
                user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username, 'is_active': False})
                user.is_active = True
                user.save()
                return True, 'Ваша учетная запись успешно активирована.'
            except SignatureExpired:
                return False, 'Ваша ссылка устарела.'
            except (
                BadSignature,
                UserModel.DoesNotExist,
                TypeError,
                UnicodeDecodeError,
                binascii.Error,
            ):
                pass
        return False, 'Неверная ссылка активации.'
