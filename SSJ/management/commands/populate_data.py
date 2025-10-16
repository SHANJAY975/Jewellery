from ...models import Product, Category
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = "This command inserts Product details"
    
    def handle(self, *args, **options):
        # Deleting the existing values
        Product.objects.all().delete()
        
        titles = [
            "Elegant 22K Gold Necklace",
            "Timeless Gold Bracelet",
            "Classic Gold Ring Design",
            "Modern Gold Chain Styles",
            "Royal Heritage Gold Collection",
            "Minimalist Daily Wear Gold Pendant",
            "Luxury Gold Bangles for Weddings",
            "Traditional Temple Gold Jewelry",
            "Charming Gold Anklet",
            "Graceful Gold Earrings",
            "Handcrafted Antique Gold Set",
            "Stylish Gold Nose Pin",
            "Golden Heart Pendant Necklace",
            "Customized Name Gold Chain",
            "Lightweight Gold Studs",
            "Wedding Special Gold Mangalsutra",
            "Elegant Gold Choker Design",
            "Golden Infinity Symbol Pendant",
            "Daily Wear Plain Gold Ring",
            "Trendy Gold Cuff Bracelet",
        ]


        descriptions = [
            "A beautifully crafted 22K gold necklace designed to add elegance to any occasion.",
            "A timeless bracelet in pure gold, symbolizing luxury and sophistication.",
            "A classic gold ring with a traditional finish, perfect for everyday wear.",
            "Modern chain designs crafted in gold for a stylish and contemporary look.",
            "Inspired by royal heritage, this collection reflects tradition and grandeur.",
            "A minimalist gold pendant suitable for daily wear and simple elegance.",
            "Luxurious wedding bangles handcrafted in pure gold for special occasions.",
            "Traditional temple-inspired gold jewelry with intricate details.",
            "A delicate gold anklet that adds a charming touch to your attire.",
            "Graceful gold earrings designed for a classy and versatile look.",
            "Antique handcrafted gold set that showcases heritage artistry.",
            "A stylish nose pin in gold, blending tradition with modern fashion.",
            "A golden heart pendant necklace representing love and beauty.",
            "Personalized name chain in gold, custom-made for your identity.",
            "Lightweight gold studs for comfortable daily use with elegance.",
            "A wedding special mangalsutra crafted with fine gold detailing.",
            "An elegant gold choker design that enhances your festive attire.",
            "A golden infinity pendant symbolizing everlasting love and bond.",
            "Plain gold ring crafted for simplicity and everyday use.",
            "Trendy gold cuff bracelet that brings a bold and modern look.",
        ]

        img_urls = [
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                    "https://fillmurray.lucidinternets.com/257/284",
                ]
       
        weights = [
            12.457,
            8.325,
            5.876,
            18.902,
            25.643,
            3.412,
            22.789,
            30.654,
            6.238,
            4.982,
            28.347,
            1.526,
            7.934,
            10.452,
            2.871,
            19.763,
            15.284,
            9.615,
            5.204,
            13.879,
        ]


        categories = Category.objects.all()
        for product_name, product_description, weight, img_url in zip(titles, descriptions, weights, img_urls):
            category = random.choice(categories)
            Product.objects.create(product_name=product_name, product_description=product_description, weight=weight, img_url=img_url, category = category)
            
        self.stdout.write(self.style.SUCCESS("Completed Inserting data into DB"))
            