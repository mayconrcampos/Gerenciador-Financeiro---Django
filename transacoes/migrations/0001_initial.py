# Generated by Django 4.2.3 on 2023-07-11 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_rename_senha_usuario_senha_cripto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=32, verbose_name='Categoria')),
                ('tipo', models.IntegerField(choices=[(1, 'Entrada'), (2, 'Saída')], verbose_name='Tipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='usuarios.usuario')),
            ],
            options={
                'verbose_name': 'Categoria',
            },
        ),
    ]
