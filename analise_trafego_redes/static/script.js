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
    mensagem.textContent = ''
  });

  $('#btnLogin').click(function(e) {
    e.preventDefault()
    const email = document.getElementById('email').value
    const senha = document.getElementById('senha').value

    $.ajax({
      type: 'POST',
      dataType: 'json',
      assync: true,
      data: {'email': email, 'senha': senha},
      url: '/login',
      success: function(dados) {
        mensagem.textContent = dados.mensagem
        setTimeout(() => {
          mensagem.textContent = ''
        }, 2500)
        if (dados.type == 'success') {
          $(location).attr('href', '/')
        }
      }
    })
  })
})

