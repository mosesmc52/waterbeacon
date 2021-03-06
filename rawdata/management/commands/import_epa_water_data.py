from rawdata.models import EpaWaterSystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import ( SDW_Importer )
import pandas as pd

class Command(BaseCommand):
    def _get_fips(self, fips_list):
        if len(fips_list) == 1:
            return fips_list[0]
        elif len(fips_list[0]) == 5:
            return fips_list[0]
        else:
            return self._get_fips(fips_list[1:])

    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        csvDirectory = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'WaterSystems')
        processed_rows = 0
        dtype = {
            'FIPSCodes': 'object',
            'RegistryID': 'str',
            'SDWDateLastVisitEPA': 'str'
        }

        importer = SDW_Importer()
        for filename in os.listdir(csvDirectory):
            path = os.path.join(csvDirectory, filename)
            data = pd.read_csv(
                path,
                dtype=dtype
            )
            # line_cnt can start at 0, as our data will be first row
            line_cnt = 0

            # remove all inactive sites
            data = data[data['PWSActivityCode'] == 'A']

            data.fillna('', inplace = True)
            data['FIPSCodes'] = data['FIPSCodes'].apply(
                lambda x: self._get_fips(x.split(', '))
            )
            data['EPARegion'] = str(data['EPARegion'][0]).rstrip('0').rstrip('.').zfill(2)

            # go through each system (row) and add it to db
            for __, system in data.iterrows():
                try:
                    processed_rows += 1
                    importer.add_watersystem_to_db(system)
                    if (processed_rows % 10000 == 0):
                        self.stdout.write('Processed row %s...' %processed_rows)
                except utils.IntegrityError:
                    self.stdout.write('%s already in the db' % system["PWSId"])
                except:
                    self.stdout.write('%s' %system)
                    raise
