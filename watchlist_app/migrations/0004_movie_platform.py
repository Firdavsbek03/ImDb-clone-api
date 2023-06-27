# Generated by Django 4.2 on 2023-06-17 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0003_streamplatform_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='watchlist_app.streamplatform'),
        ),
    ]