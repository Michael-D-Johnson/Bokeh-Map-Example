from app import app

app.config.update(SERVER_NAME='127.0.0.1:5003')

if __name__ == '__main__':
    app.run(debug=True)
