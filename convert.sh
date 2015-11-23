find ./content/ -type f -name '*.md' -print | while read filename; do head -n 1 $filename; echo "\label{section:" $filename "}" | sed 's,.md,,' | sed -e 's/[ ./]//g' | sed 's,content,,'; cat $filename | sed -n '1!p'; printf "\n\n"; done | ./md2latex.py > pattern_directory.tex

