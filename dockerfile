FROM python:3.12-slim-bullseye

# Instala dependências essenciais para Chrome e ChromeDriver funcionarem
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    gnupg \
    chromium-driver \
    chromium \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia o projeto para dentro do container
COPY . .

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Porta padrão
ENV PORT=8080

# Expõe a porta para o Railway
EXPOSE 8080

# Comando para iniciar o bot
CMD ["python", "src/chatBot.py"]
