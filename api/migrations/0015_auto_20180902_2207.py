# Generated by Django 2.0.7 on 2018-09-02 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20180902_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ID_obj',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Geo'),
        ),
    ]
