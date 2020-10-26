# Generated by Django 3.1.2 on 2020-10-26 21:33

import accountancy.mixins
import accountancy.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import nominals.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vat', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nominal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='nominals.nominal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NominalHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=20)),
                ('goods', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('due', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('period', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('c', 'cleared'), ('v', 'void')], default='c', max_length=2)),
                ('type', models.CharField(choices=[('nj', 'Journal')], max_length=2)),
                ('vat_type', models.CharField(blank=True, choices=[('i', 'Input'), ('o', 'Output')], max_length=2, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(nominals.models.ModuleTransactionBase, accountancy.models.TransactionBase, models.Model, accountancy.mixins.AuditMixin),
        ),
        migrations.CreateModel(
            name='NominalTransaction',
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
                ('type', models.CharField(choices=[('pp', 'Payment'), ('pr', 'Refund'), ('pi', 'Invoice'), ('pc', 'Credit Note'), ('nj', 'Journal'), ('sp', 'Receipt'), ('sr', 'Refund'), ('si', 'Invoice'), ('sc', 'Credit Note'), ('cp', 'Payment'), ('cr', 'Receipt')], max_length=10)),
                ('value', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nominal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominals.nominal')),
            ],
        ),
        migrations.CreateModel(
            name='NominalLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('goods', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('type', models.CharField(choices=[('nj', 'Journal')], max_length=3)),
                ('goods_nominal_transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nominal_good_line', to='nominals.nominaltransaction')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominals.nominalheader')),
                ('nominal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominals.nominal')),
                ('vat_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vat.vat', verbose_name='Vat Code')),
                ('vat_nominal_transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nominal_vat_line', to='nominals.nominaltransaction')),
                ('vat_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nominal_line_vat_transaction', to='vat.vattransaction')),
            ],
            options={
                'abstract': False,
            },
            bases=(nominals.models.ModuleTransactionBase, accountancy.models.TransactionBase, models.Model, accountancy.mixins.AuditMixin),
        ),
        migrations.CreateModel(
            name='HistoricalNominalLine',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('goods', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('type', models.CharField(choices=[('nj', 'Journal')], max_length=3)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('goods_nominal_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominaltransaction')),
                ('header', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominalheader')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('nominal', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominal')),
                ('vat_code', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vat.vat', verbose_name='Vat Code')),
                ('vat_nominal_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominaltransaction')),
                ('vat_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vat.vattransaction')),
            ],
            options={
                'verbose_name': 'historical nominal line',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalNominalHeader',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ref', models.CharField(max_length=20)),
                ('goods', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('due', accountancy.models.UIDecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('period', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('c', 'cleared'), ('v', 'void')], default='c', max_length=2)),
                ('type', models.CharField(choices=[('nj', 'Journal')], max_length=2)),
                ('vat_type', models.CharField(blank=True, choices=[('i', 'Input'), ('o', 'Output')], max_length=2, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical nominal header',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalNominal',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominal')),
            ],
            options={
                'verbose_name': 'historical nominal',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddConstraint(
            model_name='nominaltransaction',
            constraint=models.UniqueConstraint(fields=('module', 'header', 'line', 'field'), name='nominal_unique_batch'),
        ),
    ]
