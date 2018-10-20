import os

from .set import scrape_set


def test_setlist_scraper():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "dummy_set.html")

    with open(path_to_file, "r") as content_file:
        html = content_file.read()

    set = scrape_set(html, "https://www.1001tracklists.com/tracklist/1ftrfqc9/san-holo-bitbird-radio-023-2018-09-21.html")

    print(set)

    assert set == {
        'dj_name': 'San Holo',
        'source': 'https://www.1001tracklists.com/tracklist/1ftrfqc9/san-holo-bitbird-radio-023-2018-09-21.html',
        'set_title': 'San Holo - bitbird Radio 023 2018-09-21',
        'next_set': 'https://www.1001tracklists.com/tracklist/1grl3pyt/san-holo-beaudamian-bitbird-radio-024-2018-10-05.html',
        'previous_set': 'https://www.1001tracklists.com/tracklist/2uj6gx0t/san-holo-rome-in-silver-bitbird-radio-022-2018-09-10.html',
        'songs': [
            {
                'label': 'bitbird',
                'duration': 336,
                'artist': 'San Holo',
                'title': 'Everything Matters (When It Comes To You)'
            },
            {
                'label': 'bitbird',
                'duration': 260,
                'artist': 'San Holo',
                'title': 'Lift Me From The Ground'
            },
            {
                'label': 'bitbird',
                'duration': 341,
                'artist': 'San Holo',
                'title': 'Show Me'
            },
            {
                'label': 'bitbird',
                'duration': 236,
                'artist': 'San Holo',
                'title': 'Brighter Days'
            },
            {
                'label': 'bitbird',
                'duration': 221,
                'artist': 'San Holo',
                'title': 'Always On My Mind'
            },
            {
                'label': 'bitbird',
                'duration': 261,
                'artist': 'San Holo',
                'title': 'Go Back In Time'
            },
            {
                'label': 'bitbird',
                'duration': 262,
                'artist': 'San Holo',
                'title': 'Love (wip)'
            },
            {
                'label': 'bitbird',
                'duration': 292,
                'artist': 'San Holo',
                'title': 'Voices In My Head'
            },
            {
                'label': 'bitbird',
                'duration': 299,
                'artist': 'San Holo',
                'title': 'worthy'
            },
            {
                'label': 'bitbird',
                'duration': 382,
                'artist': 'Duskus & San Holo',
                'title': 'Forever Free'
            },
            {
                'label': 'bitbird',
                'duration': 362,
                'artist': 'San Holo',
                'title': 'Surface'
            },
            {
                'label': 'bitbird',
                'duration': 255,
                'artist': 'San Holo',
                'title': 'Vestal Avenue'
            }
        ]
    }
