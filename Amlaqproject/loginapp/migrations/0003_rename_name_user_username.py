# Generated by Django 4.1 on 2022-10-08 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0002_user_profile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]
