# Projet de ML/DL sur des séries temporelles de consommation électrique

Georges Hebrail et Alice Berard, employés d'EDF travaillant dans le pôle R&D, ont mis à disposition des données de consommation électrique des ménages de Sceaux, une ville située à 7 km de Paris. Ces données couvrent la période du 16 décembre 2006 au 26 novembre 2010. Bien que ces données n'aient pas été associées à une problématique particulière et qu'aucun papier de recherche n'ait été publié sur ce sujet, nous les considérons comme une excellente base de départ pour notre projet de Deep Learning sur des séries temporelles.

## Objectif
L'objectif de ce projet est d'optimiser la production d'électricité d'EDF en évitant la surproduction, ce qui permet de réduire les coûts et l'impact environnemental. En prévoyant les pics de consommation, il est également possible d'informer les ménages afin qu'ils puissent adapter leur consommation et réduire leur impact.

Nous prévoyons de prédire la puissance consommée active, qui représente l'énergie effectivement transformée et utilisée par les ménages. L'horizon de prédiction sera d'une minute.

## Jeu de données
Le jeu de données de consommation électrique fourni par le pôle R&D d'EDF contient les données de consommation électrique des ménages de Sceaux entre le 16 décembre 2006 et le 26 novembre 2010, à la minute près, pour un total de 2 049 280 observations.

La base de données brute est composée de 9 variables :

Date : La date (au format dd/mm/yyyy)
Time : L'heure (au format hh:mm:ss)
Global_active_power : La puissance active moyenne par minute dans l'ensemble du foyer (en kilowatts)
Global_reactive_power : La puissance réactive moyenne par minute dans l'ensemble du foyer (en kilowatts)
Voltage : La tension moyenne par minute (en volts)
Global_intensity : L'intensité de courant moyenne par minute dans l'ensemble du foyer (en ampères)
Sub_metering_1 : Le sous-compteur d'énergie n°1 (en watt-heures d'énergie active). Il correspond à la cuisine, contenant principalement un lave-vaisselle, un four et un micro-ondes (les plaques de cuisson ne sont pas électriques mais alimentées au gaz).
Sub_metering_2 : Le sous-compteur d'énergie n°2 (en watt-heures d'énergie active). Il correspond à la buanderie, contenant une machine à laver, un sèche-linge, un réfrigérateur et un éclairage.
Sub_metering_3 : Le sous-compteur d'énergie n°3 (en watt-heures d'énergie active). Il correspond à un chauffe-eau électrique et un climatiseur.
other_metering: Il correspond à toute autre consommation électrique

## Problématiques envisagées

Nous envisageons trois possibles problématiques pour ce sujet :

Prédire la puissance consommée active ;
Prédire la puissance consommée réactive ;
Prédire la puissance consommée apparente: $\sqrt(Global active power^2 + Global reactive power^2)$.
Dans tous les cas, l'objectif est d'optimiser la production d'électricité d'EDF en évitant la surproduction, ce qui permet de réduire les coûts et l'impact environnemental. En prévoyant les pics de consommation, il est également possible d'informer les ménages afin qu'ils puissent adapter leur consommation et réduire leur impact.

Après avoir effectué certaines recherches, nous avons appris que la puissance réactive est une puissance électromagnétique latente dans le réseau électrique, produite par des appareils tels que des bobines ou des moteurs. Cette énergie n'est pas facturée par EDF et suppose un coût, cependant elle est essentielle pour faire fonctionner ces types d'appareils. Cette puissance est stable dans le temps par construction et donc ne serait pas très intéressante à prendre comme cible.

Nous avons donc décidé de prédire la puissance consommée active.
