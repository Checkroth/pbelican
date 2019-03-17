git checkout master && git branch -D gh-pages && git checkout -b gh-pages && pelican && ghp-import -n output/ && git push origin gh-pages -f && git checkout -
