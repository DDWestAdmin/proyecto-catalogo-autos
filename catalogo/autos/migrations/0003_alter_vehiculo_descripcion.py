from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0002_vehiculo_propietario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='descripcion',
            field=models.TextField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name='Descripción',
            ),
        ),
    ]
