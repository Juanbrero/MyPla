# Dockerfile

# Etapa 1: build
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: servir con nginx
FROM nginx:alpine

# Copia el build al directorio público de nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia config personalizada de nginx
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
