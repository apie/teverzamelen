# Verzameling
Create lists for your collections. 
 
## Getting started
Run `start.bash`

## Deploy using a git hook
Check https://www.denick.org/post/08deploy/
To write the release version every time you deploy using git, add an extra row to the `post-receive` file:

    echo "Versie website: $(date)" > web/templates/footer.txt

You could also have it link to the commit on github:

    hash=$(git show -s --format=%H)
    d=$(git show -s --format=%ci)
    echo "Versie website: <a href='https://github.com/apie/teverzamelen/commit/${hash}'>${d}</a>" > web/templates/footer.txt

If this file (footer.txt) exists, it will be displayed in the footer of the webpage.

To make Gunicorn restart after the deploy:

    pkill -HUP -f teverzamelen

