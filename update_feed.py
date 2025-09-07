import os
import xml.etree.ElementTree as ET
from datetime import datetime
import email.utils
import xml.dom.minidom as minidom
from urllib.parse import quote

FEED_FILE = "feed.xml"
AUDIO_DIR = "./download/audio"
BASE_URL = "https://podcasterr.netlify.app/download/audio"


def get_file_size(path):
    return os.path.getsize(path)


def rfc2822_date():
    return email.utils.format_datetime(datetime.now())


def main():
    tree = ET.parse(FEED_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    existing_guids = {item.find("guid").text for item in channel.findall("item")}

    for filename in sorted(os.listdir(AUDIO_DIR)):
        guid = filename
        if guid in existing_guids:
            continue

        filepath = os.path.join(AUDIO_DIR, filename)
        url = f"{BASE_URL}/{quote(filename)}"
        size = str(get_file_size(filepath))
        pubdate = rfc2822_date()

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

        channel.insert(6, item)

        print(f"Added {filename} to feed")

    last_build = channel.find("lastBuildDate")
    if last_build is None:
        last_build = ET.SubElement(channel, "lastBuildDate")
    last_build.text = rfc2822_date()

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(FEED_FILE, "wb") as f:
        f.write(pretty_xml)


if __name__ == "__main__":
    main()
