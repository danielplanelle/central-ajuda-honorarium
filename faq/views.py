from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Artigo, Categoria


def inicio(request):
    # Categorias ativas que tenham ao menos 1 artigo publicado,
    # já com a contagem de artigos (uma única consulta).
    categorias = (
        Categoria.objects.filter(ativa=True)
        .annotate(
            total=Count(
                "artigos",
                filter=Q(artigos__status=Artigo.Status.PUBLICADO),
            )
        )
        .filter(total__gt=0)
        .order_by("nome")
    )
    return render(request, "faq/inicio.html", {"categorias": categorias})


def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id, ativa=True)
    artigos = categoria.artigos.filter(
        status=Artigo.Status.PUBLICADO
    ).order_by("pergunta")
    pagina = Paginator(artigos, 10).get_page(request.GET.get("page"))
    return render(
        request,
        "faq/categoria.html",
        {"categoria": categoria, "pagina": pagina},
    )


def artigo(request, artigo_id):
    artigo = get_object_or_404(
        Artigo.objects.select_related("categoria"),
        pk=artigo_id,
        status=Artigo.Status.PUBLICADO,
        categoria__ativa=True,
    )
    relacionados = (
        Artigo.objects.filter(
            categoria=artigo.categoria,
            status=Artigo.Status.PUBLICADO,
        )
        .exclude(pk=artigo.pk)
        .order_by("pergunta")[:5]
    )
    return render(
        request,
        "faq/artigo.html",
        {"artigo": artigo, "relacionados": relacionados},
    )
