#!/bin/bash

# Cloudflare Pages Deployment Script for Barboss Room
# This script helps deploy the static site to Cloudflare Pages

echo "================================"
echo "Barboss Room - Cloudflare Deploy"
echo "================================"

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "Installing Wrangler CLI..."
    npm install -g wrangler
fi

# Project configuration
PROJECT_NAME="barboss-room"
BUILD_OUTPUT="."

echo ""
echo "Deploying to Cloudflare Pages..."
echo "Project: $PROJECT_NAME"
echo ""

# Deploy to Cloudflare Pages
wrangler pages deploy $BUILD_OUTPUT --project-name=$PROJECT_NAME

echo ""
echo "================================"
echo "Deployment Complete!"
echo "Your site will be available at:"
echo "https://$PROJECT_NAME.pages.dev"
echo "================================"