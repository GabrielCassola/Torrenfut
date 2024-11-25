function filtrar() {
    var input, filter, ul, li, span, i, txtValue, count = 0;

    // Obter valor de pesquisa e os elementos
    input = document.getElementById('inputBusca');
    ul = document.getElementById('listaProdutos');
    filter = input.value.toUpperCase();

    // Pegar todos os <li> dentro do <ul>
    li = ul.getElementsByTagName("li");

    // Se o campo estiver vazio, ocultar todos os itens
    if (filter === "") {
        ul.style.display = "none";
        for (i = 0; i < li.length; i++) {
            li[i].style.display = "none";
        }
        return; // Sai da função se o campo estiver vazio
    }

    // Percorrer os <li> para verificar quais correspondem ao filtro
    for (i = 0; i < li.length; i++) {
        span = li[i].getElementsByClassName("item-text")[0]; // Seleciona o texto do item
        txtValue = span.textContent || span.innerText;

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = ""; // Mostra o item se corresponder
            count++;

            // Destaque em negrito a parte correspondente
            let regex = new RegExp(`(${filter})`, 'gi');
            span.innerHTML = txtValue.replace(regex, "<strong>$1</strong>");
        } else {
            li[i].style.display = "none"; // Esconde o item se não corresponder
        }
    }

    // Exibir ou ocultar a lista dependendo do número de correspondências
    ul.style.display = count === 0 ? "none" : "block";
}