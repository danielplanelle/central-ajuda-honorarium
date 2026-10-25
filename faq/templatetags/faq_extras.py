from django import template

register = template.Library()


@register.filter
def separar_etapas(texto):
    """
    Separa o passo a passo em etapas individuais.
    Aceita números como 1., 2. ou 1), 2).
    """
    if not texto:
        return []

    etapas = []

    for linha in texto.splitlines():
        linha = linha.strip()

        if not linha:
            continue

        # Remove a numeração que já existe no texto.
        import re
        linha = re.sub(r"^\d+[\.\)]\s*", "", linha)

        etapas.append(linha)

    return etapas