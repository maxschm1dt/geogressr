import markdown


with open('static/res/mds/de.md') as md_file:
    md_content = md_file.read()


html_content = markdown.markdown(md_content)
print(html_content)