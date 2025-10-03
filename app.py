from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import pickle
from gtts import gTTS
import os
from groq import Groq
from deep_translator import GoogleTranslator

# Initialize Flask
app = Flask(__name__)

# Initialize Groq client using environment variable or placeholder
# IMPORTANT: Replace this with your actual API key when deploying 
# For production, use environment variables: os.environ.get('GROQ_API_KEY')
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

# ------------------------------
# PROMPT TEMPLATE FOR CHATBOT
# ------------------------------
PROMPT_TEMPLATE = """
Your name is Dr.chat
You are HopeGuide, an AI-powered mental health companion.

Rules:
- Be empathetic, short, and supportive.
- Respond in the same language as user input.
- Do NOT diagnose; instead, give emotional support & coping suggestions.
- Always end by reminding user to seek professional help if needed.
- NEVER include your thinking process in your response.
- Do not use <think> tags or explain your thought process.
- Respond directly with helpful and supportive advice.

User: {user_input}
AI:
"""

# ------------------------------
# Load ML model if available
# ------------------------------
try:
    with open('model/rf_model.pkl', 'rb') as model_file:
        model_data = pickle.load(model_file)
        model = model_data['model']
        feature_columns = model_data['features']
except FileNotFoundError:
    model = None
    feature_columns = None
    print("⚠️ Warning: rf_model.pkl not found. Prediction will be limited.")

# Load suggestions dataset
# Add extra suggestions for new problem keywords
extra_suggestions = pd.DataFrame([
    {
        'user_id': 3, 
        'risk_label': 1, 
        'problem_keyword': 'mood disorder', 
        'symptom_trigger_question': 'Do you experience frequent mood changes?',
        'suggestion_en': 'Consider keeping a mood journal to identify patterns and triggers.',
        'suggestion_ta': 'மனநிலை மாற்றங்களின் முறைகளையும் தூண்டுதல்களையும் கண்டறிய ஒரு மனநிலை பத்திரிகையை வைத்திருக்க பரிசீலிக்கவும்.'
    }
])

# Load original suggestions and combine with new ones
suggestions_df = pd.concat([
    pd.read_csv('data/Combined_Mental_Health_Predictions_and_Suggestions.csv'),
    extra_suggestions
], ignore_index=True)

# ------------------------------
# Utility: Generate Audio
# ------------------------------
def generate_audio(text, lang, filename):
    """Generate and save audio from text if not already existing."""
    if not os.path.exists('static/audio'):
        os.makedirs('static/audio')

    filepath = os.path.join('static', 'audio', filename)

    # Save the audio file
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    # Return the relative path for the frontend,
    # ensuring it uses forward slashes for URLs
    relative_path = os.path.join('audio', filename)
    return relative_path.replace('\\', '/')

# ------------------------------
# CHATBOT API
# ------------------------------
@app.route('/api/chat', methods=['POST'])
def chatbot_api():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        prompt = PROMPT_TEMPLATE.format(user_input=user_message)

        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        )

        chatbot_response = response.choices[0].message.content
        
        # Remove any <think>...</think> sections from the response
        import re
        clean_response = re.sub(r'<think>.*?</think>', '', chatbot_response, flags=re.DOTALL).strip()
        
        return jsonify({"response": clean_response})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ------------------------------
# ROUTES
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html', page_class='index-bg')

@app.route('/language', methods=['GET', 'POST'])
def language_selection():
    if request.method == 'POST':
        language = request.form['language']
        return redirect(url_for('about', lang=language))
    return render_template('language.html', page_class='language-page')

@app.route('/about')
def about():
    lang = request.args.get('lang', 'en')
    about_text_en = (
        "Welcome to FeelWell. This website is designed to help you assess your mental wellness. "
        "It uses a questionnaire and a machine learning model to provide you with personalized suggestions."
    )

    about_text = GoogleTranslator(source='auto', target=lang).translate(about_text_en)
    audio_file = generate_audio(about_text, lang, f'about_{lang}.mp3')

    return render_template('about.html', about_text=about_text, audio_file=audio_file, lang=lang, page_class='about-bg')

@app.route('/questionnaire')
def questionnaire():
    lang = request.args.get('lang', 'en')
    questions_en = [
        'Are you currently experiencing a lot of stress?',
        'Have you noticed changes in your daily habits?',
        'Do you have a family history of mental illness?',
        'Have you sought treatment for a mental health condition in the past?',
        'Are you struggling to cope with day-to-day challenges?',
        'Have you lost interest in your work recently?',
        'Do you find it difficult to socialize with others?',
        'Do you experience mood swings frequently?',
        'Have you been spending more time indoors than usual?',
        'Do you have a history of mental health conditions?',
        'Would you be comfortable discussing mental health in a job interview?',
        'Are you aware of mental health care options available to you?',
        'Do you feel your sleep patterns have changed recently?',
        'Have you experienced a decreased appetite or changes in eating habits?',
        'Do you often feel overwhelmed by small tasks?'
    ]

    questions = {}
    audio_files = {}

    if not os.path.exists('static/audio/questions'):
        os.makedirs('static/audio/questions')

    for i, q_en in enumerate(questions_en):
        q_translated = GoogleTranslator(source='auto', target=lang).translate(q_en)
        questions[q_en] = q_translated
        audio_file = generate_audio(q_translated, lang, f'questions/q_{i}_{lang}.mp3')
        audio_files[q_en] = audio_file

    return render_template('questionnaire.html', questions=questions, audio_files=audio_files, lang=lang, page_class="questionnaire-page")

