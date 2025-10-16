from ...models import Product, Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command inserts Earrings Data details"
    
    def handle(self, *args, **options):
        product_names = [
            "Radiant Pearl Drop Earrings",
            "Celestial Diamond Studs",
            "Golden Blossom Jhumkas",
            "Royal Heritage Chandbalis",
            "Twilight Hoop Earrings",
            "Crimson Ruby Studs",
            "Graceful Chain Dangle Earrings",
            "Emerald Halo Stud Earrings",
            "Rose Petal Gold Drops",
            "Infinity Knot Diamond Earrings"
        ]

        product_descriptions = [
            "Elegant pearl drop earrings crafted in 18K gold, perfect for timeless sophistication.",
            "Brilliant round-cut diamond studs in 18K white gold, symbolizing celestial sparkle.",
            "Traditional 22K gold jhumkas featuring floral carvings and hanging gold beads.",
            "Regal chandbalis inspired by Mughal design, studded with tiny emerald accents.",
            "Stylish 18K gold hoop earrings with a twist pattern, ideal for daily wear.",
            "Deep red ruby studs encased in a gold frame, radiating luxury and charm.",
            "Contemporary chain-style dangle earrings in gold, adding elegance to every look.",
            "Emerald-centered gold studs surrounded by diamond halos for a royal finish.",
            "Rose gold drop earrings shaped like petals, adding soft feminine grace.",
            "18K gold infinity knot earrings with subtle diamond highlights for modern elegance."
        ]

        weights = [
            "6.2",
            "4.8",
            "10.5",
            "12.3",
            "5.6",
            "4.9",
            "7.2",
            "5.8",
            "6.0",
            "5.1"
        ]
        
        imgs = [f"products/images/{i}.jpg" for i in range(21, 31)]

        category = Category.objects.get(name="earrings")
        
        for name, description, weight, img_url in zip(product_names, product_descriptions, weights, imgs):
            Product.objects.create(
                product_name=name,
                product_description=description,
                weight=weight,
                img_url=img_url,
                category=category
            )

        self.stdout.write(self.style.SUCCESS("✅ Completed Inserting Earrings into DB"))
