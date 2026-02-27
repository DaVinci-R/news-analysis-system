FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 交互层和前端可能需要的额外依赖量
RUN pip install --no-cache-dir fastapi uvicorn

COPY . .

# 运行数据层
CMD ["python", "-m", "data_layer.main"]
