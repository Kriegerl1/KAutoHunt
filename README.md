#  KAutoHunt 2.0

O **KAutoHunt 2.0** é um bot desenvolvido para automatizar a caça de mobs no jogo, utilizando captura de tela e reconhecimento de imagem. Ele identifica sprites de monstros e move automaticamente o mouse para centralizar a mira.

O sistema foi desenvolvido em **Python** utilizando bibliotecas como `pyautogui`, `keyboard`, `pygetwindow` e `PIL`, garantindo alta precisão na detecção dos sprites.

---

## 📌 Requisitos Funcionais

- Identificar sprites dos mobs na tela e mover o mouse automaticamente para centralizar a mira.
- Buscar tanto a imagem original quanto sua versão espelhada para maior precisão.
- Detectar a imagem de "morte" do mob e mudar automaticamente de alvo.
- Ativar e desativar a caça pressionando a tecla **End**.
- Capturar prints da tela e analisar padrões para localizar os mobs.
- Ativar a janela do jogo automaticamente caso esteja minimizada.

---

## 🔧 Requisitos Não Funcionais

### **Desempenho**
- O bot opera com uma pequena pausa entre buscas (**0.05s**) para evitar alto consumo de CPU.
- O processamento das imagens é otimizado usando **numpy** e **OpenCV**.

### **Compatibilidade**
- Desenvolvido para rodar no **Windows**.
- O reconhecimento de imagem depende da resolução e qualidade dos sprites.

### **Interface**
- A interação acontece via terminal, com mensagens indicando o estado da caça e localização dos mobs.

---

## 🚀 Como Usar

### Clone o Repositório
```bash
git clone https://github.com/Kriegerl1/KAutoHunt.git
```

### Navegue até a pasta raiz do projeto
```bash
cd KAutoHunt
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

### Execute o bot
```bash
python main.py
```

---

## 💪 Como Funciona
1. **Configuração**: Antes de iniciar, defina a tecla de ativação para **End** e pressione **Enter**.
2. **Identificação de Mobs**: O bot busca as imagens dos mobs (original e espelhada) na tela.
3. **Movimentação**: Se um mob for encontrado, o mouse se move automaticamente para centralizar a mira.
4. **Verificação de Morte**: Se o mob morto for detectado, o bot muda de alvo.
5. **Tecla de Ativação**: Pressione **End** para ligar/desligar a caça.

---

## 🐝 Tecnologias Utilizadas
- **Python** (interpretação e lógica do bot)
- **PyAutoGUI** (movimentação do mouse e captura de tela)
- **Keyboard** (monitoramento de teclas)
- **PyGetWindow** (ativar a janela do jogo)
- **OpenCV** e **NumPy** (processamento de imagem)
- **PIL (Pillow)** (captura e manipulação de imagens)

---

## 🛠️ Possíveis Melhorias
- Implementar detecção mais rápida com **template matching** do OpenCV.
- Adicionar suporte para mais resoluções de tela.
- Criar uma interface gráfica para configuração dos sprites.

---

## 🏆 Contribuição
Caso queira contribuir, faça um *fork* do repositório, crie uma *branch* para suas modificações e envie um *pull request*.

---

## ⚖️ Licença
Este projeto é de uso pessoal e não deve ser utilizado para fins comerciais sem autorização.

