document.addEventListener("DOMContentLoaded", function () {
    const text = "Bem Vindo Ao Sistema ";
    const typingElement = document.getElementById("typing");
    const buttons = document.querySelectorAll('.copy-button');
  
    let index = 0;
    typingElement.innerHTML = "";
  
    function typeEffect() {
      if (index < text.length) {
        typingElement.innerHTML += text.charAt(index);
        index++;
        setTimeout(typeEffect, 250); // Velocidade de digitação
      } 
    }
    typeEffect();

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
  