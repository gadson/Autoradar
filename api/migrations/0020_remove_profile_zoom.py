# Generated by Django 2.0.7 on 2018-09-16 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_profile_select'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='zoom',
        ),
    ]
