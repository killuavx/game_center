# -*- coding: utf-8 -*-

class FeedbackActionException(Exception):
    pass


class RequestProcessException(Exception):
    pass


class NotDefineOperationError(Exception):
    pass


class StaticContentTypeError(Exception):
    pass


class WorkingDirectoryNotFound(Exception):
    pass