from django.db import models
from stdimage.models import StdImageField
import uuid
from hashlib import sha256
from django import forms

# Create your models here.
class Base(models.Model):
    criado = models.DateTimeField("Criação", auto_now_add=True)
    modificado = models.DateTimeField("Modificado", auto_now=True)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        abstract = True


# Nomeando arquivos para fazer upload ao DB com nome unico
def get_file_path(_instance, filename: str):
    extensao = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extensao}"
    return filename

class Usuario(Base):
    nome = models.CharField("Nome", max_length=128, blank=False)
    email = models.EmailField("Email", unique=True, blank=False)
    senha_cripto = models.CharField("Senha", max_length=64, blank=False)
    imagem = StdImageField("Imagem", upload_to=get_file_path, delete_orphans=True ,variations={"thumb": {"width": 480, "height": 480, "crop": True}})
    facebook = models.CharField("Facebook", max_length=128, default="#")
    twitter = models.CharField("Twitter", max_length=128, default="#")
    instagram = models.CharField("Instagram", max_length=128, default="#")
    linkedin = models.CharField("Linkedin", max_length=128, default="#")

    @property
    def senha(self):
        return self.senha_cripto

    @senha.setter
    def senha(self, senha):
        self.senha_cripto = sha256(senha.encode()).hexdigest()

    class Meta:
        verbose_name = "Usuario"

    def __str__(self):
        return self.nome