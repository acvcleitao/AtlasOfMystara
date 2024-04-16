# Atlas of Mystara
#teshis #work #IST #AtlasOfMystara #DnD #tese

## Documents
[[1st Contact]]
[[1st Contact Feedback]]
[[1st Contact V2]]


## Objectives
[[DnD|Dungeons & Dragons]] was the very first role-playing game in the world, and will be 50 years old next year. Over time, it has gone through many versions (OD&D, D&D, AD&D eds. 1-5). Although the rules were adjusted many times, one thing remains consistent: the existence of campaign settings. Early on, adventures were all home-brewed and each DM created their own setting. TSR then made some of the settings from early adopters and TSR founders/employees official. Grayhawk was Gary Gygax\`s setting. Blackmoor was Dave Arneson\`s. These early campaign settings still resonate nowadays. Mordenkainen, of "Mordenkainen\`s Sword" fame, was Gygax\`s PC in Grayhawk, for instance! 
 
In this context, one of the very first settings was the Known World, later called Mystara. Originally tied to D&D, it was the setting many players in the early 80\`s adventured in, years before the appearance of more famous ones such as Dragonlance, weirder ones such as Dark Sun or Planescape, and certainly before the now-ubiquitous but rather vanilla Forgotten Realms. Unlike Faerûn, though, the plainer of the plain high-fantasy settings (ok, the Underdark is cool...), and perhaps because people were still experimenting with things back then, Mystara is a lively, strange but interesting mix-match of cultures and countries. 
 
One of the big things for Mystara players were always maps and politics. In fact, apart from all the info you got from rulebooks and adventure modules, a series of books, called Gazetters, was published detailing individual countries, geographically, economically and politically (https://www.drivethrurpg.com/product/16974/GAZ1-The-Grand-Duchy-of-Karameikos-Basic). A boxed set, "Dawn of the Emperors", detailed the two big superpowers in the central region of the Known World, Thyatis and Alphatia. Later, "Champions of Mystara: Heroes of the Princess Ark" expanded this knowledge to other regions of the world (and beyond). And, let us not forget, this planet is hollow, and if you go through the polar openings, you\`ll find yourself in the Hollow World, where Mystara\`s Immortals preserve old civilizations. 
 
All of these materials came with hexmaps. Sometimes they changed a bit from product to product. Sometimes they were changed by cataclysmic events as in-game time moved on. But, still, looking at one is looking at a living world. 
 
Although the setting hasn't had official support pretty much since WotC bought TSR, there is still, to this day, an active community of Mystaran fans. They have produced more gazetteers, more maps, more adventures, a magazine! All is accessible in the big hub for all Mystaran things, the Vaults of Pandius (http://pandius.com/) 
 
The focus of this thesis are the maps. There were lots of paper maps. Thorfinn Tait, cartographer extraordinaire, has been creating digital versions for decades, now, and collecting them in the Atlas of Mystara (https://mystara.thorfmaps.com/). He has georeferenced many regions, solved inconsistencies, etc. What do we want to do? Well, these maps are, mostly, just pictures, right now. Also, they cover only a small part of the planet, but other cartographers and DMs have created maps for other regions that are more or less accepted by the community. So, what we want to do here is: 
 
1) properly index available maps 
2) parse those maps and get "beyond dumb pictures", by finding out which hexes, towns, etc are at each lat/lon (*)  
3) create a webmap that integrates all available maps (think: Google Maps for Mystara) 
 
(*) easier than it sounds, as Thorf has gone to great lengths already to tackle the normalization aspect of this (https://mystara.thorfmaps.com/appendix-l/) 
 
Step 1 is essentially to go through the Atlas and Vaults and see what is there (both these sites are indexed, so it should not be that hard) 
Step 2 will probably imply some image processing to identify hex types etc. but this is not really rocket science, as we\`re dealing with, essentially, uniform grids of hexes with a pre-determined list of possible contents (plains, mountains, etc.). In some cases, yes, some manual checking of out-of-bounds cases will be necessary, alas. 
Step 3 will use all this information to create the map, using whatever information is available, in a way In which if Thorf or some other cartographer creates a new map, we can just "drop it in there"


## Requirements

Must have played Dungeons & Dragons or a similar RPG in the past. This is important for us to have a shared language when discussing these matters. Didn\`t understand (or got interested by) the description above? Maybe this subject is not for you...  
 
We\`re going to do a webmap, so knowledge of web technology (HTML, CSS, JS) is important. We will probably be using SVG as well so that is also important. 
 
Having taken the InfoVis course will help with the above and with knowledge of D3, which may end up being relevant here, as well. 
 
And, it should go without saying, a love for fantasy maps will certainly help! 
 
Finally: are you applying to this thesis? Get in touch, we should talk (don\`t just select it on Fenix and wait for the magic to happen).

## Valuable links
### [Mapping tools](https://assets.adobe.com/public/c5d6e7cc-9441-453d-7965-795dcaef8c54)
Thorfinn made a bunch of tools available including tile sets and guides on how to create maps. It's a valuable resource to use as a reference to identify hexes in his maps
[Link to the post](https://www.thorfmaps.com/tools/)

### [Lining up Mystara 1 (2015)](https://www.thorfmaps.com/lining-up-mystara-i/)
This section has a ton of links to many maps
In this series of posts, I’m going to work through all of Mystara’s overland maps, connecting them up and resolving problems.  Also responding to feedback from the community and adjusting as necessary.  The end result will be a coherent set of maps that fix the respective locations of all the land masses on Mystara, as well as locking in latitudes and longitudes, global dimensions, and the exact location and composition of the polar lips between the Outer and Hollow Worlds.  This will enable the georeferencing of Mystara, which opens up lots of fun possibilities for future maps.

First let’s take stock of the known issues.  Resolved issues will be struck off with links to relevant articles as we cover them.

- ~~How 8 mile per hex maps interlock with 24 mile per hex maps~~:
    - ~~Known World/Great Waste~~ ([Lining Up Mystara II](http://www.thorfmaps.com/lining-up-mystara-ii/))
    - ~~Great Waste/Gulf of Hule~~ ([Mystara Reborn post](https://www.facebook.com/groups/mystara.reborn/permalink/1063364303708134/))
    - ~~Serpent Peninsula~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
    - ~~Orc’s Head Peninsula~~ ([Mystara Mapping Issues](http://www.thorfmaps.com/mystara-mapping-issues/), [Orc’s Head Peninsula and Trident Bay](http://www.thorfmaps.com/orcs-head-peninsula-and-trident-bay/), [Savage Coast Trail Map](http://www.thorfmaps.com/savage-coast-trail-map/))
    - ~~Isle of Dawn~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
- ~~How 24 mile per hex maps interlock with each other~~:
    - ~~Known World/Great Waste~~ ([Lining Up Mystara II](http://www.thorfmaps.com/lining-up-mystara-ii/))
    - ~~Great Waste/Hule~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/); for link with 8 mile per hex maps, see [Mystara Reborn post](https://www.facebook.com/groups/mystara.reborn/permalink/1063364303708134/); also see [Piazza post](http://www.thepiazza.org.uk/bb/viewtopic.php?f=3&t=14611) about Great Escarpment)
    - ~~Isle of Dawn/Alphatia~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
    - ~~Isle of Dawn/Ochalea~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
    - ~~Isle of Dawn/Pearl Islands~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
    - ~~Isle of Dawn/Alatian Islands~~ ([Lining Up Mystara III](http://www.thorfmaps.com/lining-up-mystara-iii/))
    - ~~Norwold/Known World & Northlands~~ ([Lining Up Mystara VII](http://www.thorfmaps.com/lining-up-mystara-vii/))
    - ~~Davania~~ ([Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/))
- ~~How 24 mile per hex maps interlock with 72 mile per hex maps~~:
    - ~~Known World, Isle of Dawn, Alphatia, Ochalea & Pearl Islands, Alatians, Serpent Peninsula~~ (obsolete; use 24 mile per hex maps)
    - ~~Alphatia/Bellissaria/Esterhold~~ ([Lining Up Mystara IV](http://www.thorfmaps.com/lining-up-mystara-iv/), [Lining Up Mystara V](http://www.thorfmaps.com/lining-up-mystara-v/))
    - ~~Davania~~ ([Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/))
    - ~~Norwold~~ ([Lining Up Mystara VII](http://www.thorfmaps.com/lining-up-mystara-vii/))
- ~~How 72 mile per hex maps interlock with each other~~:
    - ~~Overall~~ ([Lining Up Mystara V](http://www.thorfmaps.com/lining-up-mystara-v/))
    - ~~Davania~~ ([Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/))
- ~~How the world map lines up with the hex maps~~ ([Lining Up Mystara XI](http://www.thorfmaps.com/lining-up-mystara-xi/), [Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/), [Lining Up Mystara XV](http://www.thorfmaps.com/lining-up-mystara-xv/), [Lining Up Mystara XVI](http://www.thorfmaps.com/lining-up-mystara-xvi/), [Lining Up Mystara XVII](http://www.thorfmaps.com/lining-up-mystara-xvii/), [Lining Up Mystara XVIII](http://www.thorfmaps.com/lining-up-mystara-xviii/))
- ~~Latitudes~~ ([Lining Up Mystara IX](http://www.thorfmaps.com/lining-up-mystara-ix/), [Lining Up Mystara X](http://www.thorfmaps.com/lining-up-mystara-x/), [Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/), [Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/))
    - ~~Position of equator~~ ([Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/), [Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/), [Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/))
    - Exact latitudes of major cities ([Lining Up Mystara XII](http://www.thorfmaps.com/lining-up-mystara-xii/), [Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/), [Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/))
    - Definition of latitude on Mystara ([Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/))
- Longitudes
- ~~Axial Tilt~~ ([Axial Tilt thread at The Piazza](http://www.thepiazza.org.uk/bb/viewtopic.php?f=22&t=8423), [Lining Up Mystara IX](http://www.thorfmaps.com/lining-up-mystara-ix/))
- Polar Openings
    - ~~Location of start of Polar Lip~~ ([Lining Up Mystara IX](http://www.thorfmaps.com/lining-up-mystara-ix/), [Lining Up Mystara X](http://www.thorfmaps.com/lining-up-mystara-x/))
    - Latitude within the Polar Openings ([Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/))
    - ~~What land falls within the Polar Openings~~ ([Lining Up Mystara IX](http://www.thorfmaps.com/lining-up-mystara-ix/), [Lining Up Mystara X](http://www.thorfmaps.com/lining-up-mystara-x/), [Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/), [Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/), [Lining Up Mystara XV](http://www.thorfmaps.com/lining-up-mystara-xv/), [Lining Up Mystara XVI](http://www.thorfmaps.com/lining-up-mystara-xvi/), [Lining Up Mystara XVII](http://www.thorfmaps.com/lining-up-mystara-xvii/))
    - How to map these regions
- ~~Global dimensions~~ ([Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/), [Lining Up Mystara XIV](http://www.thorfmaps.com/lining-up-mystara-xiv/), [Lining Up Mystara XIX](http://www.thorfmaps.com/lining-up-mystara-xix/))
- ~~Hollow World~~: ([Lining Up Mystara XIII](http://www.thorfmaps.com/lining-up-mystara-xiii/))
    - ~~How Iciria’s 40 mile per hex map corresponds to the Hollow World map~~ ([Lining Up Mystara XVI](http://www.thorfmaps.com/lining-up-mystara-xvi/), [Lining Up Mystara XVII](http://www.thorfmaps.com/lining-up-mystara-xvii/))
    - Georeferencing the Hollow World

### [42 Rolls of duck tape](https://42ducktape.blogspot.com/search/label/490%20project)
42 Rolls of duck tape is a website that showcases the attempt at something similar to our objective in a smaller scale. Here [Lance Duncan](https://www.blogger.com/profile/13817319325489613672 "author profile") tries to create an [interactive map](http://www.csun.edu/~lpd22879/leaflet/leaflet.html) of a region of Mystara. This interactive map has a lot of limitations but it's still a nice representation of what we can achieve. It can be useful to identify what went right and what went wrong in this case study.

#### Pros
It works! When you click on a city you can view information about it
```markdown
**Village south of Radlebb**  
Ruler (Leige Lord): Reeve (local lord)  
Population (culture): 50 - 999 (Traladaran)  
Economic Base: Farming  
Form of Government: Feudal
```

#### Cons
Efficiency:
- Panning is not seamless (at all)
- The map takes forever to load
- Very small scale
- [[The zoom problem]] is not fixed
- crocked perspective

See the [interactive map](http://www.csun.edu/~lpd22879/leaflet/leaflet.html) for more info

### [Vault of Pandius](http://pandius.com/atlas.html)
The [Vault of Pandius](http://pandius.com/atlas.html) is a library of several maps of Mystara that are made with varying degrees of precision ([[miles per hex]]).
It has a [Big section with lots of maps](http://pandius.com/mystara.html#maps)  like the [Mystara Outer World 1000 AC, 72 miles per hex](http://pandius.com/motrwrld.html) which is going to be very useful in the web map section that regards the Outer World
![[Mystara72mphclear.png]]

### [Let’s Map Mystara 1986](https://www.thorfmaps.com/lets-map-mystara-1986/)
Another big library of [[Thorfinn Tait]]'s maps
### [Lining Up Mystara Revisited III](https://www.thorfmaps.com/lining-up-mystara-revisited-iii/)
In this post from [Thorfinn Tait Cartography](https://www.thorfmaps.com "Thorfinn Tait Cartography") it's shown a 3D model of the entire world of Mystara created by Thorfinn Tait. This 3D model has apparently been created by using very big maps and wrapping them around a sphere (with small adjustments to perspective) using an online tool

### [Lining Up Mystara XIX](https://www.thorfmaps.com/lining-up-mystara-xix/)
Lining up Mystara revisited.

### [Thorfinn's patreon](https://www.patreon.com/thorfinn)
Thorfinn's patreon has a big library of high quality PNG's of Mystara. The teacher is subscribed to this Patreon so we can use these resourced further on.
The Patron also gives access to the discord which we can use to contact Thorfinn later on.

### [mkhexgrid](https://www.nomic.net/~uckelman/mkhexgrid/)
mkhexgrid is a open-source software for generating hex maps. It's written in C++ and has a lot of customization tools to work with. It can be useful to explore the necessities of hexagon tile's attributes and methods when inserted in a hex map.


### [A brief history of hex](https://www.flerlagetwins.com/2018/11/what-hex-brief-history-of-hex_68.html?m=1)


### [Hexagonal Chess](https://en.wikipedia.org/wiki/Hexagonal_chess)

### [Hex Map Wikipedia](https://en.wikipedia.org/wiki/Hex_map)

### [Hex Maps Revisited](https://www.linkedin.com/pulse/hex-maps-revisited-good-way-visualise-data-peter-j%C3%B6nsson)


Python > node.js
O professor tem um odio ao node (muitos ficheiros).
Se tiver bem feito podemos ter factored out como biblioteca e ter um toolchain que se possa usar no futuro para outras coisas.
Falar com a dsi para ver opçoes de hosting em python para o projeto
para alem das ferramentas queremos inspiração
o documento esta uma serie de coisas, bora começar a por direitinho
tem que haver uma narrativa, um fio condutor. Quando 
a versão n+1 devia começar a ter uma estrutura com a historia dos hexagonos e da sua manipulação
1 - Obriga a arrumar as ideias na cabeça
- ja estou a começar a ter muitas coisas na cabeça
- ver um bocadinho melhor e encontrar lacunas
2 - Mais proximo da versao final
3 - Pode começar a ser um problema estar a fazer um trabalho bom demais
- hexagonos vs triangulos vs quadrados e interessante e pode ser uma primeira secção do trabalho relacionado ter na introdução "ja sao utilizados desde os war games etc" mas corro o risco de ficar sem espaço. Ao estruturar o documento posso ver se fico sem espaço (25 paginas). se chegarmos a conclusao que esta muito grande, guardamos para a versão final caso seja vantajoso para o doc final (80 paginas)
4 - Delinear a solução
- webmap
- python
- homebrew
- work in documents
	- um diagrama de blocos da arquitetura da coisa
		- base de dados?
		- frontend com esta e esta coisa para quem edita o mapa e para quem faz outra coisa
		- mostrar o mapa a diferentes escalas
		- utilizador?
		- resumo do que vai ser
		- complementado com uma cena de bullets
	- Fazer uns esboços dos ecrãs
		- Figma?
		- brainstorming de design
Tentar fazer isto na proxima/ proximas duas
Começar a fazer proof of concept depois 
Como guardar o mapa? SVG? BITMAP?
Queria ter tempo de as fazer para se montar umas coisas que nao sejam brincadeiras a tempo de por no documento para a discussao ser melhor (bem visto pelo juri)
desenhar o mapa -> trivial, svg styles etc mas e facil
desafio -> vou buscar o mapa a web fazer parse sacar infor dos hexagonos e por no nosso sistema. vai apanhar bem vai apanhar mal, tem de haver correção por parte do user. O mapa tem de encaixar pelos mapas que a gente tem. Há mapas que não encaixam :( As vezes é preciso rodar um bocadinho.
Desafio -> Integração de mapas!!!! Há mapas que não concordam... O que fazer? Tem que se conseguir encaixar! Não devemos substimar esta parte.

O Thorf está a vir ao de cima portanto a ideia mantem-se de falar com ele quando o projeto estiver mais avançado. Visto que ele é o gold standard convem a nossa ideia bater com a dele em relacao a projeções e coisas do estilo.


-> Assim que der mandar um draft mais bonito com os headers das secções e deixar a branco as secções que nao tem nada ainda (chapter 3 e 4). Tentar mandar antes da reunião. Fazer a lista de bullets. **Fazer num google doc** para o professor poder contribuir ao longo da semana