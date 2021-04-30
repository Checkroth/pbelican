Title: Setting up a Self-Hosted Server
Date: 2021-04-30
Modified: 2021-04-30
Category: blog
Tags: linux, ubuntuserver, selfhosting, plex, grafana, prometheus
Slug: self-hosted-server
Authors: Charles Heckroth
<!-- Summary: Introductory steps to getting an ubuntu server running in your home. -->

This post is mostly meant as a reminder to myself in case I'm in a position where I have to set it all up again.

Setting up a new server from scratch can be particularly annoying when you have to remember all of the minor configuration steps you figured out by trial-and-error. This is a record of some of those steps to make it easier for myself in the future, and for anybody else who might be interested.

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

If your network is unbroadcasted, add `scan_ssid=1` to the bottom of the network object you just created in `etc/wpa_supplicant.conf`.

If you want to go _only_ on WiFi, you may want to mark ethernet is optional in `/etc/netplan/00-installer-config.yaml`

My config looks like the following:

```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp8s0:
      optional: true
      dhcp4: true
  version: 2
  wifis:
    wlp6s0:
      access-points:
        "mywifiESSID":
          password: "mywifipassword"
      dhcp4: true
```

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

Your new ubuntu server should already be ssh-ready. Simply ensure that you are on the same local network as your server and then ssh to its private network IP address, or use the public IP if you aren't on the same network as the server.

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

You can either copy the link that this page takes you to, and paste it over in your server with `wget copiedlink`, or you can just scp. If you did the 「Going Remote」 section above, it should be as simple as:

- Download the latest version of plexmediaserver, something like `plexmediaserver_1.22.3.4392-d7c624def_amd64.deb`
- Copy the file to your server with `scp plexmediaserver_1.22.3.4392-d7c624def_amd64.deb dopeserver:`

Then you just install with dpkg on the server, `sudo dpkg -i plexmediaserver_1.22.3.4392-d7c624def_amd64.deb`.

You should be able to see plex running with `systemctl status plexmediaserver`, and you should be able to see it from your main computer using the private network IP address on port 32400, ` http://192.168.1.123:32400/`

## Metrics

For all parts below, keep the following in mind:

- For downloading you can use `wget` or you can download via browser and SCP as outlined under Plex.
- All the filenames/dates I'm using are of the current version at-time-of-writing. They may be different, please check the linked release pages.
- I am using the `/opt` directory just because I prefer it, as it helps be keep track of which services I am manually managing. Most guides will tell you to use `/etc` and that's fine too.
- I create a user for each service. This isn't strictly necessary.

### Node Exporter

Note: There are lots of other exporters. I recommend adding whatever piques your interest.

