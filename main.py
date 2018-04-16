from collections import namedtuple
import json
import requests
import re


GREATSCHOOLS_BASE_URL = 'https://www.greatschools.org/'

# there are two ways in python to format strings, %s and {named}.
# %s allows you to do:
#
# print 'hi, %s!' % 'becca'
#
# whereas the {named} typed allows you to do:
#
# print 'hi, {name}!'.format(name='becca')
#
# they each serve different purposes, the {name} format is nice
# if you have different pieces of the string that you want to fill
# out and it would be hard to keep track of which is which without
# naming them
SCHOOL_SEARCH_URL = '%s/{state}/{city}/{district}/schools/' % GREATSCHOOLS_BASE_URL


# namedtuples allow us to create semi-structured pieces of
# data for things represent high level objects in our program,
# in this case, school districts. the alternative would be
# to store a list of urls directly, but that doesn't allow us to
# take advantage of the shared structure of the elements
# of the SCHOOL_DISTRICTS list, which might come in handy later
# on (otherwise its just a bunch of strings which we can't make
# any assumptions about or add any more data to)
District = namedtuple('District', [
    'state',
    'city',
    'district',
])

School = namedtuple('School', [
    'name',
    'id',
    'street',
    'city',
    'state',
    'zipcode',
    'schoolType',
    'preschool',
    'gradeRange',
    'fitScore',
    'maxFitScore',
    'gsRating',
    'on_page',
    'strongFit',
    'okFit',
    'communityRatingStars',
    'profileUrl',
    'reviewUrl',
    'zillowUrl',
    'lat',
    'lng',
    'numReviews',
    'zIndex',
])


# you could theoretically try to start with something like
# "fairfield suisun" and try to figure out from the website
# what the state/city and full district name are, but for
# now we're just filling them out directly, and we can
# back track later if we need to
SCHOOL_DISTRICTS = [
    District(
        state='california',
        city='fairfield',
        district='fairfield_suisun-unified-school-district',
    ),
]


def find_schools_in_school_district_cdata(cdata):
    '''
    this is the worst and hardest part of grabbing data from the district
    website. this makes some horrible assumptions that are likely to change
    about the CDATA structure in the html thats delivired.

    it would be MUCH better to be able to do something like:

    ```
    parsed = {}
    for data in cdata.split(';'):
        key, value = data.split('='):
        parsed[key] = json.loads(value)
    return parsed
    ```

    where parsed now contains the key and the json-parsed object
    it corresponds to in the cdata. the problem with this is that
    ';' is not a real delimiter, ie it is contained in some of the
    data elements themselves. this is a common problem and I'm sure there's
    a solution I'm just not thinking of, but for now, we can just do this horrible
    hack to pull out the information we want directly
    '''
    x = re.search('gon.map_points=(.*);gon.sprite_files', cdata).group(1)

    # in python 3, you can merge two dictionaries with {**a, **b}, and
    # so we're doing that here to supply the default zIndex value if its
    # not contained in the args directly.
    #
    # see https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
    return (School(**{**args, **{'zIndex': 0}}) for args in json.loads(x))


def get_schools(district):
    # make an http GET request to pull down information
    # for this particular school district
    html = requests.get(SCHOOL_SEARCH_URL.format(
        state=district.state,
        city=district.city,
        district=district.district,
    )).text

    data_line = None
    for line in html.split('\n'):
        # greatschools happens to store all of its data at the top of
        # its page in a line that happens to start with "window.gon".
        # this allows us to get the data in json format, which is easier
        # to deal with than html
        if line.startswith('window.gon'):
            data_line = line

    if data_line is None:
        # couldn't find what we were looking for. abort.
        raise Exception('unable to find data line')

    for school in find_schools_in_school_district_cdata(data_line):
        # ok now we have the school. there's some information
        # we can pull out directly from this, but we probably
        # want to go to the profileUrl and pull out the rest
        #
        # TODO
        print(school)


def main():
    for district in SCHOOL_DISTRICTS:
        get_schools(district)


if __name__ == '__main__':
    main()
