# Part 2

Edit the inventory with the EC2 instance IP, and then run the same
``ansible-plabybook`` command like you did for lab 1. But if you
don't have that handy, here it is:

```bash
ansible-playbook -i inventory playbook.yml --user ubuntu --private-key ~/.ssh/KEY_NAME
```

The output from Ansible is familiar to you, right? If you examine the new ``playbook.yml``
in this lab, you will find some strange ``{{ package_name }}`` syntax
and the addition of ``vars`` block. You can probably guess, we are going to have
a deep dive into variables and templating with Ansible.

## Variables in Ansible

Ansible, like programming languages, have variable scope and variable precedence.
You can read more about this on [Variables](http://docs.ansible.com/ansible/playbooks_variables.html). 
With me, you just need to know three things right now:

* YAML syntax

* assigning variables

* and how to use the ``{{ }}`` Jinja templating language


## YAML syntax

You will learn YAML as you work with Ansible. Suppose you have a Python list
like ``["foo", "bar", "foobar"]``, then you can write the YAML:
For a list of items, you can write

```yaml
- foo
- bar
- foobar

Now suppose you want a dictionary of things, in Python:

```python
{
    "orange" : {
        "type" : "fruit"
    },
    "cat" : {
        "type" : "animal"
    }
}
```

Then, in YAML you can write:

```yaml
orange:
  type: fruit
cat:
  type: animal
```

What if you want to name these things, or encapsulate them under one name? Try this:

```yaml
list_of_items:
  - foo
  - bar
  - foobar

dict_of_items:
  orange:
    type: fruit
  cat:
    type: animal
```

Obviously you can mix list and dictionary in YAML. No big deal.

**IMPORTANT**: In YAML, everything is either a string, a boolean, or a number (integer,
float), depending on the implementation of YAML.

In other words, ``foo`` is a string with three characters. ``list_of_items`` is also
a string, not a variable. Ansible's ability to treat things like a variable ( a
reference to some value), is the result of using the template language Jinja2.

## Jinja2

Jinja2 is written in Python, a popular templating language / engine, developed
by the awesome developers who have created many awesome stuff (e.g. Flask)
for the Python community.

Let's run the file ``template.py``. The output is ``Hello, John``. Open the file,
there are four lines of Python code.

```
from jinja2 import Template

my_name = "John"
template = Template("Hello, {{ my_name }}")
print(template.render(my_name=my_name))
```

The concept should be simple. There is a template of characters,
with ``{{ }}`` being the syntax for placeholder for the templating
language.

Jinja is a powerful templating language because it has some
Python-like syntax, such as a for loop or a conditional statement.
Jinja files can have any extension, but by convention we use ``.j2``.
Let's open up ``aws-config-template.j2``.

```python
# Total: {{ regions | length }}
{% for region, output_format in regions.items() %}
[default]
region={{ region }}
output={{ output_format }}
{% endfor %}
```

and if you run ``aws_config_template.py``, the output to your Terminal
screen should look like

```python
# Total: 2
[east]
region=us-east-1
output=json

[west]
region=us-west-2
output=json
```

The first line in the template file uses a built-in filter called ``length``,
basically gets the length of the dictionary called ``regions``. You can do
some crazy creativity things with this, with some complex conditional
configurations.

Back to Ansible, since Ansible is written in Python, Ansible
just imports jinja2 library, and render the line
``apt: name={{ package_name }} update_cache=yes`` by
replacing ``package_name`` with the one under the ``vars`` block.

There are different places you can put variables, and the way
we are doing is what we called "in-line" / "embedded" variables
within a playbook.
