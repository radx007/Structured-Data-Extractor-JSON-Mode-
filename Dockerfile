# =========================
# STAGE 1: BUILDER
# =========================
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV LIBRARY_PATH=/usr/local/cuda/lib64/stubs:$LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs:/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Create libcuda.so.1 symlink so the linker can resolve it
RUN ln -sf /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    ccache \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/ggml-org/llama.cpp.git
WORKDIR /opt/llama.cpp

# Build BOTH llama-server AND llama-mtmd-cli
RUN cmake -B build \
    -DGGML_CUDA=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CUDA_ARCHITECTURES=75 \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_EXAMPLES=OFF \
    -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
    -DCMAKE_EXE_LINKER_FLAGS="-L/usr/local/cuda/lib64/stubs -lcuda" \
    -DCMAKE_SHARED_LINKER_FLAGS="-L/usr/local/cuda/lib64/stubs" \
    && cmake --build build --target llama-server -j$(nproc) \
    && cmake --build build --target llama-mtmd-cli -j$(nproc) \
    && strip build/bin/llama-server \
    && strip build/bin/llama-mtmd-cli

# Gather all shared libs into one folder
RUN mkdir -p /opt/llama_libs && \
    cp build/bin/libggml*.so* /opt/llama_libs/ && \
    cp build/bin/libllama*.so* /opt/llama_libs/ && \
    cp build/bin/libmtmd*.so* /opt/llama_libs/ 2>/dev/null; exit 0

# =========================
# STAGE 2: RUNTIME
# =========================
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib/llama:/usr/local/cuda/lib64:$LD_LIBRARY_PATH

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy both binaries
COPY --from=builder /opt/llama.cpp/build/bin/llama-server /usr/local/bin/llama-server
COPY --from=builder /opt/llama.cpp/build/bin/llama-mtmd-cli /usr/local/bin/llama-mtmd-cli

# Copy shared libs
COPY --from=builder /opt/llama_libs/ /usr/local/lib/llama/

# Symlink both binaries into /opt/llama/ to match your settings.py paths exactly
RUN mkdir -p /opt/llama && \
    ln -sf /usr/local/bin/llama-server /opt/llama/llama-server && \
    ln -sf /usr/local/bin/llama-mtmd-cli /opt/llama/llama-mtmd-cli

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]