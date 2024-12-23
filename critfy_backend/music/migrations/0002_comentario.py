# Generated by Django 5.1.3 on 2024-11-29 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('avaliacao', models.IntegerField(choices=[(1, '1 estrela'), (2, '2 estrelas'), (3, '3 estrelas'), (4, '4 estrelas'), (5, '5 estrelas')], default=5)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='music.album')),
            ],
        ),
    ]
