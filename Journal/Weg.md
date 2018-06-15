# Unser Weg

Unser erster Schritt bei dem neuen Projekt war es, uns eine Übersicht über unsere Aufgabenstellung zu verschaffen. Dabei hat uns das Dokument *Simulation von Bewegung Anregung zur Arbeitstechnik* sehr geholfen. 

Als nächstes haben wir das Runge-Kutta-Verfahren zweiter Ordung programiert. Dabei gab es vor Allem am Anfang Schwierigkeiten, das zweistufige Verfahren, was bei unserer Simulation für die Fortbewegung von Mond und Rakete in Relation zu der Erder von Nöten ist, richtig zu verstehen. Eine weitere Aufgabe war es die Anfangswerte und Konstanten in unserer Simulation zu recherchieren und zu berechnen wie zum Beispiel die Erd- oder die Mondmasse. Diese Werte sind von nöten um die Diffrenzialgleichen für das Zweikörperproblem aufzustellen und zu lösen. Somit können wir die korrekte Bahn des Mondes um die Erde, die von den Gravitationskräften beeinflusst wird, berechnen. Bei unserer Berechnung gehen wir davon aus, dass sich die Erde im Mittelpunkt bei den Koordinaten (0/0) befindet. Die Gravitationskräfte (der Erde und des Mondes) die sich auf die Rakete auswirken kann man praktisch auf die selbe Art berechnen. Für die Schubkraft, die einen Einfluss auf die Rakete hat, wird anhand von einem Vektor berechnet beziehungsweise sie fliegt in die Richtung des Vektors.
```python 
    # moon
    def rII_dgl(r):
        return ((-G * EARTH_MASS * MOON_MASS) / np.linalg.norm(r) ** 2) / REDUCED_MASS * r / np.linalg.norm(r)

    r = moon.pos - earth.pos
    v = moon.velocity - earth.velocity
    r_new, v_new = numerical_integrate(rII_dgl, r, v, dt / steps, steps)
    moon.pos = r_new
    moon.velocity = v_new

    # saturnV
    e_pos = earth.pos
    m_pos = moon.pos
    s_pos = saturnV.pos
    s_v = saturnV.velocity
    saturnV_fs = saturnV.fs
    print(saturnV.pos)
```
 
-Anfangswerte sameln / berechnen [x]
-zwei Dif.: Zweikörper numerisch, Position für Rakete berechnen  / Gravitations + Schubkraft(Vektor) Einwirkungen [x]
-bahngeschw. um auf bahn bleiben
-"porjektions Rechteck" Skalierung auf allen Bildschirm
-collison
