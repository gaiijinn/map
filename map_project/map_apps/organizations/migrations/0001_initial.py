# Generated by Django 3.2.16 on 2024-07-01 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationImgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='org/')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_type', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn'), ('instagram', 'Instagram'), ('website', 'Website'), ('other', 'Other')], default='other', max_length=20)),
                ('link', models.URLField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='OrgTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('about_us', models.CharField(blank=True, max_length=512, null=True)),
                ('org_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.orgtypes')),
            ],
        ),
    ]
