import streamlit as st
import pandas as pd
from pathlib import Path

from src.eligibility import find_matching_programs
from src.llm import generate_explanation


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="HaqDarmand AI",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 2.5rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(
            135deg,
            #e8f5e9,
            #e3f2fd
        );
        border: 1px solid #d9e6df;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# LOAD PROGRAM DATA
# ==========================================

@st.cache_data
def load_programs():

    excel_path = Path("data") / "programs.xlsx"

    if not excel_path.exists():

        st.error(
            "programs.xlsx was not found. "
            "Please make sure the file exists inside the data folder."
        )

        st.stop()

    try:

        df = pd.read_excel(excel_path)

    except PermissionError:

        st.error(
            "Permission denied while reading programs.xlsx. "
            "Please close the Excel file if it is open and restart the app."
        )

        st.stop()

    except Exception as error:

        st.error(
            f"Could not read programs.xlsx: {error}"
        )

        st.stop()

    # ------------------------------------------
    # Clean column names
    # ------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


programs = load_programs()


# ==========================================
# LANGUAGE
# ==========================================

language = st.selectbox(
    "🌐 Language",
    [
        "English",
        "اردو"
    ]
)


is_urdu = language == "اردو"


# ==========================================
# LANGUAGE TEXT
# ==========================================

if is_urdu:

    title = "🤝 حق دارمند AI"

    subtitle = "پاکستان کے لیے AI پر مبنی فوائد تلاش کرنے والا نظام"

    description = (
        "اپنے لیے موزوں وظائف، مالی معاونت اور "
        "صحت سے متعلق معاونتی پروگرام تلاش کریں۔"
    )

    about_title = "👤 اپنے بارے میں بتائیں"

    age_label = "عمر"

    province_label = "صوبہ / علاقہ"

    education_label = "تعلیمی سطح"

    student_label = "🎓 میں اس وقت طالب علم ہوں"

    income_label = "ماہانہ گھریلو آمدنی (PKR)"

    family_label = "خاندان کے افراد کی تعداد"

    support_title = "🎯 آپ کس قسم کی معاونت چاہتے ہیں؟"

    category_label = "زمرہ منتخب کریں"

    find_button = "🔎 میرے لیے فوائد تلاش کریں"

    results_title = "✨ آپ کے لیے ممکنہ پروگرامز"

    no_matches = (
        "فراہم کردہ معلومات کی بنیاد پر کوئی "
        "مماثل پروگرام نہیں ملا۔"
    )

    matches_found = "ہمیں آپ کے لیے ممکنہ طور پر موزوں پروگرام ملا۔"

    matches_found_plural = "ہمیں آپ کے لیے ممکنہ طور پر موزوں پروگرامز ملے۔"

    organization_label = "ادارہ"

    category_result_label = "زمرہ"

    region_label = "علاقہ"

    score_label = "📊 مماثلت کا اسکور"

    potential_match = "ممکنہ مماثلت"

    why_match = "### ✅ یہ پروگرام آپ کے لیے کیوں موزوں ہو سکتا ہے"

    documents_label = "### 📄 مطلوبہ دستاویزات"

    no_documents = "دستاویزات کی معلومات دستیاب نہیں۔"

    application_label = "### 📝 درخواست دینے کا طریقہ"

    official_label = "### 🔗 سرکاری ذریعہ"

    open_source = "سرکاری ذریعہ کھولیں"

    last_verified_label = "آخری تصدیق"

    ai_explanation = "🤖 AI وضاحت"

    generating = "وضاحت تیار کی جا رہی ہے..."

    ai_error = "AI وضاحت تیار نہیں کی جا سکی۔"

    api_error = "براہ کرم اپنی Google API configuration چیک کریں۔"

    footer_text = (
        "یہ ایپ صرف معلوماتی مماثلت فراہم کرتی ہے۔ "
        "حتمی اہلیت کی تصدیق ہمیشہ متعلقہ پروگرام کے سرکاری ذریعہ سے کریں۔"
    )

else:

    title = "🤝 HaqDarmand AI"

    subtitle = "AI-Powered Benefits Finder for Pakistan"

    description = (
        "Discover scholarships, financial assistance, "
        "and health-support programs that may be relevant to you."
    )

    about_title = "👤 Tell Us About Yourself"

    age_label = "Age"

    province_label = "Province / Region"

    education_label = "Education Level"

    student_label = "🎓 I am currently a student"

    income_label = "Monthly Household Income (PKR)"

    family_label = "Family Size"

    support_title = "🎯 What Support Are You Looking For?"

    category_label = "Select a category"

    find_button = "🔎 Find My Benefits"

    results_title = "✨ Your Potential Matches"

    no_matches = (
        "No matching programs were found based on the "
        "information provided."
    )

    matches_found = "We found 1 potentially relevant program."

    matches_found_plural = "We found {} potentially relevant program(s)."

    organization_label = "Organization"

    category_result_label = "Category"

    region_label = "Region"

    score_label = "📊 Match Score"

    potential_match = "potential match"

    why_match = "### ✅ Why It May Match"

    documents_label = "### 📄 Required Documents"

    no_documents = "No document information available."

    application_label = "### 📝 How to Apply"

    official_label = "### 🔗 Official Source"

    open_source = "Open Official Source"

    last_verified_label = "Last verified"

    ai_explanation = "🤖 AI Explanation"

    generating = "Generating explanation..."

    ai_error = "AI explanation could not be generated."

    api_error = "Please check your Google API configuration."

    footer_text = (
        "This application provides informational matches only. "
        "Final eligibility must always be confirmed through the official program source."
    )


