# Usa imagem oficial Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto para dentro do container
COPY . .

# Instala dependências do sistema (bibliotecas necessárias pro Chromium)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libgbm1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxext6 \
    libxi6 \
    libgl1 \
    && apt-get clean

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install --with-deps

# Expõe a porta usada pelo Flask (ajuste se necessário)
EXPOSE 5000

# Comando para rodar sua aplicação
CMD ["xvfb-run", "-a", "python", "main.py"]

