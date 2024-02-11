import os

# List of terrain types and features
terrain_types = [
    "plains_grassland",
    "forest",
    "jungle",
    "desert",
    "mountains",
    "hills",
    "water",
    "swamp",
    "tundra",
    "urban",
    "farmland",
    "ruins",
    "volcano",
    "caves",
    "coast",
    "magical",
    "badlands",
    "foothills",
    "savanna",
    "steppe",
    "moor",
    "plateau",
    "canyon",
    "oasis",
    "lava_fields",
    "quicksand",
    "tropical_islands",
    "sky",
    "netherworld",
    "underwater",
    "fjord",
    "lagoon",
    "mesa",
    "floodplain",
    "estuary",
    "salt_marsh",
    "coral_reef",
    "mangrove_swamp",
    "geothermal_area",
    "tropical_rainforest",
    "savannah",
    "alpine_meadow",
    "glacial_lake",
    "subterranean_river",
    "lunar_landscape",
    "abyssal_plain",
    "fairy_ring",
    "spirit_grove",
    "crystal_cavern",
    "temporal_rift",
    "unknown"
]

# Main directory path
main_directory = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\CNN\Dataset"

# Create subfolders for each terrain type
for terrain_type in terrain_types:
    folder_path = os.path.join(main_directory, terrain_type)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created folder: {folder_path}")
