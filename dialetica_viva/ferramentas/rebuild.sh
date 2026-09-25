#!/bin/bash
set -e
cd /tmp/book/src
rm -f /tmp/book/out.docx
zip -q -X -r /tmp/book/out.docx . -x '.DS_Store'
cd /tmp/book
rm -f out.pdf
soffice --headless --convert-to pdf --outdir /tmp/book out.docx >/dev/null 2>&1
pdfinfo out.pdf | grep Pages
