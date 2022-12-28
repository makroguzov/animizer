import pathlib

import fastapi
import uvicorn

from src import model

app = fastapi.FastAPI(title='Animizer')

MODEL = model.Model(
    pathlib.Path(__file__).parent.resolve() / 'model'
)


@app.get('/',
         response_class=fastapi.responses.JSONResponse)
def predict_score(title: str, description: str):
    return {
        'title': f'{float(MODEL.predict(title, description)):.1f}'
    }


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8008, reload=True)
