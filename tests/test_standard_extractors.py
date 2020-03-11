from web_parser.parsers import HTMLParserEngine
from web_parser.extractors import ParagraphsExtractor, PageOverviewExtractor, \
    AllLinksExtractor, AllLinksAnalyticsExtractor, JSONLDExtractor, TableContentExtractor, \
    MetaTagExtractor, HeadingsExtractor, FeedUrlExtractor
from web_parser.utils import yaml_to_json, convert_html_to_selector
import os

path = os.getcwd()
html = open("{}/tests/page.html".format(path), "r").read()


def test_paragraphs_extractor():
    extraction_manifest = yaml_to_json(open("{}/tests/extract.yaml".format(path)).read())
    engine = ParagraphsExtractor(html_selector=convert_html_to_selector(html),
                                 extractor_id="paragraphs_extractor")
    result = engine.run()
    assert result['paragraphs_extractor'] is not None
    assert result['paragraphs_extractor'].__len__() > 0
    assert type(result) is dict


def test_links_extractor():
    result = AllLinksExtractor(html_selector=convert_html_to_selector(html),
                               extractor_id="links_extractor").run()
    assert result['links_extractor'] is not None
    assert result['links_extractor'].__len__() > 0
    assert type(result) is dict


def test_links_analytics_extractor():
    result = AllLinksAnalyticsExtractor(
        html_selector=convert_html_to_selector(html),
        extractor_id="links_analytics_extractor").run()
    assert 'links_analytics_extractor' in result
    assert result['links_analytics_extractor'].__len__() > 0
    first_domain_data = result['links_analytics_extractor'][0]
    assert 'domain' in first_domain_data
    assert 'links' in first_domain_data
    assert 'links_count' in first_domain_data
    assert type(result) is dict


def test_json_ld_extractor():
    result = JSONLDExtractor(html_selector=convert_html_to_selector(html),
                             extractor_id="json_ld_extractor").run()
    assert 'json_ld_extractor' in result
    assert result['json_ld_extractor'].__len__() > 0
    first_json_ld = result['json_ld_extractor'][0]
    assert first_json_ld['@context'] == 'http://schema.org'
    assert first_json_ld['@type'] == "WebSite"
    assert first_json_ld['alternateName'] == "Invana Labs"
    assert first_json_ld['url'] == "https://invana.io"
    assert type(result) is dict


def test_table_extractor():
    result = TableContentExtractor(html_selector=convert_html_to_selector(html),
                                   extractor_id="table_extractor").run()
    assert 'table_extractor' in result
    assert result['table_extractor'].__len__() > 0
    first_table = result['table_extractor'][0][0]
    assert first_table['#'] == 'Mark'
    assert first_table['First'] == "Otto"
    assert first_table['Last'] == "@mdo"
    assert type(result) is dict


def test_meta_tags_extractor():
    result = MetaTagExtractor(html_selector=convert_html_to_selector(html),
                              extractor_id="meta_extractor").run()
    assert 'meta_extractor' in result
    assert result['meta_extractor'].__len__() > 0
    assert result['meta_extractor']['meta__viewport'] == 'width=device-width, initial-scale=1'
    assert result['meta_extractor']['title'] == 'Invana Knowledge Platform'
    assert type(result) is dict


def test_headings_extractor():
    result = HeadingsExtractor(
        html_selector=convert_html_to_selector(html),
        extractor_id="headings_extractor").run()
    assert 'headings_extractor' in result
    assert result['headings_extractor'][0] == "Knowledge Platform"
    assert type(result) is dict


def test_feed_url_extractor():
    result = FeedUrlExtractor(
        html_selector=convert_html_to_selector(html),
        extractor_id="feed_url_extractor").run()
    assert 'feed_url_extractor' in result
    assert result['feed_url_extractor']['rss__xml'] == "/feed.xml"
    assert type(result) is dict

#
# def test_page_overview_extractor():
#     result = PageOverviewExtractor(
#         html_selector=convert_html_to_selector(html),
#         extractor_id="overview_extractor").run()
#     print("===", result)
#     assert 'overview_extractor' in result
#     assert result['overview_extractor']['rss__xml'] == "/feed.xml"
#     assert type(result) is dict
