# Generated by Django 4.2.7 on 2023-12-01 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('username', models.CharField(blank=True, max_length=150, unique=True, verbose_name='имя пользователя')),
                ('name', models.CharField(default='', max_length=150, verbose_name='имя')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='номер телефона')),
                ('telegram_id', models.CharField(max_length=250, verbose_name='телеграм id')),
                ('payment_verification', models.BooleanField(default=False, verbose_name='подтверждение оплаты')),
                ('is_employee', models.BooleanField(default=False, verbose_name='работник')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='персонал')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='админ')),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'unique_together': {('phone',)},
            },
        ),
    ]
