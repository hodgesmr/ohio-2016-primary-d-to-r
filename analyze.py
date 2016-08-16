#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import os
import urllib
import zipfile

COUNTIES = [
    'ADAMS',
    'ALLEN',
    'ASHLAND',
    'ASHTABULA',
    'ATHENS',
    'AUGLAIZE',
    'BELMONT',
    'BROWN',
    'BUTLER',
    'CARROLL',
    'CHAMPAIGN',
    'CLARK',
    'CLERMONT',
    'CLINTON',
    'COLUMBIANA',
    'COSHOCTON',
    'CRAWFORD',
    'CUYAHOGA',
    'DARKE',
    'DEFIANCE',
    'DELAWARE',
    'ERIE',
    'FAIRFIELD',
    'FAYETTE',
    'FRANKLIN',
    'FULTON',
    'GALLIA',
    'GEAUGA',
    'GREENE',
    'GUERNSEY',
    'HAMILTON',
    'HANCOCK',
    'HARDIN',
    'HARRISON',
    'HENRY',
    'HIGHLAND',
    'HOCKING',
    'HOLMES',
    'HURON',
    'JACKSON',
    'JEFFERSON',
    'KNOX',
    'LAKE',
    'LAWRENCE',
    'LICKING',
    'LOGAN',
    'LORAIN',
    'LUCAS',
    'MADISON',
    'MAHONING',
    'MARION',
    'MEDINA',
    'MEIGS',
    'MERCER',
    'MIAMI',
    'MONROE',
    'MONTGOMERY',
    'MORGAN',
    'MORROW',
    'MUSKINGUM',
    'NOBLE',
    'OTTAWA',
    'PAULDING',
    'PERRY',
    'PICKAWAY',
    'PIKE',
    'PORTAGE',
    'PREBLE',
    'PUTNAM',
    'RICHLAND',
    'ROSS',
    'SANDUSKY',
    'SCIOTO',
    'SENECA',
    'SHELBY',
    'STARK',
    'SUMMIT',
    'TRUMBULL',
    'TUSCARAWAS',
    'UNION',
    'VANWERT',
    'VINTON',
    'WARREN',
    'WASHINGTON',
    'WAYNE',
    'WILLIAMS',
    'WOOD',
    'WYANDOT',
]

PRIMARY_2016_COLUMN = 95
PREVIOUS_PRIMARY_COLUMNS = [93, 92, 90, 88, 87, 86, 84, 82, 81, 79, 78, 77, 75, 74, 73, 72, 69, 68, 66, 64, 63, 61, 58, 57, 54, 50, 46]

R_BALLOTS_CAST = 0
D_TO_R_CONVERSION_COUNT = 0

COLOR_BLUE = '\033[94m'
COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_GREEN = '\033[92m'
END_COLOR = '\033[0m'

MY_DIR = os.path.dirname(os.path.realpath(__file__))
DATETIME_STRING = datetime.utcnow().strftime("%Y_%m_%dT%H_%M_%SZ")
OUTPUT_DIR = '{}/data/{}/'.format(MY_DIR, DATETIME_STRING)

for county in COUNTIES:
    county_2016_r_count = 0
    county_d_to_r_count = 0

    output_data = []

    # 1. Download the county voter data
    print '{}\nDownloading {} County data...{}'.format(
        COLOR_YELLOW,
        county.title(),
        END_COLOR,
    )

    url = 'ftp://sosftp.sos.state.oh.us/free/Voter/{}.zip'.format(county)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    downloaded_file = '{}{}.zip'.format(OUTPUT_DIR, county)
    urllib.urlretrieve(url, downloaded_file)
    with zipfile.ZipFile(downloaded_file, 'r') as z:
        z.extractall(OUTPUT_DIR)
    os.remove(downloaded_file)

    old_filename = '{}{}.TXT'.format(OUTPUT_DIR, county)
    county_filename = '{}{}_COUNTY.csv'.format(OUTPUT_DIR, county)
    os.rename(old_filename, county_filename)

    # 2. Count the immediate D -> R primary switches
    print '{}Analyzing {} County data...{}'.format(
        COLOR_YELLOW,
        county.title(),
        END_COLOR,
    )

    with open(county_filename, 'rb') as input_file:
        reader = csv.reader(input_file)

        header = next(reader)
        output_data.append(header)

        for row in reader:
            if row[PRIMARY_2016_COLUMN] == "R":
                county_2016_r_count += 1

                _ = 0
                decided = False
                while _ < len(PREVIOUS_PRIMARY_COLUMNS) and not decided:
                    if row[PREVIOUS_PRIMARY_COLUMNS[_]] == "R":  # Not a switch
                        decided = True
                    elif row[PREVIOUS_PRIMARY_COLUMNS[_]] == "D":  # A switch
                        output_data.append(row)
                        county_d_to_r_count += 1
                        decided = True
                    _ += 1

    # 3. Write output data
    print '{}Writing {} County output data...{}'.format(
        COLOR_YELLOW,
        county.title(),
        END_COLOR,
    )

    output_filename = '{}{}_COUNTY_D_TO_R.csv'.format(OUTPUT_DIR, county)
    with open(output_filename, 'w') as output_file:
        output_writer = csv.writer(output_file)
        for row in output_data:
            output_writer.writerow(row)

    # 4. Clean up download file
    print '{}Cleaning up...{}'.format(
        COLOR_YELLOW,
        END_COLOR,
    )
    os.remove(county_filename)

    # 5. Console output
    print '{}Republican ballots{}{}: {}{}'.format(
        COLOR_RED,
        END_COLOR,
        COLOR_GREEN,
        county_2016_r_count,
        END_COLOR,
    )
    print u'{}D{} {}→{} {}R{}{}: {}{}'.format(
        COLOR_BLUE,
        END_COLOR,
        COLOR_GREEN,
        END_COLOR,
        COLOR_RED,
        END_COLOR,
        COLOR_GREEN,
        county_d_to_r_count,
        END_COLOR,
    )
    R_BALLOTS_CAST += county_2016_r_count
    D_TO_R_CONVERSION_COUNT += county_d_to_r_count

print u'{}\n\nTotal Ohio 2016{} {}Republican ballots{}{}: {}{}'.format(
    COLOR_GREEN,
    END_COLOR,
    COLOR_RED,
    END_COLOR,
    COLOR_GREEN,
    R_BALLOTS_CAST,
    END_COLOR,
)
print u'{}Total Ohio 2016{} {}D{} {}→{} {}R{}{}: {}{}'.format(
    COLOR_GREEN,
    END_COLOR,
    COLOR_BLUE,
    END_COLOR,
    COLOR_GREEN,
    END_COLOR,
    COLOR_RED,
    END_COLOR,
    COLOR_GREEN,
    D_TO_R_CONVERSION_COUNT,
    END_COLOR,
)

flip_percentage = (float(D_TO_R_CONVERSION_COUNT)/float(R_BALLOTS_CAST))*100
print u'{0}Flip percentage: {1:.2f}%{2}'.format(
    COLOR_GREEN,
    flip_percentage,
    END_COLOR,
)

print '{}\nData saved to:{} {}{}{}'.format(
    COLOR_YELLOW,
    END_COLOR,
    COLOR_GREEN,
    OUTPUT_DIR,
    END_COLOR,
)
