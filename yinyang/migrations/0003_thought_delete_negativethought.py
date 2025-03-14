# Generated by Django 5.0.6 on 2024-07-27 20:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yinyang', '0002_negativethought'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(max_length=250)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(choices=[('WORK', 'Work'), ('PERSONAL', 'Personal'), ('RELATIONSHIP', 'Relationship'), ('STUDIES', 'Studies'), ('MONEY', 'Money'), ('FAMILY', 'Family'), ('HEALTH', 'Health')], default='PERSONAL', max_length=50)),
                ('thought_type', models.CharField(choices=[('NEGATIVE', 'Negative'), ('POSITIVE', 'Positive')], default='NEGATIVE', max_length=50)),
                ('edited', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='NegativeThought',
        ),
    ]
