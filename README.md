# 🇵🇰 HaqDarmand AI

### AI-Powered Benefits Finder for Pakistan

**HaqDarmand AI** is an AI-powered decision-support platform designed to help people in Pakistan discover government, educational, financial, healthcare, and other support programs they may qualify for.

Instead of searching through scattered information across different websites and documents, users can provide their basic information and receive relevant programs, match scores, eligibility reasons, required documents, application guidance, official sources, and an AI-generated explanation in a simple interface.

> **HaqDarmand AI does not provide official eligibility decisions.**
> It helps users identify potentially relevant programs based on the information they provide. Final eligibility should always be confirmed through the respective official source.

---

## 🎯 The Problem

Millions of people may be eligible for scholarships, financial assistance, healthcare support, and other public-benefit programs, but discovering the right opportunities can be difficult.

Information is often:

* Scattered across different platforms
* Difficult to search and compare
* Presented with complex eligibility requirements
* Difficult to understand for non-technical users
* Missing a personalized way to determine which programs may be relevant

As a result, eligible individuals may never discover programs that could benefit them.

---

## 💡 Our Solution

**HaqDarmand AI** brings program discovery and personalized matching into one simple platform.

Users provide information such as:

* Age
* Province
* Education level
* Student status
* Income
* Family size
* Desired support category

The system processes this information against a verified program dataset and identifies potentially relevant programs.

The platform then presents:

1. Relevant programs
2. Match scores
3. Reasons for the match
4. Program descriptions
5. Required documents
6. Application steps
7. Official sources
8. Last verification information
9. AI-generated explanations
10. English/Urdu interface support

---

# ✨ Key Features

### 🔎 Personalized Benefits Discovery

Users enter their information once and receive programs that may be relevant to their circumstances.

### 📊 Eligibility Matching

The eligibility engine compares user information against program requirements and produces match scores and reasons.

Example:

```text
Match Score: 85%

✓ Province matches
✓ Education level matches
✓ Student status matches
✓ Income appears within requirement
```

### 🤖 AI-Powered Explanations

The AI explains:

* Why a program may be relevant
* Which requirements appear to match
* What documents may be required
* What the user should do next

The system is designed to provide decision support rather than claim official eligibility.

### 🧠 Retrieval / RAG

The retrieval layer finds relevant program information based on user queries and connects that information with the AI explanation system.

Example:

```text
User:
"Which scholarships are available for university students?"

        ↓

Retrieval System

        ↓

Relevant Program Information

        ↓

AI Explanation
```

### 🇵🇰 Pakistan-Focused Program Data

The project uses a curated dataset of **8–12 real and verified Pakistani programs**, with important eligibility information collected from reliable sources.

Each program can include:

* Program name
* Organization
* Category
* Province
* Description
* Age requirements
* Education requirements
* Income requirements
* Student requirements
* Family requirements
* Required documents
* Application procedure
* Official URL
* Verification date

### 🌐 English & Urdu

The interface supports both **English and Urdu**, making the platform more accessible to users across Pakistan.

### 📋 Program Details

Each result can provide:

* Program information
* Organization
* Description
* Match score
* Required documents
* How to apply
* Official source
* Last verified date

---

# 🏗️ How It Works

```text
                    ┌─────────────────────┐
                    │   Verified Program  │
                    │        Data         │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Eligibility Matching │
                    │      + Retrieval     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AI Explanation    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Final Results    │
                    └─────────────────────┘
```

The project's workflow separates the data, AI/eligibility, frontend, integration, and documentation responsibilities so that each component can be developed and tested independently before final integration.

---

# 🧠 System Architecture

HaqDarmand AI follows a modular architecture:

```text
User
 │
 ▼
Streamlit Interface
 │
 │ User Information
 ▼
Eligibility Matching
 │
 ├──────────────► Match Scores
 │
 ├──────────────► Match Reasons
 │
 ▼
Retrieval / RAG
 │
 ▼
Relevant Program Information
 │
 ▼
AI Explanation
 │
 ▼
Program Results
 │
 ├── Program Details
 ├── Required Documents
 ├── Application Steps
 ├── Official Source
 └── Verification Date
```