# ==========================================
# HEADER
# ==========================================

st.markdown(
    f"""<div class="hero"><h1>{title}</h1><p>{subtitle}</p><p>{description}</p></div>""",
    unsafe_allow_html=True
)


# ==========================================
# USER INFORMATION
# ==========================================

st.markdown(
    f'<div class="section-title">{about_title}</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    age = st.number_input(
        age_label,
        min_value=1,
        max_value=100,
        value=21
    )

    province = st.selectbox(
        province_label,
        [
            "Punjab",
            "Sindh",
            "Khyber Pakhtunkhwa",
            "Balochistan",
            "Islamabad Capital Territory",
            "Gilgit-Baltistan",
            "Azad Jammu and Kashmir"
        ]
    )

    education = st.selectbox(
        education_label,
        [
            "Any",
            "Matric",
            "Intermediate",
            "University",
            "Graduate",
            "Postgraduate"
        ]
    )


with col2:

    student_status = st.checkbox(
        student_label
    )

    income = st.number_input(
        income_label,
        min_value=0,
        value=50000,
        step=5000
    )

    family_size = st.number_input(
        family_label,
        min_value=1,
        max_value=30,
        value=4
    )


# ==========================================
# SUPPORT CATEGORY
# ==========================================

st.markdown(
    f'<div class="section-title">{support_title}</div>',
    unsafe_allow_html=True
)

category_options = {
    "All": "تمام",
    "Scholarship": "اسکالرشپ",
    "Financial Assistance": "مالی معاونت",
    "Health Support": "صحت کی معاونت"
}

if is_urdu:

    category_display = st.selectbox(
        category_label,
        list(category_options.values())
    )

    reverse_category = {
        value: key
        for key, value in category_options.items()
    }

    category = reverse_category[category_display]

else:

    category = st.selectbox(
        category_label,
        [
            "All",
            "Scholarship",
            "Financial Assistance",
            "Health Support"
        ]
    )


st.divider()


# ==========================================
# FIND BENEFITS
# ==========================================

