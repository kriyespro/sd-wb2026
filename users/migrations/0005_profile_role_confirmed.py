from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_os_hub_abc'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
