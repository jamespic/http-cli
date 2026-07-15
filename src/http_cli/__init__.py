import sys
from argparse import ArgumentParser
from collections.abc import Iterable
from http.client import HTTPConnection, HTTPSConnection
from ssl import _create_unverified_context
from urllib.parse import urlsplit


def main(argv: Iterable[str] | None = None) -> int:
    argparser = ArgumentParser(
        description="Barebones utility to make HTTP requests using the standard library http.client"
    )
    argparser.add_argument(
        "-X",
        "--request",
        default="GET",
        help="HTTP method to use (default: GET)",
    )
    argparser.add_argument(
        "-H",
        "--header",
        action="append",
        help="HTTP header to include in the request (can be specified multiple times)",
    )
    argparser.add_argument(
        "-d",
        "--data",
        help="Data to include in the request body (for POST, PUT, etc.)",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output (request and response headers)",
    )
    argparser.add_argument(
        "-o",
        "--output",
        help="File to write the response body to (default: stdout)",
        default="-",
    )
    argparser.add_argument(
        "-k",
        "--insecure",
        action="store_true",
        help="Allow insecure server connections when using SSL (ignore certificate verification)",
    )
    argparser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=60,
        help="Timeout for the request in seconds (default: 60)",
    )
    argparser.add_argument("url", help="URL to make the request to")

    args = argparser.parse_args(argv)

    url_parts = urlsplit(args.url, scheme="http", allow_fragments=False)

    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()

    path = url_parts.path or "/"
    if url_parts.query:
        path += "?" + url_parts.query

    match url_parts.scheme:
        case "http":
            conn = HTTPConnection(url_parts.netloc, timeout=args.timeout)
        case "https":
            if args.insecure:
                conn = HTTPSConnection(
                    url_parts.netloc,
                    context=_create_unverified_context(),
                    timeout=args.timeout,
                )
            else:
                conn = HTTPSConnection(url_parts.netloc, timeout=args.timeout)
        case _:
            print(f"Unsupported URL scheme: {url_parts.scheme}")
            return 1

    try:
        if args.verbose:
            print(f"> {args.request} {path} HTTP/1.1", file=sys.stderr)
            for key, value in headers.items():
                print(f"> {key}: {value}", file=sys.stderr)
            if args.data:
                print(f"> {args.data}", file=sys.stderr)

        conn.request(args.request, path, body=args.data, headers=headers)
        response = conn.getresponse()
        if args.verbose:
            print(
                f"< HTTP/{response.version / 10:.1f} {response.status} {response.reason}",
                file=sys.stderr,
            )
            for key, value in response.getheaders():
                print(f"< {key}: {value}", file=sys.stderr)

        content_length = response.getheader("Content-Length")
        if content_length is not None:
            content_length = int(content_length)
            body = response.read(content_length)
        else:
            body = response.read()

        if args.output == "-":
            sys.stdout.buffer.write(body)
        else:
            with open(args.output, "wb") as f:
                f.write(body)

        return 0 if response.status < 400 else 1
    finally:
        conn.close()
