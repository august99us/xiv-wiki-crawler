import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
from Changes.change import Change
import logging

class WikiChangesDiffCalculator:
    """
    Documentation goes here
    """
    wiki_changes_url = "https://ffxiv.consolegameswiki.com/wiki/Special:RecentChanges?hidebots=1&translations=filter&hidelog=1&limit=50&days=7&enhanced=1&urlversion=2"
    pages_to_skip_regex = "User:|User talk:|UserWiki:|Template:"

    def __init__(self, recent_changes_logger, change_indexer):
        self.recent_changes_logger = recent_changes_logger
        self.change_indexer = change_indexer

    def index_changes(self) -> None:
        # Retrieve the html on the page
        req = urllib.request.Request(self.wiki_changes_url, headers={'User-Agent' : "UriangerBot"}) 
        con = urllib.request.urlopen(req)
        html_bytes = con.read()
        html = html_bytes.decode("utf-8")

        # Process the html for the changes we are interested in
        soup = BeautifulSoup(html, 'html.parser')
        changes_list = soup.find("div", {"class": "mw-changeslist"})
        # Pluck the inner <table> elements that represent the last 50 articles that changed
        changes = changes_list.find_all("table", {"class": "mw-changeslist-line"})
        changes_object_list = []
        # Iterate through the changes
        for change in changes:
            # Pluck out the <td> element data-target-page property. This is supposed to represent the name of the
            # article that was changed
            change_inner_td_element_data_target = change.find("td", {"class": "mw-changeslist-line-inner"}).get("data-target-page")
            if change_inner_td_element_data_target is None:
                # If this data-target-page property was not found in the <td> element, it likely means that there
                # were multiple changes made to this article in a row, in which case the entry on the Recent Changes
                # page is a list with changes nested in a > dropdown. In this case, we can find the data-target-page
                # element in a different, sub <td> element
                change_inner_td_element_data_target = change.find("td", {"class": "mw-enhanced-rc-nested"}).get("data-target-page")
            logging.info("Parse changed article name: " + change_inner_td_element_data_target)
            # Now if the artcle changed name has User: or User talk:, we know it is a change to a user page and
            # therefore we can drop the change
            if re.search(self.pages_to_skip_regex, change_inner_td_element_data_target) is not None:
                logging.info("Matched user or user talk page so skipping : " + change_inner_td_element_data_target)
                continue
            # Else, we pluck out the datetime and the link to the article and record it in our list
            try:
                changes_object_list.append(Change(change.get("data-mw-ts"), change_inner_td_element_data_target,
                    change.find("span", {"class": "mw-title"}).a.get("href")))
            except AttributeError:
                # Something weird happened here, this is a case not caught
                logging.warn("Something weird happened here " + change.prettify())
                raise

        print([str(item) for item in changes_object_list])

        # Now we need to compare the list of changes to the last list of changes we've seen.
        new_changes = self.recent_changes_logger.lookup_new_changes(changes_object_list)

        # Indexing issues are critical but should not necessarily mean the execution should stop
        indexing_issues = 0
        # The recent changes logger records processed changes in order to dedupe and reduce the
        # number of changes indexed per indexing run. Therefore logging issues are not necessarily
        # critical issues (they will just cause a specific wiki change to be re-indexed multiple times)
        # unless ALL logging operations are failing, in which case it may cause too many requests
        # to be sent to the wiki
        logging_issues = 0
        for change in new_changes:
            try:
                self.change_indexer.index_change(change)
            except Exception as e:
                indexing_issues += 1
                logging.exception("Issue indexing a new change")
                continue
            try:
                self.recent_changes_logger.record_processed_change(change)
            except Exception as e:
                logging.warn(e)
                logging_issues += 1


        logging.info(f"{len(new_changes) - indexing_issues} new changes from the wiki were successfully indexed.")

        # actually it would be better to emit a metric here, i will change this later.
        if indexing_issues > 0:
            # TODO: alarm
            pass
        if logging_issues >= 0.5*len(new_changes):
            # TODO: alarm
            pass
