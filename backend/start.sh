#!/bin/bash

# Запуск backend
source venv/bin/activate
python3 app.py &

# Запуск frontend
cd ../frontend
npm run dev -- --host




