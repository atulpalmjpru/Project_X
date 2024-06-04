# from flask import Flask, render_template
# from youtube_transcript_api import YouTubeTranscriptApi
# import random

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/process')
# def process():
#     video_id = 'DpxxTryJ2fY'  # Enter your YouTube video ID here
#     transcript_text = get_video_transcript(video_id)
#     gap_filled_text, gaps = create_gap_filling(transcript_text)
#     return render_template('result.html', gap_filled_text=gap_filled_text, gaps=gaps)

# def get_video_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         text_segments = [segment['text'] for segment in transcript]
#         return text_segments
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# def create_gap_filling(text_segments, num_gaps=3):
#     gap_filled_text = ""
#     gaps = []

#     # Iterate over each text segment
#     for segment in text_segments:
#         words = segment.split()
#         # Select random indices to create gaps
#         gap_indices = random.sample(range(len(words)), min(num_gaps, len(words)))
#         gap_indices.sort(reverse=True)  # Sort indices in descending order

#         # Create a new sentence with gaps
#         gap_filled_sentence = ""
#         for i, word in enumerate(words):
#             if i in gap_indices:
#                 gap_filled_sentence += "______ "  # Insert a gap
#                 gaps.append(word)  # Store the word that was removed for later answer checking
#             else:
#                 gap_filled_sentence += word + " "
#         gap_filled_text += gap_filled_sentence.strip() + "\n"

#     return gap_filled_text, gaps

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template,request
from youtube_transcript_api import YouTubeTranscriptApi
import random

app = Flask(__name__)

global_gap_count = 1  # Initialize global gap count

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_segments = [segment['text'] for segment in transcript]
        return text_segments
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def create_gap_filling(text_segments, num_gaps=3):
    global global_gap_count  # Access global gap count
    gap_filled_text = ""
    gaps = []

    # Iterate over each text segment
    for segment in text_segments:
        words = segment.split()
        # Select random indices to create gaps
        gap_indices = random.sample(range(len(words)), min(num_gaps, len(words)))
        gap_indices.sort(reverse=True)  # Sort indices in descending order

        # Create a new sentence with gaps
        gap_filled_sentence = ""
        for i, word in enumerate(words):
            if i in gap_indices:
                gap_filled_sentence += f"______{global_gap_count} "  # Insert a gap with global gap count
                gaps.append(word)  # Store the word that was removed for later answer checking
                global_gap_count += 1  # Increment global gap count
            else:
                gap_filled_sentence += word + " "
        gap_filled_text += gap_filled_sentence.strip() + "\n"

    return gap_filled_text, gaps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        video_id = request.form['video_id']
        transcript_text = get_video_transcript(video_id)

        global global_gap_count  # Reset global gap count for each request
        global_gap_count = 1

        gap_filled_text, gaps = create_gap_filling(transcript_text)

        return render_template('GapfillingExercise.html', gap_filled_text=gap_filled_text, gaps=gaps)
    else:
        return render_template('video_id_form.html')
def other_page():
    gaps=gaps  # Replace with your actual list of words
    return render_template('Answers.html', gaps=gaps)


if __name__ == "__main__":
    app.run(debug=True)

