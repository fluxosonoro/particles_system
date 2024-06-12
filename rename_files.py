import os

def rename_files(directory, prefix='file_'):
    # Lista todos os arquivos no diretório
    files = os.listdir(directory)
    
    # Filtra apenas os arquivos (excluindo diretórios)
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    
    # Ordena os arquivos para garantir ordem ao renomear
    files.sort()
    
    for index, filename in enumerate(files):
        # Define a nova extensão para manter a extensão original do arquivo
        extension = os.path.splitext(filename)[1]
        # Define o novo nome do arquivo
        new_name = f"{index + 1}{extension}"
        # Caminhos completos
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)
        # Renomeia o arquivo
        os.rename(old_file, new_file)
        print(f"Renamed: {old_file} to {new_file}")

# Diretório onde os arquivos estão localizados
directory = 'output_images_resized'

# Chama a função para renomear os arquivos
rename_files(directory)
