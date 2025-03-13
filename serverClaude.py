from flask import Flask, request, jsonify, abort
from llama_cpp import Llama
import os
import logging
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Verificar se o diretório de modelos existe, se não, criar
os.makedirs(r"models\llama-3", exist_ok=True)

# Caminho do modelo
modelo_path = r"models\llama-3\Meta-Llama-3-8B.Q4_0.gguf"

# Carregar o modelo com suporte a CUDA
try:
    logger.info(f"Carregando modelo de {modelo_path}...")
    llm = Llama(
        model_path=modelo_path,
        n_ctx=2048,       # Contexto de 2048 tokens
        n_threads=6,      # Número de threads para processamento
        n_batch=512,      # Tamanho do batch para inferência
        n_gpu_layers=40   # Número de camadas para mover para a GPU
    )
    logger.info("Modelo carregado com sucesso!")
except FileNotFoundError:
    logger.error(f"Arquivo do modelo não encontrado em {modelo_path}")
    logger.info("Por favor, baixe o modelo LLaMA 3 8B ou 7B GGUF do Hugging Face (https://huggingface.co/TheBloke)")
    exit(1)
except Exception as e:
    logger.error(f"Erro ao carregar o modelo: {str(e)}")
    exit(1)

def gerar_prompt_manchester(dados_paciente):
    """
    Gera um prompt estruturado para o modelo LLaMA 3 com foco no Protocolo Manchester
    e diagnósticos diferenciais.
    
    Args:
        dados_paciente (dict): Dicionário com os dados do paciente
        
    Returns:
        str: Prompt formatado para o modelo
    """
    prompt = f"""<|im_start|>system
Você é um médico especialista em emergências com vasta experiência em triagem e classificação de risco.
Sua tarefa é analisar os dados do paciente e fornecer:

1. Classificação de Risco pelo Protocolo Manchester:
   - VERMELHO (emergência): atendimento imediato
   - LARANJA (muito urgente): atendimento em até 10 minutos
   - AMARELO (urgente): atendimento em até 60 minutos
   - VERDE (pouco urgente): atendimento em até 120 minutos
   - AZUL (não urgente): atendimento em até 240 minutos

2. Sugestão de conduta médica inicial específica para este caso, incluindo exames e intervenções.

3. Cinco hipóteses diagnósticas em ordem de probabilidade.

Base sua análise exclusivamente nos dados fornecidos. Seja conciso e objetivo.
<|im_end|>

<|im_start|>user
Dados do Paciente:
- Idade: {dados_paciente.get('idade', 'Não informada')} anos
- Sexo: {dados_paciente.get('sexo', 'Não informado')}
- Sintomas principais: {dados_paciente.get('sintomas', 'Não informados')}
- Sinais vitais: {dados_paciente.get('sinais_vitais', 'Não informados')}
- Histórico relevante: {dados_paciente.get('historico', 'Não informado')}
- Tempo de início dos sintomas: {dados_paciente.get('tempo_inicio', 'Não informado')}

Por favor, forneça a classificação Manchester, conduta imediata e hipóteses diagnósticas.
<|im_end|>

<|im_start|>assistant
"""
    return prompt

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    try:
        inicio = time.time()
        data = request.json
        
        # Validação de entrada
        if not data or not all(key in data for key in ['idade', 'sexo', 'sintomas', 'sinais_vitais', 'historico', 'tempo_inicio']):
            abort(400, description="Dados do paciente incompletos ou inválidos.")
        
        # Estrutura os dados do paciente
        dados_paciente = {
            'idade': data.get('idade', ''),
            'sexo': data.get('sexo', ''),
            'sintomas': data.get('sintomas', ''),
            'sinais_vitais': data.get('sinais_vitais', ''),
            'historico': data.get('historico', ''),
            'tempo_inicio': data.get('tempo_inicio', '')
        }
        
        # Gera o prompt estruturado
        prompt = gerar_prompt_manchester(dados_paciente)
        
        # Configurações de geração
        response = llm(
            prompt,
            max_tokens=400,  # Reduza o número de tokens
            temperature=0.1,
            top_p=0.9,
            repeat_penalty=1.1
        )
        
        resposta = response["choices"][0]["text"].strip()
        
        # Registrar tempo de processamento
        tempo_processamento = time.time() - inicio
        logger.info(f"Tempo de processamento: {tempo_processamento:.2f} segundos")
        
        return jsonify({
            "diagnostico": resposta,
            "modelo": "LLaMA 3",
            "aviso": "Este é um diagnóstico preliminar gerado por IA e não substitui a avaliação de um profissional médico."
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar diagnóstico: {str(e)}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "modelo": "LLaMA 3"})

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask na porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)