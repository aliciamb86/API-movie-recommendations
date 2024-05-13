from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import asyncpg
from fastapi import BackgroundTasks
from cred import apikey, db_url


os.chdir(os.path.dirname(os.path.dirname(__file__)))


app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/pedir_recomendacion')
async def recomendacion(pregunta_usuario: str):
    prompt_template = PromptTemplate.from_template(
        "Cual es tu pregunta {pregunta}."
    )

    # Inicializa el modelo de lenguaje
    llm = ChatOpenAI(api_key=apikey)

    # Define el rol del usuario en el prompt
    prompt_usuario = {"role": "user", "content": prompt_template.format(pregunta=pregunta_usuario)}

    # Realiza la llamada al modelo de lenguaje con el prompt completo
    respuesta = llm.invoke([{"role": "system", "content": """Eres un especialista en cine.
                                                        Puedes dar críticas de las películas o series que te pregunten,
                                                        y recomendar películas o series a partir de un género, temática, plataforma, actor o director.
                                                        Entiendes los títulos de películas y series en su idioma original, o los títulos en su versión de España.
                                                        Si te solicitan otra cosa responde amablemente que no puedes ayudarles, y sugiere que te pregunten por cine.
                                                        Termina tu respuesta despidiéndote, pero nunca hagas una pregunta al despedirte"""}, prompt_usuario])
    print("Respuesta del modelo:", respuesta.content)
    # Devuelve la respuesta generada por el modelo
    return respuesta.content



DATABASE_URL = db_url


@app.post('/ingesta_datos')
async def insert(data: dict, background_tasks: BackgroundTasks):
    pregunta = data.get("pregunta_usuario")
    respuesta = data.get("respuesta")

    background_tasks.add_task(save_to_database, pregunta, respuesta)

    return {"message": "Data received and will be saved."}


async def save_to_database(pregunta: str, respuesta: str):
    try:
        # Conectar a la base de datos PostgreSQL
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            # Comprobar si la tabla existe, y si no, crearla
            async with pool.acquire() as connection:
                await connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cinema_data (
                        id SERIAL PRIMARY KEY,
                        pregunta TEXT,
                        respuesta TEXT
                    )
                    """
                )

                # Ejecutar la consulta SQL para insertar los datos en la tabla
                await connection.execute(
                    "INSERT INTO cinema_data (pregunta, respuesta) VALUES ($1, $2)",
                    pregunta, respuesta
                )
    except Exception as e:
        print(f"Error al guardar datos en la base de datos: {e}")

        
@app.get('/historial', response_class=HTMLResponse)
async def historial():
    try:
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            async with pool.acquire() as connection:
                # Consultar la base de datos para obtener el historial
                records = await connection.fetch("SELECT * FROM cinema_data")
                
                # Construir una tabla HTML con los datos del historial
                historial_html = "<h2>Historial</h2><table border='1'><tr><th>ID</th><th>Pregunta</th><th>Respuesta</th></tr>"
                for record in records:
                    historial_html += f"<tr><td>{record['id']}</td><td>{record['pregunta']}</td><td>{record['respuesta']}</td></tr>"
                historial_html += "</table>"
                
                return historial_html
    except Exception as e:
        print(f"Error al obtener el historial desde la base de datos: {e}")
        return "Error al obtener el historial desde la base de datos"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
