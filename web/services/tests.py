# Create your tests here.
from rest_framework.test import APITestCase


class ViewsTest(APITestCase):
    def test_that_post_request_of_just_public_data_returns201(self):
        body = {
            "osReadable": "Mac OS 10.13.",
            "application": "mantidplot",
            "url": "http://localhost:8082/api/error/1",
            "uid": "0fec31b855cee2c550fef974eaf6dc52",
            "host": "9405be8af9e6d0a7f9c67e5ced27f674",
            "dateTime": "2018-08-31T12:52:13.755155Z",
            "osName": "Darwin",
            "osArch": "x86_64",
            "osVersion": "17.5.0",
            "ParaView": "0",
            "mantidVersion": "3.13.20180831.1025",
            "mantidSha1": "f4af35836cf4e89250d7e0db356cd6e9356737db",
            "facility": "ISIS",
            "exitCode": "",
            "upTime": "00:00:06.795771000"
        }

        url = '/api/error'
        response = self.client.post(url, body, format='json', secure=True)

        self.assertEqual(201, response.status_code)

    def test_that_post_request_with_empty_name_and_email_returns201(self):
        body = {
            "osReadable": "Mac OS 10.13.",
            "application": "mantidplot",
            "url": "http://localhost:8082/api/error/1",
            "uid": "0fec31b855cee2c550fef974eaf6dc52",
            "host": "9405be8af9e6d0a7f9c67e5ced27f674",
            "dateTime": "2018-08-31T12:52:13.755155Z",
            "osName": "Darwin",
            "osArch": "x86_64",
            "osVersion": "17.5.0",
            "ParaView": "0",
            "mantidVersion": "3.13.20180831.1025",
            "mantidSha1": "f4af35836cf4e89250d7e0db356cd6e9356737db",
            "facility": "ISIS",
            "exitCode": "",
            "upTime": "00:00:06.795771000",
            "name": "",
            "email": ""
        }

        url = '/api/error'
        response = self.client.post(url, body, format='json', secure=True)

        self.assertEqual(201, response.status_code)

    def test_that_post_request_with_name_and_email_returns201(self):
        body = {
            "osReadable": "Mac OS 10.13.",
            "application": "mantidplot",
            "url": "http://localhost:8082/api/error/1",
            "uid": "0fec31b855cee2c550fef974eaf6dc52",
            "host": "9405be8af9e6d0a7f9c67e5ced27f674",
            "dateTime": "2018-08-31T12:52:13.755155Z",
            "osName": "Darwin",
            "osArch": "x86_64",
            "osVersion": "17.5.0",
            "ParaView": "0",
            "mantidVersion": "3.13.20180831.1025",
            "mantidSha1": "f4af35836cf4e89250d7e0db356cd6e9356737db",
            "facility": "ISIS",
            "exitCode": "",
            "upTime": "00:00:06.795771000",
            "name": "public",
            "email": "public@email"
        }

        url = '/api/error'
        response = self.client.post(url, body, format='json', secure=True)

        self.assertEqual(201, response.status_code)

    def test_that_post_request_with_textbox_returns201(self):
        body = {
            "osReadable": "Mac OS 10.13.",
            "application": "mantidplot",
            "url": "http://localhost:8082/api/error/1",
            "uid": "0fec31b855cee2c550fef974eaf6dc52",
            "host": "9405be8af9e6d0a7f9c67e5ced27f674",
            "dateTime": "2018-08-31T12:52:13.755155Z",
            "osName": "Darwin",
            "osArch": "x86_64",
            "osVersion": "17.5.0",
            "ParaView": "0",
            "mantidVersion": "3.13.20180831.1025",
            "mantidSha1": "f4af35836cf4e89250d7e0db356cd6e9356737db",
            "facility": "ISIS",
            "exitCode": "",
            "upTime": "00:00:06.795771000",
            "textBox": "Explanatory text"
        }

        url = '/api/error'
        response = self.client.post(url, body, format='json', secure=True)

        self.assertEqual(201, response.status_code)

    def test_that_post_request_with_stacktrace_returns201(self):
        body = {
            "osReadable": "Mac OS 10.13.",
            "application": "mantidplot",
            "url": "http://localhost:8082/api/error/1",
            "uid": "0fec31b855cee2c550fef974eaf6dc52",
            "host": "9405be8af9e6d0a7f9c67e5ced27f674",
            "dateTime": "2018-08-31T12:52:13.755155Z",
            "osName": "Darwin",
            "osArch": "x86_64",
            "osVersion": "17.5.0",
            "ParaView": "0",
            "mantidVersion": "3.13.20180831.1025",
            "mantidSha1": "f4af35836cf4e89250d7e0db356cd6e9356737db",
            "facility": "ISIS",
            "exitCode": "",
            "upTime": "00:00:06.795771000",
            "textBox": "Explanatory text",
            "stacktrace": "This is what went wrong",
        }

        url = '/api/error'
        response = self.client.post(url, body, format='json', secure=True)

        self.assertEqual(201, response.status_code)
