# Generated by Django 4.2.4 on 2023-08-10 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('annotation', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='static/posts/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='accounts.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
