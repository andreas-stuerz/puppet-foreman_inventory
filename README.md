# foreman_inventory

#### Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
    * [Install requirements](#install-requirements)
    * [Configure hammer-cli-foreman](#configure-hammer-cli-foreman)
3. [Usage](#usage)
    * [Examples](#examples)

## Description

This module includes a Bolt plugin to generate Bolt targets from foreman.

More information about foreman: https://theforeman.org/

## Requirements

* [hammer-cli](https://github.com/theforeman/hammer-cli)
* [hammer-cli-foreman](https://github.com/theforeman/hammer-cli-foreman)


### Install requirements
Make sure you have the following packages installed:

``` text
git curl libssl-dev libreadline-dev zlib1g-dev autoconf bison build-essential libyaml-dev libreadline-dev libncurses5-dev libffi-dev libgdbm-dev
```

For install the needed requirements into bolt:

``` text
/opt/puppetlabs/bolt/bin/gem install --user-install hammer_cli_foreman
```

Find the install diretory of the hammer cli bin (referenced as $INSTALL_DIR):

``` text
/opt/puppetlabs/bolt/bin/gem list -d hammer_cli_foreman | grep "Installed at"

 Installed at: ~/.gem/ruby/2.5.0
``` 

Make sure you can execute hammer under $INSTALL_DIR/bin/hammer:

``` 
~/.gem/ruby/2.5.0/bin/hammer
``` 

Use the above path for the parameter: **hammer_cli_bin**

### Configure hammer-cli-foreman
To enable and configure the foreman plugin execute the following steps:

``` 
mkdir -p ~/.hammer/cli.modules.d

for i in `gem contents hammer_cli|grep cli_config.template.yml`; do cp $i  ~/.hammer/.; done

mv ~/.hammer/cli_config.template.yml ~/.hammer/cli_config.yml

vi ~/.hammer/cli.modules.d/foreman.yml
[...]
:foreman:
  :enable_module: true
  :host: 'https://<FOREMAN_FQDN>/'
  :username: '<FOREMAN_USER>'
  :password: <FORMAN_PASSWORD>
[...]

chmod 600 ~/.hammer/cli.modules.d/foreman.yml

~/.gem/ruby/2.5.0/bin/hammer --fetch-ca-cert https://<FOREMAN_FQDN>/
``` 

## Usage

The plugin supports looking up hosts managed via foreman through the command "hammer host lists".

Required fields:
-   `query`: Foreman Filter query for hosts. (Example: "managed=true")

Optional fields:
-   `per_page`: Limit results for the foreman search query (default to `1000`)
-   `page`: Show filter page (default to `1`)
-   `pw_prompt`: Securely ask for the foreman password? (default to `false`)
-   `hammer_cli_bin`: The binary path of the hammer (default to `~/.gem/ruby/2.5.0/bin/hammer`)

### Examples

Common usage:

`inventory.yaml`
```yaml
groups:
  - name: foreman_hosts
    targets:
      - _plugin: foreman_inventory
        query: "os = CentOS and managed=true"

```

Hammer cli is installed globally under /usr/local/bin/hammer. 
The file ~/.hammer/cli.modules.d/foreman.yml has no password configured. So we want to ask for it each time.
We also want to show the second half of 100 servers.

`inventory.yaml`
```yaml
groups:
  - name: foreman_hosts
    targets:
      - _plugin: foreman_inventory
        query: "os = CentOS and managed=true"
        hammer_cli_bin: '/usr/local/bin/hammer'
        pw_prompt: true
        per_page: 50
        page: 2
```

