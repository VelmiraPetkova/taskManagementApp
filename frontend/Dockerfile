# Стъпка 1: Ако имаш build стъпка (например React/Vue), тук може да добавиш
FROM node:16 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Стъпка 2: Nginx като сървър за статични файлове
FROM nginx:alpine

# Копираме файловете в nginx директорията за static content
# Ако имаш build папка - използвай COPY build/ /usr/share/nginx/html/
# Ако работиш с plain JS и файловете са в корена, копирай ги директно

COPY . /usr/share/nginx/html

# Експонираме порт 80
EXPOSE 80

# CMD е по default за nginx - няма нужда да го променяме
