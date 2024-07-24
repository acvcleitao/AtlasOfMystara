# AtlasOfMystara

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


## How to run
The Atlas of Mystara consists of three essential parts:
- The frontend made using react
- The backend made in python
- The NoSQL database using MongoDB Atlas as its host

To run the Atlas locally you first need to locate to the backend directory, activate the virtual environment within and run the backend using `python app.py`. The virtual environment comes pre-installed with all the necessary libraries, so no need to worry about dependencies other than python itself. The second step is to, on a new terminal window, navigate to the frontend directory titled "atlas_of_mystara" and simply running the command `npm start`. This should open a new tab in your browser with the Atlas ready to explore. The database is currently configured to allow access from any IP so all the avaliable features should be working as intended.


## How to Run the Project

The Atlas of Mystara comprises three essential components:
- **Frontend**: Built with React
- **Backend**: Developed in Python
- **Database**: NoSQL database hosted on MongoDB Atlas

### Prerequisites
Ensure you have the following installed on your machine:
- Python
- Node.js and npm

### Running the Project Locally

#### Backend
1. Navigate to the backend directory:
   ```sh
   cd path/to/project/Backend
   ```

2. Activate the virtual environment:

   ```sh
   source venv/bin/activate  # For macOS/Linux
   .\venv\Scripts\activate  # For Windows
   ```
3. Run the backend server:
   ```sh
    python app.py
   ```

    The virtual environment includes all necessary libraries, so no additional dependency installation is required.

#### Frontend
1. Open a new terminal window and navigate to the frontend directory:
   ```sh
   cd path/to/project/atlas_of_mystara
   ```
2. Start the frontend application:
   ```sh
    npm start
   ```
    This command will launch the application in your default web browser.

#### Database
The MongoDB Atlas database is configured to allow access from any IP address, ensuring all features are fully functional out-of-the-box.
Accessing the Application

Once both the backend and frontend are running, the Atlas of Mystara will be accessible via your web browser, ready for you to explore.




## Valuable Links

- 1st Contact -> https://docs.google.com/document/d/1X3xuly5_aY4tdo8RlVtbUTseC1qCqhgOm8x9EP0cXI0/edit
- 1st Figma Prototype -> https://www.figma.com/file/cSNIjZVw9psdQMD66WC6E3/Atlas-of-Mystara

## Considerations


## Apendix


This markdown (as well as the others in the repo) was made in Obsidian.md so some formating issues might occur
