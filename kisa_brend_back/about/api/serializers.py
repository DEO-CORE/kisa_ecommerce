from rest_framework import serializers
from about.models import MainPageSettings, BrandPrinciple, BrandHistory, TeamBlock


class MainPageSettingsSerializer(serializers.ModelSerializer):
    team_photo_url = serializers.SerializerMethodField()
    hero_video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MainPageSettings
        fields = ('slogan', 'manifesto', 'team_photo', 'team_photo_url', 'hero_video', 'hero_video_url')
    
    def get_team_photo_url(self, obj):
        if obj.team_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.team_photo.url)
            return obj.team_photo.url
        return None
    
    def get_hero_video_url(self, obj):
        if obj.hero_video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_video.url)
            return obj.hero_video.url
        return None


class BrandPrincipleSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BrandPrinciple
        fields = ('id', 'number', 'title', 'description', 'icon', 'icon_url', 'is_active')
    
    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class BrandHistorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BrandHistory
        fields = ('id', 'year', 'title', 'description', 'image', 'image_url', 'is_active')
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class TeamBlockSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamBlock
        fields = ('text', 'photo', 'photo_url')
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None