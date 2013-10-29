# -*- coding: utf-8 -*-
import sh
import os
import re

__author__ = 'me'

AAPT_CMD = None
def set_package_parser_exe(exe_path):
    global AAPT_CMD
    AAPT_CMD=exe_path

def get_package_parser_exe():
    global AAPT_CMD
    return AAPT_CMD

class PackageFileParser(object):

    _match_row_to_dict = dict(
        package=dict(pattern="package: name='(?P<package_name>[^']+)' "
                        "versionCode='(?P<version_code>[^']+)' "
                        "versionName='(?P<version_name>[^']+)'",
        ),
    )
    _match_row_to_list = dict(
        densities=dict(start_with="densities", type=int),
        locales=dict(start_with="locales", ),
        supports_screens=dict(start_with="supports-screens"),
    )
    _match_row_to_value = dict(
        sdk_version=dict(start_with="sdkVersion", type=int),
        target_sdk_version=dict(start_with="targetSdkVersion", type=int),
        max_sdk_version=dict(start_with='maxSdkVersion', type=int),
        native_code=dict(start_with='native-code', type=str),
    )
    _findall_row_to_dict = dict(
        application_labels=dict(pattern="application-label(-([^:]+))?:'([^']+)'",
                                dict_idx=(1, 2)
        ),
        application_icons=dict(pattern="application-icon(-([^:]+))?:'([^']+)'",
                               dict_idx=(1, 2)
        ),

        uses_implied_permissions=dict(
            pattern="uses-implied-permission:'([^']+)','([^']+)'",
            dict_idx=(0, 1)
        ),
        uses_implied_features=dict(
            pattern="uses-implied-feature:'([^']+)','([^']+)'",
                                dict_idx=(0, 1)
        ),
    )
    _findall_to_list = dict(
        uses_permissions=dict(pattern="uses-permission:'([^']+)'"),
        uses_features=dict(pattern="uses-feature:'([^']+)'"),
    )

    def __init__(self, filename):
        assert os.path.isfile(filename)
        self._filename = filename
        aapt_cmd_path = get_package_parser_exe()
        if aapt_cmd_path:
            sh.aapt = sh.Command(aapt_cmd_path)

        self._profile_data = dict()
        self._profile_text = None
        self._profile_dict_keys = []
        self._prepare_to_profile_keys()

    def _prepare_to_profile_keys(self):
        keys = list(self._match_row_to_dict.keys())
        keys.extend(self._match_row_to_value.keys())
        keys.extend(self._match_row_to_list.keys())
        keys.extend(self._findall_row_to_dict.keys())
        keys.extend(self._findall_to_list.keys())
        self._profile_dict_keys = keys

    def __getattr__(self, key):
        if not self.has_profile_attr(key):
            raise AttributeError("No profile %s in Parser"%key)

        if not self.is_parsed():
            self.parse_to_profile()

        return self._profile_data[key]

    def has_profile_attr(self, key):
        return key in self._profile_dict_keys

    def is_parsed(self):
        return len(self._profile_data) > 0

    def parse_to_profile(self):
        self._profile_text = self.badging_text()

        text_splited = self._profile_text.split("\n")
        first_line = text_splited[0]
        self._parse_package(first_line)

        for key, matcher in self._findall_row_to_dict.items():
            self._parse_findall_row_to_dict(key, matcher, self._profile_text)

        for key, matcher in self._findall_to_list.items():
            self._parse_findall_to_list(key, matcher, self._profile_text)

        del text_splited[0]
        for key, matcher in self._match_row_to_value.items():
            self._parse_row_to_value(key, matcher, text_splited)

        for key, matcher in self._match_row_to_list.items():
            self._parse_row_to_list(key, matcher, text_splited)

    def badging_text(self):
        aapt = sh.aapt
        result = aapt('d', 'badging', self._filename)
        #result.call_args['encoding'] = sys.getdefaultencoding()
        return str(result)

    def _parse_package(self, row_text):
        pattern = self._match_row_to_dict.get('package').get('pattern')
        m = re.match(pattern, row_text)
        package=m.groupdict()
        package['version_code'] = int(package.get('version_code'))
        self._profile_data.update(dict(package=package))

    def _parse_row_to_value(self, key, matcher, lines):
        start_with = matcher.get('start_with')
        _type = matcher.get('type')
        val = None
        for row in lines:
            if row.startswith(start_with):
                _part2 = row.split(':')[1]
                val = _part2.lstrip(" ").strip("'")
                val = _type(val)
                break

        self._profile_data.update({key:val})

    def _parse_findall_row_to_dict(self, key, matcher, text):
        res = re.findall(matcher.get('pattern'), text)
        dict_idx = matcher.get('dict_idx')
        dict_vals= dict()
        for row in res:
            dict_vals[row[dict_idx[0]]] = row[dict_idx[1]]

        self._profile_data.update({key: dict_vals})

    def _parse_findall_to_list(self, key, matcher, text):
        res = re.findall(matcher.get('pattern'), text)
        self._profile_data.update({key: res})

    def _parse_row_to_list(self, key, matcher, lines):
        start_with = matcher.get('start_with')
        _type = matcher.get('type', str)
        vals = None
        for row in lines:
            if row.startswith(start_with):
                part2 = row.split(":")[1].lstrip(" ")
                vals = map(lambda e: _type(e.strip("'")), part2.split(" "))
        self._profile_data.update({key: list(vals)})

    def fetch_file(self, resource_filename, to_path):
        # unzip popup to confirm next action when file duplication
        # it wait to user interactive, use noui input stream
        def replace_confirm_interact(line, stdin, process):
            stdin.put('y', timeout=3)
            return True

        sh.unzip(self._filename,
                 resource_filename,
                 d=to_path,
                 _out=replace_confirm_interact)
        # wait for unzip file
        import time
        time.sleep(1)
        return os.path.join(to_path, resource_filename)
