# Generated by Django 4.0.5 on 2022-08-13 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_message_text_topic_text_topic_title_user_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='moderator',
            field=models.BooleanField(default=False),
        ),
    ]