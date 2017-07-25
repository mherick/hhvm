#!/usr/bin/env python3

import contextlib
import json
import os
import re
import subprocess


class LspCommandProcessor:
    def __init__(self, proc):
        self.proc = proc

    @classmethod
    @contextlib.contextmanager
    def create(cls):
        # yes shell = True is generally a bad idea, but
        # in this case we want to pick up your environment entirely because
        # hack depends heavily on it to work
        proc = subprocess.Popen('hh_client lsp',
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        yield cls(proc)

        proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()

    def communicate(self, json_commands):
        transcript = {}

        notify_id = self._first_id()

        # send all the commands at once without reading anything
        for json_command in json_commands:
            self.send(json_command)

            id, notify_id = self._make_transcript_id(json_command, notify_id)

            transcript[id] = self._transcribe(json_command, None)

        # read responses for requests, skip notifications as they shouldn't
        # have responses
        for id in transcript:
            if not self.is_notify_id(id):
                transcript[id] = self._transcribe_receive(transcript[id]["sent"])

        return transcript

    def send(self, json_command):
        serialized = json.dumps(json_command)
        content_length = len(serialized)
        payload = f"Content-Length: {content_length}\n\n{serialized}"
        self._write(payload)

    def receive(self):
        return self._read()

    def parse_commands(self, raw_data):
        raw_json = json.loads(raw_data)
        return [self._eval_json(command) for command in raw_json]

    def is_notify_id(self, id):
        return id.startswith('NOTIFY_')

    def is_request_command(self, json_command):
        return 'id' in json_command

    def is_request_id(self, id):
        return id.startswith('REQUEST_')

    def _make_transcript_id(self, json_command, notify_id):
        id = ''

        if self.is_request_command(json_command):
            id = self._request_id_of(json_command)
        else:
            notify_id = self._next_id(notify_id)
            id = self._notify_id_of(notify_id)

        return id, notify_id

    def _transcribe_receive(self, json_command):
        return self._transcribe(json_command,
                                json.loads(self.receive()))

    def _transcribe(self, json_command, json_response):
        return {"sent": json_command,
                "received": json_response}

    def _next_id(self, id):
        return id + 1

    def _first_id(self):
        return 0

    def _notify_id_of(self, id):
        return 'NOTIFY_' + str(id)

    def _request_id_of(self, json_command):
        return 'REQUEST_' + str(json_command['id'])

    def _eval_json(self, json):
        if isinstance(json, dict):
            return {k: self._eval_json(v) for k, v in json.items()}
        elif isinstance(json, list):
            return [self._eval_json(i) for i in list]
        elif isinstance(json, str):
            match = re.match(r'>>>(.*)', json)
            if match is None:
                return json
            return eval(match.group(1))  # noqa: P204
        else:
            return json

    def _write(self, s):
        self.proc.stdin.write(s.encode())
        self.proc.stdin.flush()

    def _read_content_length(self):
        # read the 'Content-Length:' line and absorb the newline
        # after it
        length_line = self.proc.stdout.readline().decode()
        self.proc.stdout.read(len("\n\n"))

        # get the content length as an integer for the
        # rest of the package
        parts = length_line.split(":", 1)
        return (int(parts[1].strip()))

    def _read_content(self, length):
        return self.proc.stdout.read(length)

    def _read(self):
        length = self._read_content_length()
        return self._read_content(length)


# string replacement methods meant to be called
# within a command processing script.
def path_expand(path):
    return os.path.abspath(path)


def file_uri(path):
    return "file://" + path_expand(path)


def read_file(file):
    with open(file, "r") as f:
        return f.read()
