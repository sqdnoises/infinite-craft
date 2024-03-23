---
description: Interacting with the infinite-craft Command Line Interface (or CLI).
---

# 💻 Command Line Interface (CLI)

When you install Two CLI apps are installed. `infinite-craft` and `infinitecraft`.\
You can use either, both do the exact same thing.

## Display help

To view the help page of the CLI, use the `-h`or `--help` tag.

```
infinite-craft --help
```

## Reset `discoveries.json`

You can reset your `discoveries.json` file to its initial 4 elements using the command below

```
infinite-craft reset -d "/path/to/discoveries.json"
```

## Run Mock API

You can start a mock API on your device using the command below.

```
infinite-craft mock
```

{% hint style="info" %}
The mock API listens on `127.0.0.1` (aka `localhost`) on port `8080`.
{% endhint %}

### Customize Mock API

You can also start it at a custom host and port.

```
infinite-craft mock --host 0.0.0.0 --port 80
```

***

**NOTE:** If `infinite-craft` or `infinitecraft` is not on PATH, you can use:

* `python3 -m infinite-craft` (for Linux/MacOS)
* `python -m infinite-craft` (for Windows)

Same with `infinitecraft`.
