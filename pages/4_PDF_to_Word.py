import streamlit as st
import pymupdf
from pdf2docx import Converter
from docx import Document
from docx.enum.section import WD_ORIENT
import tempfile
import os
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PDF to Word",
    page_icon="📝",
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
# HELPER FUNCTION
# ============================================================

def clean_font_name(font_name):
    """
    Membersihkan nama font dari metadata PDF.

    Contoh:
        ABCDEF+ArialMT -> Arial
        ABCDEF+Arial-BoldMT -> Arial
    """

    if not font_name:
        return ""

    name = font_name.strip()

    # Hapus prefix subset PDF
    # Contoh: ABCDEF+ArialMT
    name = re.sub(
        r"^[A-Z]{6}\+",
        "",
        name
    )

    # Nama font PDF yang umum
    replacements = [
        ("-BoldItalicMT", ""),
        ("-BoldMT", ""),
        ("-ItalicMT", ""),
        ("-MT", ""),
    ]

    for old, new in replacements:

        if name.endswith(old):

            name = (
                name[:-len(old)]
                + new
            )

            break

    # ArialMT -> Arial
    if name.endswith("MT"):

        name = name[:-2]

    return name.strip()


def detect_fonts(pdf_document):
    """
    Mendeteksi font yang digunakan oleh PDF.

    Hanya untuk informasi.
    Font tidak akan dipaksa ulang ke DOCX.
    """

    fonts = set()

    for page in pdf_document:

        blocks = page.get_text(
            "dict"
        ).get(
            "blocks",
            []
        )

        for block in blocks:

            if block.get("type") != 0:
                continue

            for line in block.get(
                "lines",
                []
            ):

                for span in line.get(
                    "spans",
                    []
                ):

                    font_name = span.get(
                        "font",
                        ""
                    )

                    cleaned = clean_font_name(
                        font_name
                    )

                    if cleaned:
                        fonts.add(cleaned)

    return sorted(
        fonts,
        key=str.lower
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">📝 PDF to Word</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Konversi dokumen PDF menjadi file Word yang dapat diedit '
    'dengan mempertahankan tata letak asli semaksimal mungkin.'
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
        1. Unggah file PDF.<br>
        2. Orientasi dokumen dan jenis font akan terdeteksi secara otomatis.<br>
        3. Klik <b>Convert to Word</b>.<br>
        4. Unduh dokumen Word yang telah dikonversi.
        <br><br>
        <b>Catatan:</b> Konverter berupaya mempertahankan tata letak asli PDF, tabel, gambar, dan formatnya.
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
    help="Upload one PDF document to convert into Word."
)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file:

    pdf_bytes = uploaded_file.getvalue()

    try:

        # ====================================================
        # OPEN PDF
        # ====================================================

        pdf_document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        page_count = len(
            pdf_document
        )

        # ====================================================
        # CHECK EMPTY PDF
        # ====================================================

        if page_count == 0:

            st.error(
                "The uploaded PDF does not contain any pages."
            )

            pdf_document.close()

            st.stop()


        # ====================================================
        # DETECT DOCUMENT ORIENTATION
        # ====================================================

        # We treat the whole PDF as one orientation.
        # The first page is used as the reference.

        first_page = pdf_document[0]

        page_width = first_page.rect.width
        page_height = first_page.rect.height

        if page_width > page_height:

            orientation = "Landscape"

        else:

            orientation = "Portrait"


        # ====================================================
        # DETECT PDF FONTS
        # ====================================================

        detected_fonts = detect_fonts(
            pdf_document
        )


        # ====================================================
        # FILE INFORMATION
        # ====================================================

        st.success(
            f"PDF successfully loaded — "
            f"{page_count} page(s)."
        )

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


        # ====================================================
        # DOCUMENT ORIENTATION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'Document Orientation'
            '</div>',
            unsafe_allow_html=True
        )

        orientation_icon = (
            "↔️"
            if orientation == "Landscape"
            else "↕️"
        )

        col1, col2, col3 = st.columns(
            [1, 2, 1]
        )

        with col2:

            st.info(
                f"{orientation_icon}  **{orientation}**\n\n"
                "Detected automatically from the PDF."
            )

        st.caption(
            f"Detected page size: "
            f"{page_width:.2f} × "
            f"{page_height:.2f} pt"
        )


        # ====================================================
        # DETECTED FONTS
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'Detected Fonts'
            '</div>',
            unsafe_allow_html=True
        )

        if detected_fonts:

            st.caption(
                "Fonts detected from the uploaded PDF:"
            )

            # Maximum 4 columns
            number_of_columns = min(
                len(detected_fonts),
                4
            )

            font_columns = st.columns(
                number_of_columns
            )

            for index, font in enumerate(
                detected_fonts
            ):

                with font_columns[
                    index % number_of_columns
                ]:

                    st.info(
                        f"🔤 {font}"
                    )

        else:

            st.warning(
                "No embedded text fonts were detected. "
                "The PDF may contain scanned images."
            )


        # ====================================================
        # FONT NOTE
        # ====================================================

        with st.expander(
            "ℹ️ About font detection"
        ):

            st.write(
                """
                The detected fonts are shown as information only.
                The converter does not force the detected fonts
                back into the Word document.

                This is intentional so that font changes do not
                disturb the table structure, text wrapping,
                spacing or pagination of the converted document.
                """
            )


        # ====================================================
        # CONVERT BUTTON
        # ====================================================

        st.markdown("---")

        if st.button(
            "📝 Convert to Word",
            type="primary",
            use_container_width=True
        ):

            temp_pdf_path = None
            temp_docx_path = None

            try:

                # ====================================================
                # CREATE TEMPORARY PDF
                # ====================================================

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_pdf:

                    temp_pdf.write(
                        pdf_bytes
                    )

                    temp_pdf_path = (
                        temp_pdf.name
                    )


                # ====================================================
                # CREATE TEMPORARY DOCX
                # ====================================================

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".docx"
                ) as temp_docx:

                    temp_docx_path = (
                        temp_docx.name
                    )


                # ====================================================
                # PROGRESS
                # ====================================================

                progress_bar = st.progress(
                    0
                )

                status_text = st.empty()

                status_text.write(
                    "Preparing PDF..."
                )

                progress_bar.progress(
                    10
                )


                # ====================================================
                # PDF → DOCX
                # ====================================================

                status_text.write(
                    "Converting PDF to Word..."
                )

                converter = Converter(
                    temp_pdf_path
                )

                # ----------------------------------------------------
                # IMPORTANT:
                #
                # max_border_width controls the maximum width
                # of a PDF shape that can be interpreted as
                # a table border.
                #
                # We use 2.0 as a trial value to reduce incorrect
                # table-border detection.
                # ----------------------------------------------------

                converter.convert(
                    temp_docx_path,
                    start=0,
                    end=None,
                    max_border_width=2.0
                )

                converter.close()

                progress_bar.progress(
                    75
                )


                # ====================================================
                # OPEN GENERATED DOCX
                # ====================================================

                status_text.write(
                    "Applying PDF page size..."
                )

                document = Document(
                    temp_docx_path
                )


                # ====================================================
                # APPLY PDF PAGE SIZE
                # ====================================================

                # PDF unit:
                # 1 point = 1/72 inch
                #
                # Therefore:
                #
                # inches = points / 72
                #

                pdf_width_inches = (
                    page_width / 72
                )

                pdf_height_inches = (
                    page_height / 72
                )


                for section in document.sections:

                    # ------------------------------------------------
                    # Preserve the actual PDF page dimensions
                    # ------------------------------------------------

                    if orientation == "Landscape":

                        section.orientation = (
                            WD_ORIENT.LANDSCAPE
                        )

                    else:

                        section.orientation = (
                            WD_ORIENT.PORTRAIT
                        )

                    # IMPORTANT:
                    # Set width and height directly from PDF.
                    # Do NOT force Letter/A4.
                    #

                    section.page_width = (
                        section.page_width
                    )

                    section.page_height = (
                        section.page_height
                    )


                    # ------------------------------------------------
                    # Set dimensions according to PDF
                    # ------------------------------------------------

                    from docx.shared import Inches

                    section.page_width = Inches(
                        pdf_width_inches
                    )

                    section.page_height = Inches(
                        pdf_height_inches
                    )


                progress_bar.progress(
                    90
                )


                # ====================================================
                # SAVE FINAL DOCX
                # ====================================================

                status_text.write(
                    "Finalizing Word document..."
                )

                document.save(
                    temp_docx_path
                )

                progress_bar.progress(
                    100
                )

                status_text.empty()

                progress_bar.empty()


                # ====================================================
                # READ WORD FILE
                # ====================================================

                with open(
                    temp_docx_path,
                    "rb"
                ) as word_file:

                    word_bytes = (
                        word_file.read()
                    )


                # ====================================================
                # SUCCESS
                # ====================================================

                st.success(
                    "PDF successfully converted "
                    f"to Word ({orientation})."
                )


                # ====================================================
                # DOWNLOAD
                # ====================================================

                output_name = (
                    uploaded_file.name
                    .rsplit(".", 1)[0]
                    + ".docx"
                )

                st.download_button(
                    label="⬇️ Download Word",
                    data=word_bytes,
                    file_name=output_name,
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.wordprocessingml.document"
                    ),
                    use_container_width=True
                )


            except Exception as e:

                st.error(
                    "An error occurred during conversion."
                )

                st.code(
                    str(e)
                )


            finally:

                # ====================================================
                # CLEAN TEMPORARY FILES
                # ====================================================

                if (
                    temp_pdf_path
                    and os.path.exists(
                        temp_pdf_path
                    )
                ):

                    os.remove(
                        temp_pdf_path
                    )

                if (
                    temp_docx_path
                    and os.path.exists(
                        temp_docx_path
                    )
                ):

                    os.remove(
                        temp_docx_path
                    )


        # ====================================================
        # CLOSE PDF
        # ====================================================

        pdf_document.close()


    except Exception as e:

        st.error(
            f"Unable to open the PDF: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Internal Doc Convert &nbsp;•&nbsp; PDF to Word
    </div>
    """,
    unsafe_allow_html=True
)