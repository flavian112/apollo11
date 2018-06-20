## Zielsetzung & Motivation

Unser Ziel ist es mit Tkinter und Pygame ein Programm zu schreiben, dass eine Mondlandung simulieren kann. Bei dieser Simulation soll das Raumschiff zuerst zum Mond geschickt werden und in dessen Umlaufbahn "parken". Anschliessend soll eine Landefähre ausgeschickt werden, die mit der Hilfe eines Antriebes sanft auf dem Mond landet.  
Der Grund wieso wir dieses eher anspruchsvolles Projekt gewählt haben, ist zum Einem weil wir  von Herr Kambor dazu motiviert wurden zum Anderen weil uns die Mondlandung fasziniert und weil wir uns gefragt haben, welche physikalischen Gesetze man bei einer Raumfahrt zum Mond beachten muss.


## Unser Weg

Unser erster Schritt bei dem neuen Projekt war es, uns eine Übersicht über unsere Aufgabenstellung zu verschaffen. Dabei hat uns das Dokument *Simulation von Bewegung Anregung zur Arbeitstechnik* geholfen und wir haben im folgenden Punkt aufgeliestet, welche Teilaufgaben es zu bewältigen gilt, um die Simulation korrekt darzustellen. </br>
Es braucht:
* Anfangswerte und Konstanten
* Ein Runge-Kutta-Verfahren für das Lösen der Differenzialgleichung, damit man die Position und die folgende Position des Mondes und der  Rakete annäherungsweise berechnen kann
* Differenzialgleichung für das Zweikörperproblem
* Kollisionserkennung
* Eine passende Geschwindigkeit der Rakete, damit diese aus der Umlaufbahn um die Erde entweichen kann und dann anschliessend auf der Umlaufbahn um den Mond «geparkt» werden kann.
* Eine passende Schubkraft, damit die Landefähre sanft auf der Oberfläche des Mondes landen kann

### Anfangswerte und Konstanten
Eine weitere Aufgabe war es die Anfangswerte und Konstanten in unserer Simulation zu recherchieren und zu berechnen wie zum Beispiel die Erd- oder die Mondmasse. Diese Werte sind von Nöten um die Diffrenzialgleichungen für das Zweikörperproblem aufzustellen und zu lösen.

### Das Runge-Kutta-Verfahren
Als nächstes haben wir das Runge-Kutta-Verfahren zweiter Ordnung programmiert. Dabei gab es vor Allem am Anfang Schwierigkeiten, das zweistufige Verfahren, was bei unserer Simulation für die Fortbewegung von Mond und Rakete in Relation zu der Erde von Nöten ist, richtig zu verstehen. 

### Das Zweikörperproblem
Mit den zuvor gesammelten Daten können wir die korrekte Bahn des Mondes um die Erde, die von den Gravitationskräften beeinflusst wird, berechnen. Bei unserer Berechnung gehen wir davon aus, dass sich die Erde im Mittelpunkt bei den Koordinaten (0/0) befindet. Die Gravitationskräfte (der Erde und des Mondes) die sich auf die Rakete auswirken kann man praktisch auf dieselbe Art berechnen. Für die Schubkraft, die einen Einfluss auf die Rakete hat, wird anhand von einem Vektor berechnet beziehungsweise sie fliegt in die Richtung des Vektors.

### Skalierung 
Damit grafisch alles Korrekt, das heisst alles in der richtigen oder in der gewollten Grösse, angezeigt wird, ist es notwendig das die Objekte Erde und Mond abhängig von der Grösse des Projektions-Rechtecks, auf dem sich unsere Animation abspielt, zu machen. 

### Kollisionserkennung
Ein weiterer Aspekt ist es, Kollisionen zu erkennen bzw. heraus zu finden, wann die Rakete "auf der Erde ist" und sich nicht einfach "in die Erde" oder "durch den Mond" bewegt. Das Problem haben wir so gelöst, indem wir die Distanz zwischen einem Punkt der Rakete und dem Mittelpunkt des Mondes oder der Erde berechnet haben und dieser sollte immer grösser als der Radius des jeweiligen Himmelskörpers sein.

