import streamlit as st
from streamlit_sortables import sort_items
from PIL import Image
import io


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JPG to PDF",
    page_icon="📑",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .page-title {
        font-size: 36px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .page-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .info-box {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #1f2937;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">📑 JPG to PDF</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Convert multiple JPG images into a single PDF document.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    """
    <div class="info-box">
        <b>Cara menggunakan :</b><br>
        1. Unggah satu atau beberapa gambar JPG.<br>
        2. Seret file untuk mengatur urutannya.<br>
        3. Klik <b>Convert to PDF</b>.<br>
        4. Unduh dokumen PDF Anda.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD JPG
# ============================================================

st.markdown(
    '<div class="section-title">Upload JPG Images</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Choose JPG images",
    type=["jpg", "jpeg"],
    accept_multiple_files=True,
    help="Upload one or more JPG images."
)


# ============================================================
# PROCESS UPLOADED FILES
# ============================================================

if uploaded_files:

    # --------------------------------------------------------
    # CREATE FILE DICTIONARY
    # --------------------------------------------------------

    file_dict = {
        f"{i + 1}. {file.name}": file
        for i, file in enumerate(uploaded_files)
    }

    file_labels = list(file_dict.keys())


    # ========================================================
    # ARRANGE FILE ORDER
    # ========================================================

    st.markdown(
        '<div class="section-title">Arrange Image Order</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Drag and drop the images to arrange the page order "
        "of your PDF."
    )

    sorted_labels = sort_items(
        file_labels
    )

    sorted_files = [
        file_dict[label]
        for label in sorted_labels
    ]


    # ========================================================
    # CURRENT ORDER
    # ========================================================

    st.markdown("### Current Order")

    for i, image_file in enumerate(
        sorted_files,
        start=1
    ):

        st.write(
            f"**{i}.** {image_file.name}"
        )


    # ========================================================
    # IMAGE PREVIEW
    # ========================================================

    st.markdown(
        '<div class="section-title">Preview</div>',
        unsafe_allow_html=True
    )

    preview_columns = st.columns(
        min(len(sorted_files), 4)
    )

    for column, image_file in zip(
        preview_columns,
        sorted_files[:4]
    ):

        with column:

            image = Image.open(
                image_file
            )

            st.image(
                image,
                caption=image_file.name,
                use_container_width=True
            )

    if len(sorted_files) > 4:

        st.caption(
            f"Showing first 4 images. "
            f"{len(sorted_files) - 4} additional "
            f"image(s) are included in the PDF."
        )


    # ========================================================
    # CONVERT TO PDF
    # ========================================================

    st.markdown("---")

    if st.button(
        "📑 Convert to PDF",
        type="primary",
        use_container_width=True
    ):

        try:

            images = []

            progress_bar = st.progress(0)

            status_text = st.empty()


            # ------------------------------------------------
            # PREPARE IMAGES
            # ------------------------------------------------

            for index, image_file in enumerate(
                sorted_files
            ):

                image = Image.open(
                    image_file
                )

                # Convert to RGB
                # because PDF does not support RGBA directly
                if image.mode != "RGB":

                    image = image.convert(
                        "RGB"
                    )

                images.append(
                    image.copy()
                )

                progress = (
                    (index + 1)
                    / len(sorted_files)
                )

                progress_bar.progress(
                    progress
                )

                status_text.write(
                    f"Preparing image "
                    f"{index + 1} of "
                    f"{len(sorted_files)}..."
                )


            # ------------------------------------------------
            # CREATE PDF IN MEMORY
            # ------------------------------------------------

            pdf_buffer = io.BytesIO()

            first_image = images[0]

            remaining_images = images[1:]


            first_image.save(
                pdf_buffer,
                format="PDF",
                save_all=True,
                append_images=remaining_images
            )


            pdf_buffer.seek(0)


            # ------------------------------------------------
            # CLEAN PROGRESS
            # ------------------------------------------------

            status_text.empty()
            progress_bar.empty()


            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            st.success(
                f"{len(images)} image(s) "
                "successfully converted to PDF."
            )


            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_buffer,
                file_name="converted_images.pdf",
                mime="application/pdf",
                use_container_width=True
            )


        except Exception as e:

            st.error(
                f"An error occurred while converting "
                f"the images: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Internal Doc Convert &nbsp;•&nbsp; JPG to PDF
    </div>
    """,
    unsafe_allow_html=True
)