# DoScan: A Simple Document Scanning Application

## Overview
DoScan is a user-friendly desktop application designed for scanning documents using computer vision techniques. Built with Python, it leverages libraries such as OpenCV, NumPy, and Tkinter to process images, detect contours, and perform perspective transformations, allowing users to obtain a clean, scanned version of their documents.


## Functionalities

1. **Image Uploading:**
   - Easily upload images from your local filesystem via a file dialog.

2. **Image Processing:**
   - Converts the uploaded image to grayscale, applies Gaussian blur, and detects edges using the Canny edge detection algorithm.
   - Identifies contours in the image and selects the largest one, assuming it's the document to be scanned.

3. **Document Rectification:**
   - Approximates the document's shape, extracting the four corners to create a top-down view.

4. **Image Display:**
   - Displays both the original and processed (scanned) images side by side for easy comparison.

5. **Saving Scanned Images:**
   - Save the scanned output in various formats (PNG, JPEG) to your preferred location.

6. **Refresh Functionality:**
   - Clear the displayed images and start a new scanning session without restarting the application.

## Usage Instructions

- Click the "Upload Image" button to open a file dialog. Select the image you wish to scan.
  
- After processing, the application displays the original image on the left and the scanned version on the right.

   <img src="https://github.com/user-attachments/assets/882346b0-8d60-486b-809e-d353184e10ac" height="350"/>

- Click the "Save Output Image" button to choose a location and file format to save your scanned document.
  
- If you want to start over, click the "Refresh" button to clear the displayed images.

- In case, image is not fit to process it will display the following error.

  <img src="https://github.com/user-attachments/assets/bb727973-4b38-4651-8a08-2d002fcaef89" width="350"/> 

## Installation Requirements

To install the required libraries, you can use the following commands:

-Install OpenCV
```bash
pip install opencv-python
```
-Install NumPy
```bash
pip install numpy
```
-Install Pillow
```bash
pip install Pillow
```

