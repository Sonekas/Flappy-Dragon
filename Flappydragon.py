import pygame
import os
import random
import json

# Inicialização do Pygame
pygame.init()
pygame.display.set_caption('Flappy Dragon')

# Ajustando para resolução vertical (smartphone)
TELA_LARGURA = 800
TELA_ALTURA = 1100

# Arquivo para salvar o recorde
ARQUIVO_RECORDE = 'recorde.json'

# Função para carregar o recorde
def carregar_recorde():
    try:
        if os.path.exists(ARQUIVO_RECORDE):
            with open(ARQUIVO_RECORDE, 'r') as arquivo:
                return json.load(arquivo)['recorde']
        return 0
    except:
        return 0

# Função para salvar o recorde
def salvar_recorde(recorde):
    with open(ARQUIVO_RECORDE, 'w') as arquivo:
        json.dump({'recorde': recorde}, arquivo)

# Carregando imagens do jogo
IMAGEM_CANO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'pillar.png')), (200, 1100))
IMAGEM_CHAO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'base.png')), (800, 200))
IMAGEM_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (800, 1100))
IMAGEM_UCHIHA = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'uchiha.png')), (100, 100))

# Carregando imagens do dragão em alta qualidade
IMAGENS_DRAGON_ORIGINAL = [
    pygame.image.load(os.path.join('imgs', 'dragon1.png')),
    pygame.image.load(os.path.join('imgs', 'dragon2.png')),
    pygame.image.load(os.path.join('imgs', 'dragon3.png')),
]

# Redimensionando o dragão com melhor qualidade
IMAGENS_DRAGON = [
    pygame.transform.smoothscale(img, (200, 150))
    for img in IMAGENS_DRAGON_ORIGINAL
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 80)
FONTE_GAME_OVER = pygame.font.SysFont('arial', 80)
FONTE_REINICIAR = pygame.font.SysFont('arial', 50)


class Dragon:
    IMGS = IMAGENS_DRAGON
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do dragon
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do dragon vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o dragon tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem com rotação
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        
        # Calcular a posição central
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 350  # Distância entre a abertura dos canos
    ESPACO_ENTRE_CANOS = 500  # Nova constante para a distância entre os canos
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # Ajustando a altura para ficar entre 100 e 600 pixels
        # Isso garante que os canos não fiquem muito altos nem muito baixos
        self.altura = random.randrange(100, 600)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, dragon):
        dragon_mask = dragon.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - dragon.x, self.pos_topo - round(dragon.y))
        distancia_base = (self.x - dragon.x, self.pos_base - round(dragon.y))

        topo_ponto = dragon_mask.overlap(topo_mask, distancia_topo)
        base_ponto = dragon_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))


