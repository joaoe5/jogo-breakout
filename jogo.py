#-*- coding: utf-8 -*-

import pygame, sys, random
from pygame.locals import*
import random

class Menu():

	def criaMenu(self):

		arq = open('recordes.txt', 'r+')
		txt = arq.readlines()

		#Altura e largura da tela do jogo
		altura = 480
		largura = 760
		
		pygame.init()
		pygame.display.set_caption('Jogo - Breakout')
		pygame.mouse.set_visible(1)

		#Criação da janela do jogo
		tela = pygame.display.set_mode((largura,altura))
		# tela.fill((0,0,24))
		#tela.fill((30,12,30))
		
		input_texto = pygame.Rect(230, 50, 140, 32)
		cor_inativo = pygame.Color('lightskyblue3')
		# cor_ativo = pygame.Color('dodgerblue2')
		cor_ativo = pygame.Color('red')
		cor = cor_inativo
		ativo = False
		texto = ''

		flag = True
		while flag:
			for event in pygame.event.get():
				if event.type == QUIT:
					flag = False
				if(event.type == MOUSEBUTTONDOWN):
					#O jogo só será iniciado se o usuário preencher o campo para nome
					if (texto_jogar_rect.collidepoint(event.pos) and texto != ""):
						jogar = Jogo()
						jogar.main(texto)
						flag = False
					if input_texto.collidepoint(event.pos):
						ativo = not ativo
					else:
						ativo = False
					cor = cor_ativo if ativo else cor_inativo
				if (event.type == KEYDOWN):
					if ativo:
						if event.key == pygame.K_BACKSPACE:
							texto = texto[:-1]
						else:
							texto += event.unicode

			tela.fill((0,0,24))

			texto_insira_nome = pygame.font.SysFont(None,36).render('Insira seu nome abaixo:', True, (255,255,255),(0,0,24)) 
			texto_insira_nome_rect = texto_insira_nome.get_rect()
			texto_insira_nome_rect = texto_insira_nome_rect.move(240,10)
			tela.blit(texto_insira_nome, texto_insira_nome_rect)

			texto_jogar = pygame.font.SysFont(None,60).render('JOGAR', True, (255,255,255),(0,0,24)) 
			texto_jogar_rect = texto_jogar.get_rect()
			texto_jogar_rect = texto_jogar_rect.move(300,100)
			tela.blit(texto_jogar, texto_jogar_rect)

			texto_recorde = pygame.font.SysFont(None,45).render('Recordes - Top 5', True, (116,189,214),(0,0,24)) 
			texto_recorde_rect = texto_recorde.get_rect()
			texto_recorde_rect = texto_recorde_rect.move(260,190)
			tela.blit(texto_recorde, texto_recorde_rect)
			
			lista_ord = []
			for i in txt:
				i = i.split(',')
				i[1] = int(i[1])
				lista_ord.append(i)

			lista_ord = sorted(lista_ord, key=lambda txt : txt[1], reverse=True)

			i = 0
			while(i < len(txt)):
				if i == 5:
					break

				jog,pont = lista_ord[i][0],lista_ord[i][1]

				texto_jogadores = pygame.font.SysFont(None,30).render(str(jog) + ' - Pontuação: ' + str(pont), True, (185,167,36),(0,0,24)) 
				texto_jogadores_rect = texto_jogadores.get_rect()
				t = 240 + (30 * i)
				texto_jogadores_rect = texto_jogadores_rect.move(230,t)
				tela.blit(texto_jogadores, texto_jogadores_rect)
				i+=1

			mostra_texto = pygame.font.Font(None,28).render(texto, True, (255,245,220))
			caixa_larg = (300)
			input_texto.w = caixa_larg
			tela.blit(mostra_texto, (input_texto.x+5, input_texto.y+5))

			pygame.draw.rect(tela, cor, input_texto, 2)

			pygame.display.flip()

			arq.close()

