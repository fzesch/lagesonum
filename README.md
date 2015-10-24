**A website created with Python Bottle and SQLite for entering and showing numbers with a timestamp. Used at LAGeSo in Berlin for helping refugees in the German registration process**
[www.lagesonum.de](http://www.lagesonum.de)

# Problem

Um in Deutschland registriert zu werden, müssen Flüchtlinge zunächst eine Nummer bekommen. Wann diese aufgerufen wird, ist schwer abzuschätzen und bisher nur vor Ort erkennbar. Die Lösung ist eine Internetseite, auf der Nummern eingetragen und abgerufen werden können. [Hintergrundartikel]( http://www.taz.de/Wartezeiten-am-Berliner-Lageso/!5228958/)

## Nutzerkreis

Die Internetseite soll von Flüchtlingen, die sich im LaGeSO registrieren wollen, genutzt werden, um herauszufinden, ob ihre Nummer schon aufgerufen wurde. Bisher stehen dort täglich mehrere hundert Menschen in der Warteschlange, um dies vor Ort zu erfahren. Freiwillige tragen dabei die Nummern ein.

# Funktionen

## Bestehende Funktionen

- Status der eigenen Nummer abfragen
- Nummern von Anzeigetafel eintragen
- Virtuelle Anzeigetafel mit eingegebenen Nummern

Die Nummern werden mit einem Fingerabdruck versehen, um die Glaubwürdigkeit eines Eintrags anhand der Zahl verschiedener Eingeber zu messen.

## Mögliche Erweiterungen 
Wir freuen uns über Beiträge (Pull Requests), die unsere [Issues](https://github.com/fzesch/lagesonum/issues) behandeln oder lösen. Diese sind am dringendsten.

Darüber hinaus gibt es größere Erweiterungen, die sinnvoll sind:
 
- Email-Benachrichtigung wenn Nummer aufgerufen wird
- Nutzerkonten mit Passwortverwaltung (oder Login über facebook)
- Validierte Eingabe vom LAGeSo (Verantwortliche können uns gerne kontaktieren, s.u.)
- SSL-Verschlüsselung der Internetseite


## Smartphone-Apps

Die Umsetzung als Android-App mit Push-Mitteilung geplant für [Refugeehackathon](http://www.refugeehackathon.de).

# Umsetzung

## Anforderungen
Die <a href="https://docs.google.com/document/d/1g8qLax2ScIFKubpZzflVgdy8Kvilo0ga94eelDZ8U-M/edit#">Anforderungen sind in einem Google-Dokument detailliert</a>.

## Technik
Die technische Umsetzung erfolgt mit dem Python-Webframework <a href="http://bottlepy.org/docs/dev/index.html">Bottle</a> und SQLite.

## Deployment
Es gibt eine [Anleitung, wie man das Projekt lokal zum Laufen bringt](INSTALL.md).

## i18n - Übersetzung und Internationalisierung

Es gibt eine gesondertes Dokument für i18n-Deployment im locales-Ordner.

# Kontakt

f.zesch@mailbox.org
