from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from bs4 import BeautifulSoup
from playsound import playsound
import requests
import time

app = Flask(__name__)
socketio = SocketIO(app)

COOLDOWN = 300

# extract links
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

links = {'https://ics.uci.edu/academics/impact/student-awards-honors/', 'https://ics.uci.edu/faculty-staff-positions/', 
         'https://ics.uci.edu/alumni/corporate-engagement/corporate-partners/', 'https://cpri.uci.edu/', 'https://create.ics.uci.edu/', 
         'https://ics.uci.edu/happening/news/?filter%5Baffiliation_posts%5D=1988', 'https://ics.uci.edu/contact-us/', 
         'https://ics.uci.edu/academics/graduate-programs/', 'https://ics.uci.edu/alumni/corporate-engagement/', 
         'https://ics.uci.edu/academics/undergraduate-programs/', 'https://ics.uci.edu/student-experience/clubs-organizations/', 
         'https://cml.ics.uci.edu/aiml/', 'https://ics.uci.edu/', 'https://ics.uci.edu/alumni/', 'https://ics.uci.edu/events/', 
         'https://ics.uci.edu/academics/campus-resources/', 'https://ics.uci.edu/academics/impact/faculty-awards-honors/', 
         'http://instagram.com/ucibrenics/', 'https://www.uci.edu', 'https://ics.uci.edu/financial-aid-and-scholarships/undergraduate-financial-awards/', 
         'https://ics.uci.edu/academics/impact/technology-transfer/', 'http://www.ics.uci.edu/~kay/python/RP0.py', 
         'https://ics.uci.edu/academics/undergraduate-academic-advising/', 'https://ics.uci.edu/computing-research/institutes-centers/', 
         'https://connectedlearning.uci.edu/media/', 'https://www.cs.uci.edu/', 'https://uci.edu/privacy/index.php', 
         'https://ics.uci.edu/academics/graduate-academic-advising/', 'http://youtube.com/UCIBrenICS', 'https://ics.uci.edu/faculty-staff-resources/', 
         'https://ics.uci.edu/honors/', 'http://isr.uci.edu/isr-events/upcoming', 'https://ics.uci.edu/admissions-information-and-computer-science/graduate-admissions/', 
         'https://uci.edu/visit/maps.php', 'https://www.ics.uci.edu/events/list/?tribe__ecp_custom_49%5B0%5D=Alumni', '/alumni/corporate-engagement/', 
         'https://ics.uci.edu/academics/undergraduate-academic-advising/ics-credit-by-exam/', 'https://ics.uci.edu/facts-figures/ics-mission-history/', 
         'https://ics.uci.edu/happening/news/?filter%5Bresearch_areas_ics%5D=1994', 'https://ics.uci.edu/academics/', 'http://www.igb.uci.edu/', 
         'https://ics.uci.edu/student-experience/entrepreneurship-student-experience/', '/people/', 'tel:1-949-824-7427', 
         'https://ics.uci.edu/alumni/corporate-engagement/research-partnerships-corporate-engagement/', 'https://ics.uci.edu/academics/graduate-fellowships-funding/', 
         'https://ics.uci.edu/happening/annual-reports-brochures/', 'https://cml.ics.uci.edu/', 'https://ics.uci.edu/upcoming-events/', 
         'https://ics.uci.edu/alumni/hall-of-fame/', 'https://ics.uci.edu/academics/impact/', 'https://cpri.uci.edu/category/events/', 'https://ics.uci.edu/make-a-gift/', 
         'https://oai.ics.uci.edu/', 'https://ics.uci.edu/happening/news/?filter%5Baffiliation_posts%5D=1989', 'http://facebook.com/UCIBrenICS', 
         'https://ics.uci.edu/alumni/corporate-engagement/student-recruitment-corporate-engagement/', 'https://futurehealth.ics.uci.edu/', 'https://www.informatics.uci.edu/', 
         'https://ics.uci.edu/departments/', 'http://www.ics.uci.edu/~kay/courses/31/namedtuples.html', 'http://www.ics.uci.edu/~kay/courses/31/design-recipe.html', 
         'https://www.cs.uci.edu/events/seminar-series/', 'http://www.ics.uci.edu/~kay/courses/31/python-details.html', 'https://connectedlearning.uci.edu/', 
         'https://www.stat.uci.edu/', 'https://ics.uci.edu/happening/news/?filter%5Baffiliation_posts%5D=1990', 'https://ics.uci.edu/alumni/ics-advisory-board/', 
         '/research-areas/', 'https://ics.uci.edu/academics/undergraduate#major', 'https://www.igb.uci.edu/seminars/', 
         'https://aisc.uci.edu/students/academic-integrity/definitions.php', 'https://ics.uci.edu/people/', 'https://datascience.uci.edu/', 
         'https://goo.gl/maps/xhK6rgUsdX2Xi7Cm7', 'https://docs.python.org/3/library/collections.html', 'https://futurehealth.uci.edu/2020-distinguished-lecture-series/', 
         'https://hpi.ics.uci.edu/hpiuci-2022-grand-opening-event/', 'https://create.ics.uci.edu/events/', 'https://ics.uci.edu/happening/news/', 'https://ics.uci.edu/admissions-information-and-computer-science/', 
         'https://ics.uci.edu/student-experience/', '#a11y-skip-link-content', 'https://www.informatics.uci.edu/explore/department-seminars/', 
         'https://ics.uci.edu/alumni/corporate-engagement/capstone-projects-corporate-engagement/', 'https://em.uci.edu/', 'https://ics.uci.edu/academics/graduate-programs#researchprograms', 
         'https://ics.uci.edu/student-experience/undergraduate-research/', 'https://directory.uci.edu/', 'http://isr.uci.edu/', 'https://ics.uci.edu/seminar-series/distinguished-lectures/', 
         'https://ics.uci.edu/facts-figures/', 'https://www.youtube.com/watch?v=Opjrpgyx9ug', 'https://www.stat.uci.edu/seminar-series/', 
         'https://ics.uci.edu/admissions-information-and-computer-science/admissions-process/', 'http://twitter.com/UCIbrenICS', None, '/accessibility-statement/', 
         'https://ics.uci.edu/academics/impact/academic-placements-of-alumni/', 'https://ics.uci.edu/computing-research/', 'https://ics.uci.edu/alumni/industry-advisory-council/', 
         'https://www.linkedin.com/company/uc-irvine-information-and-computer-sciences', 'https://ics.uci.edu/academics/graduate-programs#professionalprograms', 'https://ics.uci.edu/academics/career-development/', 
         'http://www.ics.uci.edu/~thornton/ics45c/', 'https://hpi.ics.uci.edu/', 'https://ics.uci.edu/follow-us/', 'https://ics.uci.edu/wp-content/uploads/2024/02/tutoring_Feb1_2024_CS364.png'}

url = "https://ics.uci.edu/academics/undergraduate-academic-advising/ics-credit-by-exam/"

def check_for_new_links():
    global links
    while True:
        try:
            current_links = set(get_links(url))
            
            # check for new links
            new_links = current_links - links
            print(new_links)
            if new_links:
                socketio.emit('new_links', {'links': list(new_links)})
                # play sound
                playsound('rapping.mp3')
        except Exception as e:
            pass
        
        time.sleep(COOLDOWN)
        
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('current_links', {'links': list(links)})
    
if __name__ == '__main__':
    import threading
    link_checker_thread = threading.Thread(target=check_for_new_links)
    link_checker_thread.daemon = True
    link_checker_thread.start()
    
    socketio.run(app)
    
    
