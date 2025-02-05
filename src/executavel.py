import subprocess
import os

# Caminhos dos arquivos
output_file = r"C:\Users\Rafael\documents\ProjetoScraping\data\tnike.jsonl"
transform_script = r"C:\Users\Rafael\documents\ProjetoScraping\src\transformacao\tenisnike.py"

# Garantindo que o arquivo tnike.jsonl seja removido antes da execução para evitar acumulação de dados
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Arquivo {output_file} removido.")

# Executando o Scrapy (sobrescrevendo o arquivo)
print("Executando Scrapy...")
scrapy_command = f"scrapy crawl mercadolivrenike -O {output_file}"  # -O sobrescreve o arquivo
subprocess.run(scrapy_command, shell=True, check=True)

# Executando o script de transformação
print("Executando transformação dos dados...")
subprocess.run(["python", transform_script], check=True)

print("Processo concluído!")