import random
import csv
import os
import time
from gtts import gTTS
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from utils import preprocess

def load_dataset(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    questions = [lines[i][0] for i in range(0, len(lines), 2)]
    answers = [lines[i][0] for i in range(1, len(lines), 2)]
    return questions, answers

def ask_question(text):
    print(f"Question: {text}")
    tts = gTTS(text)
    tts.save("question.mp3")
    os.system("start question.mp3" if os.name == 'nt' else "afplay question.mp3")
    time.sleep(7)

def get_user_response(timeout=30):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            response = recognizer.recognize_google(audio)
            print(f"User: {response}")
            return response
        except Exception as e:
            print(f"Error: {e}")
            return ""

def calculate_similarity(ans1, ans2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([ans1, ans2])
    return cosine_similarity(vectors[0], vectors[1])[0][0]

def conduct_interview(questions, answers):
    score = 0
    scores = []
    selected = random.sample(list(zip(questions, answers)), 5)
    for q, a in selected:
        ask_question(q)
        user_ans = get_user_response()
        if not user_ans: continue
        sim = calculate_similarity(preprocess(user_ans), preprocess(a))
        print(f"Similarity: {sim:.2f}")
        scores.append(sim)
        if sim > 0.7: score += 1
        time.sleep(2)
    return scores, score

def visualize_results(scores):
    questions = [f"Q{i+1}" for i in range(len(scores))]
    plt.figure(figsize=(10, 5))
    plt.bar(questions, scores, color='skyblue')
    plt.axhline(y=0.7, color='r', linestyle='--', label='Passing Threshold (0.7)')
    plt.ylim(0, 1)
    plt.title("Response Similarity Scores")
    plt.xlabel("Questions")
    plt.ylabel("Similarity")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    qs, ans = load_dataset('dataset.csv')
    scores, correct = conduct_interview(qs, ans)
    print(f"\nCorrect Answers: {correct} / {len(scores)}")
    visualize_results(scores)
