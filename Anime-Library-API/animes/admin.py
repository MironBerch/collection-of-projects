from django.contrib import admin

from animes.models import Staff, Studio, Anime, AnimeComment, AnimeReview, AnimeShots, Genre


admin.site.register(Staff)
admin.site.register(Studio)
admin.site.register(Anime)
admin.site.register(AnimeComment)
admin.site.register(AnimeReview)
admin.site.register(AnimeShots)
admin.site.register(Genre)