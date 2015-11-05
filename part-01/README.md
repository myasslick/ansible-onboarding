# Part 1

## Introducing Ansible

Ansible is a configuration management tool written in Python, a young but well-established
rivial to Chef and Puppet.

For tooling, Ansible's transport layer is the SSH protocol. By default, Ansible is agentless.
With the proper security credential, Ansible can connect with the remote (or local)
instance, execute the tasks on the remote host, and return the result. There is no
single point of failure unless an external service is paired with Ansible.

For syntax, unlike Puppet or Chef, there is no special DSL. Ansible's configuration
files follows the [YAML](http://yaml.org/) syntax, and files can be templated
using the popular [Jinja2](http://jinja.pocoo.org) template language.

Ansible is battery-included, with over a hundred of [modules](http://docs.ansible.com/ansible/modules_by_category.html)
users can start managing servers and configuring applications quickly. For example, you can
use Ansible to create an EC2 instance with the specification of your like using the
[ec2](http://docs.ansible.com/ansible/ec2_module.html) module, and when the instance is created
you can use the [mail](http://docs.ansible.com/ansible/mail_module.html) module
to notify yourself. The permutation of creativity is unlimited with Ansible and
Ansible's extensibility.

## Getting Ansible

This tutorial assumes that you are working with a Mac OSX computer. Linux and Windows (get ``git-bash``)
can still benefit from this tutorial more or less.

### install ansible

[Ansible Installation](http://docs.ansible.com/ansible/intro_installation.html)
is the best source. I am a developer so I am used to getting things with ``pip`` (Python
package manager), and ``virtualenv`` (Python's package "sandbox").

Here I called my virtualenv ``python-env``. You can name it anything you want.

```bash
virtualenv python-env
pip install ansible
```

If you don't have ``virtualenv`` or ``pip`` yet, use ``homebrew`` to install the missing tool.
In fact, you can also use ``homebrew`` to install Ansible.


### create EC2

The lab instance should have been created for you. Later we will have a lab for creating
EC2 instances using Ansible. For now, please have your EC2 key ready in ``$HOME/.ssh/``
directory.

Then edit the file ``inventory`` with the IP address of your EC2 instance.

### running playbook

Let's actually run something with Ansible!

```bash
ansible-playbook -i inventory playbook.yml --user ubuntu --private-key ~/.ssh/KEY_NAME
```

This playbook ``playbook.yml`` is a YAML-syntax configuration file, and has two tasks
to execute on the remote host.

The first task is to use the [``apt``](http://docs.ansible.com/ansible/apt_module.html)
module to update the APT cache. This is usually required so the ``apt`` module
can fetch packages successfully. The second task will install ``git``.

If you read the ``apt`` module page, you will see a table describes the various
options available. Each module documentation page usually come with a section
with examples for reference.

Look closely, you can tell that we can optimize our playbook. First, the default value
for ``state`` is already ``present`` in the module, and ``state`` is an optional unless
you want the package to not be installed (``state=absent``), or if you want
to always grab the latest version from Ubuntu's repository. If you want a specific version,
you can do ``name=PACKAGE_NAME=VERSION``.

So we can actually rewrite our tasks like this:

```yaml
    - name: Run apt-get update
      apt: update_cache=yes

    - name: Install git
      apt: name=git
```

Next optimization is to combine the two tasks together. Ansible
knows to run ``apt-get update`` before ``apt-get install PACKAGE``
when you specify ``apt: name=git update_cache=yes``.

So the final playbook, after two optimizations, will look like this:

```yaml
- hosts: all
  tasks:
    - name: Run apt-get update
      apt: update_cache=yes

    - name: Install git
      apt: name=git state=present
```

If you re-run this again, the playbook will finish quicker and Ansible
will also report no change, because ``git`` has already been installed.
Of course, if you think constantly updating the APT cache is a bad thing
(especially for your own private repository), you can use
``cache_valid_time`` in seconds to skip upating cache.

Now, try to play around with this playbook. We have more stuff to play
with in the next few lessons.