class Jogo():

	def main(self,texto):
		
		#Definição das variáveis de controle do jogo
		veloc_inicial_X = 3
		veloc_inicial_y = 3
		vidas_ini = 4
		veloc_Barra = 20

		score = 0
		nivel = 1
		controla_bloco = 0
		
		#Altura e largura da tela do jogo
		altura = 480
		largura = 760
		pygame.init()
		#Criação da janela do jogo
		tela = pygame.display.set_mode((largura,altura))

		#Criando blocos
		blocos = ConstroiBlocos()
		blocos.cria(largura)

		music = pygame.mixer.Sound('music.wav')
		music.set_volume(8)

		#Carregando a imagem da barra
		barra = pygame.image.load("traco.png").convert()
		barra_rect = barra.get_rect()
		
		#carregando a imagem da bola
		bola = pygame.image.load("bola.png").convert()
		bola.set_colorkey((20,0,30))
		bola_rect = bola.get_rect()
		
		#Movimentando a barra na janela - Posicao
		barra_rect =barra_rect.move((largura / 2) - (barra_rect.right / 2), altura - 20)
		#bola_rect = bola_rect.move(largura / 2, altura / 2)
		bola_rect = bola_rect.move((barra_rect.left + barra_rect.right) / 2 - 10, altura - 40)
		veloc_X = veloc_inicial_X
		veloc_y = veloc_inicial_y
		vidas = vidas_ini
		
		clock = pygame.time.Clock()
		#delay e intervalo das teclas pressionadas
		pygame.key.set_repeat(1,30)
		#Função que deixa o ponteiro do mouse invisivel na tela do jogo
		pygame.mouse.set_visible(0)
		#Texto da janela
		pygame.display.set_caption('Jogo - Breakout')
		
		flag = True
		var = 0
		executa = 1
		pausa = 0
		estado = executa
		#trol = 1
		tempo = 70

		while flag:
			#Eventos do teclado
			for event in pygame.event.get():
				if event.type == QUIT:
					flag = False
				if event.type == pygame.KEYDOWN:
					if(event.key == pygame.K_p and estado == executa):
						estado = pausa
						texto_pause = pygame.font.SysFont("arial",80).render('PAUSE', True, (255,255,255),(20,0,30)) 
						texto_pause_rect = texto_pause.get_rect()
						texto_pause_rect = texto_pause_rect.move(280,200)
						tela.blit(texto_pause, texto_pause_rect)

						texto_continue = pygame.font.SysFont("arial",20).render('Pressione C para continuar', True, (255,255,255), (20,0,30))
						texto_continue_rect = texto_continue.get_rect()
						texto_continue_rect = texto_continue_rect.move(290,280)
						tela.blit(texto_continue, texto_continue_rect)

						pygame.display.flip()

					elif (event.key == pygame.K_c and estado == pausa):
						estado = executa 
							
					if(event.key == pygame.K_ESCAPE):
						flag = False
						break
					if(event.key == pygame.K_LEFT and var == 0 and estado == executa):
						barra_rect = barra_rect.move(-veloc_Barra, 0)
						bola_rect = bola_rect.move(-veloc_Barra, 0)
						if(barra_rect.left < 0):
							barra_rect.left = 0
						if(bola_rect.left < 61):
							bola_rect.left = 61
					if(event.key == pygame.K_RIGHT and var == 0 and estado == executa):
						barra_rect = barra_rect.move(veloc_Barra, 0)
						bola_rect = bola_rect.move(veloc_Barra, 0)
						if(barra_rect.right > largura):
							barra_rect.right = largura
						if(bola_rect.right >= largura - 61):
							bola_rect.right =  largura - 61

					if(event.key == pygame.K_LEFT and var == 1 and estado == executa):
						barra_rect = barra_rect.move(-veloc_Barra, 0)
						if(barra_rect.left < 0):
							barra_rect.left = 0
					if(event.key == pygame.K_RIGHT and var == 1 and estado == executa):
						barra_rect = barra_rect.move(veloc_Barra, 0)
						if(barra_rect.right > largura):
							barra_rect.right = largura

					#Nesse momento do jogo a bola ainda esta parada, até o jogador dar inicio
					if(event.key == pygame.K_SPACE and var == 0 and estado == executa):
						var = 1
						veloc_y = 5
						bola_rect =  bola_rect.move(veloc_X, -veloc_y)

			clock.tick(tempo)

			if estado == executa:
				#O jogo pode continuar após o evento do usuário
				if var == 1:
					bola_rect =  bola_rect.move(veloc_X, -veloc_y)
					if bola_rect.right > largura:
						bola_rect.right = largura
					if bola_rect.left < 0:
						bola_rect.left = 0
					if bola_rect.left == 0 or bola_rect.right == largura:
						veloc_X = -veloc_X

					if bola_rect.top <= 0:
						veloc_y = -veloc_y
					
				#Verificando se o usuário perdeu uma vida
				if (bola_rect.top > altura and var == 1):
					vidas -= 1
					estado = executa
					if (vidas == 0):
						
						arq = open('recordes.txt', 'r+')
						txt = arq.readlines()

						concat = str(texto) + ',' +  str(score) + '\n'
						arq.write(concat)
						arq.close()

						mensagem = pygame.font.SysFont("arial",80).render("Game Over", True, (255,255,255), (20,0,30))
						mensagem_rect = mensagem.get_rect()
						mensagem_rect = mensagem_rect.move(200,200)
						tela.blit(mensagem, mensagem_rect)
						pygame.display.flip()

						#Fechando a janela do jogo em 3 segundos
						m3 = pygame.font.SysFont("arial",16).render('Fechando em 3 ', True, (255,255,255),(20,0,30))
						m3_rect = m3.get_rect()
						m3_rect = m3_rect.move(280,280)
						tela.blit(m3,m3_rect)
						pygame.display.flip()
						pygame.time.delay(1000)

						m2 = pygame.font.SysFont("arial",16).render('Fechando em 3, 2', True, (255,255,255),(20,0,30))
						m2_rect = m2.get_rect()
						m2_rect = m2_rect.move(280,280)
						tela.blit(m2,m2_rect)
						pygame.display.flip()
						pygame.time.delay(1000)

						m1 = pygame.font.SysFont("arial",16).render('Fechando em 3, 2, 1...', True, (255,255,255),(20,0,30))
						m1_rect = m1.get_rect()
						m1_rect = m1_rect.move(280,280)
						tela.blit(m1,m1_rect)
						pygame.display.flip()
						pygame.time.delay(1000)
						
						flag = False

						menu = Menu()
						menu.criaMenu()

						# sys.exit()
					veloc_X = veloc_inicial_X
					veloc_inicial_y = veloc_inicial_X
					bola_rect.center = ((barra_rect.left + barra_rect.right) / 2, altura - 30)
					var = 0

				#Verificando se a bola atingiu a barra e fazendo as operações da sua movimentação
				if (bola_rect.bottom >= barra_rect.top and
					bola_rect.bottom <= barra_rect.bottom and
					bola_rect.right >= barra_rect.left and
					bola_rect.left <= barra_rect.right): 
					veloc_y = -veloc_y
					
					offset = bola_rect.center[0] - barra_rect.center[0]
					if offset >= 0:
						if offset > 20:
							veloc_X = 5 
						elif offset > 15:
							veloc_X = 6 
						elif offset > 9:
							veloc_X = 4 
					else:
						if offset < -20:
							veloc_X = -5 
						elif offset < -15:
							veloc_X = -6 
						elif offset < -9:
							veloc_X = -4 

				#Colisão da bola no bloco
				indice =  bola_rect.collidelist(blocos.blocopadrao_rect)
				if indice != -1:
					if (bola_rect.center[0] >= blocos.blocopadrao_rect[indice].right or 
						bola_rect.center[0] <= blocos.blocopadrao_rect[indice].left) :
						veloc_X = -veloc_X
					else:
						veloc_y = -veloc_y
					music.play(0)
					blocos.blocopadrao_rect[indice:indice + 1] = []
					score += (5 * nivel)
					controla_bloco += 1

				indice2 = bola_rect.collidelist(blocos.blocovida_rect)
	
				if indice2 != -1:
					rand = random.randint(1,5)
					if rand == 1:
						vidas += 1
					elif rand == 2:
						tempo = 30
					elif rand == 3:
						tempo = 150
						veloc_Barra = 30
					elif rand == 4:
						score = score * 2
					else:
						veloc_Barra = 10
					#tempo = 150
					music.play(0)
					blocos.blocovida_rect[indice2:indice2 + 1] = []
					controla_bloco += 1

				#Após detruição total dos blocos um novo campo é criado
				if controla_bloco == 51 and bola_rect.bottom == barra_rect.top:
					tela.fill((20,0,30))
					blocos.cria(largura)
					nivel += 1
					tempo = 70
					controla_bloco = 0
					veloc_Barra = 20
					if nivel % 4 == 0:
						vidas += 1

				tela.fill((20,0,30))

				#Chamando função pra atualizar e mostrar os blocos
				for i in range(0, len(blocos.blocopadrao_rect)):
					tela.blit(blocos.blocopadrao, blocos.blocopadrao_rect[i])
				for i in range(0, len(blocos.blocovida_rect)):
					tela.blit(blocos.blocovida, blocos.blocovida_rect[i])

				if blocos.blocopadrao_rect == []:
					bloco.cria(largura)
					veloc_X = veloc_inicial_X
					veloc_y = veloc_inicial_y
					bola_rect.center = ((barra_rect.left + barra_rect.right) / 2, altura - 30)
				

				texto_vidas = pygame.font.SysFont("arial",18).render('Vidas = ' + str(vidas) + '    Nível = ' + str(nivel), True, (255,255,255),(20,0,30)) 
				texto_vidas_rect = texto_vidas.get_rect()
				texto_vidas_rect = texto_vidas_rect.move(5, 0)
				tela.blit(texto_vidas, texto_vidas_rect)

				texto_score = pygame.font.SysFont("verdana",18).render('Score = ' + str(score), True, (255,255,255),(20,0,30))
				texto_score_rect = texto_score.get_rect()
				texto_score_rect = texto_score_rect.move(600,0)
				tela.blit(texto_score, texto_score_rect)

				tela.blit(bola, bola_rect)	
				tela.blit(barra, barra_rect)
				pygame.display.flip()


