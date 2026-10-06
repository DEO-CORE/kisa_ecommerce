from rest_framework import serializers
from footer.models import Contacts, Partnership, Support, InfoPage, SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('primary_color', 'secondary_color', 'accent_color')


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('telegram_url', 'phone', 'address', 'work_hours', 'seller_name', 'country', 'registration_number', 'tax_id', 'legal_address', 'email')


class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = ('email', 'description')


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('telegram_url', 'email', 'description')


class InfoPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoPage
        fields = ('page_type', 'title', 'content', 'is_active', 'updated_at')
