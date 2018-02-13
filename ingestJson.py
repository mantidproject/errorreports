#!/usr/bin/env python

import argparse
import json
from posixpath import join as urljoin
import requests


def receive_json(source, page_num):
    if args.verbose:
        print "Pulling data from " + source
    r = requests.get(source, params={'page': str(page_num), 'format': 'json'})
    if r.status_code == requests.codes.OK:
        if args.verbose:
            print "Received", r.content.__sizeof__(), "bytes from source."
        return r.content
    else:
        pass
        # error out


def post_json(data, destination):
    r = requests.post(destination, headers={
                      "Content-Type": "application/json"}, data=data)
    if r.status_code == requests.codes.CREATED:
        # if args.verbose:
        #    print "OK. Returned an HTTP 201 for Created."
        return 0
    else:
        # if args.verbose:
        #    print "Error. Response:", r.status_code
        return 1


def iterate_and_post(jsonData, apiSource):
    try:
        true_json = json.loads(jsonData)
    except:
        print "Failed to load JSON data."
        print "Have you tried removing slashes from the end of the URL?"
        return 1
    if args.verbose:
        print "Posting objects to", apiSource
    i = 0
    errors = 0
    for element in true_json["results"]:  # iterates over inner objects
        # json.dumps removes unicode
        errors += post_json(json.dumps(element), apiSource)
        i += 1
    if errors == 0:
        if args.verbose:
            print "Posted", i, "JSON objects to destination."
    else:
        if args.verbose:
            print "Attempted", i, "JSON posts, resulted with", \
                errors, "errors."
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=1,
                        dest='page_count',
                        help="number of pages to copy data from (defaults=1)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output")
    API_TYPES = ['usage', 'feature']
    parser.add_argument('-t', '--type', choices=API_TYPES, nargs='?',
                        default=API_TYPES[0],
                        help='Select which type to ingest '
                        '(default=%s)' % API_TYPES[0])
    FROM_DEFAULT = "http://reports.mantidproject.org/api/"
    parser.add_argument("source", type=str, nargs='?',
                        default=FROM_DEFAULT,
                        help="source URL of api from which to extract (GET)"
                        " JSON (default=%s)" % FROM_DEFAULT)
    TO_DEFAULT = "http://localhost:8000/api/"
    parser.add_argument("destination", type=str, nargs='?',
                        default=TO_DEFAULT,
                        help="destination URL for insertion (POST) of JSON "
                        "data (default=%s)" % TO_DEFAULT)
    args = parser.parse_args()
    errors = 0
    get_url = urljoin(args.source, args.type)
    post_url = urljoin(args.destination, args.type)
    page_count = args.page_count

    print 'copying data from', get_url, 'to', post_url

    for page in range(1, page_count + 1):
        if args.verbose:
            print
            print "Copying page", page
        data = receive_json(get_url, page)
        errors += iterate_and_post(data, post_url)
    if errors == 0:
        print "Done."
    else:
        print "The script exited with", errors, "errors."
