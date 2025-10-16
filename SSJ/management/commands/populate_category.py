from ...models import Category
from django.core.management.base import BaseCommand
    
class Command(BaseCommand):
    help = "This command inserts Category details"
    
    def handle(self, *args, **options):
        # Deleting the existing values
        Category.objects.all().delete()
        
        categories = ['necklaces','earrings','rings','bracelets','charms']
        
        for category in categories:
            Category.objects.create(name=category)
        self.stdout.write(self.style.SUCCESS("Completed Inserting Categories into DB"))
            