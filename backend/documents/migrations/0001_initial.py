from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('INSURANCE_CARD', 'Insurance Card'), ('CITIZENSHIP', 'Citizenship / ID'), ('MEDICAL_REPORT', 'Medical Report'), ('PRESCRIPTION', 'Prescription'), ('HOSPITAL_BILL', 'Hospital Bill'), ('DISCHARGE_SUMMARY', 'Discharge Summary'), ('LAB_REPORT', 'Lab Report'), ('OTHER', 'Other')], max_length=50)),
                ('file', models.FileField(upload_to='claim_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='claims.claim')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='OCRResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extracted_text', models.TextField()),
                ('confidence_score', models.FloatField(blank=True, null=True)),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_result', to='documents.claimdocument')),
            ],
            options={
                'ordering': ['-processed_at'],
            },
        ),
    ]
