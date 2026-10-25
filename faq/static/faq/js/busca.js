(function () {
    const campo = document.getElementById("search-input");
    const artigos = document.querySelectorAll(".article-card");
    const blocos = document.querySelectorAll(".faq-category");
    const semResultados = document.getElementById("sem-resultados");

    if (!campo) return;

    // Tira acentos e maiúsculas: "Ação" vira "acao".
    function normalizar(texto) {
        return texto
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .trim();
    }

    function filtrar() {
        const termos = normalizar(campo.value).split(/\s+/).filter(Boolean);
        let total = 0;

        artigos.forEach(function (artigo) {
            const texto = normalizar(artigo.dataset.busca || "");
            // O artigo aparece se contiver TODAS as palavras digitadas.
            const combina = termos.every(function (t) {
                return texto.includes(t);
            });
            artigo.hidden = !combina;
            if (combina) total++;
        });

        // Esconde o título da categoria se nenhum artigo dela combinou.
        blocos.forEach(function (bloco) {
            const temVisivel = bloco.querySelector(".article-card:not([hidden])");
            bloco.hidden = termos.length > 0 && !temVisivel;
        });

        semResultados.hidden = termos.length === 0 || total > 0;
    }

    campo.addEventListener("input", filtrar);
})();