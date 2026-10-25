from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Artigo(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        EM_VALIDACAO = "em_validacao", "Em validação"
        APROVADO = "aprovado", "Aprovado"
        PUBLICADO = "publicado", "Publicado"

    pergunta = models.CharField(max_length=200, unique=True)
    resposta = models.TextField()
    passo_a_passo = models.TextField(blank=True)
    palavras_chave = models.CharField(max_length=300, blank=True)
    video = models.FileField(
        upload_to="videos/",
        blank=True,
        verbose_name="Vídeo explicativo"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="artigos"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RASCUNHO
    )

    autor = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pergunta