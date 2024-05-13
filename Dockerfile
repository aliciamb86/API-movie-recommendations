# Utilizar una imagen de Python oficial como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo del contenedor
WORKDIR /app

# Copiamos los archivos a ese directorio
COPY . /app

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponemos el puert en el que la aplicación está corriendo
EXPOSE 8000

# Comando para ejecutar la aplicación cuando el contenedor se inicializa
CMD ["python", "FastAPI/FastAPI.py"]