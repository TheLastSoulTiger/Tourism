# Generated by Django 5.1.1 on 2024-10-24 11:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='additional_fees',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
