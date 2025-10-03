# FeelWell: Mental Health Assessment & Support Application

A web-based application designed to assess mental health, provide personalized suggestions, and offer chat-based support.

## Features

- **Interactive Questionnaire**: Step-by-step mental health assessment with audio support
- **AI-Powered Analysis**: Machine learning model for mental health risk prediction
- **Personalized Suggestions**: Tailored recommendations based on assessment results
- **Multilingual Support**: Available in multiple languages (English, Tamil)
- **Dr. Chat**: AI-powered mental wellness companion for supportive conversations
- **Accessible Design**: Audio playback of questions and results for better accessibility

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Random Forest Classifier
- **AI Chat**: Groq API
- **Accessibility**: Text-to-Speech with gTTS
- **Translation**: Google Translate API

## Setup Instructions

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your GROQ API key as an environment variable:
   ```
   # On Windows
   set GROQ_API_KEY=your_actual_api_key
   
   # On macOS/Linux
   export GROQ_API_KEY=your_actual_api_key
   ```
4. Run the application:
   ```
   python app.py
   ```

### PythonAnywhere Deployment

1. **Sign Up/Login to PythonAnywhere**
   - Go to [PythonAnywhere](https://www.pythonanywhere.com/) and create an account or log in.

2. **Clone the Repository**
   - Open a Bash console in PythonAnywhere
   - Clone your repository:
     ```bash
     git clone https://github.com/vibhitha27/FeelWell.git
     ```

3. **Set Up a Virtual Environment**
   ```bash
   cd FeelWell
   mkvirtualenv --python=python3.9 feelwell-env
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Set up your Groq API key:
     ```bash
     echo "export GROQ_API_KEY='your_actual_groq_api_key'" >> ~/.virtualenvs/feelwell-env/bin/postactivate
     ```
   - Reload the virtualenv:
     ```bash
     workon feelwell-env
     ```

5. **Configure the Web App**
   - Go to the "Web" tab in PythonAnywhere
   - Click "Add a new web app"
   - Choose "Manual configuration" (not the "Flask" option)
   - Select Python 3.9
   - Set the path to your project (e.g., /home/yourusername/FeelWell)

6. **Configure WSGI File**
   - PythonAnywhere will generate a WSGI file
   - Edit it to look like this:

     ```python
     import sys
     import os

     # Add your project directory to the Python path
     path = '/home/yourusername/FeelWell'
     if path not in sys.path:
         sys.path.insert(0, path)

     # Set environment variables
     os.environ['GROQ_API_KEY'] = 'your_actual_groq_api_key'

     # Import your Flask app
     from app import app as application
     ```

7. **Configure Static Files**
   - In the Web tab, under "Static files"
   - Add:
     - URL: /static/
     - Directory: /home/yourusername/FeelWell/static/

8. **Reload Your Web App**
   - Click the "Reload" button for your web app
   - Your application should now be running at yourusername.pythonanywhere.com

## Screenshots

(Screenshots will be added soon)

## Future Enhancements

- Additional language support
- More comprehensive mental health assessments
- Integration with professional mental health services
- Mobile application version

## Contributors

- Vibhitha V

## License

This project is licensed under the MIT License - see the LICENSE file for details.