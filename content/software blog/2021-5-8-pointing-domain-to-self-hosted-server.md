Title: Pointing a Domain to a Self-hosted Server
Date: 2021-05-08
Modified: 2021-05-08
Category: blog
Tags: linux, ubuntuserver, selfhosting, nginx
Slug: pointing-domain-to-server
Authors: Charles Heckroth

This blog is a simple static site running on a computer in my home.

My domain from [namecheap](https://www.namecheap.com/) is pointing to the public IP of my home router.

Aside from this static site, some other things are accessible through my domain name, various private projects, slack webhooks, grafana, etc.

This post is a guide to setting this up, using:

- Namecheap (or any domain provider, but my specific setup is with namecheap)
- Nginx (for running multiple services behind the same domain)
- letsencrypt for SSL

# Network Setup

## Finding your Private and Public IP

## Port Forwarding

## Setting up LetsEncrypt

# Nginx / Web Setup

## With letsencrypt

## Pointing to a static site

## Reverse proxies for other stuff
