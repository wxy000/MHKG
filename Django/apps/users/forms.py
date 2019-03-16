from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-_a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class': "layui-input admin-input admin-input-username",
                                   'autocomplete': "off",
                                   'placeholder': u'请输入用户名'}), )
    email = forms.EmailField(label='邮箱',
                             widget=forms.TextInput(attrs={
                                 'class': "layui-input admin-input",
                                 'autocomplete': "off",
                                 'placeholder': u'请输入邮箱'}), )
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(attrs={
                                    'class': "layui-input admin-input",
                                    'autocomplete': "off",
                                    'placeholder': u'请输入密码'}), )
    password2 = forms.CharField(label='再次输入密码',
                                widget=forms.PasswordInput(attrs={
                                    'class': "layui-input admin-input admin-input-verify",
                                    'autocomplete': "off",
                                    'placeholder': u'请再次输入密码'}), )

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise forms.ValidationError("长度不得小于3！")
        elif len(username) > 50:
            raise forms.ValidationError("长度不得大于50！")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在！")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("该邮箱已被注册！")
        else:
            raise forms.ValidationError("请输入有效的邮箱！")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码不得小于6位！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码不得大于20位！")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码验证不通过，请重新输入！")

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class': "layui-input admin-input admin-input-username",
                                   'autocomplete': "off",
                                   'placeholder': u'请输入用户名或邮箱'}), )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': "layui-input admin-input",
                                   'autocomplete': "off",
                                   'placeholder': u'请输入密码'}), )

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("该邮箱未注册！")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("用户名不存在！")

        return username


class UserinfoForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, required=False,
                               widget=forms.TextInput(attrs={
                                   'class': "layui-input",
                                   'readonly': "readonly"}), )
    gender = forms.CharField(max_length=6, required=False,
                             widget=forms.Select(
                                 choices=(('male', u'男'), ('female', u'女')),
                                 attrs={
                                     'class': "layui-input-block"
                                 }))
    image = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput(attrs={
                                'lay-verify': "required",
                                'id': "LAY_avatarSrc",
                                'placeholder': "图片地址",
                                'class': "layui-input",
                                'readonly': "readonly"
                            }))
    phone = forms.CharField(label='手机', max_length=50, required=False,
                            widget=forms.TextInput(attrs={
                                'class': "layui-input",
                                'autocomplete': "off"}), )
    email = forms.EmailField(label='邮箱', required=False,
                             widget=forms.TextInput(attrs={
                                 'class': "layui-input",
                                 'autocomplete': "off"}), )


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old password',
                                   widget=forms.PasswordInput(attrs={
                                       'lay-verify': "required",
                                       'class': "layui-input"
                                   }))

    password1 = forms.CharField(label='New Password',
                                widget=forms.PasswordInput(attrs={
                                    'lay-verify': "pass",
                                    'autocomplete': "off",
                                    'class': "layui-input"
                                }))
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput(attrs={
                                    'lay-verify': "repass",
                                    'autocomplete': "off",
                                    'class': "layui-input"
                                }))

    # Use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码不得小于6位！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码不得大于20位！")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')

        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码验证未通过，请重试！")

        return password2
