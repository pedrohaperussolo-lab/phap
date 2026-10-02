#!/bin/bash
# Reconstrói out.docx a partir de src/ e converte para PDF.
# Rode a partir da raiz do pacote: bash rebuild.sh
set -e
RAIZ="$(cd "$(dirname "$0")" && pwd)"
cd "$RAIZ/src"
rm -f "$RAIZ/out.docx"
zip -q -X -r "$RAIZ/out.docx" . -x '.DS_Store'
cd "$RAIZ"
rm -f out.pdf
soffice --headless --convert-to pdf --outdir "$RAIZ" out.docx >/dev/null 2>&1
pdfinfo out.pdf | grep Pages
