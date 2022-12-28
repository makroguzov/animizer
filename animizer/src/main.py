import fastapi
import nltk
import uvicorn

from src import model

app = fastapi.FastAPI(title='Animizer')


@app.on_event('startup')
def startup():
    nltk.download('stopwords')


MODEL = model.Model('../model')


@app.get('/',
         response_class=fastapi.responses.JSONResponse)
def predict_score(title: str, description: str):
    return {
        'title': f'{float(MODEL.predict(title, description)):.1f}'
    }


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8008, reload=True)
