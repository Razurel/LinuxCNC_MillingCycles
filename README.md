# LinuxCNC_MillingCycles

GladeVCP-Erweiterung für LinuxCNC (2.9.x) im AXIS-Display. Über vier Reiter (Rundloch, Rechteck,
Linie, Oberfläche) werden Vorschau-Programme (.ngc-Dateien) erzeugt, geprüft und direkt in AXIS
geladen. Geeignet für das Fräsen
auf einer 3-Achs-Maschine.

1. Überblick
  Die Bedienoberfläche liest alle Werte über HAL-Pins (milling_cycles.*) und erzeugt daraus ein GCode-Programm. Die Werte werden automatisch in UI_Save.txt gespeichert und beim nächsten Start
  wiederhergestellt. Es ist keine separate Installation von Software nötig – der gesamte Ordner wird als
  Einheit in die LinuxCNC-Konfiguration gelegt.

2. Voraussetzungen
  • LinuxCNC 2.9.x mit AXIS (die GladeVCP-Unterstützung ist enthalten)
  • Python 3 (bei LinuxCNC mitgeliefert)
  • Schreibrechte für den Zielordner (dort wird die .ngc-Datei abgelegt)


3. Installation

  3.1 Ordner kopieren
    Den kompletten Ordner MillingCycles/ (mit allen Dateien: milling_cycles.py, die *_handler.pyDateien, milling_cycles.ui, circle.py, rectangle.py, line.py, surface.py, ui_save.py, UI_Save.txt)
    als Gesamtheit nach <configs>/<deineKonfiguration>/MillingCycles/ kopieren. Zum Beispiel:
    linuxcnc/configs/MH22_Extra/MillingCycles/
    ├── milling_cycles.py (Haupt-Handler)
    ├── milling_cycles.ui (Benutzeroberfläche)
    ├── circle_handler.py (Rundloch)
    ├── rectangle_handler.py (Rechteck)
    ├── line_handler.py (Linie)
    ├── surface_handler.py (Oberfläche)
    ├── circle.py / rectangle.py / line.py / surface.py (G-Code-Generatoren)
    ├── ui_save.py (Speichern/Laden der Werte)
    └── UI_Save.txt (gespeicherte Werte)
    Hinweis: Der Ordner kann an einen beliebigen Ort gelegt werden, solange alle Dateien
    zusammenbleiben und der Pfad anschließend in der INI eingetragen wird. 
  
  3.2 INI-Datei anpassen
      In der Konfigurationsdatei (z. B. MH22_Extra.ini) im Abschnitt [DISPLAY] ergänzen:
    
    [DISPLAY]
    EMBED_TAB_NAME = MillingCycles
    EMBED_TAB_COMMAND = gladevcp -c milling_cycles -u MillingCycles/milling_cycles.py
     MillingCycles/milling_cycles.ui
    EMBED_TAB_LOCATION = north
    
    Parameter Bedeutung
    EMBED_TAB_NAME Name des Reiters, wie er in AXIS angezeigt wird.
    EMBED_TAB_COMMAND Startet GladeVCP mit dem Haupt-Handler und der UI.
    EMBED_TAB_LOCATION Anordnung des Reiters in AXIS (north / south / east / west).
    
    Der Komponentname hinter -c (milling_cycles) ist fest vorgegeben – die G-Code-Generatoren 
    lesen ihre Pins über diesen Namen (halcmd getp milling_cycles.circle_diameter usw.).
    Nur umbenennen, wenn der Name gleichzeitig in allen Dateien geändert wird.
    
    Liegt der Ordner nicht direkt im Konfigordner,
    kann auch ein absoluter Pfad eingetragen werden.
    Zum Beispiel:
    EMBED_TAB_COMMAND = gladevcp -c milling_cycles -u
    /home/$USER/linuxcnc/configs/MH22_Extra/MillingCycles/milling_cycles.py
    /home/$USER/linuxcnc/configs/MH22_Extra/MillingCycles/milling_cycles.ui
      
  3.3 HAL-Datei
    Keine Änderung nötig. Die HAL-Pins (milling_cycles.*) werden automatisch erzeugt, sobald der
    Reiter geladen wird. Alle Werte werden nur gelesen (halcmd getp), es müssen keine net- oder
    loadusr-Anweisungen ergänzt werden.
  
  3.4 Start
    LinuxCNC mit der angepassten INI starten. Der Reiter „MillingCycles" erscheint in AXIS und sollte
    sofort bedienbar sein.


