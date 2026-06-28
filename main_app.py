from ttkbootstrap import Window, Frame, Style
from ttkbootstrap.constants import BOTH
from login_page import LoginWindow
from registration_page import RegistrationWindow
from dashboard_page import display_dashboard


# Page Navigation Functions
def show_page(page_index):
    h = int(root.winfo_screenwidth())
    v = int(root.winfo_screenheight())
    """
    Display a specific page based on the index and adjust the geometry dynamically.
    """
    geometry_list = ["1100x1100", "1500x1300", f"{h}x{v}"]  # Geometry for each page
    root.geometry(geometry_list[page_index])

    # Show the corresponding page
    for frame in page_frames:
        frame.pack_forget()
    page_frames[page_index].pack(fill=BOTH, expand=True)

# Initialize Main Window
root = Window(themename="litera")
root.title("Multi-Page App")

# Define Styles
style = Style()
style.configure("Login.TFrame", background="#f0f0f0")
style.configure("Register.TFrame", background="#d9f7ff")
style.configure("Dashboard.TFrame", background="#ffffff")

# Page Frames
page_frames = []

# Page 1: Login Page
login_page = Frame(root, style="Login.TFrame")
page_frames.append(login_page)
LoginWindow(login_page, navigate_to_page=show_page)

# Page 2: Registration Page
register_page = Frame(root, style="Register.TFrame")
page_frames.append(register_page)
RegistrationWindow(register_page, navigate_to_page=show_page)

# Page 3: Dashboard Page
dashboard_page = Frame(root, style="Dashboard.TFrame")
page_frames.append(dashboard_page)
display_dashboard(dashboard_page, navigate_to_page=show_page)

# Show the first page (Login Page)
show_page(0)

# Run the App
root.mainloop()