if st.button(
    find_button,
    type="primary",
    use_container_width=True
):

    user = {

        "age": age,

        "province": province,

        "education": education,

        "student_status": student_status,

        "income": income,

        "family_size": family_size
    }

    st.session_state["user"] = user

    # ======================================
    # CATEGORY FILTER
    # ======================================

    filtered_programs = programs.copy()

    if category != "All":

        if "category" not in filtered_programs.columns:

            st.error(
                "The 'category' column is missing from programs.xlsx."
            )

            st.stop()

        category_series = (
            filtered_programs["category"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        filtered_programs = filtered_programs[
            category_series == category.strip().lower()
        ]

    # ======================================
    # ELIGIBILITY MATCHING
    # ======================================

    try:

        matches = find_matching_programs(
            user,
            filtered_programs
        )

    except Exception as error:

        st.error(
            "An error occurred while checking eligibility."
        )

        st.exception(error)

        st.stop()

    # ======================================
    # SAVE RESULTS
    # ======================================

    st.session_state["matches"] = matches


# ==========================================
# RESULTS
# ==========================================

if "matches" in st.session_state:

    matches = st.session_state["matches"]

    st.divider()

    st.markdown(
        f'<div class="section-title">{results_title}</div>',
        unsafe_allow_html=True
    )

    # ======================================
    # NO MATCHES
    # ======================================

    if not matches:

        st.info(no_matches)

    # ======================================
    # MATCHES FOUND
    # ======================================

    else:

        if is_urdu:

            if len(matches) == 1:
                st.success(matches_found)
            else:
                st.success(
                    f"{len(matches)} ممکنہ طور پر موزوں پروگرامز ملے۔"
                )

        else:

            st.success(
                matches_found_plural.format(
                    len(matches)
                )
            )

        # ==================================
        # DISPLAY EACH PROGRAM
        # ==================================

        for index, result in enumerate(matches):

            program = result["program"]

            score = result.get(
                "score",
                0
            )

            reasons = result.get(
                "reasons",
                []
            )

            # ----------------------------------
            # LANGUAGE-SPECIFIC PROGRAM NAME
            # ----------------------------------

            if is_urdu:

                program_name = program.get(
                    "program_name_ur",
                    program.get(
                        "program_name",
                        "پروگرام کا نام دستیاب نہیں"
                    )
                )

            else:

                program_name = program.get(
                    "program_name",
                    "Program name not available"
                )

            # ----------------------------------
            # OTHER VALUES
            # ----------------------------------

            organization = program.get(
                "organization",
                "Not specified"
            )

            program_category = program.get(
                "category",
                "Not specified"
            )

            program_province = program.get(
                "province",
                "Not specified"
            )

            description = program.get(
                "description",
                "No description available."
            )

            documents = program.get(
                "documents",
                ""
            )

            application_steps = program.get(
                "application_steps",
                "Application information is not available."
            )

            official_url = program.get(
                "official_url",
                ""
            )

            last_verified = program.get(
                "last_verified",
                "Not specified"
            )

            # ==================================
            # PROGRAM CARD
            # ==================================

            with st.container(border=True):

                st.subheader(
                    f"🎓 {program_name}"
                )

                # ----------------------------------
                # BASIC INFORMATION
                # ----------------------------------

                st.write(
                    f"**{organization_label}:** "
                    f"{organization}"
                )

                st.write(
                    f"**{category_result_label}:** "
                    f"{program_category}"
                )

                st.write(
                    f"**{region_label}:** "
                    f"{program_province}"
                )

                st.write(
                    description
                )

                # ----------------------------------
                # MATCH SCORE
                # ----------------------------------

                st.write(
                    score_label
                )

                try:

                    numeric_score = float(score)

                except (ValueError, TypeError):

                    numeric_score = 0

                numeric_score = max(
                    0,
                    min(
                        numeric_score,
                        100
                    )
                )

                st.progress(
                    numeric_score / 100
                )

                if is_urdu:

                    st.write(
                        f"**{numeric_score:.0f}% "
                        f"مماثلت کا امکان**"
                    )

                else:

                    st.write(
                        f"**{numeric_score:.0f}% "
                        f"{potential_match}**"
                    )

                # ----------------------------------
                # MATCH REASONS
                # ----------------------------------

                if reasons:

                    if is_urdu:

                        st.write(
                            why_match
                        )

                        urdu_reasons = [
                            "آپ کا صوبہ پروگرام کی ضروریات سے مطابقت رکھتا ہے۔",
                            "آپ کی عمر پروگرام کی عمر کی حد کے مطابق ہے۔",
                            "آپ کی تعلیمی سطح پروگرام کی ضروریات سے مطابقت رکھتی ہے۔",
                            "آپ کی گھریلو آمدنی دستیاب آمدنی کی شرط پر پورا اترتی ہے۔",
                            "آپ طالب علم کی حیثیت سے مطلوبہ شرط پوری کرتے ہیں۔",
                            "آپ اس وقت طالب علم ہیں۔"
                        ]

                        for reason_index, reason in enumerate(reasons):

                            if reason_index < len(urdu_reasons):

                                st.write(
                                    f"✓ {urdu_reasons[reason_index]}"
                                )

                            else:

                                st.write(
                                    f"✓ {reason}"
                                )

                    else:

                        st.write(
                            why_match
                        )

                        for reason in reasons:

                            st.write(
                                f"✓ {reason}"
                            )

                # ----------------------------------
                # DOCUMENTS
                # ----------------------------------

                st.write(
                    documents_label
                )

                if pd.isna(documents) or not str(
                    documents
                ).strip():

                    st.write(
                        no_documents
                    )

                else:

                    document_list = str(
                        documents
                    ).split(";")

                    for document in document_list:

                        document = document.strip()

                        if document:

                            st.write(
                                f"• {document}"
                            )

                # ----------------------------------
                # APPLICATION
                # ----------------------------------

                st.write(
                    application_label
                )

                st.write(
                    application_steps
                )

                # ----------------------------------
                # OFFICIAL SOURCE
                # ----------------------------------

                if (
                    official_url
                    and not pd.isna(official_url)
                    and str(official_url).strip()
                ):

                    st.write(
                        official_label
                    )

                    st.link_button(
                        open_source,
                        str(official_url).strip()
                    )

                # ----------------------------------
                # LAST VERIFIED
                # ----------------------------------

                st.caption(
                    f"{last_verified_label}: "
                    f"{last_verified}"
                )

                # ----------------------------------
                # AI EXPLANATION
                # ----------------------------------

                with st.expander(
                    ai_explanation
                ):

                    try:

                        with st.spinner(
                            generating
                        ):

                            explanation = generate_explanation(
                                user,
                                program
                            )

                        st.write(
                            explanation
                        )

                    except Exception:

                        st.error(
                            ai_error
                        )

                        st.caption(
                            api_error
                        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    f"""<div class="footer">🤝 HaqDarmand AI<br><br>{footer_text}</div>""",
    unsafe_allow_html=True
)
