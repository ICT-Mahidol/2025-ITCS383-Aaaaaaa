#!/bin/bash

# Run tests for the Booth Organizer System

cd /workspaces/2025-ITCS383-Aaaaaaa/implementations/backend

# Install dependencies if not already installed
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
# pytest --cov=app --cov-report=html