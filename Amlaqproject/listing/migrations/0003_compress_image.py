# Generated by Django 4.1 on 2022-09-09 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_basicquestionair_userquestionair_listingquestionair_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='compress_image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='compress/')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compress', to='listing.listing')),
            ],
        ),
    ]
