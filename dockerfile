FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    fonts-liberation \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libxcomposite1 \
    libxrandr2 \
    libxv1 \
    libgbm1 \
    libglu1 \
    xvfb \
    libgl1 \
    unzip \
    --no-install-recommends

# Instala Chrome versão específica
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_124.0.6367.91-1_amd64.deb \
    && dpkg -i google-chrome-stable_*.deb || apt-get install -yf \
    && rm google-chrome-stable_*.deb

# Instala ChromeDriver correspondente exato
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/124.0.6367.91/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /usr/bin/ \
    && mv /usr/bin/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Verificação crítica
RUN ls -l /usr/bin/chromedriver && chromedriver --version

CMD ["python", "src/chatBot.py"]