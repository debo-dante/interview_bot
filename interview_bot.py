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

def categorize_questions(questions, answers):
    """Categorize questions into four main topics based on keywords"""
    categories = {
        "Algorithms": [],
        "Data Structures": [], 
        "Operating Systems": [],
        "Other CS Topics": []
    }
    
    # Keywords for each category
    algorithm_keywords = [
        "algorithm", "sort", "search", "binary", "bubble", "quick", "merge", "heap",
        "recursive", "dynamic programming", "complexity", "time complexity", "space complexity",
        "dijkstra", "floyd", "depth first", "breadth first", "dfs", "bfs", "shortest path",
        "minimum spanning tree", "topological", "convex hull", "interpolation", "euclidean"
    ]
    
    data_structure_keywords = [
        "tree", "graph", "stack", "queue", "linked list", "array", "hash", "binary tree",
        "avl", "heap", "priority queue", "deque", "node", "edge", "vertex", "traversal",
        "splay tree", "spanning tree", "forest", "root", "leaf", "children", "parent"
    ]
    
    os_keywords = [
        "process", "thread", "operating system", "kernel", "memory", "cpu", "scheduling",
        "deadlock", "semaphore", "mutex", "synchronization", "paging", "virtual memory",
        "fragmentation", "thrashing", "cache", "buffer", "interrupt", "context switch",
        "multiprogramming", "multitasking", "multiprocessing", "smp", "daemon", "spooling"
    ]
    
    for i, (question, answer) in enumerate(zip(questions, answers)):
        question_lower = question.lower()
        answer_lower = answer.lower()
        combined_text = question_lower + " " + answer_lower
        
        # Check which category this question belongs to
        algo_score = sum(1 for keyword in algorithm_keywords if keyword in combined_text)
        ds_score = sum(1 for keyword in data_structure_keywords if keyword in combined_text)
        os_score = sum(1 for keyword in os_keywords if keyword in combined_text)
        
        # Assign to category with highest score
        if algo_score >= ds_score and algo_score >= os_score and algo_score > 0:
            categories["Algorithms"].append((question, answer))
        elif ds_score >= os_score and ds_score > 0:
            categories["Data Structures"].append((question, answer))
        elif os_score > 0:
            categories["Operating Systems"].append((question, answer))
        else:
            categories["Other CS Topics"].append((question, answer))
    
    return categories

def display_topic_menu(categories):
    """Display available topics and their question counts"""
    print("\n=== Interview Bot - Topic Selection ===")
    print("Available Topics:")
    
    for i, (topic, questions) in enumerate(categories.items(), 1):
        print(f"{i}. {topic} ({len(questions)} questions)")
    
    print(f"{len(categories) + 1}. All Topics (Random Mix)")
    print(f"{len(categories) + 2}. Exit")
    
    return len(categories)

def get_user_choice(max_options):
    """Get and validate user's topic choice"""
    while True:
        try:
            choice = int(input(f"\nSelect a topic (1-{max_options + 2}): "))
            if 1 <= choice <= max_options + 2:
                return choice
            else:
                print(f"Please enter a number between 1 and {max_options + 2}")
        except ValueError:
            print("Please enter a valid number")

def load_dataset(path):
    """Load and parse the CSV dataset"""
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    # Skip header row and parse alternating questions/answers
    questions = []
    answers = []
    
    for i in range(1, len(lines), 2):  # Start from 1 to skip header
        if i < len(lines) and len(lines[i]) > 0:
            questions.append(lines[i][0])
        if i + 1 < len(lines) and len(lines[i + 1]) > 0:
            answers.append(lines[i + 1][0])
    
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

def conduct_interview(questions, answers, topic_name="Selected Topic"):
    """Conduct interview with questions from selected topic"""
    if len(questions) == 0:
        print(f"No questions available for {topic_name}")
        return [], 0
    
    # Select up to 5 questions (or all if fewer than 5)
    num_questions = min(5, len(questions))
    selected = random.sample(list(zip(questions, answers)), num_questions)
    
    print(f"\n=== Starting {topic_name} Interview ===")
    print(f"You will be asked {num_questions} questions.")
    print("Speak clearly after each question is read aloud.\n")
    
    score = 0
    scores = []
    
    for i, (q, a) in enumerate(selected, 1):
        print(f"\n--- Question {i}/{num_questions} ---")
        ask_question(q)
        user_ans = get_user_response()
        
        if not user_ans:
            print("No response detected. Moving to next question.")
            continue
            
        sim = calculate_similarity(preprocess(user_ans), preprocess(a))
        print(f"Similarity Score: {sim:.2f}")
        
        if sim > 0.7:
            print("✓ Good answer!")
            score += 1
        else:
            print("✗ Could be better.")
            
        scores.append(sim)
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

def main():
    """Main function with topic selection interface"""
    try:
        # Load the dataset
        print("Loading interview questions...")
        questions, answers = load_dataset('dataset.csv')
        print(f"Loaded {len(questions)} questions successfully!")
        
        # Categorize questions by topic
        print("Categorizing questions by topic...")
        categories = categorize_questions(questions, answers)
        
        # Main loop for topic selection
        while True:
            # Display menu
            max_options = display_topic_menu(categories)
            choice = get_user_choice(max_options)
            
            # Handle user choice
            if choice == max_options + 2:  # Exit
                print("Thank you for using Interview Bot! Goodbye!")
                break
            elif choice == max_options + 1:  # All topics (random mix)
                topic_name = "All Topics (Random Mix)"
                selected_questions = questions
                selected_answers = answers
            else:  # Specific topic
                topic_names = list(categories.keys())
                topic_name = topic_names[choice - 1]
                topic_data = categories[topic_name]
                selected_questions = [q for q, a in topic_data]
                selected_answers = [a for q, a in topic_data]
            
            # Conduct interview
            if len(selected_questions) == 0:
                print(f"\nNo questions available for {topic_name}. Please select another topic.")
                continue
                
            scores, correct = conduct_interview(selected_questions, selected_answers, topic_name)
            
            if scores:  # Only show results if interview was conducted
                print(f"\n=== Interview Results for {topic_name} ===")
                print(f"Correct Answers: {correct} / {len(scores)}")
                print(f"Success Rate: {(correct/len(scores)*100):.1f}%")
                
                # Ask if user wants to see visualization
                show_viz = input("\nWould you like to see the results visualization? (y/n): ").lower().strip()
                if show_viz.startswith('y'):
                    visualize_results(scores)
            
            # Ask if user wants to try another topic
            continue_choice = input("\nWould you like to try another topic? (y/n): ").lower().strip()
            if not continue_choice.startswith('y'):
                print("Thank you for using Interview Bot! Goodbye!")
                break
                
    except FileNotFoundError:
        print("Error: dataset.csv file not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()