4. Die vier Reiter

  4.1 Rundloch
    Fräst ein Rundloch (Bohrung) – sprich wahlweise eine Spirale (Helix) bis zur Endtiefe. Der Start
    erfolgt in der Mitte des Lochs.
    Eingabefeld Einheit Beschreibung
    Lochdurchmesser mm Durchmesser des fertigen Lochs.
    Lochtiefe mm Endtiefe des Lochs (positiv eingeben).
    Fräserdurchmesser mm Durchmesser des verwendeten Fräsers.
    Spiralensteigung mm/U Zustellung pro 360°-Umdrehung der Helix.
    Start Z über Werkstück mm Abstand des Werkzeugausgangspunkts über der Oberfläche.
    Rückzug zur Mitte mm Abstand, um den am Schluss zur Mitte zurückgefahren wird.
    Zustell-Feed (Z) mm/min Vorschub beim Zuschnitt senkrecht (Z-Achse).
    Schnitt-Feed (XYZ) mm/min
    Vorschub beim Spiral-/Rundfräsen in der Ebene. Bei der Helix steuert er
    auch die Z-Absenkung der Spirale.

  4.2 Rechteck
    Fräst eine Rechteckkontur – wahlweise eine Innenkontur (Tasche, Außenseite der Kontur) oder eine
    Außenkontur (Umriss des Werkstücks).
    Eingabefeld Einheit Beschreibung
    Fräserdurchmesser mm Durchmesser des verwendeten Fräsers.
    Rechteck-Breite mm Breite der Rechteckkontur (X).
    Rechteck-Tiefe mm Tiefe der Rechteckkontur (Y).
    Z-Zustellung mm Zustellung pro Schnittebene.
    Frästiefe mm Endtiefe der Rechteckkontur.
    Start Z über Werkstück mm Ausgangshöhe des Werkzeugs.
    Startpunkt – Anfahrpunkt: Links Oben / Rechts Oben / Mitte / Links Unten / Rechts Unten.
    Fräsart – Innenkontur (Tasche) oder Außenkontur (Umriss).
    Zustell-Feed (Z) mm/min Vorschub bei der Z-Zustellung.
    Schnitt-Feed (XY) mm/min Vorschub beim Umfahren der Kontur.

  4.3 Gerade Linie
    Fräst eine gerade Nut (Schlitz) in vorgegebener Länge, Tiefe und Richtung.
    Eingabefeld Einheit Beschreibung
    Fräserdurchmesser mm Durchmesser des verwendeten Fräsers.
    Schnittlänge mm Länge der Nut in Fräsrichtung.
    Frästiefe mm Endtiefe der Nut.
    Z-Zustellung mm Zustellung pro Schnittebene.
    Start Z über
    Werkstück
    mm Ausgangshöhe des Werkzeugs.
    Winkel °
    Frischrichtung (wie bei einer Uhr: 0° nach hinten, 90° nach rechts, 180°
    nach vorn, 270° nach links).
    Zustell-Feed (Z) mm/min Vorschub bei der Z-Zustellung.
    Schnitt-Feed (XY) mm/min Vorschub beim Längsfräsen.

  4.4 Oberfläche
    Fräst eine Fläche (z. B. Platte) mäanderförmig eben. Es werden Bahnen mit eingestellter
    Überlappung und Schrittweite gefahren.
    Eingabefeld Einheit Beschreibung
    Fräserdurchmesser mm Durchmesser des verwendeten Fräsers.
    Z-Zustellung mm Tiefenzustellung pro Schnittebene.
    Werkstück-Breite mm Breite des zu fräsenden Bereichs (X).
    Werkstück-Tiefe mm Tiefe des zu fräsenden Bereichs (Y).
    Frästiefe mm Endtiefe der Oberflächenbearbeitung.
    Start Z über Werkstück mm Ausgangshöhe des Werkzeugs.
    Überlappung % Überlappung der Bahnen (0–99 %).
    Startpunkt – Anfahrpunkt: Links Oben / Rechts Oben / Links Unten / Rechts Unten.
    Zustell-Feed (Z) mm/min Vorschub bei der Z-Zustellung.
    Schnitt-Feed (XY) mm/min Vorschub beim Bahnfahren.


