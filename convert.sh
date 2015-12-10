find ./content/ -type f -name '*.md' -print | while read filename; do sed -n '3p' $filename | sed -E 's/title: ([^/]*)/\\section{\1}/g'; echo "\label{section:" $filename "}" | sed 's,.md,,' | sed -e 's/[ ./]//g' | sed 's,content,,'; tail -n+7 $filename; printf "\n\n"; done | ./md2latex.py > pattern_directory.tex

