# Usa Python mais completo com sistema base decente
FROM python:3.12-bullseye

# Atualiza e instala Chrome + ChromeDriver + dependências
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
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instala Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Instala ChromeDriver compatível
RUN CHROME_VERSION=$(google-chrome-stable --version | sed 's/[^0-9.]//g' | cut -d'.' -f1) && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Define diretório de trabalho
WORKDIR /app

# Copia código
COPY . .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Porta padrão (só se precisar Flask ou algo parecido)
ENV PORT=8080

# Expõe porta
EXPOSE 8080

# Comando para iniciar o bot
CMD ["python", "src/chatBot.py"]