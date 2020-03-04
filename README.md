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
You can skip this steps if you already have the requirements installed. Just make sure you specify the path to hammer 
in the parameter **hammer_cli_bin**.

Make sure you have the following packages installed:

``` text
git curl libssl-dev libreadline-dev zlib1g-dev autoconf bison build-essential libyaml-dev libreadline-dev libncurses5-dev libffi-dev libgdbm-dev
```

Install the needed requirements into bolt:

``` text
/opt/puppetlabs/bolt/bin/gem install --user-install hammer_cli_foreman
```

Find the installation diretory of the hammer cli bin (referenced as $INSTALL_DIR):

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
echo ":foreman:\n  :enable_module: true" > ~/.hammer/cli.modules.d/foreman.yml
chmod 600 ~/.hammer/cli.modules.d/foreman.yml
``` 

## Usage

The plugin supports looking up hosts managed via foreman through the command `hammer host lists.

Required fields:
-   `query`: Foreman Filter query for hosts. (Example: "managed=true")

Optional fields:
-   `server_url`: URL to access foreman (defaults to `''`)
-   `username`: Username to access foreman (defaults to `''`)
-   `password`: Password for foreman. Overrides pw_prompt. (defaults to `''`)
-   `per_page`: Limit results for the foreman search query (default to `1000`)
-   `page`: Show filter page (default to `1`)
-   `pw_prompt`: Securely ask for the foreman password? (default to `false`)
-   `hammer_cli_bin`: The binary path of the hammer (default to `~/.gem/ruby/2.5.0/bin/hammer`)

### Examples

Common usage:

Query foreman server and use a bolt pkcs7 secret as foreman password.

More information about bolt secrets:
https://puppet.com/docs/bolt/latest/using_plugins.html#secret-plugins

`inventory.yaml`
```yaml
groups:
  - name: foreman_hosts
    targets:
      - _plugin: foreman_inventory
        query: "os = CentOS and managed=true"
        server_url: "https://foreman.example.de/"
        username: 'username'
        password:
          _plugin: pkcs7
          encrypted_value: |
            <FOREMAN_PASSWORD_SECRET>        

```

Hammer is installed under `/usr/local/bin/hammer`. The file `~/.hammer/cli.modules.d/foreman.yml` contains the forman server_url, username and passord.
We also want to show the second half of 100 servers.

`inventory.yaml`
```yaml
groups:
  - name: foreman_hosts
    targets:
      - _plugin: foreman_inventory
        query: "os = CentOS and managed=true"
        hammer_cli_bin: '/usr/local/bin/hammer'
        per_page: 50
        page: 2
```

### Know Issues

CA Certificate for foreman server specified in `server_url` is missing:
```
Error executing plugin foreman_inventory from resolve_reference in foreman_inventory: SSL certificate verification failed
Make sure you configured the correct URL and have the server's CA certificate installed on your system.

You can use hammer to fetch the CA certificate from the server. Be aware that hammer cannot verify whether the certificate is correct and you should verify its authenticity after downloading it.

Download the certificate as follows:

  $ hammer --fetch-ca-cert https://foreman.example.de/
```

Solution:

Fetch the certificate with the hammer binary specified in `hammer_cli_bin`
```
~/.gem/ruby/2.5.0/bin/hammer --fetch-ca-cert https://foreman.example.de
```
