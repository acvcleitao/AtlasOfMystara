import cv2
import argparse
import PoCHexFinder
import PoCHexMaker
import PoCHexTranslator
import PoCHexReconstructor
import Test

def process_image(image_path):
    image = cv2.imread(image_path)

    hexFound = PoCHexFinder.HexFinder(image)

    cv2.imshow("Final Image", hexFound)
    cv2.imshow("Hexagonal Grid", hexFound)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    PoCHexReconstructor.HexReconstructor(image)

    result = Test.HexTranslator(hexFound)
    # Grid parameters
    # TODO: Get these values dynamically
    grid_size = (7, 3)  # Number of hexagons in each direction (width, height)
    tile_size = 19     # Size of each hexagon
    orientation = 'pointy'  # 'pointy' or 'flat'

    finalCanvas = PoCHexMaker.HexMaker(grid_size, result[1], result[2])

    cv2.imshow("Hexagonal Grid", finalCanvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser(description='Image Processing for Hexagonal Grid')
    parser.add_argument('image_path', help='Path to the image for processing')
    
    args = parser.parse_args()
    image_path = args.image_path
    """
    image_path = r"PoC\Database\Tests101\your_image3.jpg"
    process_image(image_path)
