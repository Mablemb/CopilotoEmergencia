import requests
import json
import time
import os
import csv
from datetime import datetime

# URL da API
API_URL = "http://127.0.0.1:5000/diagnostico"

# Função para enviar dados e obter resposta
def testar_caso(caso, modelo):
    headers = {"Content-Type": "application/json"}
    
    # Registrar tempo inicial
    inicio = time.time()
    
    # Enviar requisição para API
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(caso), timeout=300)
        
        # Registrar tempo de resposta
        tempo_resposta = time.time() - inicio
        
        if response.status_code == 200:
            resultado = response.json()
            return {
                'resposta': resultado["diagnostico"],
                'tempo_resposta': round(tempo_resposta, 2),
                'status': 'sucesso'
            }
        else:
            return {
                'resposta': f"Erro: {response.status_code}",
                'tempo_resposta': round(tempo_resposta, 2),
                'status': 'erro'
            }
    except Exception as e:
        return {
            'resposta': f"Erro na requisição: {str(e)}",
            'tempo_resposta': 0,
            'status': 'erro'
        }

# Casos de teste
casos_teste = [
    {
        'id': 1,
        'descricao': 'Dor Torácica Aguda',
        'dados': {
            'idade': '58',
            'sexo': 'M',
            'sintomas': 'Dor torácica opressiva de forte intensidade com irradiação para membro superior esquerdo, sudorese, náusea',
            'sinais_vitais': 'PA 165/90 mmHg, FC 102 bpm, Temp 36.5°C, SatO2 94%',
            'historico': 'Hipertensão, diabetes tipo 2, ex-tabagista (30 maços/ano)',
            'tempo_inicio': '2 horas'
        }
    },
    {
        'id': 2,
        'descricao': 'Dispneia Progressiva',
        'dados': {
            'idade': '72',
            'sexo': 'F',
            'sintomas': 'Falta de ar progressiva há 3 dias, tosse seca, ortopneia, edema em membros inferiores',
            'sinais_vitais': 'PA 150/95 mmHg, FC 110 bpm, Temp 37.1°C, SatO2 88% em ar ambiente',
            'historico': 'Insuficiência cardíaca, fibrilação atrial, uso de furosemida (suspendeu há 5 dias)',
            'tempo_inicio': '3 dias, com piora nas últimas 12 horas'
        }
    },
    {
        'id': 3,
        'descricao': 'Sintomas Neurológicos Agudos',
        'dados': {
            'idade': '67',
            'sexo': 'M',
            'sintomas': 'Hemiparesia à direita de início súbito, disartria, desvio de rima labial à esquerda',
            'sinais_vitais': 'PA 190/105 mmHg, FC 88 bpm, Temp 36.8°C, SatO2 96%',
            'historico': 'Hipertensão mal controlada, dislipidemia',
            'tempo_inicio': '45 minutos'
        }
    },
    {
        'id': 4,
        'descricao': 'Trauma Múltiplo',
        'dados': {
            'idade': '22',
            'sexo': 'M',
            'sintomas': 'Dor abdominal intensa após acidente de moto, escoriações múltiplas, deformidade em membro inferior direito',
            'sinais_vitais': 'PA 90/60 mmHg, FC 125 bpm, Temp 36.2°C, SatO2 93%',
            'historico': 'Sem comorbidades conhecidas',
            'tempo_inicio': '30 minutos (tempo do acidente)'
        }
    },
    {
        'id': 5,
        'descricao': 'Febre e Letargia em Criança',
        'dados': {
            'idade': '3',
            'sexo': 'F',
            'sintomas': 'Febre alta (39.8°C), irritabilidade, sonolência, rigidez de nuca, vômitos, exantema petequial',
            'sinais_vitais': 'PA 85/50 mmHg, FC 150 bpm, Temp 39.8°C, SatO2 95%',
            'historico': 'Vacinação em dia, sem comorbidades',
            'tempo_inicio': '12 horas'
        }
    },
    {
        'id': 6,
        'descricao': 'Dor Abdominal Aguda',
        'dados': {
            'idade': '45',
            'sexo': 'F',
            'sintomas': 'Dor em quadrante inferior direito, náuseas, febre baixa, anorexia',
            'sinais_vitais': 'PA 125/75 mmHg, FC 92 bpm, Temp 37.8°C, SatO2 98%',
            'historico': 'Colecistectomia prévia, apendicectomia negada',
            'tempo_inicio': '24 horas, com piora nas últimas 6 horas'
        }
    },
    {
        'id': 7,
        'descricao': 'Crise Psiquiátrica',
        'dados': {
            'idade': '32',
            'sexo': 'M',
            'sintomas': 'Agitação psicomotora, discurso incoerente, alucinações auditivas, agressividade, insônia há 3 dias',
            'sinais_vitais': 'PA 150/90 mmHg, FC 105 bpm, Temp 36.9°C, SatO2 98%',
            'historico': 'Esquizofrenia diagnosticada, não faz uso regular da medicação há 2 semanas',
            'tempo_inicio': 'Piora gradual há 1 semana'
        }
    },
    {
        'id': 8,
        'descricao': 'Dispneia Súbita',
        'dados': {
            'idade': '48',
            'sexo': 'F',
            'sintomas': 'Falta de ar súbita, dor torácica pleurítica, taquipneia',
            'sinais_vitais': 'PA 110/70 mmHg, FC 115 bpm, Temp 37.0°C, SatO2 89%',
            'historico': 'Pós-operatório de artroplastia de joelho há 10 dias, em uso de anticoagulante',
            'tempo_inicio': '2 horas'
        }
    },
    {
        'id': 9,
        'descricao': 'Crise Convulsiva',
        'dados': {
            'idade': '28',
            'sexo': 'F',
            'sintomas': 'Convulsão tônico-clônica generalizada, período pós-ictal com confusão mental',
            'sinais_vitais': 'PA 140/85 mmHg, FC 108 bpm, Temp 36.7°C, SatO2 94%',
            'historico': 'Epilepsia conhecida, gravidez de 18 semanas',
            'tempo_inicio': 'Crise há 15 minutos, duração aproximada de 3 minutos'
        }
    },
    {
        'id': 10,
        'descricao': 'Intoxicação',
        'dados': {
            'idade': '17',
            'sexo': 'F',
            'sintomas': 'Sonolência, vômitos, pupilas mióticas, bradicardia',
            'sinais_vitais': 'PA 90/50 mmHg, FC 52 bpm, Temp 35.8°C, SatO2 91%',
            'historico': 'Histórico de depressão, encontrada em casa com frascos vazios de benzodiazepínicos',
            'tempo_inicio': 'Desconhecido, encontrada há aproximadamente 1 hora'
        }
    }
]

