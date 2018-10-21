import os

from .set import scrape_set


def test_regular_scraping():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
        current_directory, "snapshots/regular_set.html")

    with open(path_to_file, "r") as content_file:
        html = content_file.read()

    set = scrape_set(
        html,
        "https://www.1001tracklists.com/tracklist/1ftrfqc9/san-holo-bitbird-radio-023-2018-09-21.html")

    assert set == {
        'dj_name': 'San Holo',
        'source': 'https://www.1001tracklists.com/tracklist/1ftrfqc9/san-holo-bitbird-radio-023-2018-09-21.html',
        'set_title': 'San Holo - bitbird Radio 023 2018-09-21',
        'next_set': 'https://www.1001tracklists.com/tracklist/1grl3pyt/san-holo-beaudamian-bitbird-radio-024-2018-10-05.html',
        'previous_set': 'https://www.1001tracklists.com/tracklist/2uj6gx0t/san-holo-rome-in-silver-bitbird-radio-022-2018-09-10.html',
        'occasion': None,
        'venue': None,
        'artist_links': [],
        'related_links': [],
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


def test_id_scraping():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "snapshots/id_set.html")

    print(path_to_file)

    with open(path_to_file, "r") as content_file:
        html = content_file.read()

    set = scrape_set(html, "https://www.1001tracklists.com/tracklist/ltk7cx9/swacq-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html")

    assert set == {
        'dj_name': 'SWACQ',
        'next_set': None,
        'previous_set': None,
        'set_title': 'SWACQ @ Revealed Night, Q-Factory Amsterdam, Amsterdam Dance Event, Netherlands 2018-10-20',
        'source': 'https://www.1001tracklists.com/tracklist/ltk7cx9/swacq-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
        'occasion': 'Amsterdam Dance Event',
        'venue': 'Q-Factory Amsterdam',
        'artist_links': [
            'https://www.1001tracklists.com/tracklist/ltk7cx9/swacq-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/1ykwrmb1/swacq-revealed-radio-174-2018-07-06.html',
            'https://www.1001tracklists.com/tracklist/jx645n1/tiesto-swacq-we-are-loud-club-life-567-2018-02-09.html'
        ],
        'related_links': [
            'https://www.1001tracklists.com/tracklist/14ht0wsk/magnificence-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/2vg3u17t/tom-and-jame-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/tb4y0r1/kaaze-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/1xng7m69/suyano-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/ply7spk/manse-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/229gmln1/sick-individuals-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/29rw08lk/syzz-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/g4jvdhk/reggio-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/11qd0ru9/dannic-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html',
            'https://www.1001tracklists.com/tracklist/194tffst/maddix-revealed-night-q-factory-amsterdam-amsterdam-dance-event-netherlands-2018-10-20.html'
        ],
        'songs': [
            {
                'artist': 'SWACQ',
                'duration': 222,
                'label': 'Musical Freedom Records',
                'title': 'Kayos'
            },
            {
                'artist': 'Quintino',
                'duration': 183,
                'label': "Spinnin' Records",
                'title': 'Inferno'
            },
            None,
            {
                'artist': 'GTA & Damien N-Drix',
                'duration': 181,
                'label': 'Mad Decent',
                'title': 'Drix'},
            {
                'artist': 'JOYRYDE & Skrillex',
                'duration': 199,
                'label': 'OWSLA',
                'title': 'Agen Wida'
            },
            None,
            None,
            {
                'artist': 'Oomloud',
                'duration': 245,
                'label': 'Hysteria Records',
                'title': 'Rumbabox'},
            {
                'artist': 'Sandjake',
                'duration': None,
                'label': None,
                'title': 'Shine (Steff Da Campo Remix)'
            }
        ]
    }
