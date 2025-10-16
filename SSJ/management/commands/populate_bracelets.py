from ...models import Product, Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command inserts Bracelets Data details"
    
    def handle(self, *args, **options):
        product_names = [
                "Golden Charm Link Bracelet",
                "Diamond Grace Tennis Bracelet",
                "Royal Heritage Kada",
                "Floral Elegance Gold Bracelet",
                "Infinity Twist Bangle",
                "Rose Bloom Diamond Bracelet",
                "Classic Men’s Solid Gold Kada",
                "Emerald Glow Designer Bracelet",
                "Pearl Harmony Chain Bracelet",
                "Golden Mesh Statement Bracelet"
            ]

        product_descriptions = [
                "A stunning 22K gold link bracelet featuring delicate charm accents for a chic everyday look.",
                "Elegant 18K white gold tennis bracelet set with fine-cut diamonds, perfect for evening wear.",
                "Majestic 22K gold kada with embossed traditional motifs, inspired by royal artistry.",
                "A feminine bracelet in 22K gold, showcasing intricate floral patterns for festive occasions.",
                "Modern 18K gold bracelet with an infinity twist design, symbolizing everlasting connection.",
                "Beautifully crafted 18K rose gold bracelet adorned with tiny diamond blooms for subtle sparkle.",
                "Bold men’s kada made of 22K solid gold, featuring a smooth matte finish and engraved edges.",
                "Luxury bracelet featuring a central emerald surrounded by artistic gold detailing.",
                "Graceful 18K gold chain bracelet with alternating pearls and gold beads for a soft, elegant touch.",
                "Statement bracelet with interwoven gold mesh design, combining modern flair with classic style."
            ]

        weights = [
                "14.5",
                "12.2",
                "20.8",
                "10.6",
                "11.4",
                "9.8",
                "25.3",
                "13.9",
                "8.7",
                "16.5"
            ]
        
        imgs = [ f"products/images/{i}.jpg" for i in range(11,21) ]

        category = Category.objects.get(name="bracelets")
        
        for name, description, weight, img_url in zip(product_names, product_descriptions, weights, imgs):
            Product.objects.create(product_name=name, product_description=description, weight=weight, img_url=img_url, category=category)
        self.stdout.write(self.style.SUCCESS("Completed Inserting Bracelets into DB"))
            