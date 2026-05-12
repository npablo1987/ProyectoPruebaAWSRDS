# Etapa 1: Build de la aplicación Angular
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build:prod

# Etapa 2: Servir con Nginx
FROM nginx:alpine

COPY --from=build /app/dist/servicio-angular /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
