from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('claims', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HumanReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[('APPROVE', 'Approve'), ('REJECT', 'Reject'), ('REQUEST_MORE_DOCUMENTS', 'Request More Documents'), ('PARTIALLY_APPROVE', 'Partially Approve')], max_length=40)),
                ('approved_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('comment', models.TextField()),
                ('reviewed_at', models.DateTimeField(auto_now_add=True)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='human_reviews', to='claims.claim')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-reviewed_at'],
            },
        ),
    ]
