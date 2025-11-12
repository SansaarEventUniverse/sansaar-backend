from django.urls import path

from presentation.views.health import health_check
from presentation.views.event_views import (
    create_event,
    get_event,
    update_event,
    save_draft,
    get_draft,
)
from presentation.views.event_status_views import (
    publish_event,
    unpublish_event,
    cancel_event,
    complete_event,
)
from presentation.views.datetime_views import (
    export_ical,
    list_timezones,
)
from presentation.views.search_views import (
    search_events,
    get_search_filters,
    get_search_suggestions,
)
from presentation.views.category_views import (
    manage_categories,
    get_category_stats,
    manage_tags,
    get_tag_suggestions,
    get_tag_stats,
)
from presentation.views.location_views import (
    search_nearby,
    search_by_location,
    get_map_events,
)
from presentation.views.recommendation_views import (
    get_recommendations,
    manage_preferences,
    get_similar_events,
)
from presentation.views.search_analytics_views import (
    get_search_analytics,
    get_search_performance,
    get_popular_searches,
)
from presentation.views.media_views import (
    upload_media,
    get_media_gallery,
    delete_media,
)
from presentation.views.document_views import (
    upload_document,
    get_documents,
    download_document,
    delete_document,
)
from presentation.views.calendar_views import (
    export_to_calendar,
    sync_calendar,
    calendar_webhook,
    get_calendar_syncs,
)
from presentation.views.template_views import (
    create_template,
    get_templates,
    get_template,
    apply_template,
    update_template,
    delete_template,
    clone_template,
)
from presentation.views.clone_views import (
    clone_event,
    bulk_clone,
    clone_series,
    get_clones,
    get_clone_info,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('search/', search_events, name='search_events'),
    path('search/filters/', get_search_filters, name='get_search_filters'),
    path('search/suggestions/', get_search_suggestions, name='get_search_suggestions'),
    path('search/analytics/', get_search_analytics, name='get_search_analytics'),
    path('search/performance/', get_search_performance, name='get_search_performance'),
    path('search/popular/', get_popular_searches, name='get_popular_searches'),
    path('nearby/', search_nearby, name='search_nearby'),
    path('search/location/', search_by_location, name='search_by_location'),
    path('map/', get_map_events, name='get_map_events'),
    path('recommendations/', get_recommendations, name='get_recommendations'),
    path('users/<str:user_id>/preferences/', manage_preferences, name='manage_preferences'),
    path('<str:event_id>/similar/', get_similar_events, name='get_similar_events'),
    path('<str:event_id>/media/', upload_media, name='upload_media'),
    path('<str:event_id>/media/gallery/', get_media_gallery, name='get_media_gallery'),
    path('<str:event_id>/media/<str:media_id>/', delete_media, name='delete_media'),
    path('<str:event_id>/documents/', upload_document, name='upload_document'),
    path('<str:event_id>/documents/list/', get_documents, name='get_documents'),
    path('<str:event_id>/documents/<str:document_id>/', download_document, name='download_document'),
    path('<str:event_id>/documents/<str:document_id>/delete/', delete_document, name='delete_document'),
    path('<str:event_id>/calendar/export/', export_to_calendar, name='export_to_calendar'),
    path('<str:event_id>/calendar/sync/', sync_calendar, name='sync_calendar'),
    path('<str:event_id>/calendar/syncs/', get_calendar_syncs, name='get_calendar_syncs'),
    path('<str:event_id>/apply-template/', apply_template, name='apply_template'),
    path('calendar/webhook/', calendar_webhook, name='calendar_webhook'),
    path('templates/', create_template, name='create_template'),
    path('templates/list/', get_templates, name='get_templates'),
    path('templates/<str:template_id>/', get_template, name='get_template'),
    path('templates/<str:template_id>/update/', update_template, name='update_template'),
    path('templates/<str:template_id>/delete/', delete_template, name='delete_template'),
    path('templates/<str:template_id>/clone/', clone_template, name='clone_template'),
    path('bulk-clone/', bulk_clone, name='bulk_clone'),
    path('<str:event_id>/clone/', clone_event, name='clone_event'),
    path('<str:event_id>/clone-series/', clone_series, name='clone_series'),
    path('<str:event_id>/clones/', get_clones, name='get_clones'),
    path('<str:event_id>/clone-info/', get_clone_info, name='get_clone_info'),
    path('categories/', manage_categories, name='manage_categories'),
    path('categories/stats/', get_category_stats, name='get_category_stats'),
    path('tags/', manage_tags, name='manage_tags'),
    path('tags/suggestions/', get_tag_suggestions, name='get_tag_suggestions'),
    path('tags/stats/', get_tag_stats, name='get_tag_stats'),
    path('timezones/', list_timezones, name='list_timezones'),
    path('drafts/get/', get_draft, name='get_draft'),
    path('drafts/', save_draft, name='save_draft'),
    path('<str:event_id>/ical/', export_ical, name='export_ical'),
    path('<str:event_id>/publish/', publish_event, name='publish_event'),
    path('<str:event_id>/unpublish/', unpublish_event, name='unpublish_event'),
    path('<str:event_id>/cancel/', cancel_event, name='cancel_event'),
    path('<str:event_id>/complete/', complete_event, name='complete_event'),
    path('<str:event_id>/update/', update_event, name='update_event'),
    path('<str:event_id>/', get_event, name='get_event'),
    path('', create_event, name='create_event'),
]
