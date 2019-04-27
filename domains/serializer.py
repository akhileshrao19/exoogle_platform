from urllib.parse import urlparse

from rest_framework import serializers as rest_serializer

from .models import UserLink, PeerLink, RawUserData

from ipware import get_client_ip


class ValidateDomain(object):
    def validate_domain(self, domain):
        url = urlparse(domain).netloc
        if url is None:
            raise rest_serializer.ValidationError('Invalid Url')
        return url


class CreateInstance(object):
    def create(self, validated_data):
        request = self.context['request']
        ip, is_routable = get_client_ip(request)
        instance = self.Meta.model.objects.filter(ip=ip, domain=validated_data['domain']).first()
        if instance is None:
            return self.Meta.model.objects.create(ip=ip, domain=validated_data['domain'])
        else:
            instance.count += 1
            instance.save()
        return instance


class GetIp(object):
    def get_ip(self, instance):
        return instance.ip


class CommonSerializer(CreateInstance, rest_serializer.ModelSerializer):
    class Meta:
        fields = ('domain',)


class PeerLinkSerializer(CommonSerializer, GetIp, ValidateDomain):
    ip = rest_serializer.SerializerMethodField(source='ip')

    class Meta(CommonSerializer.Meta):
        model = PeerLink
        fields = CommonSerializer.Meta.fields + ('ip',)


class UserLinkSerializer(CommonSerializer):
    class Meta(CommonSerializer.Meta):
        model = UserLink


class RawUserDataSerializer(CommonSerializer):
    class Meta(CommonSerializer.Meta):
        model = RawUserData


class UserSerializer(rest_serializer.Serializer, GetIp, ValidateDomain):
    domain = rest_serializer.URLField(max_length=256)
    ip = rest_serializer.SerializerMethodField(source='ip')

    class Meta(object):
        fields = ('domain', 'ip')

    def create(self, attr):
        if PeerLink.objects.filter(domain__icontains=attr['domain']).exists():
            serializer = UserLinkSerializer(data=attr, context=self.context)
        else:
            serializer = RawUserDataSerializer(data=attr, context=self.context)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
