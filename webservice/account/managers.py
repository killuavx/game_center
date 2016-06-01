# -*- coding: utf-8 -*-
from django.contrib.auth.models import UserManager as UserBaseManager, Group, AnonymousUser
from django.db.models import Q
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager


class UserQuerySet(QuerySet):
    def by_profile_with(self, **kwargs):
        kwargs = {('gamecenter_profile__%s' % qf): qv for qf, qv in
                  kwargs.items()}

        return self.filter(
            **kwargs
        )

    def published(self):
        return self.filter(is_active=True)

    def get_by_appbind(self, app, uid):
        return self.get(
            appbinds__app=app,
            appbinds__uid=uid,
        )


class UserManager(UserBaseManager, PassThroughManager):
    def create_user(self,
                    username,
                    email=None,
                    phone=None,
                    password=None,
                    **extra_fields):
        from account.models import Profile
        user = super(UserManager, self).create_user(username=username,
                                                    password=password,
                                                    **extra_fields)
        group_player, _is_new = Group.objects.get_or_create(name='player')
        user.groups.add(group_player)
        Profile.objects.create(user=user,
                               email=email,
                               phone=phone)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = super(UserManager, self).create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class ProfileManager(PassThroughManager):

    def get_visible_profiles(self, user=None):
        """
        Returns all the visible profiles available to this user.

        For now keeps it simple by just applying the cases when a user is not
        active, a user has it's profile closed to everyone or a user only
        allows registered users to view their profile.

        :param user:
            A Django :class:`User` instance.

        :return:
            All profiles that are visible to this user.

        """
        profiles = self.all()

        filter_kwargs = {'user__is_active': True}

        profiles = profiles.filter(**filter_kwargs)
        if user and isinstance(user, AnonymousUser):
            profiles = profiles.exclude(Q(privacy='closed') | Q(privacy='registered'))
        else: profiles = profiles.exclude(Q(privacy='closed'))
        return profiles


class UserAppBindManager(PassThroughManager):

    def all_appbinds(self, app):
        return self.all().filter(app=app)

    def get_appbind(self, app, uid):
        return self.all().filter(app=app, uid=uid)
