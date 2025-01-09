FROM python:3.10-slim as builder

WORKDIR /app

# requirements.txt를 먼저 복사
COPY requirements.txt .

# 빌더 단계의 모든 설치를 하나의 RUN으로 통합
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    python3-dev \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/* \
    && CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS -DGGML_CCACHE=OFF" \
    && pip install --no-cache-dir -r requirements.txt

# 실행 스테이지
FROM python:3.10-slim

WORKDIR /app

# 실행 단계의 모든 설치를 하나의 RUN으로 통합
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY app app/

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]