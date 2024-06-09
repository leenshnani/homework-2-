from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# صفحة الاتصال
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحة من نحن
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()