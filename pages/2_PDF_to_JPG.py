import streamlit as st
import pymupdf
import io
import zipfile


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PDF to JPG",
    page_icon="🖼️",
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
    '<div class="page-title">🖼️ PDF to JPG</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Convert PDF pages into high-quality JPG images.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    """
    <div class="info-box">
        <b>Cara menggunakan:</b><br>
        1. Unggah file PDF.<br>
        2. Pilih kualitas gambar.<br>
        3. Klik <b>Convert to JPG</b>.<br>
        4. Pratinjau dan unduh file JPG Anda.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD PDF
# ============================================================

st.markdown(
    '<div class="section-title">Upload PDF</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    accept_multiple_files=False,
    help="Upload one PDF file to convert into JPG images."
)


# ============================================================
# PDF PROCESSING
# ============================================================

if uploaded_file:

    try:

        # Read PDF
        pdf_bytes = uploaded_file.read()

        # Open PDF from memory

        pdf_document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        page_count = len(pdf_document)

        st.success(
            f"PDF successfully loaded — {page_count} page(s)."
        )

        # --------------------------------------------------------
        # FILE INFORMATION
        # --------------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "File Name",
                uploaded_file.name
            )

        with col2:
            st.metric(
                "Total Pages",
                page_count
            )

        # --------------------------------------------------------
        # IMAGE QUALITY
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">Image Quality</div>',
            unsafe_allow_html=True
        )

        quality = st.select_slider(
            "Choose conversion quality",
            options=[
                "Low",
                "Medium",
                "High"
            ],
            value="High"
        )

        # Zoom determines output resolution
        if quality == "Low":
            zoom = 1.0
            quality_description = "Smaller file size"

        elif quality == "Medium":
            zoom = 1.5
            quality_description = "Balanced quality and file size"

        else:
            zoom = 2.0
            quality_description = "Higher image quality"

        st.caption(
            f"{quality_description}."
        )

        # --------------------------------------------------------
        # CONVERT BUTTON
        # --------------------------------------------------------

        st.markdown("---")

        if st.button(
            "🖼️ Convert to JPG",
            type="primary",
            use_container_width=True
        ):

            jpg_files = []

            progress_bar = st.progress(0)

            status_text = st.empty()

            # ----------------------------------------------------
            # CONVERT EVERY PAGE
            # ----------------------------------------------------

            for page_number in range(page_count):

                page = pdf_document.load_page(page_number)

                matrix = pymupdf.Matrix(
                    zoom,
                    zoom
                )

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                jpg_bytes = pixmap.tobytes(
                    "jpg"
                )

                file_name = (
                    f"{uploaded_file.name.rsplit('.', 1)[0]}"
                    f"_page_{page_number + 1}.jpg"
                )

                jpg_files.append(
                    {
                        "name": file_name,
                        "data": jpg_bytes
                    }
                )

                progress = (
                    (page_number + 1) / page_count
                )

                progress_bar.progress(
                    progress
                )

                status_text.write(
                    f"Converting page "
                    f"{page_number + 1} of "
                    f"{page_count}..."
                )

            status_text.empty()
            progress_bar.empty()

            st.success(
                f"Successfully converted "
                f"{page_count} page(s) to JPG."
            )

            # ====================================================
            # PREVIEW
            # ====================================================

            st.markdown(
                '<div class="section-title">Preview</div>',
                unsafe_allow_html=True
            )

            # Show first 3 pages only
            preview_files = jpg_files[:3]

            preview_columns = st.columns(
                len(preview_files)
            )

            for column, jpg_file in zip(
                preview_columns,
                preview_files
            ):

                with column:

                    st.image(
                        jpg_file["data"],
                        caption=jpg_file["name"],
                        use_container_width=True
                    )

            if page_count > 3:

                st.caption(
                    f"Showing first 3 pages. "
                    f"{page_count - 3} additional page(s) "
                    f"are available for download."
                )

            # ====================================================
            # DOWNLOAD SECTION
            # ====================================================

            st.markdown("---")

            st.markdown(
                '<div class="section-title">Download</div>',
                unsafe_allow_html=True
            )

            # ----------------------------------------------------
            # SINGLE PAGE
            # ----------------------------------------------------

            if len(jpg_files) == 1:

                st.download_button(
                    label="⬇️ Download JPG",
                    data=jpg_files[0]["data"],
                    file_name=jpg_files[0]["name"],
                    mime="image/jpeg",
                    use_container_width=True
                )

            # ----------------------------------------------------
            # MULTIPLE PAGES
            # ----------------------------------------------------

            else:

                # Create ZIP in memory
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(
                    zip_buffer,
                    mode="w",
                    compression=zipfile.ZIP_DEFLATED
                ) as zip_file:

                    for jpg_file in jpg_files:

                        zip_file.writestr(
                            jpg_file["name"],
                            jpg_file["data"]
                        )

                zip_buffer.seek(0)

                st.download_button(
                    label="⬇️ Download All JPGs (ZIP)",
                    data=zip_buffer,
                    file_name=(
                        f"{uploaded_file.name.rsplit('.', 1)[0]}"
                        "_JPG.zip"
                    ),
                    mime="application/zip",
                    use_container_width=True
                )

                # Individual downloads
                with st.expander(
                    "Download individual pages"
                ):

                    for jpg_file in jpg_files:

                        st.download_button(
                            label=(
                                f"⬇️ {jpg_file['name']}"
                            ),
                            data=jpg_file["data"],
                            file_name=jpg_file["name"],
                            mime="image/jpeg",
                            use_container_width=True,
                            key=jpg_file["name"]
                        )

        pdf_document.close()

    except Exception as e:

        st.error(
            f"An error occurred while processing "
            f"the PDF: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Internal Doc Convert &nbsp;•&nbsp; PDF to JPG
    </div>
    """,
    unsafe_allow_html=True
)