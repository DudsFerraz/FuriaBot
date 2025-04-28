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
    --no-install-recommends

RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_124.0.6367.91-1_amd64.deb \
    && dpkg -i google-chrome-stable_*.deb || apt-get install -yf \
    && rm google-chrome-stable_*.deb

RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) \
    && CHROMEDRIVER_URL=https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION.0.0.0/linux64/chromedriver-linux64.zip \
    && wget -q -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL" \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && mv /usr/bin/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /usr/bin/chromedriver-linux64

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/chatBot.py"]