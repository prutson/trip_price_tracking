# Usa uma imagem oficial com Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install --with-deps

# Expõe a porta da aplicação
EXPOSE 8080

# Roda o app
CMD ["python", "main.py"]
