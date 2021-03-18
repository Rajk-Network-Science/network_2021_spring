### 4. házi

Kötelező olvasmány:
- [Inferring User Demographics and Social Strategies in Mobile Social Networks](https://ericdongyx.github.io/papers/KDD14-Dong-et-al-WhoAmI-demographic-prediction.pdf)

Opcionális olvasmány:
- [A Study of Age and Gender seen through Mobile Phone Usage Patterns in Mexico](https://arxiv.org/pdf/1511.06656.pdf)

**Fő feladat: skálamentes hálózat generálása**

Generáljatok skálamentes hálózatokat, szám szerint 3-at:
- BA - modell
- Copy - modell
- Link selection - modell

Minden esetben:
- Lépésenként adj hozzá éleket, írj egy ciklust ami generál mondjuk egy 1000 csúcsból álló hálózatot.
- A kezdeti csúcsok száma legyen 20, ami legyen ER-gráf.
- A véletlen szimuláció legyen *reprodukálható*.
- Egy új csúcs adjon hozzá 3 élt. 
- Reprodukáljátok az 5.19 ábrát, ehhez mondjuk 10 lépésenként jegyezzétek fel a megfelelő mértékeket.

Ehhez networkX-et használjatok. Ha valamelyik megadott paraméter hülyeségnek bizonyul, változtasatok rajta nyugodtan, a lényeg, hogy mindhárom esetben ugyanazt használjátok, hogy hasonló hálózatok jöjjenek ki. Azért fontos ez a házi, mert hálózatok tulajdonságait a véletlennel összehasonlítva szokták tesztelni, ez itt most a base case előállítása.

Ennek a feladatnak a végrehajtásához elengedhetetlen, hogy részproblémára bontsátok a sztorit. Kb a következő lépések vannak:
- ER - hálózat generálása
- Egy csúcs hozzáadása egy meglévő hálózathoz (erre a 3 külön módszer)
- Eredmények feljegyzése
- Eredmények transzformációja
- Eredmények vizualizációja

Aki ezekről, vagy a háziban vizsgált hálózatról csinál egy szép vizuált [pyvisben](https://pyvis.readthedocs.io/en/latest/) hatalmas előrelépést tehet egy kiválóan megfelelt felé, viszont ez nem kötelező. 100k csúcs felett ez szerintem eléggé be fog akadni, alkalmazzatok valamilyen backbone extraction módszert, pl ezt: https://gist.github.com/clayadavis/724061da0f989bff6e7f25cbc21e63fa

**Egyebek: Gamma-becslés**

A múlt heti házban használt hálózatban mérjétek ki a gamma paramétert. Ehhez nem kell mást tenni, mint ráilleszteni egy egyenest a már meglévő scatterplotokra. Egyszerűen hangzik, de nem az! :) 

Lineáris regresszió pythonban: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

Arra is figyeljetek, hogy az elején még nem érvényesül a hatványszabály, ami torzítja a meredekséget. Próbáljátok meg tényleg csak a lineáris részéhez behúzni, annak a meredeksége a fontos.


Hajrá, jövő héten Skypeolunk!
