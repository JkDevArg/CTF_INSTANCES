from flask import Flask, request, render_template, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG') or 'CTF{placeholder_flag_here}'

# Flag exposed in app config so players can reach it via {{config.FLAG}}
app.config['FLAG'] = FLAG


@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    user_input = ''
    error = None

    if request.method == 'POST':
        user_input = request.form.get('template', '')
        if len(user_input) > 500:
            error = 'Template too long (max 500 chars).'
        else:
            try:
                output = render_template_string(user_input)
            except Exception as e:
                error = f'Render error: {e}'

    return render_template('index.html', output=output, user_input=user_input, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
