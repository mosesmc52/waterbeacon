import json
from django.core.management.base import BaseCommand
from django.conf import settings
from rawdata import models as rawdata_models
from app import models as app_models
from django.db.models import Sum

class Command(BaseCommand):

    def handle(self, *args, **options):
        total  = app_models.location.objects.filter(population_served = 0).count()
        print('total: %s' % ( total ))

        completed = 0
        for location in app_models.location.objects.filter(population_served = 0):
            if not location.fips_county:
                print('location: %s skip' % (location.pk))
                continue

            location.population_served = rawdata_models.EpaWaterSystem.objects.filter( FIPSCodes__contains = location.fips_county ).aggregate(Sum('PopulationServedCount'))['PopulationServedCount__sum']
            location.save()

            completed +=1
            if completed % 100 == 0:
                total  = app_models.location.objects.filter(population_served = 0).count()
                print('%s [%s]' % ( total , completed))