# Função para salvar resultados em CSV
def salvar_resultados(resultados, nome_modelo):
    # Criar diretório para resultados se não existir
    os.makedirs('resultados', exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resultados/teste_{nome_modelo}_{timestamp}.csv"
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['ID', 'Descrição', 'Tempo Resposta (s)', 'Resposta'])
        
        for result in resultados:
            writer.writerow([
                result['caso_id'],
                result['descricao'],
                result['tempo_resposta'],
                result['resposta']
            ])
    
    print(f"Resultados salvos em {nome_arquivo}")

# Função principal
def main():
    nome_modelo = input("Nome do modelo sendo testado: ")
    resultados = []
    
    print(f"Iniciando teste com {len(casos_teste)} casos para o modelo {nome_modelo}...")
    
    for caso in casos_teste:
        print(f"\nTestando Caso {caso['id']}: {caso['descricao']}")
        print("Enviando dados...")
        
        resultado = testar_caso(caso['dados'], nome_modelo)
        
        if resultado['status'] == 'sucesso':
            print(f"Resposta recebida em {resultado['tempo_resposta']} segundos")
            print("\n=== RESPOSTA DO MODELO ===")
            print(resultado['resposta'])
        else:
            print(f"ERRO: {resultado['resposta']}")
        
        resultados.append({
            'caso_id': caso['id'],
            'descricao': caso['descricao'],
            'tempo_resposta': resultado['tempo_resposta'],
            'resposta': resultado['resposta']
        })
        
        # Perguntar se deseja continuar após cada caso
        if caso != casos_teste[-1]:
            continuar = input("\nPressione Enter para continuar ou 'q' para sair: ")
            if continuar.lower() == 'q':
                break
    
    # Salvar resultados
    salvar_resultados(resultados, nome_modelo)

if __name__ == "__main__":
    main()