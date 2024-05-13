import pygame
from random import randint

class Peli:
    def __init__(self):
        pygame.init()
        self.leveys = 640
        self.korkeus = 480
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.lataa_kuvat()
        self.uusi_peli(2)
        pygame.display.set_caption("Mörköluola")
        self.naytto = pygame.display.set_mode((self.leveys,self.korkeus))
        self.kello = pygame.time.Clock()
        self.silmukka()

    def uusi_peli(self,hirviomaara,pisteet=0,taso=1):
        self.taso = taso
        self.kaynnissa = True #peli käynnissä
        self.nopeus = 3
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False
        self.ammuttu = False
        self.pisteet = pisteet
        self.maara = hirviomaara
        self.alkuperainenmaara = hirviomaara
        self.kohdat = []
        self.oviauki = False
        self.ovixy = (self.leveys/2-self.kuvat[2].get_width()/2,20)
        for _ in range(self.maara):
            self.kohdat.append([randint(-200,self.leveys+200-self.morko.get_width()) , randint(0,4) , True , randint(1,2), False])
            #                   aloituskohta (myöhemmin x-koordinaatti), mistä reunasta (myöhemmin y-koordinaatti), vasta luotu?, liikenopeus, tainnutettu?
        self.ammusx = self.ammusy = 0
        self.ammussxy = (0,10)
        self.x = 320 - self.robo.get_width()/2
        self.y = 240 - self.robo.get_height()/2

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["hirvio","kolikko","ovi","robo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
        self.robo = self.kuvat[3]
        self.morko = self.kuvat[0]

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN and self.kaynnissa:
                if tapahtuma.key == pygame.K_LEFT and self.kaynnissa:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT and self.kaynnissa:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP and self.kaynnissa:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN and self.kaynnissa:
                    self.alas = True
                if tapahtuma.key == pygame.K_SPACE and self.ammuttu == False and self.kaynnissa:
                    self.ammuttu = True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli(2)

            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku(self):
        if self.oikealle and self.x<640-self.robo.get_width():
            self.x += self.nopeus
        if self.vasemmalle and self.x>0:
            self.x -= self.nopeus
        if self.ylos and self.y>0:
            self.y -= self.nopeus
        if self.alas and self.y<480-self.robo.get_height():
            self.y += self.nopeus

    def ammus(self):
        if not self.ammuttu:        #jos ei ammuttu, aseta seuraavan ammuksen liikerata
            self.ammusx = self.x
            self.ammusy = self.y
            if self.vasemmalle and self.oikealle:
                pass
            elif self.vasemmalle:
                self.ammussxy = (-10,0)
            elif self.oikealle:
                self.ammussxy = (10,0)
            if self.ylos and self.alas:
                pass
            elif self.ylos:
                self.ammussxy = (0,-10)
            elif self.alas:
                self.ammussxy = (0,10)
            if self.ylos and self.vasemmalle:
                self.ammussxy = (-10,-10)
            if self.ylos and self.oikealle:
                self.ammussxy = (10,-10)
            if self.alas and self.vasemmalle:
                self.ammussxy = (-10,10)
            if self.alas and self.oikealle:
                self.ammussxy = (10,10)
        if self.ammuttu:                    #liikuta ammusta kun ammuttu
            self.ammusx += self.ammussxy[0]
            self.ammusy += self.ammussxy[1]
            if self.ammusx < -50 or self.ammusx > self.leveys+50-self.kuvat[1].get_width() or self.ammusy < -50 or self.ammusy > self.korkeus+50-self.kuvat[1].get_height():
                self.ammuttu = False

    def hirvio(self):
        self.poistettavat = []
        for i in range(self.maara):     #käy läpi möröt listassa, olisin varmaan voinut myös omat luokat tehdä möröille
            try:
                if self.kohdat[i][2] == True:   #jos hirviön ensimmäinen kerta
                    self.kohdat[i][2] = False
                    if self.kohdat[i][1] == 0:
                        self.kohdat[i][1] = self.kohdat[i][0]
                        self.kohdat[i][0] = -200
                    if self.kohdat[i][1] == 1:
                        self.kohdat[i][1] = self.kohdat[i][0]
                        self.kohdat[i][0] = self.leveys + 200
                    if self.kohdat[i][1] == 2:
                        self.kohdat[i][1] = -200
                    if self.kohdat[i][1] == 4:
                        self.kohdat[i][1] = self.korkeus + 200
            except:
                continue
            if not self.kohdat[i][4]:
                if self.kohdat[i][0] > self.x:
                    self.kohdat[i][0] -= self.kohdat[i][3]
                if self.kohdat[i][0] < self.x:
                    self.kohdat[i][0] += self.kohdat[i][3]
                if self.kohdat[i][1] > self.y:
                    self.kohdat[i][1] -= self.kohdat[i][3]
                if self.kohdat[i][1] < self.y:
                    self.kohdat[i][1] += self.kohdat[i][3]

                #jos pelaaja osuu mörköön VVVVV         
                if self.kohdat[i][0]+self.morko.get_width()/2 > self.x and self.kohdat[i][0]+self.morko.get_width()/2 < self.x + self.robo.get_width() and self.kohdat[i][1]+self.morko.get_height()/2 > self.y and self.kohdat[i][1]+self.morko.get_height()/2 < self.y + self.robo.get_height():
                    self.kaynnissa = False
                    #self.uusi_peli(2)

                #jos ammus osuu mörköön VVVVV
                if self.ammuttu and self.morko.get_rect(topleft=(self.kohdat[i][0], self.kohdat[i][1])).colliderect(self.kuvat[1].get_rect(topleft=(self.ammusx,self.ammusy))):
                    self.kohdat[i][4] = True
                    self.ammuttu = False
                    self.pisteet += 10
                    self.poistettavat.append(i)

        for x in self.poistettavat: #poista tainnutetut möröt
            self.kohdat.pop(x)
            self.maara -= 1

    def piirra_naytto(self):
        self.naytto.fill((100, 100, 100))

        if self.oviauki:
            self.naytto.blit(self.kuvat[2],self.ovixy)

        if self.kaynnissa:
            self.naytto.blit(self.robo, (self.x, self.y))

        for i in range(self.maara):
            if not self.kohdat[i][4]:
                self.naytto.blit(self.morko, (self.kohdat[i][0], self.kohdat[i][1]))

        if self.ammuttu:
            self.naytto.blit(self.kuvat[1],(self.ammusx,self.ammusy))

        teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, (255, 255, 255))
        self.naytto.blit(teksti, (500, 0))
        teksti = self.fontti.render(f"Taso: {self.taso}", True, (255, 255, 255))
        self.naytto.blit(teksti, (500, 24))
        teksti = self.fontti.render(f"Mörköjä: {self.maara}", True, (255, 255, 255))
        self.naytto.blit(teksti, (500, 48))

        teksti = self.fontti.render(f"Nuolet: liiku | Space: ammu", True, (255, 255, 255))
        self.naytto.blit(teksti, (0, 450))

        if not self.kaynnissa:
            teksti = self.fontti.render(f"Hävisit! Paina F2 aloittaaksesi uuden pelin", True, (255, 255, 255))
            self.naytto.blit(teksti, (0, 0))
        pygame.display.flip()
        self.kello.tick(60)

    def ovitarkistus(self):
        if self.maara == 0 and not self.oviauki:    #kun mörköjä ei ole, ja ovi ei ole vielä auki
            self.oviauki = True
        if self.oviauki and self.kuvat[2].get_rect(topleft=self.ovixy).colliderect(self.robo.get_rect(topleft=(self.x,self.y))): #kun pelaaja menee ovesta
            self.uusi_peli(self.alkuperainenmaara+1,self.pisteet,self.taso+1) #seuraava taso: enemmän mörköjä
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.liiku()
            self.ammus()
            self.hirvio()
            self.ovitarkistus() #onko möröt hoideltu
            self.piirra_naytto()

Peli()