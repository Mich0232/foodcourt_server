# Generated by Django 2.0.7 on 2018-08-03 15:06

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180802_1447'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='mealrecipe',
            managers=[
                ('recipes', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='meal',
            name='meal_id',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='recipes',
        ),
        migrations.AddField(
            model_name='mealrecipe',
            name='meal',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.Meal'),
            preserve_default=False,
        ),
    ]
