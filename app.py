import streamlit as st
from PIL import Image
import oil_painting
import water_coloring
import pencil_sketch

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

        # If the user checks one of the follwing options on the sidebar
        if st.sidebar.checkbox("Oil Painting"):
            # Getting the final image
            final_image = oil_painting.oil_effect(uploaded_file)

            st.markdown("---")
            st.markdown("# Oil Painting")
            # Displaying the image
            st.image(final_image,caption = "Oil Painting", use_column_width=True)

        elif st.sidebar.checkbox("Water Coloring"):
            # Getting the final image
            final_image = water_coloring.water_effect(uploaded_file)

            st.markdown("---")
            st.markdown("# Water Painting")
            # Displaying the image
            st.image(final_image,caption = "Water Coloring", use_column_width=True)

        elif st.sidebar.checkbox("Pencil Sketch"):
            st.markdown("---")
            st.markdown("# Pencil Sketch")
            # Displaying the image
            if st.checkbox("Black & White"):
                # Getting the final image
                final_image = pencil_sketch.sketch_effect(uploaded_file, 1)

                st.image(final_image,caption = "B&W Sketch", use_column_width=True)
            elif st.checkbox("Color"):
                # Getting the final image
                final_image = pencil_sketch.sketch_effect(uploaded_file, 0)

                st.image(final_image,caption = "Color Sketch", use_column_width=True)

if __name__ == "__main__":
    main()
