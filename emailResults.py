import smtplib, ssl
from pathlib import Path
import datetime as dt
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import configparser
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def generateChart(TEST_CASES):

    pieChart = str(Path("Logs", dt.datetime.now().strftime("%m_%d_%y"), "chart.png").absolute())
    labels = 'Pass', 'Fail'
    total_test = len(TEST_CASES.items())
    fail_cont = sum(1 for x, y in TEST_CASES.values() if x == 'FAILED')
    pass_cont = sum(1 for x, y in TEST_CASES.values() if x == 'PASSED')
    fail_percent = fail_cont/total_test*100
    pass_percent = pass_cont/total_test*100
    sizes = [pass_percent, fail_percent]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=['Green', 'Red'])
    ax1.axis('equal')  #Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(pieChart, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)

    return pieChart


def send(logFile, sender, TEST_CASES):

    #generate pie chart
    pieChart = generateChart(TEST_CASES)

    """Function for sending email containing test results"""
    #getting recipient from config file
    #config_dir = Path('./config.ini')
    config = configparser.ConfigParser()
    #full path to config /opt/Test_Framework/Master/
    config.read('config.ini')
    recipients = config.get('EMAIL', 'recipients').split(',')

    filename = Path(logFile).name
    print("Sending " + str(filename))
    #smtp_server = "mail.tauttechsystems.com"
    sender_email = sender
    #server = smtplib.SMTP(smtp_server)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Tests: " + str([i for i in TEST_CASES])
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)

    date = dt.datetime.today().strftime('%Y-%m-%d')
    html1 = """\
<h1 style="color: #5e9ca0;">Test Results</h1>
<p><em>Generated on:{date}</em></p>
<table style="height: 127px; background-color: lightgrey; border-color: black; width: 1000px;" width="1000" border="B">
<tbody>
<tr>
<td style="width: 250px;"><strong>Test Name</strong></td>
<td style="width: 165px;"><strong>Results</strong></td>
<td style="width: 2000px;"><strong>Details</strong></td>
</tr>
""".format(date=date)

    html2 = """\
<tr>
<td style="width: 250px;">{test_name}</td>
<td style="width: 165px;background-color: {color};">{result}</td>
<td style="width: 2000px;">{description}</td>
</tr>
"""
    html3 = """\
</tbody>
</table>
<p>&nbsp;**** This is a system generated email. Do not reply.****</p>
"""

    #generate HTM based on test cases and results
    for TEST_CASE, RESULT in TEST_CASES.items():
        #Added logic here to handle instances where a test description has been left out.
        if len(RESULT) == 2:
            if RESULT[0] == "FAILED":
                color = "red"
            else:
                color = "green"
            html1 = html1 + html2.format(test_name=TEST_CASE, result=RESULT[0], color=color, description=RESULT[1])
        else:
            if RESULT == "FAILED":
                color = "red"
            else:
                color = "green"
            html1 = html1 + html2.format(test_name=TEST_CASE, result=RESULT, color=color, description="NONE")
        html = html1 + html3

    part1 = MIMEText(html, "html")
    message.attach(part1)

    #attach log file here
    with open(logFile, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = {filename}",)
    message.attach(part)

    #attaching pie chart
    filename = Path(pieChart).name
    print("Sending " + str(filename))
    with open(pieChart, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = {filename}",)
    message.attach(part)

    context = ssl.create_default_context()
    port = 465
    password = "Test"
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipients, message.as_string())
