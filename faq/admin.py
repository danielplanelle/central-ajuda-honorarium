from django.contrib import admin, messages
from django.utils import timezone

from .models import Artigo, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativa")
    search_fields = ("nome",)
    list_filter = ("ativa",)


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = (
        "pergunta", "categoria", "destaque", "status", "autor", "atualizado_em"
    )
    search_fields = ("pergunta", "resposta", "palavras_chave")
    list_filter = ("status", "destaque", "categoria")
    ordering = ("pergunta",)
    readonly_fields = ("autor",)
    actions = ["publicar_selecionados", "voltar_para_validacao"]

    def save_model(self, request, obj, form, change):
        # Ao criar um artigo novo, grava quem o criou.
        if not change and not obj.autor:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

    def _mudar_status(self, request, queryset, novo_status, texto):
        total = queryset.update(status=novo_status, atualizado_em=timezone.now())
        self.message_user(
            request, f"{total} artigo(s) {texto}.", messages.SUCCESS
        )

    @admin.action(description="Publicar selecionados")
    def publicar_selecionados(self, request, queryset):
        self._mudar_status(request, queryset, Artigo.Status.PUBLICADO, "publicado(s)")

    @admin.action(description="Voltar selecionados para validação")
    def voltar_para_validacao(self, request, queryset):
        self._mudar_status(
            request, queryset, Artigo.Status.EM_VALIDACAO, "devolvido(s) para validação"
        )
