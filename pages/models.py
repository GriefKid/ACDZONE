from django.db import models


class HomePage(models.Model):
    title = models.CharField(max_length=255, default="Global Financial Access")
    hero_title = models.TextField()
    hero_subtitle = models.TextField()
    hero_primary_cta_text = models.CharField(max_length=50, default="Get Started")
    hero_primary_cta_url = models.CharField(max_length=255, default="#")
    hero_secondary_cta_text = models.CharField(max_length=50, default="Explore Products")
    hero_secondary_cta_url = models.CharField(max_length=255, default="#")

    intro_video_url = models.URLField(blank=True, null=True)
    intro_image = models.ImageField(upload_to="partners/", blank=True)

    def __str__(self):
        return "Home Page Content"


class PartnerLogo(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="partners")
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="partners/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class FeatureCard(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="features")
    icon = models.ImageField(upload_to="features/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