[Download node_exporter](https://prometheus.io/download/#node_exporter)

```
# Download, extract, move
wget https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz
tar -xzvf node_exporter-1.1.2.linux-amd64.tar.gz
sudo mv node_exporter-1.1.2.linux-amd64/node_exporter /opt/

# Set permissions
sudo useradd --no-create-home --shell /bin/false node_exporter
sudo chown node_exporter:node_exporter /opt/node_exporter
```

Next you want to make a systemd service for node exporter

Place the following in a new file: /etc/systemd/system/node_exporter.service

```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/opt/node_exporter --collector.systemd

[Install]
WantedBy=multi-user.target
```

And then run it:

```
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

You should now see node exporter on your local network ip at port 9100, `http://192.168.1.123:9100/`

### Prometheus

[Download prometheus](https://prometheus.io/download/)

```
# Download, extract, move
wget https://github.com/prometheus/prometheus/releases/download/v2.26.0/prometheus-2.26.0.linux-amd64.tar.gz
tar -xzvf node_exporter-1.1.2.linux-amd64.tar.gz
# This is renaming the folder, not putting the prometheus-2.26.0.linux-amd64 folder as a subfolder under /opt/prometheus/prometheus-2.26.0.linux-amd64.
sudo mv prometheus-2.26.0.linux-amd64 /opt/prometheus

# Set permissions
sudo useradd --no-create-home --shell /bin/false prometheus
sudo chown prometheus:prometheus /opt/prometheus
```

You really only need the `prometheus` and `prometheus.yml` files. But you can just move everything, its not that much.

Next you want to edit the yaml file you copied to include any targets you have added. I'll be including node exporter from the last step, as well as node exporter that I already have running on my main machine.

The main portion of this file is exactly what was in `prometheus.yml`, I have just added two scrape configs at the bottom.

```yaml
# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090']

  # These are the bits you add
  - job_name: 'dopeserver'
    static_configs:
    - targets: ['localhost:9100']
  - job_name: dopepersonalpc
    static_configs:
    - targets: ['192.168.1.124:9100']
```

Finally, you need a systemd service for this one too.

This goes in `/etc/systemd/system/prometheus.service`

```
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
WorkingDirectory=/opt
User=prometheus
Group=prometheus
Type=simple
ExecStart=/opt/prometheus \
    --config.file /opt/prometheus.yml

[Install]
WantedBy=multi-user.target
```

And, enable & start

```
sudo systemctl enable prometheus
sudo syetemctl start prometheus
```

You should now see node exporter on your local network ip at port 9090, `http://192.168.1.123:9090/`

### Grafana

You can install grafana enterprise. Its the same as the free version with the paywalled features in the package, but you can just leave those behind the paywall.

Following the Grafana installation guide:

```
echo "deb https://packages.grafana.com/enterprise/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana-enterprise
```

There may be a plugin there (it is for me, sometimes) that breaks grafana. You want to remove it (or move it to a persisted trash, just in case)

```
sudo mv /usr/share/grafana/plugins-bundled/gel-0.6.0/ ~/trash/
```

And enable & start

```
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

You should now see node exporter on your local network ip at port 3000, `http://192.168.1.123:3000/`

You may want to set the password or reconfigure. The configuraiton lives in `/etc/grafana/grafana.ini`.

[//]: TODO:: Add a link to the grafana-behind-reverse-proxy blog
You can change things like the port, admin_password, or setup SSL or a custom domain here. More details in a future post.

Now that you have grafana, prometheus, and node_exporter running, you'll want to set up your first dashboard.

In grafana, 
- add a data source for your local prometheus (you don't need the private network IP, just `0.0.0.0:9090`)
- Go to +(Create) -> Import -> Pop the Node Exporter Full dashboard in there: https://grafana.com/grafana/dashboards/1860

Now you should have real-time metrics for your server!

## Logging

### Promtail

Promtail is necessary to get your logs in to Loki and Grafana.

[Download promtail](https://github.com/grafana/loki/releases)

```
wget https://github.com/grafana/loki/releases/download/v2.2.1/promtail-linux-amd64.zip
7z x promtail-linux-amd64.zip
sudo mv promtail-linux-amd64 /opt/promtail
```

Promtail default configuration is kind of hard to come by. Mine looks like this, at /opt/promtail.yml:

```
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://127.0.0.1:3100/loki/api/v1/push

scrape_configs:
  - job_name: plex
    static_configs:
      - targets:
        - localhost
        labels:
          job: plex
          __path__: /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/*log
  - job_name: nginx
    pipeline_stages:
      - replace:
          expression: '(?:[0-9]{1,3}\.){3}([0-9]{1,3})'
          replace: '***'
    static_configs:
      - targets:
         - localhost
        labels:
          job: nginx_access_log
          host: canvas
          agent: promtail
          __path__: /var/log/nginx/*access.log
```

Note that my nginx access logs are set up to be compatible with [this dashboard](https://grafana.com/grafana/dashboards/12559)

And you need a service. This one doesn't have its own user group because it needs access to system logs.

The following would go in `/etc/systemd/system/promtail.service`

```
[Unit]
Description=Promtail
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecStart=/opt/promtail -config.file /opt/promtail.yml

[Install]
WantedBy=multi-user.target
```

### Loki

Grafana Loki is a nice way to get your logs from journalctl and plex in to Grafana, so you can play around with those. It will also be useful when you want to do more with your server in the future, like run a website or some application.

Following the grafana loki installation guide found [here](https://grafana.com/docs/loki/latest/installation/local/)

```
# Get and extract loki
curl -O -L "https://github.com/grafana/loki/releases/download/v2.2.1/loki-linux-amd64.zip"
unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 /opt/loki

# Get basic config
wget https://raw.githubusercontent.com/grafana/loki/master/cmd/loki/loki-local-config.yaml
sudo mv loki-local-config.yaml /opt/loki.yaml

# Set permissions
sudo chown prometheus:prometheus /opt/prometheus.yml
sudo chown prometheus:prometheus /opt/prometheus
```

I just use the default loki config with no changes.

Next, you need to add the service. I just share prometheus permissions with this one.

```
[Unit]
Description=Loki
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/opt/loki -config.file /opt/loki.yml

[Install]
WantedBy=multi-user.target
```

## Related Pages

I will come back and link to these when I write them.

- Hosting a static site / Pointing a domain to your self-hosted server
- Monitoring Everything In Your Home With Grafana/Prometheus
- Nginx and subpath proxy passes
- Exposing a development server through your locally hosted server
