#######################################################
###     Définition des constantes et variables      ###
#######################################################

var V0 = 0
var V1 = 50                     # puissance du moteur : 30 > x > 600
var V2 = 150
var V3 = 350
var V4 = 400

var TEMPS_LED = 20              # temps d'allumage des led du dessus : 1000 > x > 2
var LED_AVANT = 0               # numéro de la LED du cercle, située à l'avant
var LED_DROITE = 2
var LED_GAUCHE = 6
var ALLUME = 32                 # intensité lumineuse des LED allumées : 32 > x > 0

var CHEMIN_DROITE = 3           # valeur définie pour indiquer que la direction de droite a été prise
var CHEMIN_GAUCHE = 1

var DELTA = 100                 # delta d'intensité lumineuse maximum sur feuille noire
                                # 900 > x > 0
                                # prox.ground.delta[0] : GAUCHE
                                # prox.ground.delta[1] : DROITE

var PROX1 = 4000                # valeur d'un capteur avec un objet très proche
var PROX2 = 3000
var PROX3 = 2000
var PROX4 = 1000


var i = 0
var j = 0

var chemin[100]                 # liste contenant le chemin emprunté par le robot avec une case par intersection
var cheminTaille = 0
var cheminCompteur = 0

var ledActive = -1
var ledCompteur = 0
var ledIntensite = ALLUME
var ledListe[] = [0, 0, 0, 0, 0, 0, 0, 0]

var etatR = 0                   # état des roues du robot
                                # 0 : n'avancent pas
                                # 1 : avancent droit
                                # 2 : tournent
var etatL = 0                   # état des LEDs
                                # 0 : affichent les directions
                                # 1 : affichent le chemin

        ### Remise à zéro des fonctions du robot
call sound.system(-1) # désactive du son
call leds.top(0,0,0)
call leds.bottom.left(0,0,0)
call leds.bottom.right(0,0,0)
call leds.circle(0,0,0,0,0,0,0,0)



###########################################
###     Sous-routines utilisées         ###
###########################################
###     LEDs    ###

#   allume la LED ledActive à l'intensité ledIntensité et met en route le timer qui l'appellera récursivement
#   le timer diminue l'intensité de la lumière toutes les TEMPS_LED ms, ce qui donne un effet lumineux
sub timer_led
    timer.period[0] = TEMPS_LED
    for ledCompteur in 0:7 do
        if ledCompteur == ledActive then
            ledListe[ledCompteur] = ledIntensite
        else
            ledListe[ledCompteur] = 0
        end
    end
    call leds.circle(ledListe[0], ledListe[1], ledListe[2], ledListe[3], ledListe[4], ledListe[5], ledListe[6], ledListe[7])

#   gère l'allumage des LEDs lorsque le robot est dans le labyrinthe pour afficher la direction qu'il prend
sub allumer_led_direction
    etatL = 0
    ledIntensite = ALLUME
    callsub timer_led

sub allumer_led_chemin
    etatL = 1
    if chemin[cheminCompteur] != 0 and cheminCompteur < cheminTaille then
        ledIntensite = ALLUME
        if chemin[cheminCompteur] == CHEMIN_DOITE then
            ledActive = LED_DROITE
        elseif chemin[cheminCompteur] == CHEMIN_GAUCHE then
            ledActive = LED_GAUCHE
        end
        callsub timer_led
    else
        etatL = 0
    end

sub stop
    etatR = 0
    motor.left.target = V0
    motor.right.target = V0

sub avancer
    etatR = 1
    ledActive = LED_AVANT
    callsub allumer_led_direction
    motor.right.target = V2
    motor.left.target = V2

sub tourner_droite
    etatR = 2
    ledActive = LED_DROITE
    callsub allumer_led_direction
    motor.right.target = V2
    motor.left.target = V3
    chemin[compteurChemin] = CHEMIN_DROITE
    compteurChemin++

sub tourner_gauche
    etatR = 2
    ledActive = LED_GAUCHE
    callsub allumer_led_direction
    motor.right.target = V3
    motor.left.target = V2
    chemin[cheminCompteur] = CHEMIN_GAUCHE
    compteurChemin++


###########################
###     Evènements      ###
###########################

onevent button.forward
    etatR = 0
    etatL = 0
    for i in 0:99 do
        chemin[i] = 0
    end
    i = 0
    callsub avancer

onevent button.center
    callsub stop

onevent timer0
    if etatL == 0 then
        if ledIntensite > 0 then
            ledIntensite -= 1
            callsub timer_led
        end
    elseif etatL == 1 then
        if ledIntensite > 0 then
            ledIntensite -= 1
            callsub timer_led
        else
            cheminCompteur++
            callsub allumer_led_chemin
        end
    end

onevent prox
    if etatR == 1 then
        if prox.ground.delta[0] > DELTA then
            callsub tourner_droite
        elseif prox.ground.delta[1] > DELTA then
            callsub tourner_gauche
        end
    elseif etatR == 2 then
        if prox.ground.delta[0] <= DELTA and prox.ground.delta[1] <= DELTA then
            callsub avancer
        end
    end
