from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'alicia.data.socrata.com',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)

socrata = Socrata(auth)

(ok, view) = socrata.views.lookup('9abs-ubh5')
assert ok, view

with open('census_detail_household_median_income5.csv', 'rb') as my_file:
  (ok, job) = socrata.using_config('census_detail_household_median_income5_03-28-2019_b547', view).csv(my_file)
  assert ok, job
  # These next 3 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  assert ok, job
  (ok, job) = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)
