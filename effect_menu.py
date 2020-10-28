import streamlit as st
from effects import oil_painting, water_coloring, pencil_sketch, sepia_effect

def menu(uploaded_file):
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
    elif st.sidebar.checkbox("Sepia"):
        # Getting the final image
        final_image = sepia_effect.sepia(uploaded_file)

        st.markdown("---")
        st.markdown("# Sepia")
        # Displaying the image
        st.image(final_image,caption = "Sepia", use_column_width=True)
