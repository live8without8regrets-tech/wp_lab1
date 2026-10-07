import uuid

from django.db import migrations, models


def fill_uuids(apps, schema_editor):
    """
    Заполняет поле uuid уникальными значениями
    для всех существующих записей.
    """
    Author = apps.get_model('library', 'Author')
    Genre = apps.get_model('library', 'Genre')
    Book = apps.get_model('library', 'Book')

    for obj in Author.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])

    for obj in Genre.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])

    for obj in Book.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        # Шаг 1: добавляем поле uuid, пока без unique и с null=True
        migrations.AddField(
            model_name='author',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),

        # Шаг 2: заполняем уникальными значениями все существующие записи
        migrations.RunPython(fill_uuids, migrations.RunPython.noop),

        # Шаг 3: теперь поле можно сделать уникальным и обязательным
        migrations.AlterField(
            model_name='author',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='genre',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]