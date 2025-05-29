import time
import pytest
import requests

def test_comunicacao_c1_c2():
    try:
        requests.post("http://host.docker.internal:5002/api/reseta", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Não foi possível conectar ao sistema C1 para resetar")
    
    try:
        requests.post("http://localhost:5003/api/reseta", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Não foi possível resetar o sistema de reservas")

    time.sleep(1)

    # Cria professor na outra API
    professor = {"nome": "Prof. Teste", "id": 201}
    prof_response = requests.post(
        "http://host.docker.internal:5002/api/professores",
        json=professor,
        timeout=5
    )
    assert prof_response.status_code == 200, "Falha ao criar professor no C1"
    
    # Cria turma na outra API
    turma = {"id": 888, "nome": "Turma Integração", "professor_id": 201}
    turma_response = requests.post(
        "http://host.docker.internal:5002/api/turmas",
        json=turma,
        timeout=5
    )
    assert turma_response.status_code == 200, "Falha ao criar turma no C1"
    
    # Cria reserva na outra API
    reserva_data = {
        "turma_id": 888,
        "sala": "LAB-INTEGRACAO",
        "data": "2024-12-02",
        "hora_inicio": "09:00",
        "hora_fim": "11:00"
    }
    response_c2 = requests.post(
        "http://localhost:5003/api/reservas",
        json=reserva_data
    )
    
    if response_c2.status_code != 201:
        print(f"Erro ao criar reserva: {response_c2.status_code}")
        print(f"Resposta: {response_c2.text}")
    
    assert response_c2.status_code == 201
    
    # Verificar reserva 
    reserva = response_c2.json()
    assert reserva["sala"] == "LAB-INTEGRACAO"
    
    # Buscar reserva por ID
    reserva_id = reserva["id"]
    response_get = requests.get(f"http://localhost:5003/api/reservas/{reserva_id}")
    assert response_get.status_code == 200
    assert response_get.json()["sala"] == "LAB-INTEGRACAO"