# Build stage
FROM node:18-alpine AS frontend-builder

WORKDIR /app
ENV NODE_ENV=production
ENV VITE_API_BASE_URL=http://backend:8000

COPY package*.json ./
RUN npm ci --include=dev
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app
ENV PORT=5173
EXPOSE $PORT

RUN npm install -g serve
COPY --from=frontend-builder /app/dist ./dist

CMD ["serve", "-s", "dist", "-l", "5173"]