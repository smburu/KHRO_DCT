# Generated by Django 2.1.2 on 2020-10-13 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0013_auto_20201013_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgresearchproposal',
            name='erc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.StgEthicsCommittee', verbose_name='Ethics Reseach Entity'),
        ),
    ]