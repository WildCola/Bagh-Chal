import pygame
import sys
import math
from copy import *
import time

ADANCIME_MAX = 3
culoareEcran = (250,210,117)
culoareLinii = (0,0,0)
culoareTigrii = (255, 100, 0)
culoareCapre = (200, 200, 200)
l_stari = []

def distEuclid(p0,p1):
	(x0,y0) = p0
	(x1,y1) = p1
	return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Graph:
	JMIN = None
	JMAX = None
	GOL = '#'

	noduri = []
	muchii = []
	muchiiSalt = []

	scalare = 100
	translatie = 20
	razaPct = 10
	razaPiesa = 20

	@classmethod
	def jucator_opus(cls, jucator):
		return cls.JMAX if jucator == cls.JMIN else cls.JMIN

	@classmethod
	def initializeaza(cls):
		for i in range(5):
			for j in range(5):
				cls.noduri.append((i, j))

		for i in range(25):
			if (i+1) % 5 != 0:
				cls.muchii.append((i, i+1))
				cls.muchii.append((i+1, i))

			if i < 20:
				cls.muchii.append((i, i+5))
				cls.muchii.append((i+5, i))
				if i % 2 == 0:
					if (i + 1) % 5 != 1:
						cls.muchii.append((i, i+4))
						cls.muchii.append((i+4, i))
					if (i + 1) % 5 != 0:
						cls.muchii.append((i, i+6))
						cls.muchii.append((i+6, i))

			if (i+1) % 5 != 4 and (i+1) % 5 != 0:
				cls.muchiiSalt.append((i, i+1, i+2))
				cls.muchiiSalt.append((i+2, i+1, i))

			if i < 15:
				cls.muchiiSalt.append((i, i+5, i+10))
				cls.muchiiSalt.append((i+10, i+5, i))
				if i % 2 == 0:
					if (i + 1) % 5 != 1 and (i + 1) % 5 != 2:
						cls.muchiiSalt.append((i, i+4, i+8))
						cls.muchiiSalt.append((i+8, i+4, i))
					if (i+1) % 5 != 0 and (i+1) % 5 != 4 and i < 13:
						cls.muchiiSalt.append((i, i+6, i+12))
						cls.muchiiSalt.append((i+12, i+6, i))
		#print(cls.muchiiSalt)
		cls.coordonateNoduri = [[cls.translatie + cls.scalare * x for x in nod] for nod in cls.noduri]

	def __init__(self, tabla = None, capreMancate = None, caprePuse = None):
		if tabla:
			self.matr = tabla
			self.capreMancate = capreMancate
			self.caprePuse = caprePuse
			self.capre = []
			self.tigri = []
			for i in range(len(self.matr)):
				if self.matr[i] == 'T':
					self.tigri.append(i)
				elif self.matr[i] == 'C':
					self.capre.append(i)

		else:
			self.capreMancate = 0
			self.caprePuse = 0
			self.matr = []
			self.tigri = [0, 4, 20, 24]
			self.capre = []
			for i in range(5):
				for j in range(5):
					self.matr.append(self.GOL)
			self.matr[0] = 'T'
			self.matr[4] = 'T'
			self.matr[20] = 'T'
			self.matr[24] = 'T'

	def mutari(self, jucator):
		l_mutari = []
		if jucator == "tigri":
			for tigru in self.tigri:
				for mutare in Graph.muchii:
					if mutare[0] == tigru and self.matr[mutare[1]] == self.GOL:
						copie_matr = deepcopy(self.matr)
						copie_matr[mutare[1]] = 'T'
						copie_matr[mutare[0]] = self.GOL
						if copie_matr not in l_stari:
							l_mutari.append(Graph(copie_matr, self.capreMancate, self.caprePuse))
				for mutare in Graph.muchiiSalt:
					if mutare[0] == tigru and self.matr[mutare[1]] == 'C' and self.matr[mutare[2]] == self.GOL:
						copie_matr = deepcopy(self.matr)
						copie_matr[mutare[2]] = 'T'
						copie_matr[mutare[1]] = self.GOL
						copie_matr[mutare[0]] = self.GOL
						if copie_matr not in l_stari:
							l_mutari.append(Graph(copie_matr, self.capreMancate+1, self.caprePuse))
		else:
			if self.caprePuse < 20:
				for i in range(25):
					if self.matr[i] == self.GOL:
						copie_matr = deepcopy(self.matr)
						copie_matr[i] = 'C'
						if copie_matr not in l_stari:
							l_mutari.append(Graph(copie_matr, self.capreMancate, self.caprePuse+1))
			else:
				for capra in self.capre:
					for mutare in self.muchii:
						if mutare[0] == capra and self.matr[mutare[1]] == self.GOL:
							copie_matr = deepcopy(self.matr)
							copie_matr[mutare[1]] = 'C'
							copie_matr[mutare[0]] = self.GOL
							if copie_matr not in l_stari:
								l_mutari.append(Graph(copie_matr, self.capreMancate, self.caprePuse))
		return l_mutari

	def final(self, j_curent):
		if self.capreMancate >= 5:
			return "tigri"
		if self.mutari(j_curent) == []:
			return "capre"
		return False

	def spatii_ocupate(self):
		nr = 0
		for i in range(25):
			if self.matr[i] != Graph.GOL:
				nr += 1
		return nr

	def tigrii_liberi(self, j_curent):
		nr = 0
		l_mutari = self.mutari(j_curent)
		for tigru in self.tigri:
			for mut in l_mutari:
				if mut.matr[tigru] == Graph.GOL:
					nr += 1
					break
		return nr

	def estimeaza_scor(self, adancime, j_curent):
		t_final = self.final(j_curent)
		if t_final == self.__class__.JMAX:
			return (99999 + adancime)
		elif t_final == self.__class__.JMIN:
			return (-99999 - adancime)
		elif Graph.JMAX == "tigri":
			return 30 * self.tigrii_liberi(j_curent) + 70 * self.capreMancate - 70 * self.spatii_ocupate()
		else:
			return 30 * self.spatii_ocupate() - 30 * self.tigrii_liberi(j_curent) - 120 * self.capreMancate



	def deseneazaEcranJoc(self, ecran, de_mutat = None):
		ecran.fill(culoareEcran)
		for nod in Graph.coordonateNoduri:
			pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=self.razaPct, width=0)  # width=0 face un cerc plin

		for muchie in self.muchii:
			p0 = self.coordonateNoduri[muchie[0]]
			p1 = self.coordonateNoduri[muchie[1]]
			pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)

		for tigru in self.tigri:
			if de_mutat == tigru:
				pygame.draw.circle(surface=ecran, color=(0, 255, 0), center=self.coordonateNoduri[tigru], radius=15, width=0)
			else:
				pygame.draw.circle(surface=ecran, color=culoareTigrii, center=self.coordonateNoduri[tigru], radius=15, width=0)
			pygame.draw.circle(surface=ecran, color=(0,0,0), center=self.coordonateNoduri[tigru], radius=15, width=3)


		for capra in self.capre:
			if de_mutat == capra:
				pygame.draw.circle(surface=ecran, color=(0, 255, 0), center=self.coordonateNoduri[capra], radius=15, width=0)
			else:
				pygame.draw.circle(surface=ecran, color=culoareCapre, center=self.coordonateNoduri[capra], radius=15, width=0)
			pygame.draw.circle(surface=ecran, color=(0,0,0), center=self.coordonateNoduri[capra], radius=15, width=3)

		pygame.display.update()

