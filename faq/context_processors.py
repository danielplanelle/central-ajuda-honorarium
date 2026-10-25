from .models import Categoria


def categorias_navegacao(request):
    return {
        "categorias_navegacao": Categoria.objects.filter(ativa=True).order_by("nome")
    }
