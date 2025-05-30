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
    const dicionario = {
      TCP: 'TCP (Transmission Control Protocol), ou Protocolo de Controle de Transmissão, é um dos principais protocolos da camada de transporte no modelo TCP/IP, que é a base da comunicação na internet.',
      TLS: 'TLS (Transport Layer Security), ou Segurança da Camada de Transporte, é um protocolo de segurança que protege dados transmitidos pela internet.',
      DATA: 'Dados reais que estão sendo transmitidos entre dispositivos.',
      '_WS.MALFORMED': '_WS.MALFORMED está relacionado a um erro ou status indicando que uma mensagem WebSocket (WS) está malformada. ou seja, a mensagem recebida não segue o formato esperado pelo protocolo WebSocket.',
      ARP: 'ARP (Address Resolution Protocol), ou Protocolo de Resolução de Endereços, é um protocolo usado em redes de computadores para descobrir o endereço físico (MAC address) de um dispositivo na rede a partir de um endereço IP.',
      UDP: 'o User Datagram Protocol (UDP) é uma alternativa mais rápida, mas menos confiável, ao TCP na camada de transporte. É frequentemente usado em serviços como streaming de vídeo e jogos, onde a entrega rápida de dados é fundamental.',
      HTTP: 'o Protocolo de Transferência de Hipertexto (HTTP) é a base da Rede Mundial de Computadores, a internet com a qual a maioria dos usuários interage. Ele é utilizado para transferir dados entre dispositivos. O HTTP pertence à camada de aplicação (camada 7), porque deixa os dados com um formato que os aplicativos (como por exemplo, um navegador) podem usar diretamente, sem interpretação adicional. As camadas inferiores do modelo OSI são tratadas pelo sistema operacional de um computador, não pelos aplicativos.',
      HTTPS: 'O problema com o HTTP é que ele não é criptografado: qualquer invasor que interceptar uma mensagem HTTP poderá lê-la. O HTTPS (HTTP Seguro) corrige isso criptografando as mensagens HTTP.',
      DNS: 'DNS (Domain Name System), ou Sistema de Nomes de Domínio, é como uma “agenda de contatos” da internet. Ele traduz nomes de sites (como www.google.com) em endereços IP (como 142.250.72.14), que os computadores usam para se comunicar entre si.',
      ICMP: 'Usado para diagnóstico de rede, como o ping.',
      ICMPV6: 'Versão do ICMP para redes IPv6, usado para diagnóstico de rede, incluindo Neighbor Discovery.',
      SSH: 'SSH (Secure Shell) é um protocolo de rede usado para acessar e administrar computadores remotamente de forma segura, pela linha de comando.',
      FTP: 'Protocolo de Transferência de Arquivos (do inglês: File Transfer Protocol, abreviado FTP) é um protocolo padrão/genérico independente de hardware sobre um modo de transferir arquivos/ficheiros e também é um programa de transferência.',
      DHCP: 'DHCP (Dynamic Host Configuration Protocol), ou Protocolo de Configuração Dinâmica de Host, é um protocolo de rede que atribui automaticamente endereços IP e outras configurações de rede para os dispositivos de uma rede.'
    };

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
                            const values = context.dataset.data[context.dataIndex];
                            const descri = dicionario[label] || null
                            if (descri == null){
                                return `${label}: foi citado ${values} vezes`
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
                            linhas.push('')
                            linhas.push(`${label}: foi citado ${values} vezes`)

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
  const select = document.getElementById('selectOpt')

  $.ajax({
    type: 'POST',
    dataType: 'json',
    assync: true,
    url: '/validate',
    success: function(dados) {
      const btnLogin = document.getElementById('btn-login')
      const btnOpt = document.getElementById('opt')
      const btn2Login = document.getElementById('btn2-login')
      const btnIniciar = document.getElementById('iniciar')
      const userOpt = document.getElementById('userOpt')

      if (dados.id != null){
        btnOpt.style.display = 'flex'
        userOpt.textContent = `Olá, ${dados.nome}!`
        modal = 'dados'
        trocaModal(modal)

        btnIniciar.style.display = 'block'
      }
      else {
        btnLogin.style.display = 'block'
        btn2Login.style.display = 'block'
        btnOpt.style.display = 'none'
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

  $('#dados').click(function(e) {
    e.preventDefault()
    modalLogin.style.display = 'flex'
  })


  $(document).click(function(e) {
    if (!e.target.closest('#selectOpt') && $('#selectOpt').is(':visible')) {
      select.style.display = 'none'
    } 
    else if (e.target.closest('#userOpt')) {
      select.style.display = 'flex'
    }
  })

  $('.options').click(function(e) {
    e.preventDefault()
    select.style.display = 'none'
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
    if (modal != 'dados'){
      modal = 'cadastrar'
      modal = trocaModal(modal)
    }
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

  $('#inputEmail').keydown(function(e) {
    if (e.key === 'Enter') {
      inputSenha.focus()
    }
  })

  $('#inputSenha').keydown(function(e) {
    if (e.key === 'Enter') {
      $('#btnLogin').click()
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
  } 
  else if (modal == 'cadastrar') {
    modal = 'login'
    titulo.textContent = 'Login'
    botao.textContent = 'Entrar'
    link.textContent = 'Deseja fazer cadastro?'
    inNome.style.display = 'none'
    inGroup.style.display = 'none'
  }
  else if (modal == 'dados') {
    titulo.textContent = 'Meus dados'
    botao.textContent = 'Salvar alterações'
    link.style.display = 'none'
    inNome.style.display = 'block'
    inGroup.style.display = 'flex'
  }

  return modal
}