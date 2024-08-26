import cv2
import numpy as np
import os

pathToImages = "./Images/"
pathToProcess = "./Processed/"

if __name__ == "__main__":
    for filename in os.listdir(pathToImages):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            imgToProcess = filename[:-4]
            imgProcessedPath = os.path.join(pathToProcess, imgToProcess)

            # Make the folder to store paragraphs
            try:
                os.mkdir(imgProcessedPath)
            except FileExistsError:
                print(imgProcessedPath, " Already exists")

            img = cv2.imread(pathToImages + f"/{imgToProcess}.png", 0) 

            # Threshold the image, below 230 will be set to 255 or White. Above 230 will be set to 0
            _, binarisedImage = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)

            # ===== Initialise Variables =====
            width1 = 0 
            width2 = 0
            height1 = 0
            height2 = 0

            colMarginBlank = 30
            rowMarginBlank = 30
            parsingMargin = 12

            paragraph_counter = 1
            # ===== Initialise Variables =====


            while (np.sum(binarisedImage != 0)):
                vertical_projection = np.sum(binarisedImage, axis=0) # scan column

                # loop through every column, if the sum of a specific column pixel is not 0, parse it out
                for index, x in enumerate(vertical_projection):
                    # if found column index where got white pixel
                    if x != 0:
                        width1 = index
                        break
                
                # Get ending column
                counter = 0
                colBlankFound = False
                for a in range(len(vertical_projection[width1:])):
                    while counter < colMarginBlank:
                        # If column has no words
                        if vertical_projection[width1+a] == 0:
                            # If first time of colMarginBlank run
                            if not colBlankFound:
                                width2 = width1+a
                                colBlankFound = True
                                
                            counter += 1
                            break
                        else:
                            # If column has words
                            colBlankFound = False
                            counter = 0
                            break
                
                # Once we have width1 and width2, get the first height of paragraph.
                horizontal_projection = np.sum(binarisedImage[:, :width2], axis=1)
                for index, y in enumerate(horizontal_projection):
                    if y != 0:
                        height1 = index
                        break

                counter = 0
                rowBlankFound = False
                for b in range(len(horizontal_projection[height1:])):
                    while counter < rowMarginBlank:
                        # If column has no words
                        if horizontal_projection[height1+b] == 0:
                            # If first time of colMarginBlank run
                            if not rowBlankFound:
                                height2 = height1+b
                                rowBlankFound = True

                            counter += 1
                            break
                        else:
                            # If row has words
                            rowBlankFound = False
                            counter = 0
                            break

                # To detect table margin
                tableMargin = int((width2 - width1) / 2)

                # Table detection
                for col in range(width1, width1+tableMargin):
                    # If throughout the margin width range, discover it is not a line then it's not a table and begin parsing
                    if binarisedImage[height1][col] == 0:

                        final_img = img[height1 - parsingMargin : height2 + parsingMargin, 
                                        width1 - parsingMargin : width2 + parsingMargin]
                        
                        # Show and Write the extracted paragraphs to the spceified location in pathToProcess
                        cv2.imwrite(imgProcessedPath + f"/{imgToProcess} - Paragraph {str(paragraph_counter)}" +".png", final_img)
                        # cv2.imshow(f"{imgToProcess} - Paragraph {str(paragraph_counter)}", final_img)
                        paragraph_counter = paragraph_counter + 1
                        break
                
                # Set the specificied region to blank so it won't be ran again
                binarisedImage[height1:height2, width1:width2] = 0

        else:
            continue
  
cv2.waitKey()
cv2.destroyAllWindows()