---

# 🔄 User Flow

```text
1. User opens HaqDarmand AI
              ↓
2. Selects language
              ↓
3. Enters personal information
              ↓
4. Selects benefit category
              ↓
5. Clicks "Find My Benefits"
              ↓
6. System matches user information
              ↓
7. Relevant programs are retrieved
              ↓
8. Match scores and reasons are generated
              ↓
9. AI explanation is displayed
              ↓
10. User reviews requirements and official source
```

---

# 📂 Project Structure

The project is organized around a modular application structure:

```text
HaqDarmand-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── programs.csv
│
├── src/
│   ├── eligibility.py
│   ├── retriever.py
│   └── llm.py
│
└── assets/
```

The workflow defines `programs.csv` as the shared data interface between the data, AI/eligibility, and frontend components.

---

# 📊 Program Dataset

The core dataset follows a consistent structure:

```text
program_id
program_name
category
organization
province
description
min_age
max_age
education_level
income_limit
student_required
family_size_min
documents
application_steps
official_url
last_verified
```

The project emphasizes verification of important eligibility information against reliable or official sources rather than inventing eligibility criteria.

---

# 🤖 AI & Eligibility Pipeline

The AI component is designed around three major functions:

```text
find_matching_programs()
retrieve_programs()
generate_explanation()
```

### 1. Eligibility Matching

**Input:**

```python
user = {
    "age": 21,
    "province": "Punjab",
    "education": "University",
    "student_status": True,
    "income": 50000,
    "family_size": 4
}
```

**Output:**

```text
Program
Match Score
Reasons
```

### 2. Retrieval

The retrieval system identifies program information relevant to the user's query or circumstances.

### 3. AI Explanation

The AI transforms relevant program information into an understandable explanation for the user.

The explanation should communicate potential matches rather than make an official eligibility claim.

---

# 🛠️ Technology Stack

| Technology              | Purpose                                |
| ----------------------- | -------------------------------------- |
| **Python**              | Core application logic                 |
| **Streamlit**           | Interactive web interface              |
| **RAG / Retrieval**     | Relevant program information retrieval |
| **LLM / Generative AI** | Natural-language explanations          |
| **CSV**                 | Program dataset                        |
| **Git & GitHub**        | Version control and collaboration      |

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python installed
* Git installed
* A cloned copy of this repository

## 1. Clone the Repository

