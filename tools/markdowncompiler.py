import markdown
import os
import pypandoc

input_dir = "static/res/mds"


for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.md'):
            md_file_path = os.path.join(root, file)

            html_content = pypandoc.convert_file(md_file_path, 'html', encoding='UTF-8', outputfile=(f'static/res/htmls/{file[:-3]}.html'))