class ConstroiBlocos():

	def __init__(self):
		self.blocopadrao = pygame.image.load("bloco.png").convert()
		blocopadrao_rect = self.blocopadrao.get_rect()
		self.blocopadrao_tam = 76
		self.blocopadrao_alt = 20

		#Criando bloco vida 
		self.blocovida = pygame.image.load("vida.png").convert()
		blocovida_rect =  self.blocovida.get_rect()
		self.blocovida_tam = 46
		self.blocovida_alt = 20

	def cria(self, largura):
		pos_x = 0
		pos_y = 30
		prox = 0
		self.blocopadrao_rect = []
		for i in range (0, 56):
			if pos_x > largura:
				if prox == 0:
					prox = self.blocopadrao_tam 
					#gerar blocos em colunas diferentes
					#prox = self.blocopadrao_tam / 2
				else:
					prox = 0
				pos_x = -prox
				pos_y += self.blocopadrao_alt

			self.blocopadrao_rect.append(self.blocopadrao.get_rect())
			self.blocopadrao_rect[i] = self.blocopadrao_rect[i].move(pos_x,pos_y)
			pos_x = pos_x + self.blocopadrao_tam
		self.blocovida_rect = []
		self.blocovida_rect.append(self.blocovida.get_rect())
		self.blocovida_rect[0] = self.blocovida_rect[0].move(357,10)

if __name__ == '__main__':
	# arq = open('recordes.txt', 'r+')
	# txt = arq.readlines()
	menu = Menu()
	menu.criaMenu()