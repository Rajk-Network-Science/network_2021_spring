## GitHub és git használata

### 1. git
A git maga egy verzió-kontroll rendszer, amit arra használnak, hogy a fájlokon végzett módosítások jól visszakövethetőek legyenek. A kurzus során úgy fogtok kódot írni, hogy a módosításaitokat ebben a rendszerben rögzítitek. A gitet [itt tudjátok letölteni](https://git-scm.com/downloads). A letöltés utáni konfiguráció operációs rendszertől, illetve fehasználói preferenciáktól függően eltérhet. Ha valakinek ezzel gondja akad, keressetek minket vele nyugodtan!

A git szükséges ahhoz, hogy a saját gépetek és a GitHub repo között kommunikáni tudjatok, de egyébként teljesen offline is használható verzió-kontrollra (visszakövethető vele a lokális fájlok módosítása). A jobb megértésért [itt olvashatjátok](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F) a dokumentáció bemutatkozó részét.

### 2. GitHub, fork
A GitHub a gitre épülő felhő-szolgáltatás, ezt fogjuk használni a kurzusanyagok megosztásához és házileadáshoz. Lesz a kurzus repo-jának egy saját fiókotokhoz tartozó verziója, amit **fork**-nak hívunk. Ilyet a [kurzus repo](https://github.com/Rajk-Network-Science/network_2021_spring)-nál a jobb felső sarokban található ```Fork``` gombra kattintva tudtok készíteni:

<img scr="https://github.com/Rajk-Network-Science/network_2021_spring/blob/main/GitHub/github_fork.png">

### 3. Klónolás
Nyissátok meg a parancssort (Windows-on PowerShell, Mac-en és Ubuntu-n Terminal), és lépjetek be abba a mappába a saját gépeteken, ahova le szeretnétek tölteni a kurzus github repo-ját:
- Windows-on: ```Set-Location "mappa elérési útja/mappa neve"```
- Mac-en és Ubuntu-n: ```cd mappa elérési útja/mappa neve```

Ezután írjátok be a következő parancsot:
- ```git clone >link<```
A >link< helyére írjátok be, ami a saját fork-olt github repo-tokban megjelenik, ha a ```Clone or download``` gombra kattintotok:

<img scr="https://github.com/Rajk-Network-Science/network_2021_spring/blob/main/GitHub/github_clone.png">

## 4. Commit és pull request
Miután klónoltátok a mappát a gépetekre, másoljátok az adott feladatot (vagy csináljatok egy új notebookot) a **HÁZIK** mappán belül a saját nevetekkel ellátott mappába, és itt dolgozzatok. Miután kész vagytok az aktuális heti dolgokkal, megint nyissátok meg a paracssort, lépjetek be a kurzus mappájába, és a következő három paranccsal rögzítsétek a git rendszerében a módosításaitok, illetve töltsétek fel őket a GitHub-ra:
- ```git add .``` (ezt csak abban az esetben, ha minden változtatást commit-olni akartok, ellenkező esetben a . helyére az egyes mappák, fájlok neveit kell írni, elérési úttal együtt)
- ```git commit -m "valami üzenet"```
- ```git push```

Ha már minden fent van GitHub-on a saját repo-tokban, nyissatok egy pull request-et a kurzushoz tartozó repo felé, a ```Pull requests``` tabon a ```New pull request``` gombra kattintva:

<img scr="https://github.com/Rajk-Network-Science/network_2021_spring/blob/main/GitHub/github_pull.png">

### 5. Fork frissítése
A kurzus repo-jába folyamatosan kerülnek be új anyagok, házik, a többiek leadásai. Ahhoz, hogy mindig up-to-date legyen a lokális mappátok és a fork-otok GitHub-on, használjátok a következő parancsokat:
- ```git remote add upstream https://github.com/Rajk-Network-Science/network_2021_spring``` (ezt az elsőt csak egyszer kell megcsinálni, az alábbiakat pedig mindig, mikor frissítetek)
- ```git fetch upstream```
- ```git checkout master```
- ```git merge upstream/master```
- ```git push origin master```

Ha ez elakad, lehetséges, hogy van valami a GitHub-os repo-tokban, ami lokálisan nincs meg a gépeteken. Ebben az esetben először írjátok be az alábbi parancsot, és csak ezután a fentieket:
- ```git pull```

### 6. További infó
Azoknak, akiket részletesebben érdekel a téma, itt van egy bő félórás videósorozat a git és a GitHub használatáról: 
- [Learn git in 15 minutes](https://www.youtube.com/watch?v=USjZcfj8yxE)
- [Learn GitHub in 20 minutes](https://www.youtube.com/watch?v=nhNq2kIvi9s)
