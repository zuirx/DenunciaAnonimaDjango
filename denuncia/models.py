from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File

class Denuncia(models.Model):
    titulo = models.CharField(max_length=70, blank=True, null=True)
    descricao = models.CharField(max_length=150, blank=True, null=True)
    local = models.CharField(max_length=60, blank=True, null=True)
    data = models.DateField(auto_now_add=True)
    fotos = models.FileField(upload_to='fotos/', blank=True, null=True)
    user_ip = models.CharField(max_length=24, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.fotos:
            img = Image.open(self.fotos)
            img = img.resize((512, 512))
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)
            self.fotos = File(img_io, name=self.fotos.name)

        super().save(*args, **kwargs)