def desenhar_tela(tela, dragons, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for dragon in dragons:
        dragon.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    chao.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    pygame.display.update()

def desenhar_game_over(tela, pontos, recorde):
    # Criar uma superfície para o efeito de blur
    blur_surface = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
    blur_surface.fill((0, 0, 0))
    blur_surface.set_alpha(100)  # Aumentando a transparência para um efeito mais suave
    tela.blit(blur_surface, (0, 0))

    # Desenhar o quadrado de fundo maior
    pygame.draw.rect(tela, (0, 0, 0), (100, 200, 600, 700), border_radius=20)
    pygame.draw.rect(tela, (190, 40, 55), (100, 200, 600, 700), 3, border_radius=20)

    # Desenhar o símbolo Uchiha
    pos_x = TELA_LARGURA // 2 - IMAGEM_UCHIHA.get_width() // 2
    pos_y = 220
    tela.blit(IMAGEM_UCHIHA, (pos_x, pos_y))

    # Desenhar o texto GAME OVER com fonte menor
    texto_game_over = FONTE_GAME_OVER.render("GAME OVER", 1, (255, 255, 255))
    pos_x = TELA_LARGURA // 2 - texto_game_over.get_width() // 2
    pos_y = 350
    tela.blit(texto_game_over, (pos_x, pos_y))

    # Desenhar a pontuação final com fonte menor
    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    pos_x = TELA_LARGURA // 2 - texto_pontos.get_width() // 2
    pos_y = 450
    tela.blit(texto_pontos, (pos_x, pos_y))

    # Desenhar o recorde com fonte menor
    texto_recorde = FONTE_PONTOS.render(f"Recorde: {recorde}", 1, (255, 255, 255))
    pos_x = TELA_LARGURA // 2 - texto_recorde.get_width() // 2
    pos_y = 550
    tela.blit(texto_recorde, (pos_x, pos_y))

    # Desenhar o botão de reiniciar com fonte menor
    texto_reiniciar = FONTE_REINICIAR.render("ESPAÇO para reiniciar", 1, (255, 255, 255))
    pos_x = TELA_LARGURA // 2 - texto_reiniciar.get_width() // 2
    pos_y = 650
    
    # Desenhar o fundo do botão
    pygame.draw.rect(tela, (0, 0, 0), (pos_x - 20, pos_y - 10, texto_reiniciar.get_width() + 40, texto_reiniciar.get_height() + 20))
    pygame.draw.rect(tela, (190, 40, 55), (pos_x - 20, pos_y - 10, texto_reiniciar.get_width() + 40, texto_reiniciar.get_height() + 20), 3)
    tela.blit(texto_reiniciar, (pos_x, pos_y))

    # Retorna o retângulo do botão para detectar cliques
    botao_reiniciar = pygame.Rect(pos_x - 20, pos_y - 10, texto_reiniciar.get_width() + 40, texto_reiniciar.get_height() + 20)

    # Desenhar mensagem motivacional
    texto_tentar = FONTE_REINICIAR.render("Tente novamente, shinobi!", 1, (255, 255, 255))
    pos_x = TELA_LARGURA // 2 - texto_tentar.get_width() // 2
    pos_y = 750
    tela.blit(texto_tentar, (pos_x, pos_y))

    # Atualiza a tela
    pygame.display.update()

    return botao_reiniciar

def main():
    dragons = [Dragon(200, 550)]
    chao = Chao(950)
    canos = []
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    recorde = carregar_recorde()  # Carrega o recorde
    relogio = pygame.time.Clock()

    rodando = True
    game_over = False
    jogo_iniciado = False

    # Criando os 4 canos iniciais com espaçamento maior
    for i in range(4):
        canos.append(Cano(1000 + (i * Cano.ESPACO_ENTRE_CANOS)))

    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if not game_over:
                        if not jogo_iniciado:
                            jogo_iniciado = True
                        for dragon in dragons:
                            dragon.pular()
                    else:
                        # Reinicia o jogo quando pressionar espaço no game over
                        return main()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique esquerdo foi pressionado
                if evento.button == 1:
                    if not game_over:
                        if not jogo_iniciado:
                            jogo_iniciado = True
                        for dragon in dragons:
                            dragon.pular()
                    else:
                        # Verifica se clicou no botão de reiniciar
                        mouse_pos = pygame.mouse.get_pos()
                        if botao_reiniciar.collidepoint(mouse_pos):
                            # Reinicia o jogo
                            return main()

        if not game_over:
            # mover as coisas apenas se o jogo tiver iniciado
            if jogo_iniciado:
                for dragon in dragons:
                    dragon.mover()
                chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    for i, dragon in enumerate(dragons):
                        if cano.colidir(dragon):
                            dragons.pop(i)
                            game_over = True
                            # Atualiza o recorde se necessário
                            if pontos > recorde:
                                recorde = pontos
                                salvar_recorde(recorde)
                        if not cano.passou and dragon.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover()
                    if cano.x + cano.CANO_TOPO.get_width() < 0:
                        remover_canos.append(cano)

                # Removendo canos que saíram da tela
                for cano in remover_canos:
                    canos.remove(cano)
                    # Adicionando um novo cano quando um é removido
                    ultimo_cano = max(canos, key=lambda x: x.x)
                    canos.append(Cano(ultimo_cano.x + Cano.ESPACO_ENTRE_CANOS))

                if adicionar_cano:
                    pontos += 1

                for i, dragon in enumerate(dragons):
                    if (dragon.y + dragon.imagem.get_height()) > chao.y or dragon.y < 0:
                        dragons.pop(i)
                        game_over = True
                        # Atualiza o recorde se necessário
                        if pontos > recorde:
                            recorde = pontos
                            salvar_recorde(recorde)

            desenhar_tela(tela, dragons, canos, chao, pontos)
        else:
            # Desenha a tela de game over
            botao_reiniciar = desenhar_game_over(tela, pontos, recorde)
            # Mantém a tela de game over visível
            pygame.display.update()

if __name__ == '__main__':
    while True:
        main()
