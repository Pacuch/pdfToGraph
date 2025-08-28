import markdown

markdown_table_string = """
| Section | Subsection | Page Start | Page End |
| --- | --- | --- | --- |
| Contributors |  | 8 | 8 |
"""

# Enable the "tables" extension
html_output = markdown.markdown(markdown_table_string, extensions=['markdown.extensions.tables'])
print(html_output)
