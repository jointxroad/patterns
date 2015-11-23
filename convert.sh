find ./content/ -type f -name '*.md' -print | while read filename; do echo "\label{section:" $filename "}" | sed 's,.md,,' | sed -e 's/[ ./]//g' | sed 's,content,,'; cat $filename; printf "\n\n"; done | ./md2latex.py > pattern_directory.tex

