# expodht
This is an exporter for DHT metrics. It uses pigpio to read the sensor. It is basically
the DHT example available on the pigpio's webpage coupled with Prometheus.

## Configuration variables
| Variable         | Description                                                      |
|------------------|------------------------------------------------------------------|
| GPIO_PIN         | Pin to use for readings                                          |
| INTERVAL_SECONDS | How many seconds to wait between readings                        |
| HTTP_PORT        | Port where the prometheus endpoint will bind to                  |
| HTTP_ADDR        | Address the prometheus endpoint will listen in                   |
| DUMMY_MODE       | Useful for testing in environments where pigpiod is not running. |

## Installation
Just run: `pip install git+https://github.com/crazybolillo/expodht.git`.

## Running
You can run it directly from the CLI with `expodht`. It is recommended to use a service file. For example:

```
[Unit]
Description=DHT22 metrics exporter

[Service]
User=monitoring
Environment="HTTP_ADDR=172.17.0.1"
WorkingDirectory=/home/monitoring
ExecStart=/home/monitoring/expodht/bin/expodht
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

The service file considers that `/home/monitoring/expodht` is the root folder for a python venv where expodht was
installed with the method listed above.
