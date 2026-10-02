import flask

app = flask.Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>test2</title>
        </head>
        <body>
            <h1>Title</h1>
            <p>This is a simple Flask application.</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)