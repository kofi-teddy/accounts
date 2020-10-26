# Generated by Django 3.1.2 on 2020-10-26 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('registered', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VatTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=3)),
                ('header', models.PositiveIntegerField()),
                ('line', models.PositiveIntegerField()),
                ('ref', models.CharField(max_length=100)),
                ('period', models.CharField(max_length=6)),
                ('date', models.DateField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('field', models.CharField(choices=[('g', 'Goods'), ('v', 'Vat'), ('t', 'Total')], max_length=2)),
                ('tran_type', models.CharField(choices=[('pp', 'Payment'), ('pr', 'Refund'), ('pi', 'Invoice'), ('pc', 'Credit Note'), ('nj', 'Journal'), ('sp', 'Receipt'), ('sr', 'Refund'), ('si', 'Invoice'), ('sc', 'Credit Note'), ('cp', 'Payment'), ('cr', 'Receipt')], max_length=10)),
                ('vat_type', models.CharField(choices=[('i', 'Input'), ('o', 'Output')], max_length=2)),
                ('vat_rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('goods', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('vat', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('vat_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vat.vat')),
            ],
        ),
        migrations.AddConstraint(
            model_name='vattransaction',
            constraint=models.UniqueConstraint(fields=('module', 'header', 'line', 'field'), name='vat_unique_batch'),
        ),
    ]
