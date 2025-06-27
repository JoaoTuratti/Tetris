# Tetris Game

Um jogo clássico de Tetris implementado em Python usando Pygame, com uma funcionalidade especial de **wrapping** estilo Pac-Man!

## Descrição

Este é um jogo de Tetris moderno e colorido onde peças geométricas (tetrominós) caem do topo da tela. O objetivo é completar linhas horizontais para marcar pontos e evitar que as peças atinjam o topo da tela.

### Características Especiais

- **Wrapping Pac-Man**: As peças podem passar por um lado da tela e aparecer do outro lado!
- **Visual 3D**: Todas as peças possuem efeito visual tridimensional com bordas destacadas
- **Peça Fantasma**: Visualize onde a peça atual vai cair com uma prévia transparente
- **Cores dinâmicas**: As cores do jogo mudam constantemente para uma experiência visual única
- **Preview das próximas peças**: Veja as próximas 4 peças que virão
- **Sistema de pontuação**: Ganhe mais pontos completando múltiplas linhas simultaneamente
- **Velocidade progressiva**: O jogo fica mais rápido conforme você pontua

## Como Jogar

### Controles
- **← →** : Mover a peça para esquerda/direita
- **↓** : Acelerar a queda da peça
- **↑** : Girar a peça
- **ESC** : Sair do jogo

### Objetivo
1. Posicione as peças que caem para formar linhas horizontais completas
2. Quando uma linha é completada, ela desaparece e você ganha pontos
3. Evite que as peças atinjam o topo da tela
4. Tente fazer o maior número de pontos possível!

### Sistema de Pontuação
- **1 linha**: 100 pontos
- **2 linhas**: 400 pontos (2² × 100)
- **3 linhas**: 900 pontos (3² × 100)
- **4 linhas**: 1600 pontos (4² × 100)

## Como Executar

### Pré-requisitos
- Python 3.6 ou superior
- Pygame

### Instalação
1. Clone ou baixe este repositório
2. Instale o Pygame:
```bash
pip install pygame
```

### Executar o Jogo
```bash
python tetris.py
```

## Peças do Jogo

O jogo inclui todas as 7 peças clássicas do Tetris:

- **I** - Peça reta (4 blocos em linha)
- **O** - Quadrado (2x2 blocos)
- **T** - Formato T
- **S** - Formato S
- **Z** - Formato Z
- **J** - Formato J
- **L** - Formato L

## Funcionalidades Visuais

- Interface colorida e moderna
- **Peças com efeito 3D**: Todos os blocos possuem bordas tridimensionais realistas
- **Sistema de peça fantasma**: Visualização em tempo real de onde a peça vai cair
- Animação de flash quando linhas são completadas
- Mudança automática de cores a cada 500ms
- Letras "TETRIS" com cores dinâmicas
- Preview das próximas peças no lado direito com visual 3D

## Funcionalidades Técnicas

- **60 FPS** de gameplay suave
- **Sistema de wrapping horizontal**: As peças podem passar por um lado e aparecer do outro
- **Renderização 3D**: Sistema avançado de desenho com efeitos de profundidade
- **Algoritmo de peça fantasma**: Cálculo em tempo real da posição final da peça
- **Detecção inteligente de colisões**
- **Rotação com validação de espaço**
- **Sistema de níveis progressivos**

## Personalização

Você pode facilmente modificar:
- Cores das peças editando a lista `colors`
- Velocidade do jogo alterando `fall_speed`
- Tamanho da grade modificando `grid_width` e `grid_height`
- Tamanho dos blocos alterando `block_size`

## Recursos Especiais

### Wrapping Pac-Man Style
Diferente do Tetris tradicional, nesta versão as peças podem "atravessar" as bordas laterais da tela, aparecendo do lado oposto. Isso adiciona uma nova dimensão estratégica ao jogo!

### Visual 3D Avançado
Todas as peças do jogo possuem efeito visual tridimensional com bordas iluminadas e sombreadas, criando uma sensação de profundidade e modernidade que vai além do Tetris clássico.

### Sistema de Peça Fantasma
Uma funcionalidade avançada que mostra em tempo real onde a peça atual vai cair, facilitando o posicionamento estratégico e melhorando significativamente a experiência de jogo.

### Sistema de Cores Dinâmicas
As cores do jogo mudam constantemente, criando uma experiência visual única e vibrante a cada partida.

---

**Divirta-se jogando!**

