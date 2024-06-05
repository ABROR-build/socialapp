from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# user role
ADMIN = 'admin'
MANAGER = 'manager'
ORDINARY_USER = 'ordinary user'

# registration method
VIA_PHONE = 'via_phone'
VIA_EMAIL = 'via_email'

# steps
NEW = 'new'
CONFIRM = 'confirm'
DONE = 'done'
DONE_IMG_UPLOAD = 'done_img_upload'


class Accounts(AbstractUser):
    USER_ROLE = (
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
        (ORDINARY_USER, ORDINARY_USER)

    )

    file_extension_validator = FileExtensionValidator(
        allowed_extensions=['jpg'],
        message='File extension not allowed. Allowed extensions include  .jpg'
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=26, unique=True)
    user_role = models.CharField(max_length=14, choices=USER_ROLE, default=ORDINARY_USER)
    profile_pictire = models.ImageField(
        validators=[file_extension_validator],
        max_length=255,
        upload_to='images/',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'Accounts'

    def __str__(self):
        return f"{self.username} - {self.user_role}"


class Code(models.Model):
    REGISTRATION_METHOD = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    registration_method = models.CharField(max_length=10, choices=REGISTRATION_METHOD, default=VIA_EMAIL)
    expiry_time = models.DurationField()
    step = models.BooleanField(CONFIRM, default=False)

    if registration_method == VIA_EMAIL:
        expiry_time = datetime.timedelta(minutes=3)
    elif registration_method == VIA_PHONE:
        expiry_time = datetime.timedelta(minutes=2)

    class Meta:
        db_table = 'Code'

    def __str__(self):
        return self.account.name
