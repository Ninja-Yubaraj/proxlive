# proxlive

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-0.1.0-orange)
![Status](https://img.shields.io/badge/status-active-success)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![CLI](https://img.shields.io/badge/type-CLI-blueviolet)

Multi-threaded proxy checker that validates HTTP, HTTPS, SOCKS4, and SOCKS5 proxies.

## Try it NOW!

### Using pipx
```bash
pipx run proxlive -i proxies.json
```

### Using uv
```bash
uvx proxlive -i proxies.txt
```

## Features

- Multi-threaded checking
- Supports HTTP / HTTPS / SOCKS4 / SOCKS5
- Supports multiple input formats.
- Live progress stats.
- Timestamped output.

## Local Installation

### Using pipx (recommended for Python CLI tools)

```bash
pipx install proxlive
```

### Using uv

```bash
uv tool install proxlive
```

### Using pip (not recommended)

```bash
pip install proxlive
```

## Input Formats

### TXT format

```
http://140.227.61.201:3128
http://84.17.47.150:9002
socks4://72.195.114.184:4145
socks5://72.49.49.11:31034
```


### JSON format

```json
[
  {
    "proxy": "socks5://72.49.49.11:31034",
    "protocol": "socks5",
    "ip": "72.49.49.11",
    "port": 31034,
    "https": false,
    "anonymity": "transparent",
    "score": 1,
    "geolocation": {
      "country": "ZZ",
      "city": "Unknown"
    }
  }
]
```

✔ Output will preserve the exact structure for working proxies


## CLI Options

| Option          | Description                             |
| --------------- | --------------------------------------- |
| `-i, --input`   | Input file (.txt or .json)              |
| `-t, --threads` | Number of threads (default: 50)         |
| `--timeout`     | Request timeout in seconds (default: 5) |
| `-o, --output`  | Custom output file                      |

## Roadmap

- Retry mechanism
- Latency measurement & sorting
- Async engine
- Proxy geolocation validation
- Anonymity detection

## Author
Made with \:heart: by [Ninja-Yubaraj](https://github.com/Ninja-Yubaraj)


⭐ If you like this project, give it a star on GitHub!
