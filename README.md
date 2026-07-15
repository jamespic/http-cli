HTTP-CLI
========

A simple CLI to make HTTP requests using the stdlib http.client module.

The main goal is to make it possible to make simple http requests from inside containers,
for example for health checks, without having to install any OS dependencies (and having
to deal with security alerts for those OS dependencies).

Usage
-----

http-cli [-h] [-X REQUEST] [-H HEADER] [-d DATA] [-v] [-o OUTPUT] [-k] [-t TIMEOUT] url

Barebones utility to make HTTP requests using the standard library http.client

positional arguments:
  url                   URL to make the request to

options:
  -h, --help            show this help message and exit
  -X REQUEST, --request REQUEST
                        HTTP method to use (default: GET)
  -H HEADER, --header HEADER
                        HTTP header to include in the request (can be specified multiple times)
  -d DATA, --data DATA  Data to include in the request body (for POST, PUT, etc.)
  -v, --verbose         Print verbose output (request and response headers)
  -o OUTPUT, --output OUTPUT
                        File to write the response body to (default: stdout)
  -k, --insecure        Allow insecure server connections when using SSL (ignore certificate verification)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for the request in seconds (default: 60)