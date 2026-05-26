#!/bin/bash
# Deploy ToolStack to Vercel, Netlify, or Surge.sh
# Usage: bash deploy.sh <target>
#   target = "vercel" | "netlify" | "surge" | "all"

set -e

TARGET="${1:-vercel}"

case "$TARGET" in
  vercel)
    echo "→ Deploying to Vercel..."
    npx vercel --prod --yes
    echo "✅ Deployed to Vercel!"
    ;;
  netlify)
    echo "→ Deploying to Netlify..."
    npx netlify-cli deploy --prod --dir=.
    echo "✅ Deployed to Netlify!"
    ;;
  surge)
    echo "→ Deploying to Surge.sh..."
    npx surge --domain toolstack.surge.sh
    echo "✅ Deployed to Surge.sh! Site at https://toolstack.surge.sh"
    ;;
  all)
    echo "→ Deploying to all targets..."
    $0 vercel
    $0 netlify
    $0 surge
    ;;
  *)
    echo "Usage: bash deploy.sh [vercel|netlify|surge|all]"
    exit 1
    ;;
esac