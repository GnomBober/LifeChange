from django import template
import re

register = template.Library()


@register.filter
def embed_video_url(url):
    """Преобразует ссылку на видео в формат для iframe."""
    # YouTube
    youtube_match = re.match(r".*?youtube\.com/watch\?v=([\w-]+)", url)
    if youtube_match:
        return f"https://www.youtube.com/embed/{youtube_match.group(1)}"

    youtube_short_match = re.match(r".*?youtu\.be/([\w-]+)", url)
    if youtube_short_match:
        return f"https://www.youtube.com/embed/{youtube_short_match.group(1)}"

    # ВКонтакте
    vk_match = re.match(r".*?vk\.com/video.*?(\d+_\d+)", url)
    if vk_match:
        return f"https://vk.com/video_ext.php?oid={vk_match.group(1)}"

    # Если URL не распознан, вернуть его без изменений
    return url