@app.route('/predict', methods=['POST'])
def predict():
    lang = request.form.get('lang', 'en')
    user_responses = request.form.getlist('symptoms')

    risk_predicted = False
    problem_keywords = []

    # Simple keyword detection
    if 'Are you currently experiencing a lot of stress?' in user_responses:
        risk_predicted, problem_keywords = True, ['stress']
    if 'Are you struggling to cope with day-to-day challenges?' in user_responses:
        risk_predicted, problem_keywords = True, problem_keywords + ['anxiety']
    if 'Have you lost interest in your work recently?' in user_responses:
        risk_predicted, problem_keywords = True, problem_keywords + ['burnout']
    if 'Do you have a family history of mental illness?' in user_responses:
        risk_predicted = True
    if 'Have you sought treatment for a mental health condition in the past?' in user_responses:
        risk_predicted = True
    if 'Do you find it difficult to socialize with others?' in user_responses:
        risk_predicted = True
    if 'Do you experience mood swings frequently?' in user_responses:
        risk_predicted, problem_keywords = True, problem_keywords + ['mood disorder']
    if 'Have you been spending more time indoors than usual?' in user_responses:
        risk_predicted = True
    if 'Do you have a history of mental health conditions?' in user_responses:
        risk_predicted = True
    if 'Do you often feel overwhelmed by small tasks?' in user_responses:
        risk_predicted, problem_keywords = True, problem_keywords + ['anxiety']

    # Model-based prediction (if model exists)
    if model and feature_columns is not None:
        input_data = pd.DataFrame(columns=feature_columns)
        input_data.loc[0] = 0

        if 'Are you currently experiencing a lot of stress?' in user_responses:
            input_data['Growing_Stress'] = 1
        if 'Have you noticed changes in your daily habits?' in user_responses:
            input_data['Changes_Habits'] = 1
        if 'Do you have a family history of mental illness?' in user_responses:
            input_data['family_history'] = 1
        if 'Have you sought treatment for a mental health condition in the past?' in user_responses:
            input_data['treatment'] = 1
        if 'Are you struggling to cope with day-to-day challenges?' in user_responses:
            input_data['Coping_Struggles'] = 1
        if 'Have you lost interest in your work recently?' in user_responses:
            input_data['Work_Interest'] = 1
        if 'Do you find it difficult to socialize with others?' in user_responses:
            input_data['Social_Weakness'] = 1
        if 'Do you experience mood swings frequently?' in user_responses:
            input_data['Mood_Swings'] = 2  # Medium level of mood swings
        if 'Have you been spending more time indoors than usual?' in user_responses:
            input_data['Days_Indoors'] = 1  # 1-14 days category
        if 'Do you have a history of mental health conditions?' in user_responses:
            input_data['Mental_Health_History'] = 1
        if 'Would you be comfortable discussing mental health in a job interview?' in user_responses:
            input_data['mental_health_interview'] = 0  # No
        if 'Are you aware of mental health care options available to you?' in user_responses:
            input_data['care_options'] = 1  # Yes

        input_data = input_data.reindex(columns=feature_columns, fill_value=0)

        prediction = model.predict(input_data)
        risk_predicted = prediction[0] == 1

    # Result message
    if risk_predicted:
        result_text_en = "Based on your responses, there is a possibility of a mental health risk."
    else:
        result_text_en = "Based on your responses, there is no immediate indication of a mental health risk. Keep up with your positive mental health practices!"

    result_text = GoogleTranslator(source='auto', target=lang).translate(result_text_en)
    result_audio = generate_audio(result_text, lang, f'result_{lang}.mp3')

    # Suggestions
    suggestions_list = []
    suggestion_audios = {}
    if risk_predicted:
        for keyword in list(set(problem_keywords)):
            sugg_row = suggestions_df[suggestions_df['problem_keyword'] == keyword].iloc[0]
            sugg_text = sugg_row.get(f'suggestion_{lang}', sugg_row['suggestion_en'])
            suggestions_list.append(sugg_text)
            audio_file = generate_audio(sugg_text, lang, f'suggestion_{keyword}_{lang}.mp3')
            suggestion_audios[sugg_text] = audio_file

    return render_template('results.html',
                           result_text=result_text,
                           result_audio=result_audio,
                           suggestions=suggestions_list,
                           suggestion_audios=suggestion_audios,
                           lang=lang,
                           show_suggestions=risk_predicted,
                           page_class='results-page')

# Route for chatbot page
@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html', page_class='chatbot-page')


# Run Flask
if __name__ == '__main__':
    app.run(debug=True)