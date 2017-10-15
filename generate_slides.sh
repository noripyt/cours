#!/usr/bin/env bash

cd algorithmique
jupyter nbconvert "Cours d’algorithmique.ipynb" --to slides
mv "Cours d’algorithmique.slides.html" index.html

cd ../bases-de-données
jupyter nbconvert "Bases de données.ipynb" --to slides
mv "Bases de données.slides.html" index.html