5. Feeds – Zustell-Feed und Schnitt-Feed
    Pro Reiter gibt es zwei getrennte Vorschubwerte:
    • Zustell-Feed (Z) – langsamer Vorschub für das Eintauchen in Z-Richtung. Schützt vor
    Werkzeugbruch beim Zuschnitt.
    • Schnitt-Feed (XY) – Vorschub für die eigentliche Schnittbewegung in der Ebene (Konturen,
    Bahnen). Im Rundloch-Reiter als Schnitt-Feed (XYZ) beschriftet, weil der Spiral-G2-Satz die
    Maschine gleichzeitig in XY und Z bewegt und der Schnitt-Feed dabei auch die Z-Absenkung
    der Helix bestimmt.
    Beide Werte müssen größer als 0 sein – sonst bricht die Erzeugung mit einer Fehlermeldung ab.


6. Ablauf / Bedienung
  1. AXIS mit der angepassten INI starten – der Reiter „MillingCycles" ist sichtbar.
  
  2. Gewünschte Operation wählen und alle Werte eingeben (Maße, Feeds, Startpunkt usw.).
  
  3. Button [VORSCHAU AKTUALISIEREN] drücken. Dabei passiert Folgendes:
    • Alle SpinBox-Werte werden in die HAL-Pins geschrieben (milling_cycles.*).
    • Die Werte werden in UI_Save.txt gespeichert.
    • Der zugehörige G-Code-Generator (circle.py usw.) liest die HAL-Pins, prüft alle
      Eingaben und erzeugt eine .ngc-Datei im selben Ordner.
    • Die Datei wird automatisch in die laufende AXIS geladen (axis-remote).

  5. Das erzeugte Programm in der AXIS-Vorschau prüfen (Werkstücknullpunkt,Sicherheitsabstände).
  
  6. Werkstück einspannen, Referenzpunkte setzen und mit PLAY starten.
    Sicherheitshinweis: Die Vorschau ist ein fertiges Fräsprogramm. Vor dem Start immer den
    G-Code grafisch prüfen, Werkzeuglänge/-offset kontrollieren und die ersten Schnitte mit
    reduziertem Feed fahren.
  
  7. Gespeicherte Einstellungen (UI_Save.txt)
    Alle Werte der SpinBoxen werden beim Klick auf VORSCHAU AKTUALISIEREN in der Datei
    UI_Save.txt abgelegt (Format name=wert). Beim nächsten Start der Bedienoberfläche werden diese
    Werte automatisch wieder geladen. Wer nur einen Durchmesser ändert und danach mehrere
    gleichartige Teile fräst, muss die übrigen Werte nicht erneut eingeben.
    Auszug aus einer speicherdatei:
    circle_diameter=50.0
    circle_depth=20.0
    circle_feed_approach=100
    circle_feed_mill=200
    ...
    Die Datei kann auch von Hand bearbeitet werden (z. B. um Standardwerte zu setzen). Sie wird beim
    Vorschau-Klick des jeweiligen Reiters mit den aktuellen Werten aktualisiert.
  
  8. Fehlerbehebung und Unterstützung
  8.1 LinuxCNC aus dem Terminal starten
    Startest du LinuxCNC aus einem Terminal, erscheinen alle Meldungen der Bedienoberfläche (auch
    Python-Fehlermeldungen) direkt auf der Konsole und lassen sich lesen/kopieren:
    cd ~/linuxcnc/configs/<deineKonfiguration>
    linuxcnc <deineKonfiguration>.ini
    Beim normalen Start über das Menü wird die gleiche Ausgabe in die Datei ~/linuxcnc-debug.txt
    geschrieben. Zusätzlich zeigt AXIS das Ende des Protokolls an: Menü Machine → Show Log.
    • Python-Fehler (z. B. aus milling_cycles.py oder den *_handler.py-Dateien) erscheinen als
    Traceback mit Datei- und Zeilennummer.
    • Auch die „Vorschau wurde erzeugt…"-Meldungen und print-Ausgaben der Handler erscheinen dort.
  8.2 HAL-Pins auslesen (Werte prüfen)
    Solange LinuxCNC läuft (z. B. in einem zweiten Terminal), kannst du die übermittelten Werte direkt
    aus dem HAL auslesen. Das ist nützlich, um zu sehen, ob die Werte aus der Bedienoberfläche korrekt
    ankommen:
    # Alle Pins des MillingCycles-Komponenten auflisten
    halcmd show pin milling_cycles
    # Einen einzelnen Wert auslesen
    halcmd getp milling_cycles.circle_diameter
    halcmd getp milling_cycles.circle_feed_approach
    halcmd getp milling_cycles.surface_overlap
    Die Pins heißen milling_cycles.<reiter>_<feld>. Wichtige Pins kennen die *_handler.py-Dateien
    (alle Feldnamen der Reiter). Grafik-Nutzer finden dieselben Werte in AXIS unter Menü Machine →
    Show HAL Configuration (Suchfeld „milling_cycles").

    Zu erwartende Pins je Reiter:
    Reiter HAL-Pins
    Rundloch circle_diameter, circle_depth, circle_cutter_diameter, circle_pitch,
    circle_start_z, circle_retract, circle_feed_approach, circle_feed_mill
    Rechteck
    rectangle_cutter_diameter, rectangle_width, rectangle_depth, rectangle_z_step,
    rectangle_milling_depth, rectangle_start_z, rectangle_feed_approach,
    rectangle_feed_mill
    Linie
    line_cutter_diameter, line_length, line_depth, line_z_step, line_start_z,
    line_angle, line_feed_approach, line_feed_mill
    Oberfläche
    surface_cutter_diameter, surface_z_step, surface_width, surface_depth,
    surface_milling_depth, surface_start_z, surface_overlap, surface_feed_approach,
    surface_feed_mill
    Tipp: Erscheinen im show pin-Befehl überhaupt keine milling_cycles.*-Pins, ist die
    Bedienoberfläche nicht geladen worden (Reiter fehlt) oder der Komponentname wurde
    geändert.

  8.3 Häufige Fehler
    Problem Ursache / Lösung
    Reiter „MillingCycles" erscheint
    nicht in AXIS
    INI-Sektion prüfen (Rechtschreibung, freigesetzte Zeilen).
    Fehlerausgabe im Terminal bzw. in ~/linuxcnc-debug.txt ansehen.
    „… konnte nicht aus der
    Bedienoberfläche gelesen werden"
    Der HAL-Pin existiert nicht – die Bedienoberfläche wurde nicht
    gestartet oder der Komponentname milling_cycles wurde geändert.
    Mit halcmd show pin milling_cycles prüfen.
    „… muss größer als 0 sein"
    Ein Eingabewert ist ≤ 0 (z. B. Feed, Durchmesser). Positiven Wert
    eingeben; ggf. Pin-Wert in HAL prüfen.
    „Die Vorschau wurde erzeugt,
    konnte aber nicht in AXIS geladen
    werden"
    AXIS läuft nicht oder axis-remote ist nicht verfügbar. Den VorschauButton erneut drücken, während AXIS offen ist.
    Gespeicherte Werte werden nicht
    übernommen
    Datei UI_Save.txt existiert nicht oder ist beschädigt → neue Datei mit
    Standardwerten anlegen bzw. Ordner neu kopieren.
    Falsche Werte beim Fräsen
    Werkzeugreferenz/Nullpunkt in AXIS prüfen – die Bedienoberfläche
    liefert nur die Geometrie, nicht den Maschinennullpunkt.
    Werte kommen nicht im HAL an
    Werte werden erst beim Klick auf VORSCHAU AKTUALISIEREN
    geschrieben – vorher sind die Pins 0.

  8.4 Fehler gut melden (für den Entwickler / Foren)
    Damit ein Fehler schnell nachvollzogen werden kann, beim Melden möglichst mitliefern:
    1. Den Text der Fehlermeldung bzw. den Traceback aus dem Terminal oder aus ~/linuxcncdebug.txt.
    2. Die Ausgabe von halcmd show pin milling_cycles (mit den ausgelesenen Werten).
    3. Die LinuxCNC-Version: linuxcnc --version.
    4. Den verwendeten Eintrag in der [DISPLAY]-Sektion der INI.
    MillingCycles – GladeVCP-Erweiterung für LinuxCNC. Entstanden aus der Fräszyklen-Vorlage (Ordner Vorlage/). Diese
    Anleitung gilt für die Version mit vier Reitern, getrennten Feeds (Zustell-/Schnitt-Feed) und automatisch gespeicherten
    Einstellungen. 
