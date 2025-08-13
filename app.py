import streamlit as st
import random
import os

# ------------------------------
# Kategorileri data klasöründen oku
# ------------------------------
def get_categories(path='data'):
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    return [os.path.splitext(f)[0] for f in files]

# ------------------------------
# Seçilen kategoriden soruları yükle
# ------------------------------
def load_questions(category, path='data'):
    file_path = os.path.join(path, f"{category}.txt")
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    questions = []
    for line in lines:
        parts = line.strip().split(" - ")
        if len(parts) == 2:
            questions.append((parts[0], parts[1]))
    random.shuffle(questions)
    return questions

# ------------------------------
# Sayfa Ayarları
# ------------------------------
st.set_page_config(page_title="Rusça Kelime Testi", layout="centered")
st.title("🇷🇺 Rusça Kelime Testi")
st.markdown("**Türkçesini oku, Rusçasını yaz ✍️**")

# ------------------------------
# Kategori seçimi
# ------------------------------
categories = get_categories()
selected_category = st.selectbox("📁 Kategori Seç", categories)

# Kategori değiştiyse test durumunu sıfırla
if "last_category" not in st.session_state:
    st.session_state.last_category = selected_category

if selected_category != st.session_state.last_category:
    for key in ["questions", "current_question", "score", "answer", "show_result", "answered"]:
        st.session_state.pop(key, None)
    st.session_state.last_category = selected_category

# ------------------------------
# Test Başlat
# ------------------------------
if "questions" not in st.session_state:
    st.session_state.questions = load_questions(selected_category)
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answer = ""
    st.session_state.show_result = False
    st.session_state.answered = False

# ------------------------------
# Testi Göster
# ------------------------------
questions = st.session_state.questions

if st.session_state.current_question < len(questions):
    question, correct_answer = questions[st.session_state.current_question]
    st.markdown(f"### Soru {st.session_state.current_question + 1} / {len(questions)}")
    st.markdown(f"**Türkçesi:** `{question}`")

    st.session_state.answer = st.text_input("Rusça karşılığını yazınız:", value=st.session_state.answer)

    if st.button("✅ Cevabı Gönder"):
        if st.session_state.answered:
            st.warning("Bu soruya zaten cevap verdiniz.")
        else:
            user_answer = st.session_state.answer.strip().lower()
            correct = correct_answer.strip().lower()

            if user_answer == correct:
                st.success("✅ Doğru!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Yanlış. Doğru cevap: `{correct}`")

            st.session_state.answered = True
            st.session_state.show_result = True

    if st.session_state.answered:
        if st.button("➡️ Sonraki Soru"):
            st.session_state.current_question += 1
            st.session_state.answer = ""
            st.session_state.answered = False
            st.session_state.show_result = False

else:
    st.balloons()
    st.success(f"🎉 Test Bitti! Skorunuz: **{st.session_state.score} / {len(questions)}**")

    if st.button("🔁 Tekrar Başla"):
        for key in ["questions", "current_question", "score", "answer", "show_result", "answered"]:
            st.session_state.pop(key, None)

