from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0006_partnerprofile_must_change_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dgcapplication',
            name='status',
            field=models.CharField(
                choices=[
                    ('new', 'New'),
                    ('review', 'Under Review'),
                    ('approved', 'Approved'),
                    ('paused', 'Paused'),
                    ('cancelled', 'Cancelled'),
                    ('rejected', 'Rejected'),
                ],
                db_index=True,
                default='new',
                max_length=20,
            ),
        ),
    ]
