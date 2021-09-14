Title: Pointing a Domain to a Self-hosted Server
Date: 2021-05-08
Modified: 2021-05-08
Category: blog
Tags: linux, ubuntuserver, selfhosting, nginx
Slug: pointing-domain-to-server
Authors: Charles Heckroth
Status: Draft

This blog is a simple static site running on a computer in my home.

My domain from [namecheap](https://www.namecheap.com/) is pointing to the public IP of my home router.

Aside from this static site, some other things are accessible through my domain name, various private projects, slack webhooks, grafana, etc.

This post is a guide to setting this up, using:

- Namecheap (or any domain provider, but my specific setup is with namecheap)
- Nginx (for running multiple services behind the same domain)
- letsencrypt for SSL

# Network Setup

## Finding your Private and Public IP

Same process as outlined [in the private server setup]({filename}/2021-4-27-setting-up-a-self-hosted-server.md)

### [private](#private)

run `ifconfig`.

Ignore entires like `127.0.0.1`

Your private network IP address should be something like `192.168.1.123`.


### [public](#public)

Your public IP address will be necessary for a lot of things, most notable the following "Going Remote" step.

It can be surprisingly difficult to find your outgoing IPV4 address through cli tools, depending on your router/modem setup.

Just hit `curl https://ipinfo.io/ip` to get your public IP.


## Port Forwarding

You want to make sure your router is forwarding port 80 and 443 to the private IP found above. The process for this is different for every router.

Even if you don't want port 80 forwarded, you will need it at first to get SSL set up.

## Configuring your Domain

This step largely depends on your domain provider.

Following the steps for whever you get your domain, make an A record pointing to the *public* IP from above.

## Setting up LetsEncrypt

Basically just [this nginx post](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/).

Install certbot and the nginx plugin.

```
apt-get update
sudo apt-get install certbot
apt-get install python3-certbot-nginx
```

Make sure nginx is listening to port 80 on your domain name.

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    server_name mydopeserver.com www.mydopeserver.com;
}
```


# Nginx / Web Setup

## With letsencrypt

## Pointing to a static site

## Reverse proxies for other stuff

## SSL for Grafana

If you want to access grafana behind your nginx reverse proxy, through your domain name, over SSL, you will need to do some configuration on grafana itself.
