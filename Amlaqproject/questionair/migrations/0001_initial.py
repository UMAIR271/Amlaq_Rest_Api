# Generated by Django 4.1 on 2022-10-03 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0006_alter_listing_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('question_type', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='questionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=300)),
                ('save_in_future', models.BooleanField(default=False, null=True)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.listing')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionair.question')),
            ],
        ),
    ]
