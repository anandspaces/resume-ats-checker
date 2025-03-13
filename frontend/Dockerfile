# Build stage
FROM node:18-alpine as builder

WORKDIR /app
ENV NODE_ENV=production
ENV VITE_API_BASE_URL=http://backend:8000

COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app
ENV PORT=3000
EXPOSE $PORT

RUN npm install -g serve@14.2.0
COPY --from=builder /app/build ./build

CMD ["serve", "-s", "build", "-l", "3000"]