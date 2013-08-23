# -*- encoding=utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import StatusField
from model_utils import Choices, FieldTracker

class StatusNotSupportAction(Exception):
    pass

class StatusUndesirable(Exception):
    pass

class AuthorStatus(object):

    CODE = ""

    NAME = ""

    def review(self, author):
        raise StatusNotSupportAction()

    def activate(self, author):
        raise StatusNotSupportAction()

    def reject(self, author):
        raise StatusNotSupportAction()

    def appeal(self, author):
        raise StatusNotSupportAction()

    def __str__(self):
        return self.CODE

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.CODE)

    __unicode__ = __str__

class AuthorDraftStatus(AuthorStatus):

    CODE = "draft"

    NAME = _("Draft")

    def review(self, author):
        """ Draft --reivew--> Unactivated """
        author.status = author.STATUS.unactivated

class AuthorUnactivatedStatus(AuthorStatus):

    CODE = "unactivated"

    NAME = _("Unactivated")

    def activate(self, author):
        """ Unactivated --activate--> Activated """
        author.status = author.STATUS.activated

class AuthorActivatedStatus(AuthorStatus):

    CODE = "activated"

    NAME = _("Activated")

    def reject(self, author):
        """ Activated --reject--> Rejected """
        author.status = author.STATUS.rejected

class AuthorRejectedStatus(AuthorStatus):

    CODE = "rejected"

    NAME = _("Rejected")

    def recall(self, author):
        """ Rejected --recall--> Draft """
        author.status = author.STATUS.draft

    def appeal(self, author):
        """ Rejected --appeal--> Unactivated """
        author.status = author.STATUS.unactivated

class Author(models.Model):

    name = models.CharField(max_length=64)

    email = models.EmailField()

    phone = models.CharField(max_length=16, blank=True, null=True)

    _status = StatusField(db_column='status')

    STATUS = Choices(
        (AuthorDraftStatus(),
         AuthorDraftStatus.CODE, AuthorDraftStatus.NAME),
        (AuthorUnactivatedStatus(),
         AuthorUnactivatedStatus.CODE, AuthorUnactivatedStatus.NAME),
        (AuthorActivatedStatus(),
         AuthorActivatedStatus.CODE, AuthorActivatedStatus.NAME),
        (AuthorRejectedStatus(),
         AuthorRejectedStatus.CODE, AuthorRejectedStatus.NAME),
        )

    def get_status(self):
        return self.STATUS.__getattr__(str(self._status))

    def set_status(self, status):
        self._status = self.STATUS.__getattr__(str(status)).CODE

    status = property(get_status, set_status)

    def review(self):
        self.status.review(self)

    def activate(self):
        self.status.activate(self)

    def reject(self):
        self.status.reject(self)

    def recall(self):
        self.status.recall(self)

    def appeal(self):
        self.status.appeal(self)

    def __str__(self):
        return str(self.name)

    __unicode__ = __str__


class PackageStatus(object):

    # status code
    CODE = ""

    # status nice name
    NAME = ""

    def publish(self, package):
        raise StatusNotSupportAction()

    def review(self, package):
        raise  StatusNotSupportAction()

    def unpublish(self, package):
        raise  StatusNotSupportAction()

    def reject(self, package):
        raise  StatusNotSupportAction()

    def appeal(self, package):
        raise  StatusNotSupportAction()

    def __str__(self):
        return self.CODE

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.CODE)

    __unicode__ = __str__

    def __eq__(self, other):
        if isinstance(other, str):
            return self.CODE == other
        elif isinstance(other, self.__class__):
            return self.CODE == other.CODE
        else:
            return False

class PackageDraftStatus(PackageStatus):

    CODE = "draft"
    NAME = _("Draft")

    def review(self, package):
        """Draft --reivew--> Unpublished"""
        package.status = package.STATUS.unpublished

class PackageUnpublishedStatus(PackageStatus):

    CODE = "unpublished"
    NAME = _("Unpublished")

    def reject(self, package):
        """Unpublished --reject--> Rejected"""
        package.status = package.STATUS.rejected

    def publish(self, package):
        """Unpublished --publish--> Published"""
        package.status = package.STATUS.published

class PackagePublishedStatus(PackageStatus):

    CODE = 'published'
    NAME = _('Published')

    def reject(self, package):
        """published --reject--> Rejected"""
        package.status = package.STATUS.rejected

class PackageRejectedStatus(PackageStatus):

    CODE = "rejected"
    NAME = _("Rejected")

    def appeal(self, package):
        """Rejected --appeal--> Unpublished"""
        package.status = package.STATUS.unpublished

    def recall(self, package):
        """Rejected --recall--> Draft"""
        package.status = package.STATUS.draft

class Package(models.Model):

    title = models.CharField(max_length=128, null=False, default="", blank=True)

    package_name = models.CharField(max_length=128, null=False, default="", blank=True)

    summary = models.CharField(max_length=255, null=False, default="", blank=True )

    description = models.TextField(null=False, default="", blank=True, )

    author = models.ForeignKey(Author)

    released_datetime = models.DateTimeField(db_index=True, blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now_add=True, auto_now=True)

    """ ================== START State Design Pattern ====================== """

    STATUS = Choices(
        (PackageDraftStatus(),
             PackageDraftStatus.CODE,PackageDraftStatus.NAME),
        (PackagePublishedStatus(),
             PackagePublishedStatus.CODE, PackagePublishedStatus.NAME),
        (PackageUnpublishedStatus(),
             PackageUnpublishedStatus.CODE, PackageUnpublishedStatus.NAME),
        (PackageRejectedStatus(),
             PackageRejectedStatus.CODE, PackageRejectedStatus.NAME),
    )

    _status = StatusField(db_column="status", default=STATUS.draft)

    def get_status(self):
        return self.STATUS.__getattr__(str(self._status))

    def set_status(self, status):
        self._status = self.STATUS.__getattr__(str(status)).CODE

    status = property(get_status, set_status)
    """ ================== END State Design Pattern ======================== """

    """ START State Design Pattern Actions ======================== """
    def review(self):
        self.status.review(self)

    def publish(self):
        self.status.publish(self)

    def unpublish(self):
        self.status.unpublish(self)

    def reject(self):
        self.status.reject(self)

    def appeal(self):
        self.status.appeal(self)

    def recall(self):
        self.status.recall(self)
    """ END State Design Pattern Actions ======================== """

    tracker = FieldTracker()

    def __str__(self):
        return self.title

    __unicode__ = __str__

    def __init__(self, *args, **kwargs):
        super(Package, self).__init__(*args, **kwargs)

