# Interview Bot - Project Explanation

### 📂 Project Structure

1. **README.md**: Contains the project overview, features, installation, usage, and configuration details.
2. **interview_bot.py**: Main script of the application that handles question selection, audio playback, user response capturing, and evaluation.
3. **utils.py**: Provides text preprocessing utilities such as tokenization and stopword removal.
4. **requirements.txt**: Lists the dependencies needed for the project, including libraries for NLP, speech recognition, and visualization.
5. **dataset.csv**: Contains interview questions and answers, which the bot uses for conducting mock interviews.
6. **question.mp3**: An example audio file generated for text-to-speech playback during interviews.
7. **.git**: Git repository metadata, tracking changes and versioning.

### 📜 Working

- **Initialization**: Loads the dataset and categorizes questions into topics: Algorithms, Data Structures, Operating Systems, and Other CS Topics.
- **Question Processing**: Converts text questions to speech using Google Text-to-Speech (gTTS). Plays the audio using platform-specific commands (`afplay` on macOS).
- **User Interaction**: The user selects a topic, and up to 5 random questions are asked. Responses are captured and transcribed using `speech_recognition`.
- **Evaluation**: The bot evaluates responses using TF-IDF vectorization and cosine similarity against expected answers.
- **Visualization**: Displays performance metrics with `matplotlib`.

### 📦 Libraries Used

1. **NLTK**: For natural language processing tasks like tokenization and stopword removal.
2. **SpeechRecognition**: Transcribes spoken input into text using Google's Web Speech API.
3. **gTTS**: Converts text to speech using Google Text-to-Speech.
4. **pydub**: For processing audio files.
5. **Scikit-learn**: Applies machine learning methods to score the similarity of answers.
6. **Matplotlib**: Visualizes results with bar charts.  

### 🧠 Algorithms and Techniques

- **Text Preprocessing**: Removes punctuation, lowercases text, and filters out stopwords.
- **TF-IDF & Cosine Similarity**: Quantifies similarity between user and expected responses.
- **Random Sampling**: Selects up to 5 random questions per session.
- **Speech Synthesis and Recognition**: Converts questions to speech and listens to verbal responses.

### ⚙️ Recent Git Changes
- Added topic selection feature.
- Cleaned up the repository.
- Initial commits included dataset and main implementation.

### 🔍 Dataset
- Contains 5,496 lines, alternating between questions and expected answers.

The Interview Bot provides a comprehensive framework for interactive interview practice, leveraging AI-powered speech processing and text analysis. It's designed for educational purposes and ease of use, with future potential enhancements like support for multiple languages and web integration.
