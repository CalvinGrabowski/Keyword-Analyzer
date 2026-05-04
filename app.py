from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- QUALITY ATTRIBUTE #2: MAINTAINABILITY ---
# Using templates/ folder separates UI from logic. this is very much a work in progress
def calculate_match(resume_text, job_text):
    # Change this line in calculate_match:
    resume_words = set(resume_text.lower().replace(',', '').replace('.', '').split())
    job_words = set(job_text.lower().replace(',', '').replace('.', '').split())
    missing = job_words - resume_words
    match_percent = len(job_words & resume_words) / len(job_words) * 100 if job_words else 0
    return round(match_percent, 2), list(missing)[:5]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume = request.form.get('resume', '')
    job = request.form.get('job', '')
    
    # IH#8: GUARDRAILS
    if len(resume) < 10 or len(job) < 10:
        return "<h3>Please provide more text. <a href='/'>Go back</a></h3>"

    score, missing = calculate_match(resume, job)           # very cooked way of comparing the scores right now, but we will work on it
    return render_template('results.html', score=score, missing=missing)

if __name__ == '__main__':
    app.run(debug=True)