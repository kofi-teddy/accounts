# Generated by Django 3.1.1 on 2020-10-05 15:00

import accountancy.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vat', '__first__'),
        ('cashbook', '0001_initial'),
        ('nominals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=20)),
                ('goods', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('due', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('period', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('c', 'cleared'), ('v', 'void')], default='c', max_length=2)),
                ('type', models.CharField(choices=[('pbi', 'Brought Forward Invoice'), ('pbc', 'Brought Forward Credit Note'), ('pbp', 'Brought Forward Payment'), ('pbr', 'Brought Forward Refund'), ('pp', 'Payment'), ('pr', 'Refund'), ('pi', 'Invoice'), ('pc', 'Credit Note')], max_length=3)),
                ('cash_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashbook.cashbook')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, accountancy.models.Audit),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=(accountancy.models.Audit, models.Model),
        ),
        migrations.CreateModel(
            name='PurchaseMatching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('period', models.CharField(max_length=6)),
                ('matched_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matched_by_these', to='purchases.purchaseheader')),
                ('matched_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matched_to_these', to='purchases.purchaseheader')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, accountancy.models.Audit),
        ),
        migrations.CreateModel(
            name='PurchaseLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('goods', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('goods_nominal_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_good_line', to='nominals.nominaltransaction')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchaseheader')),
                ('nominal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nominals.nominal')),
                ('total_nominal_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_total_line', to='nominals.nominaltransaction')),
                ('vat_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vat.vat', verbose_name='Vat Code')),
                ('vat_nominal_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_vat_line', to='nominals.nominaltransaction')),
            ],
            options={
                'ordering': ['line_no'],
            },
            bases=(models.Model, accountancy.models.Audit),
        ),
        migrations.AddField(
            model_name='purchaseheader',
            name='matched_to',
            field=models.ManyToManyField(through='purchases.PurchaseMatching', to='purchases.PurchaseHeader'),
        ),
        migrations.AddField(
            model_name='purchaseheader',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.supplier'),
        ),
        migrations.CreateModel(
            name='HistoricalSupplier',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical supplier',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPurchaseMatching',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateField(blank=True, editable=False)),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('period', models.CharField(max_length=6)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('matched_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchases.purchaseheader')),
                ('matched_to', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchases.purchaseheader')),
            ],
            options={
                'verbose_name': 'historical purchase matching',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPurchaseLine',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('goods', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('goods_nominal_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominaltransaction')),
                ('header', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchases.purchaseheader')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('nominal', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominal')),
                ('total_nominal_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominaltransaction')),
                ('vat_code', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vat.vat', verbose_name='Vat Code')),
                ('vat_nominal_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='nominals.nominaltransaction')),
            ],
            options={
                'verbose_name': 'historical purchase line',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPurchaseHeader',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ref', models.CharField(max_length=20)),
                ('goods', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('due', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('period', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('c', 'cleared'), ('v', 'void')], default='c', max_length=2)),
                ('type', models.CharField(choices=[('pbi', 'Brought Forward Invoice'), ('pbc', 'Brought Forward Credit Note'), ('pbp', 'Brought Forward Payment'), ('pbr', 'Brought Forward Refund'), ('pp', 'Payment'), ('pr', 'Refund'), ('pi', 'Invoice'), ('pc', 'Credit Note')], max_length=3)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('cash_book', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cashbook.cashbook')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchases.supplier')),
            ],
            options={
                'verbose_name': 'historical purchase header',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
