from app import create_app



if __name__ == '__main__':
    #creating app
    app = create_app()
    #running app
    app.run(debug=True)