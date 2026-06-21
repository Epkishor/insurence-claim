from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('policies', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('insurance_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=255)),
                ('treatment_type', models.CharField(max_length=255)),
                ('admission_date', models.DateField()),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('claimed_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('approved_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('status', models.CharField(choices=[('PENDING_DOCUMENTS', 'Pending Documents'), ('DOCUMENTS_UPLOADED', 'Documents Uploaded'), ('PROCESSING', 'Processing'), ('UNDER_REVIEW', 'Under Review'), ('APPROVED', 'Approved'), ('PARTIALLY_APPROVED', 'Partially Approved'), ('REJECTED', 'Rejected'), ('MORE_DOCUMENTS_REQUIRED', 'More Documents Required')], default='PENDING_DOCUMENTS', max_length=40)),
                ('fraud_score', models.FloatField(blank=True, null=True)),
                ('decision_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claims.patient')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policies.insurancepolicy')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
