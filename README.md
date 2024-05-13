# IA-GENERATIVA

# FastAPI CineAPI

Este proyecto es una API desarrollada en FastAPI que proporciona recomendaciones cinematográficas y permite la ingesta de datos para construir un historial de consultas.

## Funcionalidades

- **Pedir Recomendación**: Mediante la ruta `/pedir_recomendacion`, los usuarios pueden enviar una pregunta sobre cine y recibir una recomendación generada por un modelo de lenguaje de inteligencia artificial.

- **Ingesta de Datos**: Los usuarios pueden enviar datos de preguntas y respuestas al servidor mediante la ruta `/ingesta_datos`. Estos datos se guardan en una base de datos PostgreSQL para mantener un historial de consultas.

- **Historial**: La ruta `/historial` muestra un historial de consultas almacenadas en la base de datos, incluyendo el ID de la consulta, la pregunta y la respuesta.

## Uso de la API

### Requisitos

- Docker instalado en tu sistema.
- Una API key de OpenAI para utilizar el modelo de lenguaje. Puedes obtener una en [OpenAI](https://openai.com).
- Una `DATABASE_URL` válida de Render.com o de tu propio servidor PostgreSQL.

### Instrucciones

1. Descarga la imagen de Docker desde Docker Hub:

   ```bash
   docker pull tu_usuario/fastapi-cineapi:latest


2. Ejecuta el contenedor Docker:

docker run -d --name cineapi -p 8000:8000 tu_usuario/fastapi-cineapi:latest


3. Accede a la API desde tu navegador o herramienta de desarrollo de API, utilizando las siguientes rutas:

    Home: http://localhost:8000/
    Pedir Recomendación: http://localhost:8000/pedir_recomendacion?pregunta_usuario=Tu%20pregunta%20aquí
    Ingesta de Datos: Envía una solicitud POST a http://localhost:8000/ingesta_datos con los datos de la pregunta y la respuesta en formato JSON.
    Historial: http://localhost:8000/historial


Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar esta API, no dudes en hacer un fork del repositorio, implementar tus cambios y enviar un pull request.
Agradecimientos

Este proyecto utiliza la biblioteca FastAPI para crear la API web.
Se basa en modelos de lenguaje de OpenAI para generar recomendaciones.
Utiliza una base de datos PostgreSQL para almacenar el historial de consultas.
