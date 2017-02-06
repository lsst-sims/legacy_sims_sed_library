"""
This script is meant to be run on the sims_sed_library contents once it is
loaded and set up.

It will walk through the starSED/, galaxySED/, and agnSED/ sub-directories
and verify, for each file therein

1) there are no NaNs in the data

2) there is no data in the header (something we have had trouble with before)

This script takes a LONG time to run, so I suggest only running it when you
update the sed library.

The command:

python validate_sed_contents.py

will run the script on the currently setup version of sims_sed_library

python validate_sed_contents.py --root sed/library/dir

will run the script on the version of sims_sed_library whose root directory is
sed/library/dir
"""


import argparse
import os
import numpy as np
import gzip


def _verify_sed_files(dir_name):
    """
    Load all of the SED files in dir_name.  Check that they do not contain
    any NaNs and that the header, if there is one, does not contain data.

    If the dir_name contains another dir, recursively call itself.

    Return a list of tuples.  Each tuple contains the name of the file
    that failed the test and why (either 'nan' or 'header')
    """
    dtype = np.dtype([('wv', float), ('flux', float)])
    failures = []
    contents = os.listdir(dir_name)
    for file_name in contents:
        full_name = os.path.join(dir_name, file_name)

        if os.path.isdir(full_name):
            failures += _verify_sed_files(full_name)
        else:
            # check that there are no NaNs in the data
            try:
                data = np.genfromtxt(full_name, dtype=dtype)
                if np.isnan(data['wv']).any() or np.isnan(data['flux']).any():
                    failures.append((full_name, 'nan'))
            except:
                # if we could not even load the file, just mark it as an
                # anomaly; a human will probably have to look at it
                failures.append((full_name, 'could not load'))
                continue

            # Check that the last line of the header ends as expected.
            # Headers usually end with something like
            # Flambda (ergs/s/cm^2/nm)
            # We will check for the ')' followed by a newline
            if full_name.endswith('.gz'):
                open_fn = gzip.open
            else:
                open_fn = open

            with open_fn(full_name, 'r') as input_file:
                prev_line = None
                for line in input_file:
                    if line[0]  == '#':
                        prev_line = line
                    else:
                        if (prev_line is not None and
                            not prev_line.endswith(')\n')):

                            failures.append((full_name, 'header'))
                        break

    return failures


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'A script to validate the '
                                                   'contents of sims_sed_library')

    parser.add_argument('--root', type=str, default=None,
                        help = 'The root directory of the sims_sed_library '
                               'to be validated; if not set, will use the '
                               'version currently setup by eups')

    args = parser.parse_args()
    root_dir = args.root
    if root_dir is None:
        from lsst.utils import getPackageDir
        root_dir = getPackageDir('sims_sed_library')

    failures = []
    for sub_dir in ('starSED', 'galaxySED', 'agnSED'):
        failures += _verify_sed_files(os.path.join(root_dir, sub_dir))

    if len(failures) == 0:
        print("\nEverything looks good")
    else:
        for failed_file in failures:
            print("%s failed because of: %s" %
                  (failed_file[0].replace(root_dir, ''), failed_file[1]))
