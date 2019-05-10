#!/usr/bin/python

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import configparser
import sys
import MySQLdb
import logging

MAIN_URL = 'http://forums.redflagdeals.com'
API_ENDPOINT = "https://[your_API].us-east-1.amazonaws.com/dev"


def main():

    # Initiate Log
    logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode='w',
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Read the config.ini file to get rdf values
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")

    min_votes = config['rdf_single_value'].getint('minimal_votes')
    rdf_subsection = config['rdf_multi_values'].get('rdf_subsection').replace(" ", "").split(',')
    topic_category = config['rdf_multi_values'].get('topic_category').replace(" ", "").split(',')

    # Database values
    db_conn = config['db_connection_info'].get('db_connection')
    db_user = config['db_connection_info'].get('user')
    db_pass = config['db_connection_info'].get('password')
    db_schema = config['db_connection_info'].get('schema')

    # Connect to Db
    db = MySQLdb.connect(host=db_conn,
                         user=db_user,
                         passwd=db_pass,
                         db=db_schema)

    cur = db.cursor()

    # Crawl the rdf web pages specified in the config.ini file
    for forum_subsection in rdf_subsection:
        url = MAIN_URL + forum_subsection
        try:
            page = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.error("Error: %s" % (e.args[0]))
            sys.exit(1)

        hot_deals_soup = BeautifulSoup(page.text, 'html.parser')
        bodylist = hot_deals_soup.find('div', class_="forumbg")

        if bodylist is None:
            logging.warning("RDF URL is valid, but not a HTML forum section: %s", url)
            continue

        topic_section = bodylist.find_all('li', class_="topic")

        for thread in topic_section:

            # Find the title
            thread_name = thread.find("h3", class_="topictitle")
            title = thread_name.text.replace("\n", "").strip()
            alphanumeric_title = re.sub(r'\W+', '', title)

            matching_category = False
            for category in topic_category:
                if category.lower() in title.lower():
                    matching_category = True

            # Find the votes, by default is 0. Need to differentiate between + and -
            # Only want the positive upvotes
            thread_votes = thread.find("dd", class_="total_count")
            if thread_votes is not None and matching_category:
                vote = thread_votes.text
                vote = int(re.sub("[^0-9-]", "", vote))

                if vote < min_votes:
                    continue
                logging.info(title)
                logging.info(int(vote))
            else:
                continue

            # Find the thread creation date
            thread_creation = thread.find(class_="first-post-time")
            removed_date_suffix = re.sub("(\d+)(st|nd|rd|th|),", r"\1", thread_creation.text)
            thread_time = datetime.strptime(removed_date_suffix, "%b %d %Y %I:%M %p")

            logging.info(thread_creation.text)
            logging.info(thread_time)

            # Get current datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_day = datetime.now().strftime("%Y-%m-%d")
            logging.info(current_time)

            # Get the full URL
            thread_name2 = thread.find("a", class_="topic_title_link")
            product_url = thread_name2.get('href')
            full_url = MAIN_URL + product_url
            logging.info(full_url)

            # Add to MySQL db
            try:
                cur.execute("INSERT INTO rdf_table(title, votes, thread_creation_time, url, insert_time) VALUES" \
                            " (%s, %s, %s, %s, %s);", (title, vote, thread_time, full_url, current_time))
                db.commit()
                logging.info("SQL Inserted: %s", title)
            except MySQLdb.IntegrityError as e:
                logging.info("SQL Duplicate Thread: %s", title)
            except MySQLdb.Error as e:
                logging.error("%d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)

            # Add to AWS DynamoDB via API Gateway
            data = {
                'title': title,
                'votes': vote,
                'thread_creation_time': str(thread_time),
                'insert_day': str(current_day),
                'url': full_url,
                'mp3_url': "creating",
                'db_id': alphanumeric_title
            }

            try:
                page = requests.post(API_ENDPOINT, json=data)
                logging.debug(page.content)
            except requests.exceptions.RequestException as e:
                logging.error("Error: %s" % (e.args[0]))

    db.close()


if __name__ == '__main__':
    main()
