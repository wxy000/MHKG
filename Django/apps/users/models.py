from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    """
    username：用户名
    email: 电子邮件
    password：密码
    first_name：名
    last_name：姓
    is_active: 是否为活跃用户。默认是True
    is_staff: 是否为员工。默认是False
    is_superuser: 是否为管理员。默认是False
    date_joined: 加入日期。系统自动生成。
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # org = models.CharField('Organization', max_length=128, blank=True)
    image = models.CharField(
        max_length=100, default='/static/images/default.gif', verbose_name='头像')
    gender = models.CharField(
        max_length=6, choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
    phone = models.CharField('Phone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()
