from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_proof", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="reviewed_on",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="source",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="review",
            name="source_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="flag",
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
