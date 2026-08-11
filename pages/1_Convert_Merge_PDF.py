import streamlit as st
from PyPDF2 import PdfMerger
from streamlit_sortables import sort_items
import io


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Convert / Merge PDF",
    page_icon="📄",
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
    '<div class="page-title">📄 Convert / Merge PDF</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Gabungkan beberapa file PDF menjadi satu dokumen.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    """

    <div class="info-box">
        <b>Cara menggunakan: </b><br>
        1. Unggah dua atau lebih file PDF.<br>
        2. Geser file untuk mengatur urutannya.<br>
        3. Klik <b>Merge PDF</b>.<br>
        4. Unduh PDF yang telah digabungkan.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD PDF
# ============================================================

st.markdown(
    '<div class="section-title">Upload PDF Files</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload two or more PDF files to merge."
)


# ============================================================
# SORT PDF FILES
# ============================================================

if uploaded_files:

    if len(uploaded_files) >= 2:

        st.markdown(
            '<div class="section-title">Arrange File Order</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Drag and drop the files to arrange the order "
            "of the merged PDF."
        )

        # Create unique labels for every file
        file_labels = [
            f"{i + 1}. {file.name}"
            for i, file in enumerate(uploaded_files)
        ]

        # Drag-and-drop sortable list
        sorted_labels = sort_items(
            file_labels
        )

        # Convert sorted labels back to uploaded file objects
        file_dict = {
            f"{i + 1}. {file.name}": file
            for i, file in enumerate(uploaded_files)
        }

        sorted_files = [
            file_dict[label]
            for label in sorted_labels
        ]

        # --------------------------------------------------------
        # SHOW CURRENT ORDER
        # --------------------------------------------------------

        st.markdown("### Current Order")

        for i, file in enumerate(sorted_files, start=1):

            st.write(
                f"**{i}.** {file.name}"
            )

    else:

        st.warning(
            "Please upload at least 2 PDF files to merge."
        )


# ============================================================
# MERGE PDF
# ============================================================

if uploaded_files and len(uploaded_files) >= 2:

    st.markdown("---")

    if st.button(
        "🔗 Merge PDF",
        type="primary",
        use_container_width=True
    ):

        try:

            merger = PdfMerger()

            # Add PDFs according to the user's selected order
            for pdf_file in sorted_files:

                merger.append(pdf_file)

            # Store merged PDF in memory
            merged_pdf = io.BytesIO()

            merger.write(merged_pdf)
            merger.close()

            merged_pdf.seek(0)

            st.success(
                f"{len(sorted_files)} PDF files have been "
                "successfully merged."
            )

            # ----------------------------------------------------
            # DOWNLOAD BUTTON
            # ----------------------------------------------------

            st.download_button(
                label="⬇️ Download Merged PDF",
                data=merged_pdf,
                file_name="merged_document.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"An error occurred while merging the PDF: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Internal Doc Convert &nbsp;•&nbsp; Convert / Merge PDF
    </div>
    """,
    unsafe_allow_html=True
)