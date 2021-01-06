# Verzameling
Create lists for your collections. 
 
## Getting started
Run `start.bash`

## Deploy using a git hook
Check https://www.denick.org/post/08deploy/
To write the release version every time you deploy, add an extra row to the `post-receive` file:

    echo "Versie website: $(date)" > web/templates/footer.txt

If this file exists, it will be displayed in the footer of the webpage.
