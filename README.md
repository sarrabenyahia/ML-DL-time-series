# Projet de ML/DL sur des séries temporelles de consommation électrique


## Sommaire

0. [Introduction](#introduction)
1. [Objectif](#objectif)
2. [Jeu de données](#jeu-de-données)
3. [Problématiques envisagées](#problématiques-envisagées)
4. [Conclusion](#conclusion)

## Introduction
Georges Hebrail et Alice Berard, employés d'EDF travaillant dans le pôle R&D, ont mis à disposition des données de consommation électrique des ménages de Sceaux, une ville située à 7 km de Paris. Ces données couvrent la période du 16 décembre 2006 au 26 novembre 2010. Bien que ces données n'aient pas été associées à une problématique particulière et qu'aucun papier de recherche n'ait été publié sur ce sujet, nous les considérons comme une excellente base de départ pour notre projet de Deep Learning sur des séries temporelles.

Vous retrouverez les données [ici](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption#).
Il faudra créer un fichier data où vous stockez la donnée dans celui-ci.

## Objectif
L'objectif de ce projet est d'optimiser la production d'électricité d'EDF en évitant la surproduction, ce qui permet de réduire les coûts et l'impact environnemental. En prévoyant les pics de consommation, il est également possible d'informer les ménages afin qu'ils puissent adapter leur consommation et réduire leur impact.

Nous prévoyons de prédire la puissance consommée active, qui représente l'énergie effectivement transformée et utilisée par les ménages. L'horizon de prédiction sera d'une minute.

## Jeu de données
Le jeu de données de consommation électrique fourni par le pôle R&D d'EDF contient les données de consommation électrique des ménages de Sceaux entre le 16 décembre 2006 et le 26 novembre 2010, à la minute près, pour un total de 2 049 280 observations.

La base de données brute est composée de 9 variables :

- Date : La date (au format dd/mm/yyyy)
- Time : L'heure (au format hh:mm:ss)
- Global_active_power : La puissance active moyenne par minute dans l'ensemble du foyer (en kilowatts)
- Global_reactive_power : La puissance réactive moyenne par minute dans l'ensemble du foyer (en kilowatts)
- Voltage : La tension moyenne par minute (en volts)
- Global_intensity : L'intensité de courant moyenne par minute dans l'ensemble du foyer (en ampères)
- Sub_metering_1 : Le sous-compteur d'énergie n°1 (en watt-heures d'énergie active). Il correspond à la cuisine, contenant principalement un lave-vaisselle, un four et un micro-ondes (les plaques de cuisson ne sont pas électriques mais alimentées au gaz).
- Sub_metering_2 : Le sous-compteur d'énergie n°2 (en watt-heures d'énergie active). Il correspond à la buanderie, contenant une machine à laver, un sèche-linge, un réfrigérateur et un éclairage.
- Sub_metering_3 : Le sous-compteur d'énergie n°3 (en watt-heures d'énergie active). Il correspond à un chauffe-eau électrique et un climatiseur.
other_metering: Il correspond à toute autre consommation électrique

## Problématiques envisagées

Nous envisageons trois possibles problématiques pour ce sujet :

- Prédire la puissance consommée active ;
- Prédire la puissance consommée réactive ;
- Prédire la puissance consommée apparente: $\sqrt(Global active power^2 + Global reactive power^2)$.

Dans tous les cas, l'objectif est d'optimiser la production d'électricité d'EDF en évitant la surproduction, ce qui permet de réduire les coûts et l'impact environnemental. En prévoyant les pics de consommation, il est également possible d'informer les ménages afin qu'ils puissent adapter leur consommation et réduire leur impact.

Après avoir effectué certaines recherches, nous avons appris que la puissance réactive est une puissance électromagnétique latente dans le réseau électrique, produite par des appareils tels que des bobines ou des moteurs. Cette énergie n'est pas facturée par EDF et suppose un coût, cependant elle est essentielle pour faire fonctionner ces types d'appareils. Cette puissance est stable dans le temps par construction et donc ne serait pas très intéressante à prendre comme cible.

Nous avons donc décidé de prédire la puissance consommée active.

## Conclusion

Nous avons finalement choisi de comparer deux types de modèles :

- LightGBM (LGBM), un algorithme d'apprentissage automatique ensembliste basé sur des arbres de décision boostés, qui a prouvé son efficacité dans de nombreuses tâches de prédiction ;
- ConvLSTM, un modèle hybride qui combine les avantages des réseaux de neurones convolutifs (CNN) et des LSTM (Long Short-Term Memory), adapté pour les données séquentielles, comme les séries temporelles.

Le modèle LGBM est un modèle basé sur des arbres de décision, ce qui lui permet de capturer des relations non linéaires et de gérer efficacement les données manquantes. Il utilise un ensemble de modèles faibles pour créer un modèle fort et peut être utilisé pour la classification et la régression. Dans notre cas, nous l'utilisons pour la régression afin de prédire la puissance consommée active.

Le modèle ConvLSTM, quant à lui, est un réseau de neurones hybride qui combine les avantages des CNN et des LSTM. Les CNN sont particulièrement efficaces pour extraire des caractéristiques à partir de données séquentielles, tandis que les LSTM peuvent modéliser les dépendances à long terme dans les données séquentielles. Le modèle ConvLSTM peut donc être particulièrement adapté pour la prédiction de séries temporelles.

Nous allons comparer les performances de ces deux modèles pour la prédiction de la puissance consommée active.

