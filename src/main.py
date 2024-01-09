from fastapi import FastAPI

app = FastAPI(
    title='Blitz Market'
)


@app.get('/')
def hello():
    return 'Hello world!'
