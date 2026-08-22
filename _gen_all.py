# -*- coding: utf-8 -*-
import os, json

base = r"D:\ming_software\my-tool\my-tool\pkgTools\pages"

def w(name, content):
    path = os.path.join(base, name, name + ".vue")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {name}")


