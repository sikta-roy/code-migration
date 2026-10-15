# Sandbox for compiling and running LLM-generated C code.
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc libc6-dev cppcheck python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m runner
WORKDIR /work
USER runner
