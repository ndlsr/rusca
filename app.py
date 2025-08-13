import streamlit as st
import random
import os

# Verileri yükle
def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    word_pairs = []
    for line in lines:
        if '-' in line:
            tr, ru = line.strip().split(' - ')
            word_pairs.append((tr.strip(), ru.strip()))
    return word_pairs

# Kategori seçimi
def get_categories(path='data'):
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    return [os.path.splitext(f)[0] for f in files]

# Başla
st.title("📚 Rusça Kelime Testi")
st.markdown("Türkçesini gör, Rusçasını yaz!")

# Kategorileri oku
categories = get_categories()

selected_category = st.selectbox("📁 Kategori Seç", categories)

if selected_category:
    word_list = load_words(f"data/{selected_category}.txt")
    total_questions = st.slider("🎯 Soru Sayısı", 1, len(word_list), min(10, len(word_list)))

    if 'questions' not in st.session_state:
        st.session_state.questions = random.sample(word_list, total_questions)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []

    if st.session_state.current_q < total_questions:
        current_word = st.session_state.questions[st.session_state.current_q]
        st.subheader(f"{selected_category} Testi: Soru {st.session_state.current_q + 1} / {total_questions}")
        st.markdown(f"**Türkçesi:** `{current_word[0]}`")

        user_answer = st.text_input("Rusçası nedir?", key=st.session_state.current_q)

        if st.button("Cevabı Kontrol Et"):
            correct = user_answer.strip().lower() == current_word[1].lower()
            if correct:
                st.success("✅ Doğru!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Yanlış. Doğru cevap: `{current_word[1]}`")

            st.session_state.current_q += 1

    else:
        st.success(f"🎉 Test Bitti! Skorun: {st.session_state.score} / {total_questions}")
        if st.button("🔁 Tekrar Başla"):
            del st.session_state.questions
            del st.session_state.current_q
            del st.session_state.score

