#!/usr/bin/env python3
"""Abre /tmp/book/out.docx via UNO, atualiza sumário/campos e exporta /tmp/book/out.pdf.

soffice --headless --convert-to pdf NÃO recalcula campos TOC: renderiza o texto
em cache (o placeholder). Este script abre o documento de verdade via UNO,
chama update() em cada índice (Table of Contents) e só então exporta o PDF,
para que a paginação do sumário saia correta.
"""
import subprocess, time, sys

PROFILE = "/tmp/lo_uno_profile"
subprocess.run(["rm", "-rf", PROFILE])

proc = subprocess.Popen([
    "soffice", "--headless", "--invisible", "--nologo", "--nofirststartwizard",
    "--norestore", f"-env:UserInstallation=file://{PROFILE}",
    "--accept=socket,host=localhost,port=2002;urp;"
])

import uno
from com.sun.star.beans import PropertyValue

def make_prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p

localContext = uno.getComponentContext()
resolver = localContext.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", localContext)

ctx = None
for _ in range(30):
    try:
        ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        break
    except Exception:
        time.sleep(1)

if ctx is None:
    print("FALHA: não conectou ao soffice via UNO")
    proc.terminate()
    sys.exit(1)

smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

in_url = "file:///tmp/book/out.docx"
out_url = "file:///tmp/book/out.pdf"

doc = desktop.loadComponentFromURL(in_url, "_blank", 0, (make_prop("Hidden", True),))

try:
    indexes = doc.getDocumentIndexes()
    for i in range(indexes.getCount()):
        indexes.getByIndex(i).update()
except Exception as e:
    print("Erro ao atualizar índices:", e)

try:
    doc.getTextFields().refresh()
except Exception as e:
    print("Erro ao atualizar campos de texto:", e)

doc.storeToURL(out_url, (make_prop("FilterName", "writer_pdf_Export"),))
print("PDF exportado:", out_url)

doc.close(False)
desktop.terminate()
time.sleep(1)
proc.terminate()
