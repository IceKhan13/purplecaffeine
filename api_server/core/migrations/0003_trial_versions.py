"""Add versions migration."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration"""

    dependencies = [
        ("core", "0002_trial_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="trial",
            name="versions",
            field=models.JSONField(default=list),
        ),
    ]
