# Generated by Django 3.2.23 on 2024-01-27 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_recipe_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
    ]