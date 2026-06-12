FROM node:20-alpine AS frontend-build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .

ARG VITE_BASE_PATH=/
ENV VITE_BASE_PATH=$VITE_BASE_PATH

RUN npm run build \
    && test -f dist/index.html \
    || (echo "ERROR: frontend build failed — dist/index.html missing" && exit 1)

FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx/snippets /etc/nginx/snippets
COPY --from=frontend-build /app/dist /usr/share/nginx/html

RUN test -f /usr/share/nginx/html/index.html \
    || (echo "ERROR: static files not copied into nginx image" && exit 1)

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
