import requests

def test_pedir_recomendacion():
    url = 'http://localhost:8000/pedir_recomendacion?pregunta_usuario=¿Cuál es la mejor película de Tarantino?'
    response = requests.get(url)
    assert response.status_code == 200
    # Agrega más aserciones para verificar el contenido de la respuesta si es necesario

def test_ingesta_datos():
    url = 'http://localhost:8000/ingesta_datos'
    data = {'pregunta_usuario': '¿Cuál es la mejor película de Tarantino?', 'respuesta': 'Pulp Fiction'}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    # Agrega más aserciones si es necesario

def test_historial():
    url = 'http://localhost:8000/historial'
    response = requests.get(url)
    assert response.status_code == 200
    # Agrega más aserciones para verificar el contenido de la respuesta si es necesario
