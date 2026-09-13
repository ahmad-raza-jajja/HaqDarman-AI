import pandas as pd
import re


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def clean_text(value):
    """
    Convert a value into a normalized lowercase string.
    Handles NaN, None, spaces and common formatting issues.
    """

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    text = str(value).strip().lower()

    # Normalize common separators
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text


def is_empty(value):
    """
    Check whether an Excel value is empty.
    """

    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass

    return clean_text(value) in {
        "",
        "nan",
        "none",
        "null",
        "n/a",
        "na",
        "-"
    }


# ==================================================
# PROVINCE NORMALIZATION
# ==================================================

def normalize_province(province):

    province = clean_text(province)

    aliases = {
        "punjab": "punjab",

        "sindh": "sindh",

        "kpk": "khyber pakhtunkhwa",
        "kp": "khyber pakhtunkhwa",
        "nwfp": "khyber pakhtunkhwa",
        "khyber pakhtunkhwa": "khyber pakhtunkhwa",

        "balochistan": "balochistan",

        "ict": "islamabad capital territory",
        "islamabad": "islamabad capital territory",
        "islamabad capital territory": "islamabad capital territory",

        "gb": "gilgit-baltistan",
        "gilgit baltistan": "gilgit-baltistan",
        "gilgit-baltistan": "gilgit-baltistan",

        "ajk": "azad jammu and kashmir",
        "azad jammu & kashmir": "azad jammu and kashmir",
        "azad jammu and kashmir": "azad jammu and kashmir",
    }

    return aliases.get(province, province)


# ==================================================
# PROVINCE CHECK
# ==================================================

def province_matches(user_province, program_row):

    user_province = normalize_province(user_province)

    scope = clean_text(program_row.get("scope", ""))
    program_province = clean_text(
        program_row.get("province", "")
    )

    combined = f"{scope} {program_province}"

    # ----------------------------------------------
    # Pakistan-wide programs
    # ----------------------------------------------

    pakistan_wide_terms = [
        "pakistan-wide",
        "pakistan wide",
        "all pakistan",
        "nationwide",
        "national",
        "whole pakistan",
        "across pakistan"
    ]

    if any(term in combined for term in pakistan_wide_terms):
        return True

    # ----------------------------------------------
    # No province restriction
    # ----------------------------------------------

    if program_province in {
        "",
        "all",
        "any",
        "all provinces",
        "all regions"
    }:
        return True

    # ----------------------------------------------
    # Normalize program province
    # ----------------------------------------------

    program_normalized = normalize_province(
        program_province
    )

    # ----------------------------------------------
    # Exact normalized match
    # ----------------------------------------------

    if user_province == program_normalized:
        return True

    # ----------------------------------------------
    # Partial match
    # ----------------------------------------------

    if user_province in program_normalized:
        return True

    if program_normalized in user_province:
        return True

    return False


# ==================================================
# AGE CHECK
# ==================================================

def age_matches(age, program_row):

    try:
        user_age = float(age)
    except (ValueError, TypeError):
        return True

    min_age = program_row.get("min_age", "")
    max_age = program_row.get("max_age", "")

    # ----------------------------------------------
    # Minimum age
    # ----------------------------------------------

    if not is_empty(min_age):

        try:
            if user_age < float(min_age):
                return False
        except (ValueError, TypeError):
            pass

    # ----------------------------------------------
    # Maximum age
    # ----------------------------------------------

    if not is_empty(max_age):

        try:
            if user_age > float(max_age):
                return False
        except (ValueError, TypeError):
            pass

    return True


# ==================================================
# EDUCATION NORMALIZATION
# ==================================================

