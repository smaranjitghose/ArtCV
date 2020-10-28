import streamlit as st

def menu(uploaded_file):
    # If the user checks one of the follwing options on the sidebar
    if st.sidebar.checkbox("Oil Painting"):
        # Getting the file
        from effects import oil_painting
        # Getting the final image
        final_image = oil_painting.oil_effect(uploaded_file)

        st.markdown("---")
        st.markdown("# Oil Painting")
        # Displaying the image
        st.image(final_image,caption = "Oil Painting", use_column_width=True)

    if st.sidebar.checkbox("Water Coloring"):
        # Getting the file
        from effects import water_coloring
        # Getting the final image
        final_image = water_coloring.water_effect(uploaded_file)

        st.markdown("---")
        st.markdown("# Water Painting")
        # Displaying the image
        st.image(final_image,caption = "Water Coloring", use_column_width=True)

    if st.sidebar.checkbox("Pencil Sketch"):
        # Getting the file
        from effects import pencil_sketch

        st.markdown("---")
        st.markdown("# Pencil Sketch")
        # Displaying the image
        if st.checkbox("Black & White"):
            # Getting the final image
            final_image = pencil_sketch.sketch_effect(uploaded_file, 1)

            st.image(final_image,caption = "B&W Sketch", use_column_width=True)
        if st.checkbox("Color"):
            # Getting the final image
            final_image = pencil_sketch.sketch_effect(uploaded_file, 0)

            st.image(final_image,caption = "Color Sketch", use_column_width=True)

    if st.sidebar.checkbox("Sepia"):
        # Getting the file
        from effects import sepia_effect
        # Getting the final image
        final_image = sepia_effect.sepia(uploaded_file)

        st.markdown("---")
        st.markdown("# Sepia")
        # Displaying the image
        st.image(final_image,caption = "Sepia", use_column_width=True)

    if st.sidebar.checkbox("Anime Effect"):
        # Getting the file
        from effects import anime_effect

        st.markdown("---")
        st.markdown("# Anime Effects")
        # Displaying the image
        if st.checkbox("Traditional"):
            # Getting the final image
            final_image = anime_effect.anime(uploaded_file, 1)

            st.image(final_image,caption = "Traditional", use_column_width=True)
        if st.checkbox("Anime Blue"):
            # Getting the final image
            final_image = anime_effect.anime(uploaded_file, 2)

            st.image(final_image,caption = "Anime Blue", use_column_width=True)
        if st.checkbox("Predator View"):
            # Getting the final image
            final_image = anime_effect.anime(uploaded_file, 3)

            st.image(final_image,caption = "Anime Predator View", use_column_width=True)
        if st.checkbox("Vintage"):
            # Getting the final image
            final_image = anime_effect.anime(uploaded_file, 4)

            st.image(final_image,caption = "Vintage Anime", use_column_width=True)

    if st.sidebar.checkbox("Cartoon Effects"):
        # Getting the file
        from effects import cartoon_effects, comic_cartoon_effect

        st.markdown("---")
        st.markdown("# Cartoon Effects")

        if st.checkbox("Color"):
            # Getting the final image
            final_image = cartoon_effects.cartoon(uploaded_file, 1)
            # Displaying the image
            st.image(final_image,caption = "Cartoon Effect", use_column_width=True)
        if st.checkbox("Black & White"):
            # Getting the final image
            final_image = cartoon_effects.cartoon(uploaded_file, 0)
            # Displaying the image
            st.image(final_image,caption = "B&W Cartoon Effect", use_column_width=True)
        if st.checkbox("Comic Cartoon"):
            # Getting the final image
            final_image = comic_cartoon_effect.cartoon(uploaded_file)
            # Displaying the image
            st.image(final_image,caption = "Comic Cartoon Effect", use_column_width=True)

    if st.sidebar.checkbox("Stipple Effect"):
        # Getting the file
        from effects import stipple
        # Getting the final image
        final_image = stipple.stipple_effect(uploaded_file)

        st.markdown("---")
        st.markdown("# Stipple Effect")
        # Displaying the image
        st.image(final_image,caption = "Stipple Effect", use_column_width=True)

    if st.sidebar.checkbox("Motion Blur"):
        # Getting the file
        from effects import motion_blur

        st.markdown("---")
        st.markdown("# Motion Blur")
        # Displaying the image
        if st.checkbox("Vertical Blur"):
            # Getting the final image
            final_image = motion_blur.blur(uploaded_file, 1)

            st.image(final_image,caption = "Vertical Blur", use_column_width=True)
        if st.checkbox("Horizontal Blur"):
            # Getting the final image
            final_image = motion_blur.blur(uploaded_file, 2)

            st.image(final_image,caption = "Horizontal Blur", use_column_width=True)
        if st.checkbox("Diagonal Blur"):
            # Getting the final image
            final_image = motion_blur.blur(uploaded_file, 3)

            st.image(final_image,caption = "Diagonal Blur", use_column_width=True)

    if st.sidebar.checkbox("Emboss"):
        # Getting the file
        from effects import emboss_effect

        st.markdown("---")
        st.markdown("# Emboss")
        # Displaying the image
        if st.checkbox("Grayscale"):
            # Getting the final image
            final_image = emboss_effect.emboss(uploaded_file, 1)

            st.image(final_image,caption = "Grayscale Emboss", use_column_width=True)
        if st.checkbox("Color"):
            # Getting the final image
            final_image = emboss_effect.emboss(uploaded_file, 2)

            st.image(final_image,caption = "Color Emboss", use_column_width=True)
