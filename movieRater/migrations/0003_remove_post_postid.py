# Generated by Django 4.2.7 on 2023-11-20 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movieRater', '0002_post_date_created_post_postmovieid_post_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='postId',
        ),
    ]
