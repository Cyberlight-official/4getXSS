# 4getXSS

**4getXSS** is a powerful and fast Cross-Site Scripting (XSS) vulnerability scanner that uses Selenium WebDriver to automatically detect and report potential XSS vulnerabilities on target websites.

It supports concurrent scanning of multiple URLs and payload injection to identify reflected, stored, and DOM-based XSS vulnerabilities.

## Features

- **Multi-threaded scanning** for faster vulnerability detection.
- **WebDriver pooling** for optimized resource management.
- **Alert-based detection** of XSS vulnerabilities.
- **HTML report generation** with scan results.
- **Customizable payload list** to detect different types of XSS attacks.
- **Timeout settings** for controlling the scan process.

## Requirements

Before running the tool, you need to install the following dependencies:

- Python 3.x
- **Selenium** for browser automation
- **Requests** for making HTTP requests
- **Webdriver Manager** to automatically download the required browser drivers
- **Colorama** for colored output in the terminal

Install the required packages with the following command:

```bash
pip install -r requirements.txt
