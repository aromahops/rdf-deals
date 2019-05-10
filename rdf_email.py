#!/usr/bin/python

import MySQLdb
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import configparser
import logging
import sys


def main():
    # Initiate Log
    logging.basicConfig(level=logging.DEBUG, filename="email_log.txt", filemode='w',
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Read the config.ini file to get rdf values
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")

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

    # Only send emails for current days deals
    current_day = datetime.now().strftime("%Y-%m-%d")

    # HTML Table Start tags
    start_table = "<html><table><tr><th>Title</th><th>Votes</th><th>URL</th></tr>"

    try:
        cur.execute("SELECT title, votes, url FROM rdf_table where insert_time like '%{}%'".format(current_day))
        for row in cur.fetchall():
            print(row[0], " ", row[1])
            # Append and create a HTML table
            table_row = "<tr><td>" + row[0] + "</td><td>" + str(row[1]) + "</td></td>" + row[2] + "</td></tr>"
            start_table = start_table + table_row

        # HTML Table End tags
        start_table = start_table + "</table></html>"
        logging.debug(start_table)

    except MySQLdb.Error as e:
        logging.error("Error:%d:%s" % (e.args[0], e.args[1]))
    finally:
        if db != None:
            db.close()

    receiver_email = config['rdf_single_value'].get('email')
    sender_email = "[testdev123@gmail.com]"
    password = "[your_password]"
    port = 465

    # Create MIME
    message = MIMEMultipart()
    message["Subject"] = "RDF Deals: {}".format(current_day)
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
    <html>
      <body>
        <p>Hi Boss,<br>
           Here are today's deals:<br>
           """ + '<br>' + start_table + """
        </p>
      </body>
    </html>
    """

    # Attach HTML message to email
    html_message = MIMEText(html, "html")
    message.attach(html_message)

    # ssl connection with gmail server, and then send the email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        server.login(sender_email, password)
        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )
    except smtplib.SMTPAuthenticationError as e:
        logging.warning("Email Authentication Failed")
    except smtplib.SMTPException as e:
        logging.error("Email Failed: %s" % (e.args[0]))
        sys.exit(1)


if __name__ == '__main__':
    main()
