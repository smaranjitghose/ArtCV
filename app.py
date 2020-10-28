import streamlit as st
from PIL import Image
import effect_menu

# Setting up Streamlit's page config
st.beta_set_page_config(
page_title = "ArtCV",
layout = "centered",
initial_sidebar_state = "collapsed",
)

# Just making sure we are not bothered by File Encoding warnings
st.set_option('deprecation.showfileUploaderEncoding', False)

def main():
    # Edit the title of the web app
    st.title("Artistic filters using OpenCV")
    # Option to upload an image file with jpg,jpeg or png extensions
    uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "png", "jpeg"])
    # If the user uploads an image
    if uploaded_file is not None:
        # Opening the image
        user_image = Image.open(uploaded_file)
        # Let's see what we got
        st.image(user_image, use_column_width=True)
        # Calling in the Menu of all the effects 
        effect_menu.menu(uploaded_file)
if __name__ == "__main__":
    main()
