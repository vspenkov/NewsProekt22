# Generated by Django 4.0 on 2022-01-19 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0003_alter_post_author_alter_post_data_create_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscriber',
            field=models.ManyToManyField(through='news.CategoryUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoryuser',
            name='category_through',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category'),
        ),
        migrations.AddField(
            model_name='categoryuser',
            name='user_through',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