class Stare:
	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=0):
		self.tabla_joc = tabla_joc
		self.j_curent = j_curent

		# adancimea in arborele de stari
		self.adancime = adancime

		# estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
		self.estimare = estimare

		# lista de mutari posibile din starea curenta
		self.mutari_posibile = []

		# cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa = None

	def mutari(self):
		l_mutari = self.tabla_joc.mutari(self.j_curent)
		juc_opus = Graph.jucator_opus(self.j_curent)
		l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

		return l_stari_mutari


def min_max(stare):
	if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
		stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
		return stare
	stare.mutari_posibile = stare.mutari()
	mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

	if stare.j_curent == Graph.JMAX:
		# daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
		stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
	else:
		# daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
		stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
	stare.estimare = stare.stare_aleasa.estimare
	return stare


def alpha_beta(alpha, beta, stare):
	if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
		stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
		return stare

	if alpha > beta:
		return stare  # este intr-un interval invalid deci nu o mai procesez

	stare.mutari_posibile = stare.mutari()

	if stare.j_curent == Graph.JMAX:
		estimare_curenta = float('-inf')

		for mutare in stare.mutari_posibile:
			# calculeaza estimarea pentru starea noua, realizand subarborele
			stare_noua = alpha_beta(alpha, beta, mutare)

			if (estimare_curenta < stare_noua.estimare):
				stare.stare_aleasa = stare_noua
				estimare_curenta = stare_noua.estimare
			if (alpha < stare_noua.estimare):
				alpha = stare_noua.estimare
				if alpha >= beta:
					break

	elif stare.j_curent == Graph.JMIN:
		estimare_curenta = float('inf')

		for mutare in stare.mutari_posibile:

			stare_noua = alpha_beta(alpha, beta, mutare)

			if (estimare_curenta > stare_noua.estimare):
				stare.stare_aleasa = stare_noua
				estimare_curenta = stare_noua.estimare

			if (beta > stare_noua.estimare):
				beta = stare_noua.estimare
				if alpha >= beta:
					break
	try:
		stare.estimare = stare.stare_aleasa.estimare
	except:
		print("Castigator: capre")

	return stare

