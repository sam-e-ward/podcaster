import os
import xml.etree.ElementTree as ET
from datetime import datetime
import email.utils

FEED_FILE = "feed.xml"
AUDIO_DIR = "./download/audio"
BASE_URL = "https://example.com/audio"  # <-- update with your Netlify site


def get_file_size(path):
    return os.path.getsize(path)


def rfc2822_date(path):
    ts = os.path.getmtime(path)
    return email.utils.formatdate(ts, usegmt=True)


def main():
    tree = ET.parse(FEED_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    # collect existing GUIDs
    existing_guids = {item.find("guid").text for item in channel.findall("item")}

    for filename in sorted(os.listdir(AUDIO_DIR)):
        guid = filename
        if guid in existing_guids:
            continue

        filepath = os.path.join(AUDIO_DIR, filename)
        url = f"{BASE_URL}/{filename}"
        size = str(get_file_size(filepath))
        pubdate = rfc2822_date(filepath)

        item = ET.Element("item")
        title = ET.SubElement(item, "title")
        title.text = os.path.splitext(filename)[0]

        description = ET.SubElement(item, "description")
        description.text = f"Episode from {filename}"

        enclosure = ET.SubElement(
            item, "enclosure", {"url": url, "length": size, "type": "audio/mpeg"}
        )

        guid_elem = ET.SubElement(item, "guid")
        guid_elem.text = guid

        pubdate_elem = ET.SubElement(item, "pubDate")
        pubdate_elem.text = pubdate

        # Insert at top (after channel metadata)
        channel.insert(0, item)

        print(f"Added {filename} to feed")

    tree.write(FEED_FILE, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
