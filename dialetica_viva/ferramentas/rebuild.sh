#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd /tmp/book/src
rm -f /tmp/book/out.docx
zip -q -X -r /tmp/book/out.docx . -x '.DS_Store'
cd /tmp/book
rm -f out.pdf
# O sumário é um campo TOC (ver 4.5 do LEIA-ME): soffice --convert-to pdf sozinho
# não recalcula campos, só renderiza o texto em cache. update_fields.py abre o
# documento via UNO, atualiza o índice e só então exporta o PDF.
python3 "$SCRIPT_DIR/update_fields.py"
pdfinfo out.pdf | grep Pages