def main():
	#initializare algoritm
	Graph.initializeaza()
	raspuns_valid=False
	while not raspuns_valid:
		tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
		if tip_algoritm in ['1','2']:
			raspuns_valid=True
		else:
			print("Nu ati ales o varianta corecta.")
	#initializare jucatori
	raspuns_valid=False
	while not raspuns_valid:
		Graph.JMIN=input("Doriti sa jucati cu tigri sau cu capre? ").lower()
		if (Graph.JMIN in ["tigri", "capre"]):
			raspuns_valid=True
		else:
			print("Raspunsul trebuie sa fie \"tigri\" sau \"capre\".")
	Graph.JMAX= "tigri" if Graph.JMIN == "capre" else "capre"

	tabla_curenta = Graph()
	print("Tabla initiala:")
	print(str(tabla_curenta.matr))

	stare_curenta = Stare(tabla_curenta, 'capre', ADANCIME_MAX)
	pygame.init()
	ecran = pygame.display.set_mode(size=(440, 440))
	tabla_curenta.deseneazaEcranJoc(ecran)
	de_mutat = -1
	while True:
		if stare_curenta.tabla_joc.final(stare_curenta.j_curent):
			print("Castigator: " + stare_curenta.tabla_joc.final(stare_curenta.j_curent))
			return
		if stare_curenta.j_curent == Graph.JMIN: # mutarea jucatorului
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()  # inchide fereastra
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:  # click
					pos = pygame.mouse.get_pos()
					for idx, nod in enumerate(tabla_curenta.coordonateNoduri):
						if distEuclid(pos, nod) <= Graph.razaPct:
							if (stare_curenta.tabla_joc.matr[idx] == 'T' and Graph.JMIN == "tigri") or (stare_curenta.tabla_joc.matr[idx] == 'C' and Graph.JMIN == "capre" and stare_curenta.tabla_joc.caprePuse >= 20):
								# verific daca pot selecta piesa de pe nodul pe care fac click
								if de_mutat == -1: # daca fac click pe o pisa neselectata o selectez
									de_mutat = idx
									stare_curenta.tabla_joc.deseneazaEcranJoc(ecran, de_mutat)

								else:
									de_mutat = -1 # verific daca am deja o piesa selectata si daca fac click din nou pe o pisa o deselectez
									stare_curenta.tabla_joc.deseneazaEcranJoc(ecran)
							elif stare_curenta.tabla_joc.matr[idx] == Graph.GOL:
								if de_mutat != -1: # daca am o piesa selectata si fac click pe un nod gol, verific daca pot muta piesa acolo
									l_mutari = stare_curenta.tabla_joc.mutari(stare_curenta.j_curent)
									# for mut in l_mutari:
									# 	print(mut.matr)
									copie_matr = deepcopy(stare_curenta.tabla_joc.matr)
									copie_matr[idx] = Graph.JMIN[0].upper()
									copie_matr[de_mutat] = Graph.GOL
									for mut in l_mutari:
										dif = 0
										for tigru in stare_curenta.tabla_joc.tigri:
											if tigru not in mut.tigri:
												dif += 1
										if mut.matr == copie_matr or (mut.matr[idx] == copie_matr[idx] and mut.matr[de_mutat] == Graph.GOL and dif == 1 and mut.capreMancate - stare_curenta.tabla_joc.capreMancate == 1):
											aux = stare_curenta.tabla_joc
											stare_curenta.tabla_joc = mut
											if stare_curenta.tabla_joc.caprePuse < 20:
												stare_curenta.tabla_joc.deseneazaEcranJoc(ecran)
												de_mutat = -1
												stare_curenta.j_curent = Graph.jucator_opus(stare_curenta.j_curent)
											elif stare_curenta.tabla_joc not in l_stari:
												l_stari.append(stare_curenta.tabla_joc.matr)
												stare_curenta.tabla_joc.deseneazaEcranJoc(ecran)
												de_mutat = -1
												stare_curenta.j_curent = Graph.jucator_opus(stare_curenta.j_curent)
												if stare_curenta.tabla_joc.final(stare_curenta.j_curent):
													print("Castigator: " + stare_curenta.tabla_joc.final(stare_curenta.j_curent))
													return

											else:
												stare_curenta.tabla_joc = aux
								else:
									if Graph.JMIN == "capre": # daca jucatorul este capra si inca nu a pus toate 20 caprele pe tabla, atunci pune o capra pe nodul selectat
										if stare_curenta.tabla_joc.caprePuse < 20:
											stare_curenta.tabla_joc.matr[idx] = 'C'
											stare_curenta.tabla_joc.capre.append(idx)
											stare_curenta.tabla_joc.caprePuse += 1
											stare_curenta.tabla_joc.deseneazaEcranJoc(ecran)
											stare_curenta.j_curent = Graph.jucator_opus(stare_curenta.j_curent)

		else: # mutarea calculatorului
			t_inainte = int(round(time.time() * 1000))
			if tip_algoritm == '1':
				stare_actualizata = min_max(stare_curenta)
			else:  # tip_algoritm==2
				stare_actualizata = alpha_beta(-500, 500, stare_curenta)
			stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
			print("Tabla dupa mutarea calculatorului")
			print(str(stare_curenta.tabla_joc.matr))

			stare_curenta.tabla_joc.deseneazaEcranJoc(ecran)
			# preiau timpul in milisecunde de dupa mutare
			t_dupa = int(round(time.time() * 1000))
			print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

			stare_curenta.j_curent = Graph.jucator_opus(stare_curenta.j_curent)

if __name__ == "__main__" :
	main()