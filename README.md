# Patterns
Technical patterns for integrating organisations using x-road

For most users, it would make sense to  head over to http://jointxroad.github.io/patterns/

For running a local copy, clone the repo and serve it using jekyll

Should you be adventurous and would love a PDF output, it is recommended to get a TeXLive installation from https://www.tug.org/texlive/. Main.tex should fully complile using the standard installation with the following workflow:
* Run the convert.sh script that converts the md files to LaTeX
* XeLaTeX
* BibTex
* MakeIndex
* XeLaTeX
* XeLaTeX
