from django.core.management.base import BaseCommand

from faq.dados_iniciais import ARTIGOS, CATEGORIAS
from faq.models import Artigo, Categoria


class Command(BaseCommand):
    help = "Carrega os artigos iniciais da Central de Ajuda (não duplica nem sobrescreve)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--publicar",
            action="store_true",
            help="Cria os artigos já como Publicado (o padrão é Em validação).",
        )

    def handle(self, *args, **opcoes):
        status = (
            Artigo.Status.PUBLICADO if opcoes["publicar"]
            else Artigo.Status.EM_VALIDACAO
        )

        for nome, descricao in CATEGORIAS.items():
            Categoria.objects.get_or_create(
                nome=nome, defaults={"descricao": descricao}
            )

        criados = 0
        existentes = 0

        for dados_artigo in ARTIGOS:
            categoria, pergunta, resposta, passos, chaves = dados_artigo[:5]
            video = dados_artigo[5] if len(dados_artigo) > 5 else ""
            passo_a_passo = "\n".join(
                f"{i}. {texto}" for i, texto in enumerate(passos, start=1)
            )
            _, criado = Artigo.objects.get_or_create(
                pergunta=pergunta,
                defaults={
                    "categoria": Categoria.objects.get(nome=categoria),
                    "resposta": resposta,
                    "passo_a_passo": passo_a_passo,
                    "palavras_chave": chaves,
                    "video": video,
                    "status": status,
                },
            )
            if criado:
                criados += 1
            else:
                existentes += 1

        self.stdout.write(self.style.SUCCESS(
            f"{criados} artigo(s) criado(s), {existentes} já existia(m)."
        ))
