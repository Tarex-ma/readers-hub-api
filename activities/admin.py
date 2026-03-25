from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'created_at', 'get_target_summary')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'metadata')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'content_type')
    
    def get_target_summary(self, obj):
        if obj.target:
            return str(obj.target)
        return "-"
    get_target_summary.short_description = 'Target'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')