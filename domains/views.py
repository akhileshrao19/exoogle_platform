# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import CreateAPIView
from . import serializer as domains_serializer


class PeerLinkView(CreateAPIView):
    serializer_class = domains_serializer.PeerLinkSerializer


class UserView(CreateAPIView):
    serializer_class = domains_serializer.UserSerializer
