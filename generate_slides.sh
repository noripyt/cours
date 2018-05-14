#!/usr/bin/env bash

cd algorithmique
jupyter nbconvert "Cours d’algorithmique.ipynb" --to slides
mv "Cours d’algorithmique.slides.html" index.html

cd ../bases-de-données
jupyter nbconvert "Bases de données.ipynb" --to slides
mv "Bases de données.slides.html" index.html

cd ../C
jupyter nbconvert C.ipynb --to slides
mv C.slides.html index.html

cd ../python
jupyter nbconvert Python.ipynb --to slides
mv Python.slides.html index.html

cd ../postgresql
jupyter nbconvert PostgreSQL.ipynb --to slides
mv PostgreSQL.slides.html index.html
