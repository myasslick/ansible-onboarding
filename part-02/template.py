from jinja2 import Template

my_name = "John"
template = Template("Hello, {{ my_name }}")
print(template.render(my_name=my_name))
