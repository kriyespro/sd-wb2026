from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0005_dgc_kyc_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerprofile',
            name='must_change_password',
            field=models.BooleanField(default=False),
        ),
    ]
