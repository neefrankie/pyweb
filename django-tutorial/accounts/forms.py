from django import forms
from enum import StrEnum
from typing import Optional, Dict

from django.core.exceptions import ValidationError


class BtnVariant(StrEnum):
    Primary = 'primary'
    Secondary = 'secondary'
    Success = 'success'
    Danger = 'danger'
    Warning = 'warning'
    Info = 'info'
    Light = 'light'
    Dark = 'dark'
    Link = 'link'
    OutlinePrimary = 'outline-primary'
    OutlineSecondary = 'outline-secondary'
    OutlineSuccess = 'outline-success'
    OutlineDanger = 'outline-danger'
    OutlineWarning = 'outline-warning'
    OutlineInfo = 'outline-info'
    OutlineLight = 'outline-light'
    OutlineDark = 'outline-dark'


class BtnType(StrEnum):
    Submit = 'submit'
    Reset = 'reset'
    Button = 'button'


class BtnSize(StrEnum):
    Large = "lg"
    Small = 'sm'


class Button:

    @classmethod
    def submit(cls, text: str, block=True):
        return cls(
            text,
            type_=BtnType.Submit,
            block=block,
        )

    def __init__(
            self,
            text: str,
            type_=BtnType.Button,
            variant=BtnVariant.Primary,
            block=False,
            size: Optional[BtnSize] = None,
            attrs: Dict[str, str] = None):

        if attrs is None:
            self.attrs = {}

        class_name = ["btn", f"btn-{variant}"]

        if size:
            class_name.append(f"btn-{size}")

        extra_cls = self.attrs.pop("class_name", "")

        if extra_cls:
            class_name.append(extra_cls)

        self.block = block
        self.class_name = " ".join(class_name)
        self.text = text
        self.type = type_
        self.attrs = attrs


class SignUpForm(forms.Form):
    email = forms.EmailField(label="邮箱")
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = Button(
            "注册",
            type_=BtnType.Submit,
            block=True,
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        confirm_password = cleaned_data["confirm_password"]
        if password != confirm_password:
            raise ValidationError("Passwords does not match")


class LoginForm(forms.Form):
    email = forms.EmailField(label="邮箱")
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = Button.submit("登录")


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        help_text="请输入您的电子邮箱，我们会向该邮箱发送邮件，帮您重置密码",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = Button.submit("发送邮件")


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label="确认新密码",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = Button.submit("重置")