import numpy as np
import cv2
import imutils
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def process_image(image_path, resize_dims=(500, 500)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, resize_dims)
    orig = image.copy()

    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayImageBlur = cv2.GaussianBlur(grayImage, (5, 5), 0)
    edgedImage = cv2.Canny(grayImageBlur, 100, 300)

    allContours = cv2.findContours(edgedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    allContours = imutils.grab_contours(allContours)

    if not allContours:
        messagebox.showerror("Error", "No contours found!")
        return None

    allContours = sorted(allContours, key=cv2.contourArea, reverse=True)[:1]
    perimeter = cv2.arcLength(allContours[0], True)
    ROIdimensions = cv2.approxPolyDP(allContours[0], 0.02 * perimeter, True)

    if len(ROIdimensions) != 4:
        messagebox.showerror("Error", "Could not detect a rectangular area. Please ensure the document is clearly visible and flat.")
        return None

    cv2.drawContours(image, [ROIdimensions], -1, (0, 255, 0), 2)

    ROIdimensions = ROIdimensions.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = np.sum(ROIdimensions, axis=1)
    rect[0] = ROIdimensions[np.argmin(s)]
    rect[2] = ROIdimensions[np.argmax(s)]
    diff = np.diff(ROIdimensions, axis=1)
    rect[1] = ROIdimensions[np.argmin(diff)]
    rect[3] = ROIdimensions[np.argmax(diff)]

    (tl, tr, br, bl) = rect
    widthA = np.sqrt((tl[0] - tr[0]) ** 2 + (tl[1] - tr[1]) ** 2)
    widthB = np.sqrt((bl[0] - br[0]) ** 2 + (bl[1] - br[1]) ** 2)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
    heightB = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    transformMatrix = cv2.getPerspectiveTransform(rect, dst)
    scan = cv2.warpPerspective(orig, transformMatrix, (maxWidth, maxHeight))

    return image, scan

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        original, scan = process_image(file_path)
        if scan is not None:
            display_size = (400, 400)

            original_resized = cv2.resize(original, display_size)
            scan_resized = cv2.resize(scan, display_size)

            original_rgb = cv2.cvtColor(original_resized, cv2.COLOR_BGR2RGB)
            scan_rgb = cv2.cvtColor(scan_resized, cv2.COLOR_BGR2RGB)

            img_original = Image.fromarray(original_rgb)
            img_original_tk = ImageTk.PhotoImage(image=img_original)
            label_input_image.config(image=img_original_tk)
            label_input_image.image = img_original_tk
            
            img_scan = Image.fromarray(scan_rgb)
            img_scan_tk = ImageTk.PhotoImage(image=img_scan)
            label_output_image.config(image=img_scan_tk)
            label_output_image.image = img_scan_tk
            
            global scanned_image
            scanned_image = scan

            label_input.grid(row=1, column=0, padx=(20, 10), pady=(10, 5))
            label_output.grid(row=1, column=1, padx=(10, 20), pady=(10, 5))
            btn_save.grid(row=3, column=0, columnspan=2, pady=(10, 5))
            btn_refresh.grid(row=4, column=0, columnspan=2, pady=(20, 20))

def save_image():
    if 'scanned_image' in globals():
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"),
                                                              ("JPEG files", "*.jpg"),
                                                              ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, scanned_image)
            messagebox.showinfo("Saved", "Scanned image saved successfully!")
    else:
        messagebox.showwarning("Warning", "No image to save!")

def refresh_images():
    label_input_image.config(image=None)
    label_output_image.config(image=None)
    label_input_image.image = None
    label_output_image.image = None
    label_input.grid_forget()
    label_output.grid_forget()
    btn_save.grid_forget()
    btn_refresh.grid_forget()

root = tk.Tk()
root.title("DoScan")
root.configure(bg="black")

btn_upload = tk.Button(root, text="Upload Image", command=upload_image, bg="white", fg="black", font=("Century Gothic", 12, "bold"), relief="raised")
btn_upload.grid(row=0, column=0, columnspan=4, pady=20)

label_input = tk.Label(root, text="Original Image", bg="black", fg="white", font=("Century Gothic", 14))
label_output = tk.Label(root, text="Scanned Image", bg="black", fg="white", font=("Century Gothic", 14))
label_input_image = tk.Label(root, bg="black")
label_output_image = tk.Label(root, bg="black")

label_input_image.grid(row=2, column=0, padx=(20, 10), pady=(0, 20))
label_output_image.grid(row=2, column=1, padx=(10, 20), pady=(0, 20))

btn_save = tk.Button(root, text="Save Output Image", command=save_image, bg="white", fg="black", font=("Century Gothic", 12, "bold"), relief="raised")
btn_refresh = tk.Button(root, text="Refresh", command=refresh_images, bg="white", fg="black", font=("Century Gothic", 12, "bold"), relief="raised")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

root.mainloop()
