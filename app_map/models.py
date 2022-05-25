from django.db import models
import uuid # Requerida para las instancias de placas unicas

# Create your models here.
class placa(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    #name = models.CharField(max_length=6, help_text="Ingrese el codigo de la placa")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID de la placa")

    imprint = models.CharField(max_length=6)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s' % (self.id)