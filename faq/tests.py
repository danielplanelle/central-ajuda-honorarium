from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Artigo, Categoria

class InicioTests(TestCase):
    def publicar(self, categoria, pergunta="Pergunta?"):
        return Artigo.objects.create(
            categoria=categoria, pergunta=pergunta, resposta="Resposta.",
            status=Artigo.Status.PUBLICADO,
        )

    def test_mostra_categoria_com_artigo_publicado_e_a_contagem(self):
        cat = Categoria.objects.create(nome="Checklist")
        self.publicar(cat, "Pergunta 1?")
        self.publicar(cat, "Pergunta 2?")
        resposta = self.client.get(reverse("inicio"))
        self.assertContains(resposta, "Checklist")
        self.assertContains(resposta, "2 artigos")
        self.assertContains(resposta, reverse("categoria", args=[cat.id]))
        self.assertContains(resposta, "logo-simbolo.png")

    def test_esconde_categoria_sem_artigo_publicado(self):
        cat = Categoria.objects.create(nome="Só rascunho")
        Artigo.objects.create(categoria=cat, pergunta="Rascunho?", resposta="x")
        resposta = self.client.get(reverse("inicio"))
        self.assertNotContains(resposta, "Só rascunho")

    def test_categoria_inativa_nao_aparece(self):
        cat = Categoria.objects.create(nome="Categoria escondida", ativa=False)
        self.publicar(cat)
        resposta = self.client.get(reverse("inicio"))
        self.assertNotContains(resposta, "Categoria escondida")

    def test_home_usa_uma_unica_consulta(self):
        for i in range(5):
            self.publicar(Categoria.objects.create(nome=f"Cat {i}"), f"P{i}?")
        with self.assertNumQueries(1):
            self.client.get(reverse("inicio"))


class CategoriaTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Checklist", descricao="Ajuda com o checklist."
        )

    def criar_artigo(self, pergunta, status=Artigo.Status.PUBLICADO):
        return Artigo.objects.create(
            categoria=self.categoria,
            pergunta=pergunta,
            resposta="Resposta.",
            status=status,
        )

    def test_lista_artigos_publicados_e_descricao_da_categoria(self):
        self.criar_artigo("Pergunta publicada?")
        self.criar_artigo("Pergunta em rascunho?", Artigo.Status.RASCUNHO)

        resposta = self.client.get(reverse("categoria", args=[self.categoria.id]))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ajuda com o checklist.")
        self.assertContains(resposta, "Pergunta publicada?")
        self.assertNotContains(resposta, "Pergunta em rascunho?")

    def test_categoria_inativa_ou_inexistente_retorna_404(self):
        self.categoria.ativa = False
        self.categoria.save()
        resposta_inativa = self.client.get(
            reverse("categoria", args=[self.categoria.id])
        )
        resposta_inexistente = self.client.get(reverse("categoria", args=[9999]))

        self.assertEqual(resposta_inativa.status_code, 404)
        self.assertEqual(resposta_inexistente.status_code, 404)

    def test_pagina_exibe_dez_artigos_e_link_para_proxima(self):
        for numero in range(11):
            self.criar_artigo(f"Pergunta {numero:02}?")

        primeira_pagina = self.client.get(
            reverse("categoria", args=[self.categoria.id])
        )
        segunda_pagina = self.client.get(
            reverse("categoria", args=[self.categoria.id]), {"page": 2}
        )

        self.assertEqual(len(primeira_pagina.context["pagina"].object_list), 10)
        self.assertContains(primeira_pagina, "Próxima")
        self.assertEqual(len(segunda_pagina.context["pagina"].object_list), 1)
        self.assertContains(segunda_pagina, "Anterior")

class CarregarArtigosTests(TestCase):
    def executar(self, *args):
        call_command("carregar_artigos", *args, stdout=StringIO())

    def test_carrega_16_artigos_e_nao_duplica(self):
        self.executar("--publicar")
        self.assertEqual(Artigo.objects.count(), 16)
        self.executar("--publicar")
        self.assertEqual(Artigo.objects.count(), 16)

    def test_sem_a_opcao_publicar_nada_vai_para_o_cliente(self):
        self.executar()
        self.assertFalse(
            Artigo.objects.filter(status=Artigo.Status.PUBLICADO).exists()
        )

    def test_nao_sobrescreve_correcao_feita_pela_equipe(self):
        self.executar()
        artigo = Artigo.objects.first()
        artigo.resposta = "Resposta corrigida pela equipe."
        artigo.save()
        self.executar()
        artigo.refresh_from_db()
        self.assertEqual(artigo.resposta, "Resposta corrigida pela equipe.")
class AdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "senha123")
        self.client.force_login(self.admin)
        self.categoria = Categoria.objects.create(nome="Acesso")

    def test_acao_publicar_selecionados(self):
        artigo = Artigo.objects.create(
            categoria=self.categoria, pergunta="Pergunta?", resposta="Resposta.",
            status=Artigo.Status.EM_VALIDACAO,
        )
        self.client.post(
            reverse("admin:faq_artigo_changelist"),
            {"action": "publicar_selecionados", "_selected_action": [artigo.pk]},
        )
        artigo.refresh_from_db()
        self.assertEqual(artigo.status, Artigo.Status.PUBLICADO)

    def test_autor_e_preenchido_ao_criar_pelo_admin(self):
        self.client.post(
            reverse("admin:faq_artigo_add"),
            {
                "categoria": self.categoria.pk,
                "pergunta": "Nova pergunta?",
                "resposta": "Nova resposta.",
                "passo_a_passo": "",
                "palavras_chave": "",
                "status": Artigo.Status.RASCUNHO,
            },
        )
        artigo = Artigo.objects.get(pergunta="Nova pergunta?")
        self.assertEqual(artigo.autor, self.admin)
