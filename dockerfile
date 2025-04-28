FROM zenika/alpine-chrome:with-node

# Instala Python no container
RUN apk add --no-cache python3 py3-pip

# Define o diretório de trabalho
WORKDIR /app

# Copia o código
COPY . .

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define variáveis de ambiente
ENV PORT=8080

# Expõe porta (Railway exige EXPOSE, mesmo pra Worker)
EXPOSE 8080

# Comando para rodar seu bot
CMD ["python3", "src/chatBot.py"]