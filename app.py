# pip install streamlit google-generativeai pdfplumber

import streamlit as st
import pdfplumber
import google.generativeai as genai

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def generate_questions_with_google_ai(pdf_text, additional_prompt, num_questions=3, question_type="multiple-choice"):
    prompt = (
        f"Buatlah {num_questions} soal {question_type} berdasarkan teks berikut:\n\n"
        f"{pdf_text}\n\n"
        f"Petunjuk tambahan dari pengguna: {additional_prompt}\n\n"
        "Pastikan soal-soal yang dibuat jelas, singkat, dan langsung berkaitan dengan teks di atas. Dan berikan kunci jawabannya."
    )
    response = model.generate_content(prompt)
    return response.text

st.title("AI Question Generator for Teachers")
st.write("By Irfan Yasin.")

uploaded_file = st.file_uploader("Unggah file PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Mengekstrak teks dari PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("Cuplikan Teks dari PDF")
    st.text_area("Teks:", value=pdf_text[:500], height=200)

    num_questions = st.number_input("Jumlah soal yang ingin dihasilkan", min_value=1, max_value=10, value=3)
    question_type = st.selectbox("Tipe soal", ["multiple-choice", "essay"])

    additional_prompt = st.text_area("Masukkan Perintah Tambahan (opsional):", value="", height=100)

    if st.button("Generate Soal"):
        genai.configure(api_key="AIzaSyAQ1Sxrki4B8ptuOZfJayQ-9OsPAISJ6tY")  
        model = genai.GenerativeModel("gemini-1.5-flash")

        with st.spinner("Menghasilkan soal..."):
            questions = generate_questions_with_google_ai(
                pdf_text, additional_prompt, num_questions=num_questions, question_type=question_type
            )

        st.subheader("Soal yang Dihasilkan")
        st.write(questions)
else:
    st.info("Silakan unggah file PDF untuk memulai.")