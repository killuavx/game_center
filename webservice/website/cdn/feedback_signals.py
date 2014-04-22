# -*- coding: utf-8 -*-
from django.dispatch import Signal
start_action = Signal(providing_args=["instance", "operation", "queue"])
start_model_action = Signal(providing_args=["instance", "operation", "queue"])
