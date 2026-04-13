#!/usr/bin/env bash
set -e

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright system dependencies..."
# Install system deps for Chromium on Ubuntu (Render uses Ubuntu)
apt-get update -qq 2>/dev/null || true
apt-get install -y -qq \
  libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
  libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
  libpango-1.0-0 libcairo2 libpangocairo-1.0-0 \
  2>/dev/null || true

echo "🎭 Installing Playwright browsers..."
python -m playwright install chromium

echo "✅ Build complete"
