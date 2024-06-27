import argparse
import datetime
from typing import List


def _create_xml_fragment(label_prefix: str, repo: str, list_suffix: str, ts: str) -> str:
    """
    Creates an entry fragment for a given repo.

        label_prefix: Github
        repo: go-commons
        list_suffix: ROKT.github.com
        ts: 2024-06-27T11:56:36Z
    """

    tmpl = f"""
    <entry>
        <category term='filter'></category>
        <title>Mail Filter</title>
        <updated>{ts}</updated>
        <content></content>
        <apps:property name='hasTheWord' value='list:({repo}.{list_suffix})'/>
        <apps:property name='label' value='{label_prefix}/{repo}'/>
        <apps:property name='shouldArchive' value='true'/>
        <apps:property name='sizeOperator' value='s_sl'/>
        <apps:property name='sizeUnit' value='s_smb'/>
    </entry>\n"""
    return tmpl


def create_xml_template(repos: List[str], label_prefix: str, list_suffix: str) -> str:
    """
    Given a list of github repo names (e.g. ['go-commons', 'auth0']), create an XML string to be imported as a gmail filter

    Makes some assumptions about how to structure email filters.
    """

    # get current time in this format 2024-06-27T11:56:36Z
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    tmpl_hdr = f"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <title>Mail Filters</title>
    <id>tag:mail.google.com,2008:filters:z0000001646671690990*8390708163084012076,z0000001707325959104*5822183314426085215</id>
    <updated>{ts}</updated>"""

    entries = []
    for repo in repos:
        entries.append(_create_xml_fragment(label_prefix, repo, list_suffix, ts))

    entry_str = "".join(entries)
    tmpl_footer = "</feed>\n"

    return tmpl_hdr + entry_str + tmpl_footer


def main(repos: List[str], label_prefix: str, list_suffix: str, filepath: str):
    if not filepath:
        filepath = "./filters.xml"
    output = create_xml_template(repos, label_prefix, list_suffix)
    with open(filepath, "w") as f:
        f.write(output)
    return filepath


def parse_args():
    parser = argparse.ArgumentParser(description="Parse command line arguments.")

    parser.add_argument("-r", dest="repos", type=str, required=True, help="A list of repositories separated by commas")
    parser.add_argument(
        "-l",
        dest="label",
        type=str,
        required=True,
        help="The label prefix to be used within email filters. e.g. Github",
    )
    parser.add_argument(
        "-s", dest="listserv", type=str, required=True, help="The suffix of the listserv, e.g. ROKT.github.com"
    )
    parser.add_argument(
        "-f",
        dest="filepath",
        type=str,
        required=False,
        help="An optional filepath to save the output XML file. Defaults to ./filters.xml",
    )

    args = parser.parse_args()

    # Split the -r argument into a list
    args.repos = args.repos.split(",")

    return args


if __name__ == "__main__":
    args = parse_args()
    fp = main(args.repos, args.label, args.listserv, args.filepath)
    print(f"Done! Written to {fp}")
