from pathlib import Path

from django.conf import settings
from django.core.files import File

from src.social_proof.models import GalleryWork

GALLERY_WORKS = [
    {
        "file": "media/gallery/work-01.jpg",
        "alt_uk": "Генератор Kohler на напівпричепі",
        "alt_en": "Kohler generator on a semi-trailer",
        "order": 1,
    },
    {
        "file": "media/gallery/work-02.jpg",
        "alt_uk": "Помаранчева вісь у кузові",
        "alt_en": "Orange axle loaded in the trailer",
        "order": 2,
    },
    {
        "file": "media/gallery/work-03.jpg",
        "alt_uk": "Труби та палети в кузові",
        "alt_en": "Pipes and pallets in the trailer",
        "order": 3,
    },
    {
        "file": "media/gallery/work-04.jpg",
        "alt_uk": "Шасі пікапа в кузові",
        "alt_en": "Pickup chassis loaded in the trailer",
        "order": 4,
    },
    {
        "file": "media/gallery/work-05.jpg",
        "alt_uk": "Закріплені панелі на палеті",
        "alt_en": "Strapped panels on a pallet",
        "order": 5,
    },
    {
        "file": "media/gallery/work-06.jpg",
        "alt_uk": "Штабель ящиків у кузові",
        "alt_en": "Stacked cases in the trailer",
        "order": 6,
    },
    {
        "file": "media/gallery/work-07.jpg",
        "alt_uk": "Навантаження ящиків навантажувачем",
        "alt_en": "Loading cases with a forklift",
        "order": 7,
    },
    {
        "file": "media/gallery/work-08.jpg",
        "alt_uk": "Генератори Kohler на платформі",
        "alt_en": "Kohler generators on the trailer deck",
        "order": 8,
    },
]


def seed_gallery_works() -> int:
    created = 0
    for item in GALLERY_WORKS:
        obj, was_created = GalleryWork.objects.get_or_create(
            alt_uk=item["alt_uk"],
            defaults={
                "alt_en": item["alt_en"],
                "order": item["order"],
                "is_published": True,
            },
        )
        if was_created:
            created += 1
        src = Path(settings.BASE_DIR) / "static" / item["file"]
        if src.exists() and not obj.image:
            with src.open("rb") as handle:
                obj.image.save(src.name, File(handle), save=True)
    return created
