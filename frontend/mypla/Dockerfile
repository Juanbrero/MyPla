# Dockerfile

# Etapa 1: build
FROM node:23-alpine AS build


# Permitir pasar el modo de Vite como argumento (por defecto, 'production')
ARG VITE_MODE=production
ENV VITE_MODE=$VITE_MODE


WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
# Build del frontend usando el modo correspondiente (carga .env.$VITE_MODE)
RUN npm run build -- --mode $VITE_MODE

# Etapa 2: servir con nginx
FROM nginx:alpine

# Copia el build al directorio público de nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia config personalizada de nginx
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