```bash
git clone REPOSITORY_URL
cd HaqDarmand-AI
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Application

```bash
streamlit run app.py
```

The application should then be available through the local Streamlit address shown in your terminal.

---

# 🌐 Live Application

Try the deployed application:

**[🚀 Launch HaqDarmand AI — LIVE APP](LIVE_APP_URL)**

> Replace `LIVE_APP_URL` with the final deployed application URL before submission.

---

# 📸 Screenshots

### Home / Landing Page

![HaqDarmand AI Home](assets/screenshots/home.png)

### User Information Form

![User Information Form](assets/screenshots/form.png)

### Benefits Results

![Benefits Results](assets/screenshots/results.png)

### AI Explanation

![AI Explanation](assets/screenshots/ai-explanation.png)

> Add the final screenshots to `assets/screenshots/` before submitting the project.

---

# 🧪 Testing

The project includes testing across the complete application flow.

Example test scenarios include:

| Test Case            | Expected Result                                         |
| -------------------- | ------------------------------------------------------- |
| Punjab student       | Relevant programs displayed                             |
| Sindh student        | Relevant programs displayed                             |
| High-income user     | Programs with incompatible income requirements excluded |
| Different category   | Correct category results displayed                      |
| No matching programs | Clear no-match message                                  |
| Invalid/edge input   | Application handles input safely                        |
| Official URL         | Official source link works                              |
| Urdu interface       | Interface changes correctly                             |

The final integrated application should be tested after the frontend, eligibility system, retrieval system, and AI explanation layer are connected.

---

# 🔐 Important Disclaimer

HaqDarmand AI is a **decision-support and information-discovery tool**.

The match score generated by the system does **not** represent an official approval or eligibility decision.

Users should always:

1. Review the program requirements.
2. Check the required documents.
3. Visit the official program source.
4. Confirm current eligibility requirements.
5. Follow the official application process.

Program information may change over time, so users should rely on the official source for final confirmation.

---

# 🌍 Vision & Impact

HaqDarmand AI aims to make access to public and support programs more **discoverable, understandable, and personalized**.

The long-term vision is to reduce the information gap between people who need support and the programs designed to provide it.

Potential future directions include:

* Expanding the program database
* Supporting more categories of benefits
* Increasing language accessibility
* Improving eligibility matching
* Expanding retrieval capabilities
* Adding more verified program sources
* Improving accessibility for users with limited technical literacy
* Continuously updating program information

---

# 🔮 Future Improvements

Possible future improvements include:

* Larger and continuously maintained program dataset
* More advanced semantic retrieval
* Improved ranking and matching algorithms
* Additional Pakistani languages
* Automated program verification workflows
* More detailed application guidance
* Personalized recommendation history
* Mobile-focused experience
* Accessibility improvements
* Expanded government and private-sector support programs

---

# 👥 Team

HaqDarmand AI was developed as a collaborative hackathon project with clearly separated responsibilities across data, AI, frontend, integration, testing, and documentation.

| Member       | Responsibility                        |
| ------------ | ------------------------------------- |
| **Ahmad Raza** | Team Lead, GitHub & Integration       |
| **Kumar** | Data & Research                       |
| **Ukasha** | Eligibility, Retrieval/RAG & AI       |
| **Eman** | Frontend & Streamlit                  |
| **Ubaid Ullah** | Testing, Documentation & Presentation |

---

# 📦 Hackathon Submission

### Final Project Package

| Deliverable                      | Link                                     |
| -------------------------------- | ---------------------------------------- |
| 💻 GitHub Repository             | **[Repository](https://github.com/ahmad-raza-jajja/HaqDarman-AI)**  |
| 🚀 Live Application              | **[Live App](LIVE_APP_URL)**             |
| 📊 Presentation Slides           | **[Slides](https://docs.google.com/presentation/d/1Ev4QYuX26xImGuRe47SuLWLe738IQmqwN8BL7hCT4xA/edit?usp=sharing)**                 |
| 📋 Product Requirements Document | **[PRD](https://docs.google.com/document/d/1sJgdplzZXns3vlqx1lXasjqW2EQSOjJO/edit?usp=sharing&ouid=105894103748681231741&rtpof=true&sd=true)**                       |
| 🎥 Demo Video                    | **[Demo Video](DEMO_VIDEO_URL)**         |
| 🧪 Test Report / Bug Report      | **[Testing Documentation](TESTING_URL)** |



---

# 📑 Project Documentation

Additional project documentation:

* **PRD:** [https://docs.google.com/document/d/1sJgdplzZXns3vlqx1lXasjqW2EQSOjJO/edit?usp=sharing&ouid=105894103748681231741&rtpof=true&sd=true]
* **Presentation:** [https://docs.google.com/presentation/d/1Ev4QYuX26xImGuRe47SuLWLe738IQmqwN8BL7hCT4xA/edit?usp=sharing]
* **Demo:** [DEMO_VIDEO_URL]
* **Testing Report:** [TESTING_URL]

---

# 🏆 Hackathon Focus

HaqDarmand AI focuses on combining:

**Verified Data + Eligibility Matching + Retrieval + Generative AI + Accessible UX**

into a single platform designed around a real-world problem in Pakistan.

The goal is not simply to provide another chatbot, but to create a structured benefits-discovery experience where users can understand **which programs may be relevant, why they may be relevant, what they may need, and where they should verify and apply**.

---

# 📜 License

This project is currently intended as a hackathon project.

Add the appropriate license here before public release:

```text
LICENSE: [ADD LICENSE]
```

---

# ⭐ Support the Project

If you find HaqDarmand AI useful or interesting:

⭐ Star the repository
🍴 Fork the project
💡 Suggest improvements
🐛 Report issues
🤝 Contribute to the project

---

## 🇵🇰 HaqDarmand AI

**Making support programs easier to discover, understand, and access.**

> **Discover. Understand. Verify. Apply.**