def normalize_education(value):

    value = clean_text(value)

    if not value:
        return ""

    value = value.replace("&", "and")
    value = value.replace("/", " ")
    value = value.replace("-", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


# ==================================================
# EDUCATION CHECK
# ==================================================

def education_matches(user_education, program_education):

    user_education = normalize_education(
        user_education
    )

    program_education = normalize_education(
        program_education
    )

    # ----------------------------------------------
    # User selected Any
    # ----------------------------------------------

    if user_education in {
        "",
        "any",
        "all"
    }:
        return True

    # ----------------------------------------------
    # Program has no education restriction
    # ----------------------------------------------

    if program_education in {
        "",
        "any",
        "all",
        "all levels",
        "any level",
        "not specified"
    }:
        return True

    # ----------------------------------------------
    # Direct match
    # ----------------------------------------------

    if user_education == program_education:
        return True

    if user_education in program_education:
        return True

    # ----------------------------------------------
    # Education groups
    # ----------------------------------------------

    education_groups = {

        "matric": [
            "matric",
            "matriculation",
            "secondary",
            "secondary school",
            "10th",
            "grade 10"
        ],

        "intermediate": [
            "intermediate",
            "higher secondary",
            "hssc",
            "12th",
            "grade 12",
            "college"
        ],

        "university": [
            "university",
            "undergraduate",
            "bachelor",
            "bachelors",
            "bs",
            "bsc",
            "ba",
            "bba",
            "bcom",
            "mbbs",
            "bds"
        ],

        "graduate": [
            "graduate",
            "bachelor",
            "bachelors",
            "undergraduate",
            "bs",
            "bsc",
            "ba",
            "bba",
            "bcom",
            "mbbs",
            "bds"
        ],

        "postgraduate": [
            "postgraduate",
            "post graduate",
            "master",
            "masters",
            "ms",
            "msc",
            "mphil",
            "phd",
            "mba",
            "mcom"
        ]
    }

    # ----------------------------------------------
    # User education group
    # ----------------------------------------------

    user_keywords = education_groups.get(
        user_education,
        [user_education]
    )

    # ----------------------------------------------
    # Check program education
    # ----------------------------------------------

    for keyword in user_keywords:

        if keyword in program_education:
            return True

    # ----------------------------------------------
    # Also check common program group wording
    # ----------------------------------------------

    if user_education == "university":

        university_terms = [
            "university",
            "undergraduate",
            "bachelor",
            "bs",
            "bsc",
            "ba",
            "bba",
            "bcom",
            "mbbs",
            "bds"
        ]

        if any(
            term in program_education
            for term in university_terms
        ):
            return True

    if user_education == "postgraduate":

        postgraduate_terms = [
            "postgraduate",
            "master",
            "ms",
            "msc",
            "mphil",
            "phd",
            "mba"
        ]

        if any(
            term in program_education
            for term in postgraduate_terms
        ):
            return True

    return False


# ==================================================
# STUDENT STATUS CHECK
# ==================================================

def student_status_matches(
    user_student_status,
    required_status
):

    required = clean_text(required_status)

    # ----------------------------------------------
    # No restriction
    # ----------------------------------------------

    if required in {
        "",
        "any",
        "all",
        "no",
        "false",
        "not required",
        "optional",
        "not specified",
        "nan"
    }:
        return True

    # ----------------------------------------------
    # Required student
    # ----------------------------------------------

    student_required_values = {
        "yes",
        "true",
        "1",
        "required",
        "student",
        "students",
        "currently a student",
        "current student"
    }

    if required in student_required_values:

        return bool(user_student_status)

    # ----------------------------------------------
    # Text contains student requirement
    # ----------------------------------------------

    if "student" in required:

        return bool(user_student_status)

    # ----------------------------------------------
    # Unknown value
    # Don't reject program unnecessarily
    # ----------------------------------------------

    return True


# ==================================================
# INCOME CHECK
# ==================================================

def income_matches(user_income, program_income):

    if is_empty(program_income):
        return True

    try:
        user_income = float(user_income)
    except (ValueError, TypeError):
        return True

    # If Excel stores numeric value
    if isinstance(program_income, (int, float)):

        try:
            return user_income <= float(program_income)
        except (ValueError, TypeError):
            return True

    income_text = clean_text(program_income)

    # ----------------------------------------------
    # No income restriction
    # ----------------------------------------------

    no_restriction_terms = [
        "not income-tested",
        "not income tested",
        "no income limit",
        "no income restriction",
        "not specified",
        "any income",
        "all income"
    ]

    if any(
        term in income_text
        for term in no_restriction_terms
    ):
        return True

    # ----------------------------------------------
    # Extract numbers
    # ----------------------------------------------

    numbers = re.findall(
        r"\d+(?:,\d+)*(?:\.\d+)?",
        income_text
    )

    if not numbers:
        return True

    try:

        numeric_values = [
            float(number.replace(",", ""))
            for number in numbers
        ]

    except (ValueError, TypeError):
        return True

    # ----------------------------------------------
    # Income range
    # Example:
    # 0 - 50000
    # ----------------------------------------------

    if len(numeric_values) >= 2:

        lower = numeric_values[0]
        upper = numeric_values[1]

        # Handle reversed range safely
        if lower > upper:
            lower, upper = upper, lower

        return lower <= user_income <= upper

    # ----------------------------------------------
    # Single maximum income
    # ----------------------------------------------

    maximum_income = numeric_values[0]

    return user_income <= maximum_income


# ==================================================
# SAFE VALUE
# ==================================================

def safe_value(value, default=""):

    if is_empty(value):
        return default

    return str(value).strip()


# ==================================================
# MAIN MATCHING FUNCTION
# ==================================================

def find_matching_programs(user, programs):

    matches = []

    if programs is None:
        return matches

    if not isinstance(programs, pd.DataFrame):
        return matches

    if programs.empty:
        return matches

    for row_index, program in programs.iterrows():

        try:

            # ======================================
            # PROVINCE
            # ======================================

            if not province_matches(
                user.get("province", ""),
                program
            ):
                continue

            # ======================================
            # AGE
            # ======================================

            if not age_matches(
                user.get("age"),
                program
            ):
                continue

            # ======================================
            # EDUCATION
            # ======================================

            if not education_matches(
                user.get("education", ""),
                program.get("education_level", "")
            ):
                continue

            # ======================================
            # STUDENT STATUS
            # ======================================

            if not student_status_matches(
                user.get("student_status", False),
                program.get("student_status_required", "")
            ):
                continue

            # ======================================
            # INCOME
            # ======================================

            if not income_matches(
                user.get("income", 0),
                program.get(
                    "max_monthly_income_pkr",
                    ""
                )
            ):
                continue

            # ======================================
            # PROGRAM DATA
            # ======================================

            program_id = safe_value(
                program.get(
                    "program_id",
                    ""
                ),
                str(row_index + 1)
            )

            program_name = safe_value(
                program.get(
                    "program_name",
                    ""
                ),
                "Program name not available"
            )

            program_name_ur = safe_value(
                program.get(
                    "program_name_ur",
                    ""
                ),
                program_name
            )

            category = safe_value(
                program.get(
                    "category",
                    ""
                ),
                "Not specified"
            )

            organization = safe_value(
                program.get(
                    "implementing_agency",
                    ""
                ),
                "Not specified"
            )

            province = safe_value(
                program.get(
                    "province",
                    ""
                ),
                "Not specified"
            )

            description = safe_value(
                program.get(
                    "benefits_coverage",
                    ""
                ),
                "No description available."
            )

            documents = safe_value(
                program.get(
                    "required_documents",
                    ""
                )
            )

            application_steps = safe_value(
                program.get(
                    "application_steps",
                    ""
                ),
                "Application information is not available."
            )

            official_url = safe_value(
                program.get(
                    "official_url",
                    ""
                )
            )

            helpline = safe_value(
                program.get(
                    "helpline",
                    ""
                )
            )

            special_criteria = safe_value(
                program.get(
                    "special_criteria",
                    ""
                )
            )

            last_verified = safe_value(
                program.get(
                    "last_verified",
                    ""
                ),
                "Not available"
            )

            # ======================================
            # MATCH REASONS
            # ======================================

            reasons = [
                "Your province matches the program.",
                "Your age meets the program's age criteria.",
                "Your education level matches the program requirements.",
                "Your household income meets the available income criteria."
            ]

            if user.get("student_status", False):

                required_status = clean_text(
                    program.get(
                        "student_status_required",
                        ""
                    )
                )

                if required_status in {
                    "yes",
                    "true",
                    "1",
                    "required",
                    "student",
                    "students"
                }:

                    reasons.append(
                        "You meet the student-status requirement."
                    )

                else:

                    reasons.append(
                        "You are currently a student."
                    )

            # ======================================
            # SAVE MATCH
            # ======================================

            matches.append({

                "program": {

                    "program_id": program_id,

                    "program_name": program_name,

                    "program_name_ur": program_name_ur,

                    "category": category,

                    "organization": organization,

                    "province": province,

                    "description": description,

                    "documents": documents,

                    "application_steps": application_steps,

                    "official_url": official_url,

                    "helpline": helpline,

                    "special_criteria": special_criteria,

                    "last_verified": last_verified
                },

                "score": 100,

                "reasons": reasons

            })

        except Exception as error:

            print(
                f"[SKIPPED ROW {row_index}] "
                f"unexpected error: {error}"
            )

            continue

    return matches