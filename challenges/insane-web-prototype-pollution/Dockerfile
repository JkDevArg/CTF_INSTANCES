FROM node:20-slim
WORKDIR /app
COPY app/ .
RUN npm init -y && npm install express
EXPOSE 80
CMD ["node", "app.js"]
