from jinja2 import Environment, FileSystemLoader

regions = {
    "east": "json",
    "west": "plain"
}

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("aws-config-template.j2")
print(template.render(regions=regions))
