# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_alter_application_university'),
    ]

    operations = [
        # Rename address_line1 to address
        migrations.RenameField(
            model_name='application',
            old_name='address_line1',
            new_name='address',
        ),
        # Remove address_line2
        migrations.RemoveField(
            model_name='application',
            name='address_line2',
        ),
        # Remove state
        migrations.RemoveField(
            model_name='application',
            name='state',
        ),
        # Remove country
        migrations.RemoveField(
            model_name='application',
            name='country',
        ),
        # Remove age field (now a property)
        migrations.RemoveField(
            model_name='application',
            name='age',
        ),
        # Add email field
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(max_length=255, default=''),
            preserve_default=False,
        ),
        # Update nationality with default
        migrations.AlterField(
            model_name='application',
            name='nationality',
            field=models.CharField(default='Tanzanian', max_length=100),
        ),
    ]






