from django.db import models
from django.utils.text import slugify

class Mess(models.Model):
    mess_name = models.CharField(max_length=255, verbose_name="Mess Name")
    owner_name = models.CharField(max_length=255, verbose_name="Owner Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(
        help_text="Contains all details of the mess, including timings, menus, leave policies, etc.",
        verbose_name="Description"
    )
    
    # Store coordinates/address. Using JSONField is perfect for OSM
    # Example format: {"lat": 12.3456, "lng": 78.9012, "address": "Street name, city"}
    location = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON containing location details compatible with OpenStreetMap (e.g. {'lat': 0.0, 'lng': 0.0, 'address': ''})",
        verbose_name="Location Coordinates & Address"
    )
    
    food_per_day = models.PositiveIntegerField(
        default=3,
        help_text="Normally every mess provides 3 meals per day",
        verbose_name="Meals Per Day"
    )
    
    subscription_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monthly subscription rate",
        verbose_name="Monthly Subscription Rate"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mess"
        verbose_name_plural = "Messes"
        ordering = ["-created_at"]

    def __str__(self):
        return self.mess_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.mess_name)
            # Handle unique constraints
            original_slug = self.slug
            queryset = Mess.objects.all().filter(slug=self.slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                queryset = Mess.objects.all().filter(slug=self.slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)
                count += 1
        super().save(*args, **kwargs)
