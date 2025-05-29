document.addEventListener("DOMContentLoaded", function () {
    const text = "Bem Vindo Ao Sistema ";
    const typingElement = document.getElementById("typing");
    const buttons = document.querySelectorAll('.copy-button');
    
    let index = 0;
    typingElement.innerHTML = "";
    
    // efeito de digitação
    function typeEffect() {
      if (index < text.length) {
        typingElement.innerHTML += text.charAt(index);
        index++;
        setTimeout(typeEffect, 250); // Velocidade de digitação
      } 
    }
    typeEffect();

    // botão copiar codigo
    buttons.forEach(button => {
      button.addEventListener('click', () => {
          const code = button.nextElementSibling.innerText;
          navigator.clipboard.writeText(code)
              .then(() => {
                  button.textContent = "Copiado!";
                  setTimeout(() => button.textContent = "Copiar", 1500);
              })
              .catch(() => {
                  button.textContent = "Erro!";
              });
      });
  });
});


document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('grafico').getContext('2d');
  
    let grafico;

    // gerar o grafico
    if (!grafico) {
    const grafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'quantidade',
                data: valores,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
              y: {
                  beginAtZero: true
              }
            },
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            const label = context.label.toString().toUpperCase();  
                            const descri = dicionario[label] || null
                            if (descri == null){
                                return 'quantidade'
                            }
                            const linha_max = 40;
                            const words = descri.split(' ');
                            let linhas = [];
                            let linha_atual = '';
                            
                            words.forEach(word => {
                              if ((linha_atual + word).length > linha_max) {
                                linhas.push(linha_atual.trim());
                                linha_atual = word + ' ';
                              } else {
                                linha_atual += word + ' ';
                              }
                            });
                            if (linha_atual.length) {
                              linhas.push(linha_atual.trim());
                            }

                            return linhas;
                        },
                    }
                }
            }
        }
        });
    } else {
    grafico.data.labels = labels;
    grafico.data.datasets[0].data = valores;
    grafico.update();
    }
});

$(document).ready(function() {

  let modal = 'login'

  $.ajax({
    type: 'POST',
    dataType: 'json',
    assync: true,
    url: '/validate',
    success: function(dados) {
      const btnLogin = document.getElementById('btn-login')
      const btnLogout = document.getElementById('btn-logout')
      const btn2Login = document.getElementById('btn2-login')
      const btnIniciar = document.getElementById('iniciar')
      if (dados.id != null){
        btnLogout.style.display = 'block'
        btnIniciar.style.display = 'block'
      }
      else {
        btnLogin.style.display = 'block'
        btn2Login.style.display = 'block'
      }
    }
  })

  $('#btn-login').click(function(e) {
    e.preventDefault()
    modalLogin.style.display = 'flex'
  })

  $('#btn2-login').click(function(e) {
    e.preventDefault()
    modalLogin.style.display = 'flex'
  })

  $('#btn-logout').click(function(e) {
    e.preventDefault()
    $.ajax({
      type: 'POST',
      dataType: 'json',
      assync: true,
      url: '/logout',
      success: function(dados) {
        if (dados.type == 'success') {
          $(location).attr('href', '/')
        }
      }
    })
  })

  $('#sairModal').click(function(e) {
    e.preventDefault()
    modalLogin.style.display = 'none'
    $('#inputNome').val('')
    $('#inputCnpj').val('')
    $('#inputTelefone').val('')
    $('#inputEmail').val('')
    $('#inputSenha').val('')
    modal = 'cadastrar'
    modal = trocaModal(modal)
  });

  $('#linkCadastrar').click(function(e) {
    e.preventDefault()
    modal = trocaModal(modal)
  })

  $('#btnLogin').click(function(e) {
    e.preventDefault()
    const nome = document.getElementById('inputNome').value
    const cnpj = document.getElementById('inputCnpj').value
    const telefone = document.getElementById('inputTelefone').value
    const email = document.getElementById('inputEmail').value
    const senha = document.getElementById('inputSenha').value

    if (modal == 'login') {
      login(email, senha)
    } else if (modal == 'cadastrar') {
      cadastro(nome, cnpj, telefone, email, senha)
    }
  })

  $('#inputCnpj').keydown(function(e) {
    if (!Number(e.key) && e.key != 'Backspace') {
      e.preventDefault()
    }
  })

  $('#inputTelefone').keydown(function(e) {
    const texto = $('#inputTelefone').val()

    if (e.key != 'Backspace') {
      if (!Number(e.key)) {
      e.preventDefault()
      }
      else if (texto.length == 2) {
        $('#inputTelefone').val(texto + ' ')
      }
      else if (texto.length == 8) {
        $('#inputTelefone').val(texto + '-')
      }
      else if (texto.length == 13) {
        e.preventDefault()
      } 
    }
  })
})

function login(email, senha) {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    assync: true,
    data: {'email': email, 'senha': senha},
    url: '/login',
    success: function(dados) {
      $('.form-login').append(`
        <div class="spam-login">
          <p>${dados.mensagem}</p>
        </div>  
      `)
      setTimeout(() => {
        $('.spam-login').remove()
      }, 2500)
      if (dados.type == 'success') {
        $(location).attr('href', '/')
      }
    }
  })
}

function cadastro(nome, cnpj, telefone, email, senha) {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    assync: true,
    data: {'nome': nome, 'cnpj': cnpj, 'telefone': telefone, 'email': email, 'senha': senha},
    url: '/cadastro',
    success: function(dados) {
      $('.form-login').append(`
        <div class="spam-login">
          <p>${dados.mensagem}</p>
        </div>  
      `)
      setTimeout(() => {
        $('.spam-login').remove()
        if (dados.type == 'success') {
          login(email, senha)
        }
      }, 2500)
    }
  })
}

function trocaModal(modal) {
  const titulo = document.getElementById('modal-titulo')
  const botao = document.getElementById('btnLogin')
  const link = document.getElementById('linkCadastrar')
  const inNome = document.getElementById('inputNome')
  const inGroup = document.getElementById('inputGroup')

  if (modal == 'login') {
    modal = 'cadastrar'
    titulo.textContent = 'Fazer cadastro'
    botao.textContent = 'Cadastrar-se'
    link.textContent = 'Deseja fazer login?'
    inNome.style.display = 'block'
    inGroup.style.display = 'flex'
  } else if (modal == 'cadastrar') {
    modal = 'login'
    titulo.textContent = 'Login'
    botao.textContent = 'Entrar'
    link.textContent = 'Deseja fazer cadastro?'
    inNome.style.display = 'none'
    inGroup.style.display = 'none'
  }

  return modal
}