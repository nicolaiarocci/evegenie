"""
EveGenie class for building Eve settings and schemas.
"""
import json
import os.path

from jinja2 import Environment, PackageLoader


class EveGenie(object):

    template_env = Environment(loader=PackageLoader('evegenie', 'templates'))

    def __init__(self, data=None, filename=None):

        if filename and not data:
            if os.path.isfile(filename):
                with open(filename, 'r') as ifile:
                    data = ifile.read().strip()

        if not isinstance(data, (basestring, dict)):
            raise TypeError('Input is not a string: {}'.format(data))
            sys.exit(1)

        if isinstance(data, basestring):
            data = json.loads(data)

        schema_source = data
        for endpoint in schema_source:
            setattr(self, endpoint, self.parse_endpoint(schema_source[endpoint]))

    def parse_endpoint(self, endpoint_source):
        schema = {}
        for k, v in endpoint_source.iteritems():
            item = {'type': self.get_type(v)}
            if item['type'] == 'dict':
                item['schema'] = {}
                for i in v:
                    item['schema'][i] = {'type': self.get_type(v[i])}
            schema[k] = item

        return schema

    def get_type(self, source_type):
        if isinstance(source_type, basestring):
            eve_type = 'string'
        elif isinstance(source_type, int):
            eve_type = 'integer'
        elif isinstance(source_type, float):
            eve_type = 'float' # this could also be 'number'
        elif isinstance(source_type, dict):
            eve_type = 'dict'
        elif isinstance(source_type, list):
            eve_type = 'list'
        elif isinstance(source_type, bool):
            eve_type = 'boolean'

        return eve_type

    def write_file(self, filename):
        template = self.template_env.get_template('settings.py.j2')
        settings = template.render(
            schema=self.__dict__,
        )
        with open(filename, 'w') as ofile:
            ofile.write(settings)

    def __str__(self):
        return json.dumps(self.__dict__)