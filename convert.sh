find ./content/ -type f -name '*.md' -print | while read filename; do echo "\label{" $filename "}" | sed 's,.md,,' | sed -e 's/[ ./]//g'; cat $filename; printf "\n\n"; done | ./md2latex.py

