import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
font = pygame.font.Font(None, 50)
while True:
    screen.fill((0,255,0))
    t = font.render("TESTE ABRIU!", True, (0,0,0))
    screen.blit(t, (200,250))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            raise SystemExit
