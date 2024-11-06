find . -type f -name '*.bib' -exec cat {} \; > ./all-info


um alle bib dateien zu kopieren



academic import --bibtex my_publications
um zu importieren


find . -name '*.md' -print0 | xargs -0 sed -i "" "s/~/ /g"