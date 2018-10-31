import sys
import json
import argparse

from database import create_database_connection, upload_set

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--files',
                        nargs='+',
                        help="json files to import")
    parser.add_argument('--onlyqueue',
                        action="store_true",
                        help="only export the queue file, don't upload the songs")
    parser.add_argument('--blacklistfile',
                        help="path to a txt file with links (one per line)")

    args = parser.parse_args()

    # Build Blacklist
    blacklist = set()
    if(args.blacklistfile):
        with open(args.blacklistfile) as f:
            for line in f:
                blacklist.add(line.strip())

    # Establish Database connection
    if not args.onlyqueue:
        try:
            conn = create_database_connection()
        except Exception as e:
            print(e)
            sys.exit()

    # Load setlists
    setlists = []
    for path in args.files:
        with open(path, "r+") as f:
            data = json.loads(f.read().strip())
            setlists.extend(data)

    # Remove duplicates
    clean_sets = []
    clean_set_sources = []
    for setlist in setlists:
        if not(setlist["source"] in clean_set_sources):
            clean_set_sources.append(setlist["source"])
            clean_sets.append(setlist)
    print("Removed %s duplicates from list." % (len(setlists) - len(clean_set_sources)))

    queue = []
    for index, set in enumerate(clean_sets):
        if not args.onlyqueue:
            print("Uploading %s of %s - %s" % (index, len(clean_sets), set["set_title"]))

            try:
                upload_set(conn, set)
            except Exception as e:
                print("Could not upload set because of %s" % e)
                cursor = conn.cursor()
                cursor.execute("ROLLBACK")
                conn.commit()
                continue

        # Load urls
        urls = []
        if(set["previous_set"]):
            urls.append(set["previous_set"])

        if(setlist["next_set"]):
            urls.append(set["next_set"])

        for link in set["artist_links"]:
            urls.append(link)

        for link in set["related_links"]:
            urls.append(link)

        # Remove duplicates and already scraped ones
        clean_urls = []
        for url in urls:
            if(url not in clean_set_sources and url not in clean_urls and url not in blacklist):
                clean_urls.append(url)

        # Add urls to queue
        queue.extend(clean_urls)
        if(len(clean_urls) > 0):
            print("Added %s links to queue" % len(clean_urls))

    # Save queue
    with open("queue.txt", "w") as f:
        for url in queue:
            f.write(str(url) + "\n")
