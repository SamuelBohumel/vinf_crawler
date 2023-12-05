## Samuel Bohumel (samuel.bohumel) - Private Space 


## Konzultacia č. 1 
Po prvej konzultacii

## Konzultácia č. 2 

19.10.2023 - Pseudokód doplní, crawloval dáta, používa regex. Do budúcej konzultácie doplní parsovanie, začne indexovanie pomocou PyLucine.


Pseudokód:

1.  crawl celého archívu podľa mesiacov, na každej stránke sú linky na články\
2.  uloženie linkov do súboru.\
3.  prechádzanie linkov a stiahnutie raw html každého článku do samostatného súboru.\
4.  Parsovanie - prejdenie každého súroru a uloženie textov (paragrafov) do jedného súboru.\
5.  Indexácia.\

## Konzultácia číslo 3 

9.11.2023 - Dáta má indexované. Do budúcej konzultácie pridá spojenie s wikipédiou a príprava na prezentáciu.

## Prezentácia + Konzultácia číslo 4 

24.11.2023 - Prezentácia OK. Študent má spojenie s wikipédiou cez Spark pomocou paralelného spracovania. Do budúcej konzultácie dorobiť unit testy a príprava na záverečné odovzdanie projektu.

## Dokumentácia projektu 
Rozhodol som sa spracovať dáta na stránke www.space.com, na ktorej sú vedecké články s vesmírnou tématikou. Tu je môj postup riešenia

### Získanie dát 
1.  crawl celého archívu podľa mesiacov, na každej stránke sú linky na články \
2.  uloženie linkov do samostatného súboru.\
3.  prechádzanie linkov a stiahnutie raw html každého článku do samostatného súboru.\
Po tomto kroku mám všetky dáta v jednom priečinku, každý článok je v samostatnom súbore.
### Parsovanie dát 
Najprv som si dáta spojil do jedného súboru, aby som v procese čistenia ušetril čas, keďže otvorenie a zatvorenie súboru je časovo najnáročnejšia operácia (Po rade cvičiaceho). Behom tohto procesu som si zároveň aj čistil dáta, bral som len obsah html tabu <p></p>, keďže som chcel pracovať len s článkami. V tomto súbore som jednotlivé články rozdeili svojim delimiterom (----------) \
Túto časť som robil pomocou apache spark, ktorý mám rozbehaný lokálne - submitol som job - python skript ktorý to robí. \
Po tom čo som mal dáta v jednom súbore som súbor prešiel ešte raz a údaje som si uložil do formátu json - je to pole objektov, kde klúč je názov článku a hodnota je samotný článok.

### Obohatenie dát 
V rámci obohatenia dát som si pomocou knižnice rake_nltk vytiahol kľúčové slová z každého článku. Tie som následne spojil a odstránil duplicitné. \
Následne som tieto kľúčovné slová spájal s extrahovaným dumpom z wikipedie - xml súbor som si prerobil na json formát a ten prerobil na slovník v pythone, ktorý je viac krát vnorený (tak ako bola štruktúra toto XMLka). \
Potom som si v tomto dictionary našiel kľúčové slová ktoré som našiel a extrahoval tabuľky s údajmi. Tie sú k dispozícii vo finálnom hladaní.

### Logika vyhľadávania 
V rámci vyhľadávania som si vytvoril grafické používateľské rozhranie kvôli príjemnejšej skúsenosti.
V podstate môj program fuguje na dvoch spôsoboch vyhľadávania:
#### Hľadanie relevantného článku 
V tomto móde vezmem vstup (query) a použijem ho s vyhľadávaním PyLucene. Všetky články aj s nadpismi mám naindexované. Potom už používam IndexSearcher. 
#### Hľadanie parametrov z wikipedie 
V tomto type som si určil svoj formát query ktorú treba zadať: \
info:<keyword>|<argument> \
Po napísaní info:<keyword> sa vyhľadá kľúčové slovo v získaných dátach, v prípade úspechu a nájdenia sa zobrazia riadky vo formáte \
<parameter>: hodnota \
Následne je možné pridaním znaku "alebo" (|) dopísať parameter. Príklad použitia: \
dopyt - "info:sun|mass" \
výsledok - "Mass: 1.9885×1030kg"

### Unit testy 
Väčšina mojich testov sa zamerala na spomínané hľadanie parametrov. Testoval som však aj relevanciu nájdených článkov pomocou kľúčových slov.
