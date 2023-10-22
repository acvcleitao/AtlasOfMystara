import cv2
import numpy as np
import PoCHexFinder
import PoCHexMaker
import PoCHexTranslator
import PoCHexReconstructor
import Test

image = cv2.imread("your_image3.jpg")

hexFound = PoCHexFinder.HexFinder(image)

cv2.imshow("Final Image", hexFound)
cv2.imshow("Hexagonal Grid", hexFound)
cv2.waitKey(0)
cv2.destroyAllWindows()

PoCHexReconstructor.HexReconstructor(image)


result = Test.HexTranslator(hexFound)
# Grid parameters
grid_size = (7, 3)  # Number of hexagons in each direction (width, height)
tile_size = 19     # Size of each hexagon
orientation = 'pointy'  # 'pointy' or 'flat'

finalCanvas = PoCHexMaker.HexMaker(grid_size, result[1], result[2])

cv2.imshow("Hexagonal Grid", finalCanvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
