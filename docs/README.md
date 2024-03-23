---
description: Introduction of sqdnoises' infinite-craft Python library.
cover: .gitbook/assets/cover.png
coverY: 0
layout:
  cover:
    visible: true
    size: full
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# 📖 Introduction

infinite-craft is an **API Wrapper** of [Neal's Infinite Craft game](https://neal.fun/infinite-craft) in **Python** for people to implement in their programs.

[**View `infinite-craft` on PyPI.**](https://pypi.org/project/infinite-craft/)

## Key Features

* Stores elements in a neatly indented JSON file
* Starts with the four main elements: Water, Fire, Wind, Earth
* Uses [`neal.fun`](https://neal.fun/)'s [Infinite Craft](https://neal.fun/infinite-craft/) API to pair elements together
* Built-in ratelimiting handler
* Custom API support
* Asynchronous library
* Conveniently access discovered elements

{% hint style="info" %}
Do you have any issues or problems? Join our [Discord server](https://discord.gg/sAecE3YVEe) to get help or [make a GitHub issue](https://github.com/sqdnoises/infinite-craft/issues/new).
{% endhint %}

## How does it work?

This library basically contacts the URL:\
[https://neal.fun/api/infinite-craft/pair?first=element+name\&second=element+name](https://neal.fun/api/infinite-craft/pair?first=element+name\&second=element+name)\
Tricks it with some headers, and handles everything accordingly.

Everything is handled in a user-friendly manner and asynchronously, so it should be really easy to use it in your programs.

{% hint style="info" %}
Want to contribute? Make a pull request at [infinite-craft's GitHub repository](https://github.com/sqdnoises/infinte-craft)!
{% endhint %}

## License

[![](https://img.shields.io/badge/LICENSE-MIT-red?style=for-the-badge\&labelColor=black)](LICENSE/)\
_View the_ [_**MIT License**_](LICENSE/) _license that comes with this library._

***

🌟 Please star the [GitHub repo](https://github.com/sqdnoises/infinite-craft/stargazers) and show some love 💖
