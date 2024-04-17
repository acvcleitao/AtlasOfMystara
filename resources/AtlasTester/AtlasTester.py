# TODO: Write the complete pipeline for the processMap function using the existing functions in the Atlas backend

import os

def processMap(image_path):
    # Implement the image processing pipeline here
    return ["word1", "word2", "word3"]


def compareWords(image_name, words):
    absolute_truth_path = os.path.join("AbsoluteTruth", image_name)
    if not os.path.exists(absolute_truth_path):
        print(f"Absolute truth file not found for {image_name}")
        return 0

    with open(absolute_truth_path, "r") as file:
        absolute_truth_words = [line.strip() for line in file]

    num_matches = sum(1 for word, truth_word in zip(words, absolute_truth_words) if word == truth_word)
    return num_matches

def main():
    unprocessed_maps_folder = "UnprocessedMaps"
    for filename in os.listdir(unprocessed_maps_folder):
        image_path = os.path.join(unprocessed_maps_folder, filename)
        words = processMap(image_path)
        num_matches = compareWords(os.path.splitext(filename)[0], words)
        print(f"Matches for {filename}: {num_matches}")

if __name__ == "__main__":
    main()
