from flask import Flask

app = Flask("app/" + __name__)

@app.route('/')
def home():
    return "Flask App"

if __name__ == '__main__':
  app.run()