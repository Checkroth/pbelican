Title: Setting up a Self-Hosted Server
Date: 2021-04-27
Category: blog
Tags: linux, ubuntuserver, selfhosting, plex, grafana, prometheus
Slug: self-hosted-server
Authors: Charles Heckroth
Summary: Introductory steps to getting an ubuntu server running in your home.
Status: Draft

This post is mostly meant as a reminder to myself in case I'm in a position where I have to set it all up again.

# Requirements and Outline

## Tools used

1) A computer

I built this: https://pcpartpicker.com/user/checkroth/saved/#view=cThqmG

But you could really use anything.

2) 2 USB thumb drives at least 4GB each.

2.a One Should have [ubuntu server](https://ubuntu.com/download/server) installation medium.

2.b The other should have a [live usb](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview). This is generally useful if you run in to trouble at any point.

## Overall Process

The simple steps overview is:

1. Build a computer
2. Partition and format your hardrive either with a live usb or from the server installer
3. Install ubuntu server
4. Set up networking
5. Set up desired software (plex, grafana, etc.)

# System Setup

## Preparation

My goal was primarily to have a plex server to serve my music and video collection that's been bouncing between various storage and streaming services for the past ten years.

As such, my server required a lot of space, but I wanted to keep the operating system itself separate from the server. So I made a ~120GB partition in my 2TB hard drive using [gparted](https://gparted.org/) off of my live usb. The rest is formatted to simply store plex media.

I recommend doing something similar to this if you have a lot of storage space, as eventually you will want to [move your operating system](https://askubuntu.com/a/741727/509039), and having just the essentials during that process makes things a lot easier. 

## Installation

Make sure you have an ethernet connection before starting, even if you ultimately want to use Wi-Fi
Straightforward. Boot from the ubuntu server install usb and follow the interactive steps.

## Networking

In case you have a wifi card on your server, the following must be done

Install wpa_supplicant, and then register your wifi:

`wpa_passphrase ESSID passphrase | sudo tee /etc/wpa_supplicant.conf`

where ESSID is the name of your wifi network. This is the name of the network when you connect on any device, like your phone. If you don't have such a device available you can list them with the following steps:

- install network-manager with `apt install network-manager`
- run `nmcli dev wifi`

Finally, if your network is unbroadcasted, add `scan_ssid=1` to the bottom of the network object you just created in `etc/wpa_supplicant.conf`.

## Finding your IPv4

### private

run `ifconfig`.

Ignore entires like `127.0.0.1`

Your private network IP address should be something like `192.168.1.123`.


### public

Your public IP address will be necessary for a lot of things, most notable the following "Going Remote" step.

It can be surprisingly difficult to find your outgoing IPV4 address through cli tools, depending on your router/modem setup.

Just hit `curl https://ipinfo.io/ip` to get your public IP.

## Going Remote

If you're anything like me, the first thing you'll want to do once your server is running is... stop interacting with your server directly.

Your new ubuntu server should already be ssh-ready. Simply ensure that you are on the same local network as your server and then ssh to its private network IP address.

You need the username you created when spinning up your server.

```
ssh myserveradmin@192.168.1.123
```

If that works, exit back to your host machine and run

```
ssh-copy-id  myserveradmin@192.168.1.123
```

And now you should be able to access your server over SSH from your local network without a password!

### Making it even easier

If you gave a name to your new server as many nerds are want to do, you might want to be able to communicate with it with just that name!

Assuming my server user name is `myserveradmin` from above, and you named your server `DopeServer`, add the following to your host's `~/.ssh/config`

```
Host dopeserver
    User myserveradmin
	HostName 192.168.1.123
```

Now you can get in with just `ssh dopeserver`

# Software

Details for how to set up my most heavily used software packages for the new server.

## Plex

Download [plexmediaserver](https://www.plex.tv/media-server-downloads/).

You can either copy the link that this page takes you to, and paste it over in your server with `wget copiedlink`, or you can just scp. If you Did the 「Going Remote」 section above, it should be as simple as:

- Download the latest version of plexmediaserver, something like `plexmediaserver_1.22.3.4392-d7c624def_amd64.deb`
- Copy the file to your server with `scp plexmediaserver_1.22.3.4392-d7c624def_amd64.deb dopeserver:`



## Metrics

## Logging

## Other uses

# Related Pages

- Pointing a domain to your self-hosted server
- Monitoring Everything In Your Home With Grafana/Prometheus
- Nginx and subpath proxy passes
- Exposing your development server through your locally hosted server
