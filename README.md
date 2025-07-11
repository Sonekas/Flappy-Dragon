# Flappy Dragon

Flappy Dragon é uma recriação do clássico jogo Flappy Bird, desenvolvido em Python utilizando a biblioteca Pygame. Neste jogo, os jogadores controlam um dragão que deve voar através de uma série de canos, evitando colisões e buscando a maior pontuação possível. O jogo inclui um sistema de recordes para acompanhar o melhor desempenho do jogador.




## Funcionalidades

*   **Jogabilidade Clássica:** Controles simples de um toque para fazer o dragão voar.
*   **Gráficos Aprimorados:** Imagens de dragão em alta qualidade e cenários temáticos.
*   **Sistema de Recordes:** Salva e exibe a maior pontuação alcançada pelo jogador.
*   **Interface Intuitiva:** Tela de Game Over com pontuação, recorde e opção de reiniciar.
*   **Tema Uchiha:** Elementos visuais inspirados no clã Uchiha, adicionando um toque único ao jogo.




## Como Jogar

1.  **Início do Jogo:** Pressione a tecla ESPAÇO ou clique com o botão esquerdo do mouse para iniciar o jogo.
2.  **Controle do Dragão:** Pressione a tecla ESPAÇO ou clique com o botão esquerdo do mouse para fazer o dragão voar para cima. Solte para que ele caia.
3.  **Objetivo:** Navegue o dragão através dos canos sem colidir com eles ou com o chão.
4.  **Pontuação:** Cada par de canos que o dragão atravessa com sucesso adiciona um ponto à sua pontuação.
5.  **Fim de Jogo:** O jogo termina quando o dragão colide com um cano ou com o chão. A tela de Game Over exibirá sua pontuação e o recorde atual.
6.  **Reiniciar:** Na tela de Game Over, pressione a tecla ESPAÇO ou clique no botão "ESPAÇO para reiniciar" para começar uma nova partida.




## Instalação

Para rodar o Flappy Dragon em sua máquina local, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Sonekas/Flappy-Dragon.git
    ```

2.  **Navegue até o diretório do projeto:**

    ```bash
    cd Flappy-Dragon
    ```

3.  **Instale as dependências:**

    Certifique-se de ter o `pip` instalado. Em seguida, instale o Pygame:

    ```bash
    pip install pygame
    ```

4.  **Execute o jogo:**

    ```bash
    python Flappydragon.py
    ```




## Estrutura do Projeto

O projeto Flappy Dragon é organizado da seguinte forma:

*   `Flappydragon.py`: O arquivo principal do jogo, contendo a lógica do jogo, classes para o dragão, canos e chão, e a função `main` que executa o jogo.
*   `imgs/`: Diretório que armazena todas as imagens utilizadas no jogo, incluindo:
    *   `bg.png`: Imagem de fundo do jogo.
    *   `base.png`: Imagem do chão.
    *   `pillar.png`: Imagem dos canos.
    *   `dragon1.png`, `dragon2.png`, `dragon3.png`: Imagens para a animação do dragão.
    *   `uchiha.png`: Imagem do símbolo Uchiha, utilizada na tela de Game Over.
*   `recorde.json`: Arquivo JSON onde o recorde de pontuação é salvo e carregado.




## Créditos

*   **Desenvolvedor:** Sonekas
*   **Inspirado em:** Flappy Bird
*   **Tecnologia:** Pygame (Python)

---




## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.




## Versão Web

Uma versão web do Flappy Dragon foi desenvolvida para demonstração e portfólio. Esta versão pode ser acessada diretamente no navegador, oferecendo a mesma experiência de jogo em uma plataforma diferente.

*   **Repositório da Versão Web:** [https://github.com/Sonekas/Flappy-Dragon-Web](https://github.com/Sonekas/Flappy-Dragon-Web)




*   **Demonstração Online:** [https://sonekas.github.io/Flappy-Dragon-Web/](https://sonekas.github.io/Flappy-Dragon-Web/)


