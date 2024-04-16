# Atlas of Mystara, First Steps
#AtlasOfMystara #tese #thesis
## **List of Hexmap examples**

#### Objective: list 3 or 4 examples of hexmap usage (editor, tool, webmap) and a brief description of at least one of them.

**1.**       **HEXTML (**[https://hextml.playest.net/](https://hextml.playest.net/)**)**

**·**         **HEXTML is a hexmap editor specifically made with the purpose of DnD campaigns. It has many interesting features that would be very useful to a DM such as connecting maps via a submaps menu, adding secret notes only visible to the DM and allowing for collaboration both for help building the map itself and for other players to join in and play the campaign directly on the website.**

**·**         **As for editing of the hexmaps it has tiles of various colours each with different names, allowing users to add their own tile set if they choose to do so. It has a stamp system that lets you stamp out tiles with other tiles and/or symbols. It also allows users to override the background colours of the hexes by using the colour menu. It’s possible to manually add rivers, roads and borders to all hexes. The map editor also has a fog of war feature that can hide certain tiles from the players until the DM desires to do so.**

**·**         **The hexes themselves can have information in them. They each have three menus where it’s possible to input text: Text (used for hovering text on the tile), Secret Notes (only visible to the DM) and Player’s Notes (visible to both the player and the DM)**

**·**         **The map also has the option of using three different grid shapes. Two of them are hexagon grids with the hexagons aligned in different ways and the last one is a square grid.**

**·**         **There is a feature to export the map to an image, I’ve made a very simple map which covers most of the features of this editor (presented below) and found out the map-to-image is a bit flawed as it cuts the right outer edge of the map. The exported map doesn’t include the borders, the rivers and the roads I’ve added and the hexes have a thicker border than in the editor.****
![[Pasted image 20230909163538.png]]

**2.**       **Molotov Cockatiel Hex Map Maker (**[https://molotovcockatiel.com/hex-map-maker/](https://molotovcockatiel.com/hex-map-maker/)**)**

**·**         **This one has a simpler approach to hex map making. It asks the user to prompt out the map size and it generates it for him letting the user paint over the generated map with solid colour only tiles.**

**·**         **What I found interesting about this one was the fact that it exports the map to SVG and to an “array of hexes”. This sadly turned out to be a list of lists containing numbers from one to eight which were associated to each of the possible hexes the editor used (with one being the clear tile and eight being the custom tile), meaning there was no difference between two different custom tiles.**

**·**         **The tool also pointed out that “**Pointed-top hexes take up more vertical room, so flat top generally works better.” Which might be important to note.

**3.**       **Worldographer / Hexographer II (**[https://worldographer.com/](https://worldographer.com/)**)**

**·**         **I tested Worldographer on a free version, this one is a full-fledged application with a lot more features and detail than the others.**

**·**         **It has the feature of generating its own maps with options for generating rivers, roads, nations and more. It’s possible to fully customise any given tile with numerous options for transparency, texture, colour, etc.**

**·**         **In this editor, hexes have two numbers associated with them, one for the row and the other for the column, making it easy to locate a hex by its coordinates.**

**·**         ![](file:///C:/Users/acvcl/AppData/Local/Temp/msohtmlclip1/01/clip_image002.gif)
**This editor solved a problem present in bigger maps. How do you zoom out? The hexes are too small on maps of bigger sizes; this makes them hard to see when looking at a whole continent for example. Worldographer solves this by creating bigger hexes made up of the smaller hexes.**

**·**         **As for zooming in, Worldographer has (similarly to the first example) map links that increase the level of detail. You traverse to the maps via a menu called info that appears on the right side of the screen when clicking a tile. These maps, often used as town or village maps. These aren’t exactly made form premade tile sets but are essentially a picture with a uniform hex grid on top.**
![[Pasted image 20230909163634.png]]

**3.**       **HexSim (****[https://www.hexsim.net/home](https://www.hexsim.net/home)****)**

**·**         **HexSim simulates the behaviour of plant and animal life on a Hexmap. The map’s layout is static but its content changes every tick to simulate species’ interactions.**

## **2. List of Papers**

#### **Objective: list 4 or 5 papers related to the project**

1.       Ali Mahdavi-Amiri, Erika Harrison & Faramarz Samavati (2015) Hexagonal connectivity maps for Digital Earth, International Journal of Digital Earth, 8:9, 750-769, DOI: [https://doi.org/10.1080/17538947.2014.927597](https://doi.org/10.1080/17538947.2014.927597)

·         Here six types of hexagonal refinement are mentioned. 1-to-3, 1-to-4, and 1-to-7 refinement in both their centroid-aligned (c-refinements) and vertex-aligned (v-refinements) variants. These refinement approaches could be used to zoom in/zoom out of a hex map.

![[Pasted image 20230909163704.png]]

2.       Martyniuk, Taras. "Implementing Hexmap Generation Framework using Cube Coordinate System in Unity3D." (2021)

**·**         In this paper, different coordinate systems for hex grids are discussed. Two alternatives are proposed. The first one is similar to the system used in **Worldographer. Essentially, each hex has two coordinates that represent the offset of that hex in relation to the edge of the grid. Meaning hex (1,3) would be on the second column of the forth row of the grid (since it starts at 0). The second approach uses cube coordinates to differentiate the hexes. With three axis (x, y, z) which are aligned with the three pairs of sides a hexagon has can also be used to map out the grid. The study concludes that The added axis of cube system allows for a natural and much easier transition to neighbouring hexes and simplifies algorithms.**

![[Pasted image 20230909163720.png]]


3.       Yao, X.; Yu, G.; Li, G.; Yan, S.; Zhao, L.; Zhu, D. HexTile: A Hexagonal DGGS-Based Map Tile Algorithm for Visualizing Big Remote Sensing Data in Spark. _ISPRS Int. J. Geo-Inf._ **2023**, _12_, 89. [https://doi.org/10.3390/ijgi12030089](https://doi.org/10.3390/ijgi12030089)

4.       Rummelt, N. Array Set Addressing: Enabling Efficient Hexagonally Sampled Image Processing. Ph.D. Thesis, Unversity of Florida, Gainesville, FL, USA, 2010

Duszak, P.; Siemiątkowska, B.; Więckowski, R. Hexagonal Grid-Based Framework for Mobile Robot Navigation. _Remote Sens._ **2021**, _13_, 4216. [https://doi.org/10.3390/rs13214216](https://doi.org/10.3390/rs13214216)