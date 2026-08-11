import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Internal Doc Convert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #1f2937;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 35px;
    }

    /* Section title */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #1f2937;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Tool card */
    .tool-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 28px;
        min-height: 230px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .tool-icon {
        font-size: 36px;
        margin-bottom: 10px;
    }

    .tool-title {
        font-size: 21px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 8px;
    }

    .tool-description {
        font-size: 15px;
        color: #6b7280;
        line-height: 1.5;
        min-height: 48px;
    }

    /* Footer */
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
    '<div class="main-title">INTERNAL DOC CONVERT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Internal document conversion tools for your daily document needs.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# WELCOME
# ============================================================

st.markdown(
    """
    ### Welcome 👋

    Easily convert, merge, and manage your document files using
    the tools below.
    """,
    unsafe_allow_html=False
)

st.markdown(
    '<div class="section-title">What do you want to do?</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOOL CARDS
# ============================================================

col1, col2 = st.columns(2, gap="large")


# ------------------------------------------------------------
# CARD 1 - CONVERT / MERGE PDF
# ------------------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📄</div>
            <div class="tool-title">Convert / Merge PDF</div>
            <div class="tool-description">
                Convert PDF files or combine multiple PDF documents
                into a single file.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/1_Convert_Merge_PDF.py",
        label="Open Tool →",
        icon="📄"
    )


# ------------------------------------------------------------
# CARD 2 - PDF TO JPG
# ------------------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">🖼️</div>
            <div class="tool-title">PDF to JPG</div>
            <div class="tool-description">
                Convert PDF pages into high-quality JPG images
                for easier sharing and use.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/2_PDF_to_JPG.py",
        label="Open Tool →",
        icon="🖼️"
    )


# ============================================================
# SECOND ROW
# ============================================================

col3, col4 = st.columns(2, gap="large")


# ------------------------------------------------------------
# CARD 3 - JPG TO PDF
# ------------------------------------------------------------

with col3:

    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📑</div>
            <div class="tool-title">JPG to PDF</div>
            <div class="tool-description">
                Convert one or multiple JPG images into a
                single PDF document.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/3_JPG_to_PDF.py",
        label="Open Tool →",
        icon="📑"
    )


# ------------------------------------------------------------
# CARD 4 - PDF TO WORD
# ------------------------------------------------------------

with col4:

    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📝</div>
            <div class="tool-title">PDF to Word</div>
            <div class="tool-description">
                Convert PDF documents into editable Microsoft
                Word files.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/4_PDF_to_Word.py",
        label="Open Tool →",
        icon="📝"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Internal Doc Convert &nbsp;•&nbsp; Internal Document Tools
    </div>
    """,
    unsafe_allow_html=True
)