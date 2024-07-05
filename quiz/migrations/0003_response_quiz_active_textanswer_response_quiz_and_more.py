# Generated by Django 4.1.7 on 2024-07-04 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_delete_ans'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.textquestion')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.response')),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.CreateModel(
            name='McqAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.mcqoption')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.mcq')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.response')),
            ],
        ),
    ]
