#!/usr/bin/env python3

import asyncio
import subprocess

from flask import Flask, jsonify, request
from flask_restful import Resource, Api


loop = asyncio.get_event_loop()
app = Flask(__name__, static_folder=None)
api = Api(app, catch_all_404s=True)

app.config.from_pyfile('.config')


async def run_shell_commands():
    directory = 'cd {}'.format(app.config['ANSIBLE_PLAYBOOK'])
    ansible = 'ansible-playbook frontend.yml'

    subprocess.call('{} && {}'.format(directory, ansible), shell=True)


class GithubEnpoint(Resource):
    def post(self):
        print('Got push with: {0}'.format(request.get_json()))
        message = {'message': 'Someone pushed a commit'}
        loop.run_until_complete(run_shell_commands())

        return jsonify(message)


api.add_resource(GithubEnpoint, '/push')


if __name__ == '__main__':
    app.run(port=6000, use_reloader=False)
