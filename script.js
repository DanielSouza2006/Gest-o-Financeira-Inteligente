let card=document.querySelector('.card');
let loginButton=document.querySelector('.loginButton');
let cadastroButton=document.querySelector('.cadastroButton');

loginButton.onclick =()=>{
    card.classList.remove('cadastroActive');
    card.classList.add('loginActive');
}

cadastroButton.onclick =()=>{
    card.classList.remove('loginActive');
    card.classList.add('cadastroActive');
}


function fazerLogin() {
    // 1. Pegamos os valores que o usuário digitou
    const user = document.getElementById('usuario').value;
    const pass = document.getElementById('senha').value;

    // 2. Criamos o "pacote" (objeto)
    const dados = { "usuario": user, "senha": pass };

    // 3. Enviamos para o endereço do nosso servidor Python
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST', // Estamos "postando" (enviando) algo
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados) // Transforma o objeto em texto para a viagem
    })
    .then(resposta => resposta.json()) // Espera a resposta do Python
    .then(resultado => {
        alert(resultado.mensagem); // Mostra na tela: "Sucesso" ou "Erro"
    });
}