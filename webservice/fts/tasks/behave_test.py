# -*- coding: utf-8 -*-
import behave
import behave.configuration
from django_jenkins.tasks.behave_tests import (testCaseFactory,
                                               get_features,
                                               get_app,
                                               Task as BehaveBaseTask)


def make_test_suite(features_dir, app_label):
    DjangoBehaveTestCase = testCaseFactory(app_label)

    class DjangoBehaveTestCaseFix(DjangoBehaveTestCase):
        def __init__(self, features_dir):
            behave_config = behave.configuration.Configuration()
            super(DjangoBehaveTestCaseFix, self).__init__(features_dir)
            self.behave_config.stdout_capture = behave_config.stdout_capture
            self.behave_config.stderr_capture = behave_config.stderr_capture

    return DjangoBehaveTestCaseFix(features_dir=features_dir)


class Task(BehaveBaseTask):
    def build_suite(self, suite, **kwargs):
        for label in self.test_labels:
            if '.' in label:
                print("Ignoring label with dot in: %s" % label)
                continue
            app = get_app(label)

            # Check to see if a separate 'features' module exists,
            # parallel to the models module
            features_dir = get_features(app)
            if features_dir is not None:
                # build a test suite for this directory
                features_test_suite = make_test_suite(features_dir, label)
                suite.addTest(features_test_suite)

