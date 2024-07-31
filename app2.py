import requests
from tkinter import Tk, Label, Menu, PhotoImage
from PIL import Image, ImageTk
import io

class CatImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Cat Image Gallery")

        # Create a menu bar
        self.menu = Menu(root)
        root.config(menu=self.menu)

        # Create a "File" menu
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Get New Image", command=self.update_image)

        # Create a label for displaying the image
        self.label = Label(root)
        self.label.pack()

        # Load the initial image
        self.update_image()

    def get_random_cat_image_url(self):
        url = "https://api.thecatapi.com/v1/images/search"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[0]['url']
        return None

    def update_image(self):
        url = self.get_random_cat_image_url()
        if url:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))

            # Handle GIFs
            if image.format == 'GIF':
                self.show_gif(image)
            else:
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo

    def show_gif(self, image):
        self.gif_frames = []
        self.gif_index = 0

        for frame in range(0, image.n_frames):
            image.seek(frame)
            frame_image = ImageTk.PhotoImage(image.copy())
            self.gif_frames.append(frame_image)

        self.label.config(image=self.gif_frames[0])
        self.update_gif()

    def update_gif(self):
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.label.config(image=self.gif_frames[self.gif_index])
        self.root.after(100, self.update_gif)  # Adjust delay for frame rate

# Create the main window
root = Tk()
app = CatImageApp(root)
root.mainloop()
