# Interview Bot

An AI-powered interview practice bot that conducts mock interviews using text-to-speech, speech recognition, and natural language processing to evaluate responses.

## Features

- **Topic Selection**: Choose from 4 categorized topics or practice with all questions
- **Text-to-Speech**: Questions are read aloud using Google Text-to-Speech (gTTS)
- **Speech Recognition**: Captures and transcribes user responses via microphone
- **Response Evaluation**: Uses TF-IDF vectorization and cosine similarity to score answers
- **Visual Analytics**: Displays performance metrics with charts
- **Smart Question Selection**: Selects up to 5 questions from your chosen topic
- **Interactive Menu**: User-friendly interface for topic selection and session management

## Requirements

- Python 3.7+
- Microphone access
- Internet connection (for speech recognition and TTS)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/debo-dante/interview_bot.git
cd interview_bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a dataset file named `dataset.csv` with your questions and answers:
```csv
What is your biggest strength?
My biggest strength is problem-solving and analytical thinking
Tell me about yourself
I am a passionate developer with experience in...
```

## Usage

1. Ensure your microphone is working and connected
2. Run the interview bot:
```bash
python interview_bot.py
```

3. The bot will:
   - Display a menu with 4 topic categories:
     * **Algorithms** (sorting, searching, complexity analysis, etc.)
     * **Data Structures** (trees, graphs, arrays, linked lists, etc.)
     * **Operating Systems** (processes, memory management, scheduling, etc.)
     * **Other CS Topics** (general computer science concepts)
   - Allow you to select a specific topic or practice with all questions
   - Ask up to 5 questions from your chosen topic
   - Play each question as audio
   - Listen for your spoken response (30-second timeout)
   - Calculate similarity between your answer and the expected answer
   - Display results and optional visualizations
   - Offer to continue with another topic

## How It Works

### Topic Categorization
The bot automatically categorizes questions into four main topics based on keyword analysis:

1. **Algorithms**: Sorting algorithms, search algorithms, complexity analysis, dynamic programming, graph algorithms, etc.
2. **Data Structures**: Trees, graphs, stacks, queues, arrays, linked lists, hash tables, heaps, etc.
3. **Operating Systems**: Process management, memory management, scheduling, synchronization, deadlocks, etc.
4. **Other CS Topics**: General computer science concepts that don't fit into the above categories

### Question Processing
- Questions are loaded from `dataset.csv` and automatically categorized
- Up to 5 questions are selected from your chosen topic
- Questions are converted to speech using Google TTS

### Response Evaluation
- User responses are captured via speech recognition
- Both user and expected answers are preprocessed (tokenized, lowercased, stop words removed)
- Similarity is calculated using TF-IDF vectorization and cosine similarity
- Scores above 0.7 are considered "correct"

### Results Visualization
- Bar chart showing similarity scores for each question
- Red dashed line indicates the passing threshold (0.7)
- Final score summary displayed

## File Structure

```
interview_bot/
├── interview_bot.py    # Main application
├── utils.py           # Text preprocessing utilities
├── requirements.txt   # Python dependencies
├── dataset.csv        # Questions and answers (create this)
└── README.md         # This file
```

## Configuration

### Timeout Settings
- Default response timeout: 30 seconds
- Modify in `get_user_response(timeout=30)`

### Similarity Threshold
- Default passing threshold: 0.7
- Modify in `conduct_interview()` function

### Number of Questions
- Default: 5 questions per session
- Modify in `random.sample(list(zip(questions, answers)), 5)`

## Dataset Format

Create a `dataset.csv` file with alternating questions and answers:
```csv
Question 1
Expected Answer 1
Question 2
Expected Answer 2
...
```

## Troubleshooting

### Common Issues

1. **Microphone not working**: Ensure microphone permissions are granted
2. **Speech recognition errors**: Check internet connection and speak clearly
3. **Audio playback issues**: Verify system audio settings
4. **Missing dataset**: Create `dataset.csv` with your questions and answers

### Platform-Specific Notes

- **Windows**: Uses `start` command for audio playback
- **macOS/Linux**: Uses `afplay` command for audio playback

## Dependencies

- `nltk`: Natural language processing
- `speechrecognition`: Speech-to-text conversion
- `gtts`: Google Text-to-Speech
- `pydub`: Audio processing
- `scikit-learn`: Machine learning utilities
- `matplotlib`: Data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Web interface
- [ ] Advanced NLP models for better evaluation
- [ ] Question difficulty levels
- [ ] Progress tracking over time
- [ ] Export results to PDF/CSV

## Support

For issues or questions, please open an issue on GitHub.
