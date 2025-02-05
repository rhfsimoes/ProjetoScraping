import subprocess
import os
import sys
import psutil

# Caminhos dos arquivos
output_file = r"C:\Users\Rafael\documents\ProjetoScraping\data\tnike.jsonl"
scrapy_project_dir = r"C:\Users\Rafael\documents\ProjetoScraping\src"  # Caminho para a pasta src
transform_script = r"C:\Users\Rafael\documents\ProjetoScraping\src\transform\tnike.py"
streamlit_script = r"C:\Users\Rafael\documents\ProjetoScraping\src\dashboard\dashnike.py"

# Garantindo que o arquivo tnike.jsonl seja removido antes da execução
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Arquivo {output_file} removido.")

# Mudando para a pasta do projeto Scrapy
os.chdir(scrapy_project_dir)  # Muda o diretório de trabalho para 'src'

# Executando o Scrapy (sobrescrevendo o arquivo)
print("Executando Scrapy...")
scrapy_command = f"scrapy crawl mercadolivrenike -O {output_file}"

try:
    subprocess.run(scrapy_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar Scrapy: {e}")
    exit(1)

# Executando o script de transformação com o Python correto
print("Executando transformação dos dados...")
try:
    subprocess.run([sys.executable, transform_script], check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o script de transformação: {e}")
    exit(1)

# Função para verificar se o Streamlit já está rodando
def is_streamlit_running():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and "streamlit" in proc.info['name'].lower():
                return True  # Streamlit já está rodando
            if proc.info['cmdline'] and any("streamlit" in arg for arg in proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

# Verificando se o Streamlit está rodando
if not is_streamlit_running():
    print("Streamlit não está rodando. Iniciando agora...")
    try:
        subprocess.Popen(["streamlit", "run", streamlit_script], shell=True)
        print("Streamlit iniciado com sucesso!")
    except Exception as e:
        print(f"Erro ao iniciar o Streamlit: {e}")
else:
    print("Streamlit já está rodando.")

print("Processo concluído!")
