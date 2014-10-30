# -*- coding: utf-8 -*-
from datetime import timedelta
import math
from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.exceptions import Throttled
from rest_framework.throttling import UserRateThrottle, BaseThrottle, SimpleRateThrottle


class ScratchCardPlayDailyThrottle(UserRateThrottle):

    scope = 'scratch_card_play_daily'

    # 每天最多次数
    daily_max_times = 15

    # 5分钟间隔
    interval_seconds = 60 * 5

    # 间隔5次，等候间隔时间
    interval_times = 5

    def __init__(self, *args, **kwargs):
        super(ScratchCardPlayDailyThrottle, self).__init__(*args, **kwargs)
        self.previous_time = None
        self._cache = cache

    def get_rate(self):
        return "%d/day" % self.daily_max_times

    def parse_rate(self, rate):
        num, period = rate.split('/')
        num_requests = int(num)
        timenow = now().astimezone()
        next_datetime = (timenow + timedelta(days=1))\
            .replace(hour=0, minute=0, second=0, microsecond=0)
        duration = (next_datetime - timenow).seconds
        return (num_requests, duration)

    def wait(self):
        if self.daily_max_times == len(self.history):
            return None

        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        allow, wait_seconds = self.allow_next_interval()
        if not allow:
            return wait_seconds

        available_requests = self.num_requests - len(self.history) + 1

        return remaining_duration / float(available_requests)

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self._cache.get(self.key, [])
        self.now = self.timer()
        self.previous_time = self._cache.get("%s_previous" % self.key)
        allow, wait_seconds = self.allow_next_interval()
        if not allow:
            return False

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

    def make_request_history(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return

        self.history = self._cache.get(self.key, [])
        self.now = self.timer()

    def throttle_success(self):
        flag = super(ScratchCardPlayDailyThrottle, self).throttle_success()
        self._cache.set("%s_previous" % self.key, self.now, self.duration)
        return flag

    def allow_next_interval(self):
        if len(self.history) == 0 or not self.previous_time:
            return True, None

        if len(self.history) % self.interval_times == 0:
            wait_seconds = (self.previous_time + self.interval_seconds) - self.now
            if wait_seconds <= 0:
                return True, None
            else:
                return False, wait_seconds
        else:
            return True, None

    def check_allowed(self, request, view):
        self.make_request_history(request=request, view=view)
        allow, wait_seconds = self.allow_next_interval()
        if not allow:
            return False
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        return len(self.history) < self.num_requests


class ScratchCardPlayThrottled(Throttled):

    def __init__(self, wait=None, detail=None):
        self.wait = wait
        if wait is None:
            self.detail = "今天已经刮完了,明天再来吧~"
        else:
            #minutes = int(self.wait/60.0)
            #secoinds = int(self.wait)
            #self.detail = "%s%s后，又可以刮奖哦~" % (minutes or secoinds, '分钟' if minutes else '秒')
            minutes = math.ceil(self.wait/60.0)
            self.detail = "%s%s后，又可以刮奖哦~" % (minutes, '分钟')


class NaturalDayMixin(object):

    # 每天最多次数
    daily_max_times = 3

    def get_rate(self):
        return "%d/day" % self.daily_max_times

    def parse_rate(self, rate):
        num, period = rate.split('/')
        num_requests = int(num)
        timenow = now().astimezone()
        next_datetime = (timenow + timedelta(days=1)) \
            .replace(hour=0, minute=0, second=0, microsecond=0)
        duration = (next_datetime - timenow).seconds
        return (num_requests, duration)


class LotteryPlayDailyThrottle(NaturalDayMixin, UserRateThrottle):

    scope = 'lottery_play_daily'

    def __init__(self, *args, **kwargs):
        super(LotteryPlayDailyThrottle, self).__init__(*args, **kwargs)
        self._cache = cache

    def wait(self):
        if self.daily_max_times == len(self.history):
            return None

        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        available_requests = self.num_requests - len(self.history) + 1

        return remaining_duration / float(available_requests)

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self._cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

    def make_request_history(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return

        self.history = self._cache.get(self.key, [])
        self.now = self.timer()

    def check_allowed(self, request, view):
        self.make_request_history(request=request, view=view)
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        return len(self.history) < self.num_requests


class LotteryPlayThrottled(Throttled):

    detail = "今天抽奖次数已经用完了,明天再来吧~"

    def __init__(self, wait=None, detail=None):
        self.wait = wait
        if detail:
            self.detail = detail
