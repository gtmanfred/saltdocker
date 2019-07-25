# Supported tags and respective `Dockerfile` links

- [`2019.2.0`, `2019.2`, `latest`](https://github.com/saltstack/saltdocker/tree/master/Dockerfile.j2)
- [`2018.3.4`, `2018.3`](https://github.com/saltstack/saltdocker/tree/master/Dockerfile.j2)

# What is SaltStack?

SaltStack is a configuration management tool / orchestration platform.

This image contains a running salt-master and salt-api process, which can be used to control other salt-minions.

![logo](https://avatars2.githubusercontent.com/u/1147473?s=500&v=4)

# How to use this image

## start a salt instance

```console
$ docker run --name salt --hostname salt -P -e SALT_SHARED_SECRET=mysecretpassword -d saltstack/salt
```

The default `salt` user is created but the shared secret is specified in the `/etc/salt/master.d/api.conf`.

The api listens on port `8000` with `ssl` enabled.

# How to extend this image

There are many ways to extend the `salt` image. Without trying to support every possible use case, here are just a few that we have found useful.

## Environment Variables

The SaltStack image uses several environment variables which are easy to miss. While none of the variables are required, they may significantly aid you in using the image.

### `SALT_MASTER_CONFIG`

A JSON object. This variable is dumped to /etc/salt/master.d/master.conf and can be used to provide extra config for the salt master.

### `SALT_API_CONFIG`

A JSON object. This variable is dumped to /etc/salt/master.d/api.conf, and defaults to the following.

```yaml
rest_cherrypy:
  port: 8000,
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/certs/localhost.key
external_auth:
    sharedsecret:
        salt: ['.*', '@wheel', '@jobs', '@runner']
sharedsecret: $SALT_SHARED_SECRET
```

### `SALT_SHARED_SECRET`

If this environment variable is set, it will set the sharedsecret variable for using the salt-api with the salt user.

## Salt Wheel Modules

If the salt-master is not configured immediately at the start, the master config can be updated using wheel modules via the salt api using the [Salt Config Wheel Module](https://docs.saltstack.com/en/latest/ref/wheel/all/salt.wheel.config.html)

## Volumes for Salt Keys

In order to make volumes available to the `salt` user in the container, assign the group id `450` to the directory before it mounting it on the container.
