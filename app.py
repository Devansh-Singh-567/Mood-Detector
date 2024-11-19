from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# HTML content as a string
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Mood Songs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }
        .container {
            text-align: center;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        input, button {
            padding: 10px;
            font-size: 16px;
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 80%;
            max-width: 500px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .mood-message {
            margin-top: 20px;
            font-size: 18px;
        }
        .song-link {
            margin-top: 10px;
        }
        .song-link a {
            color: #4CAF50;
            font-weight: bold;
            text-decoration: none;
        }
        .song-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Check your Mood and Listen the Song</h1>
        <p>Type something below, and I'll recommend a song based on your emotions!</p>
        <textarea id="user-input" placeholder="Type something..."></textarea>
        <button onclick="analyzeMood()">Analyze Mood</button>

        <div class="mood-message" id="mood-message"></div>
        <div class="song-link" id="song-link"></div>
    </div>

    <script>
        async function analyzeMood() {
            const userInput = document.getElementById("user-input").value;

            // Send user input to the backend for sentiment analysis
            const response = await fetch('/analyze_mood', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `user_input=${encodeURIComponent(userInput)}`
            });

            const data = await response.json();
            
            // Display mood message
            const moodMessage = document.getElementById("mood-message");
            const songLink = document.getElementById("song-link");

            // Display mood
            moodMessage.innerHTML = `Your mood is: <strong>${data.mood}</strong>`;

            // Display song link
            songLink.innerHTML = `Here’s a song to cheer you up: <a href="${data.song_link}" target="_blank">Listen Now</a>`;
        }
    </script>

</body>
</html>
"""

@app.route('/')
def index():
    return html_content  # Serve HTML content directly as a string

@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    user_input = request.form['user_input']
    
    # Analyze sentiment
    sentiment = analyzer.polarity_scores(user_input)
    score = sentiment['compound']
    
    # Determine mood and song link based on sentiment score
    if score <= -0.5:
        mood = 'sad'
        song_link = "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"  # Example hype song
    elif score >= 0.5:
        mood = 'happy'
        song_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example cheerful song
    else:
        mood = 'neutral'
        song_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example cheerful song
    
    return jsonify({"mood": mood, "song_link": song_link})

if __name__ == '__main__':
    app.run(debug=True)
