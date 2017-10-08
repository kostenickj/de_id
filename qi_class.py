import csv, sys


class qi_rec:
    def __init__(self, sid, course_id, continent, region, pcode, city, subdivision,
                 LoE, YoB, gender, forum_posts, forum_votes, forum_endorsed, forum_threads, forum_comments,
                 forum_pinned,
                 prof_country, email_domain):
        '''
        Create an object that contains only the quasi-identifiers that are not functionally determinable. This will
        lead to a smaller record that can be used to build the generalization and suppression/chaffing tables
        :param sid: The student id
        :param course_id: The course id
        :param region: The region in which the student is identified
        :param pcode: Postal code, which can be used as a key for nearly all of the rest of the location information
        :param LoE: Level of education
        :param YoB: Year of birth
        :param gender: Gender
        :param forum_posts: Number of forum posts
        :param forum_votes: Number of forum votes
        :param forum_endorsed: Number of endorsements in the forums
        :param forum_threads: Number of threads the student of which the student has been a part
        :param forum_comments: Number of forum comments
        :param forum_pinned: Number of posts pinned
        :param prof_country: Self-reported country of origin
        :param email_domain: Email domain
        '''
        self.sid = sid
        self.course_id = course_id
        self.continent = continent
        self.region = region
        self.pcode = pcode
        self.city = city
        self.subdivision = subdivision
        self.LoE = LoE
        self.YoB = YoB
        self.gender = gender
        self.forum_posts = forum_posts
        self.forum_votes = forum_votes
        self.forum_endorsed = forum_endorsed
        self.forum_threads = forum_threads
        self.forum_comments = forum_comments
        self.forum_pinned = forum_pinned
        self.prof_country = prof_country
        self.email_domain = email_domain

    def clean_rec(self):
        self.YoB = clean_YoB(self.YoB)
        self.LoE = clean_LoE(self.LoE)

    def collapse_tails(self):
        self.forum_posts = collapse_forum_posts(self.forum_posts)
        self.forum_votes = collapse_forum_votes(self.forum_votes)
        self.forum_endorsed = collapse_forum_endorsed(self.forum_endorsed)
        self.forum_threads = collapse_forum_threads(self.forum_threads)
        self.forum_comments = collapse_forum_comments(self.forum_comments)
        self.forum_pinned = collapse_pinned_counts(self.forum_pinned)


    def collapse_rec(self):
        self.forum_posts = collapse_forum_posts(self.forum_posts)
        self.forum_comments = collapse_forum_comments(self.forum_comments)
        self.forum_endorsed = collapse_forum_endorsed(self.forum_endorsed)
        self.forum_threads = collapse_forum_threads(self.forum_threads)

    def write_csv_line(self, csv_out):
        '''
        Write a line containing only the quasi-identifiers to a csv file that is handed in as a parameter
        :param csv_out: An open csv.writer to which the line is written
        :return: None
        '''
        outline = self.extract_qi_line()
        csv_out.writerow(outline)
        return None

    def extract_qi_line(self):
        '''
        Create and return a list of quasi-identifiers from a qi_rec that can be written to a .csv file
        :return: A list of quasi-identifiers in the current qi_rec
        '''
        out_line = [self.sid, self.course_id,
                    self.region, self.pcode, self.city, self.continent, self.subdivision,
                    self.LoE, self.YoB, self.gender,
                    self.forum_posts, self.forum_votes, self.forum_endorsed,
                    self.forum_threads, self.forum_comments,
                    self.email_domain]
        return out_line


def clean_YoB(in_year):
    '''
    Check the value supplied for year of birth, and if it seems unlikely/impossible, replace the value with nothing,
    which indicates no reported value. Currently, anyone reporting a birth year prior to 1034 or after 2005 fits the
    unlikely/impossible rubric.
    :param in_year: the year of birth reported
    :return: either the reported year, or the empty string
    '''
    if (in_year < '1934') or (in_year > '2005'):
        in_year = ''
    return in_year


def clean_LoE(loe):
    '''
    Clean the LoE data, mapping responses of null, blank, learn, and Learn to the blank response
    :param loe: self-reported level of education
    :return: either '' or the self-reported level
    '''
    if loe == 'null' or loe == 'learn' or loe == 'Learn':
        loe = ''
    return loe


def collapse_forum_posts(nposts):
    '''
    Collapse the long tail for the count of forum posts; if a value is in the long tail return the minimum count
    in the tail, otherwise return the count handed in
    :param nposts: count of posts on a forum
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if nposts > 57:
        nposts = 57
    return nposts


def collapse_forum_comments(fc_posts):
    '''
    Collapse the long tail for the count of forum comments; if a value is in the long tail return the minimum count
    in the tail, otherwise return the count handed in
    :param fc_posts: count of comments on a forum
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if fc_posts > 54:
        fc_posts = 55
    return fc_posts


def collapse_forum_endorsed(f_endorsed):
    '''
    Collapse the long tail for the count of forum endorsements; if a value is in the long tail return the minimum count
    in the tail, otherwise return the count handed in
    :param f_endorsed: count of endorsements on a forum
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if f_endorsed > 0:
        f_endorsed = 1
    return f_endorsed


def collapse_forum_threads(f_threads):
    '''
    Collapse the long tail for the forum threads, giving all those counts over a particular threshold the value of the
    minimum count
    :param f_threads: Number of threads to check to see if in the long tail
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if f_threads > 26:
        f_threads = 26
    return f_threads

def collapse_forum_votes(votes):
    '''
    Collapse the long tail for the forum votes, giving all those counts over a particular threshold the value of the
    minimum count
    :param votes: Number of votes to check to see if in the long tail
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if votes > 30:
        votes = 30
    return votes


def collapse_event_counts(e_counts):
    '''
    Collapse the long tail for the forum event counts, giving all those counts over a particular threshold the value of the
    minimum count
    :param f_threads: Number of event counts to check to see if in the long tail
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if e_counts >182:
        e_counts = 182
    return e_counts

def collapse_pinned_counts(p_counts):
    '''
    Collapse the long tail for the forum pinned counts, giving all those counts over a particular threshold the value of
    the minimum count
    :param p_counts: Number of pinned counts to check to see if in the long tail
    :return: the number of the smallest count in the tail if the count is in the tail, or the original count otherwise
    '''
    if p_counts > 1:
        p_counts = 1
    return p_counts


def create_from_full_csv(cline):
    '''
    Re-arranges the items in a line read in from a csv file to be in the right order to create a qi_rec. At this point,
    it also removes all of the fields that are either not quasi-identifiers or can be mapped from other information.
    :param cline: A line from a .csv file containing all the information about a student/course pair
    :return: a qi_rec object, initialized with the non-functionally determined quasi-identifiers
    '''
    new_qi = qi_rec(cline[1], cline[0], cline[11],
                    cline[13], cline[15], cline[12], cline[14],
                    cline[22], cline[23], cline[24],
                    cline[34], cline[35], cline[36], cline[37], cline[38], cline[39],
                    cline[51], cline[53])
    return new_qi


def create_header_from_full(cline):
    '''
    Create a header from a .csv line. It is assumed that the .csv line handed in as a parameter is itself a header; this
    just re-arranges the items to correspond to the order used for writing out the qi_rec in qi_rec.write_csv_line.
    :param cline:
    :return:
    '''
    head_qi = create_from_full_csv(cline)
    short_head = head_qi.extract_qi_line()
    return short_head


def register_filter(line):
    '''
    Filter that returns True if the 'registered' flag is set, otherwise returns False. This should always return True
    :param line: Line from the .csv file containing the HarvardX data
    :return: True if the person registered, otherwise false
    '''
    if line[3] == 'True':
        return True
    else:
        return False


def viewed_filter(line):
    '''
    Filter that returns True if the 'viewed' flag is set, otherwise returns False.
    :param line: Line from the .csv file containing the HarvardX data
    :return: True if the person viewed some of the content of the course, otherwise false
    '''
    if line[4] == 'True':
        return True
    else:
        return False


def explored_filter(line):
    '''
    Filter that returns True if the 'explored' flag is set, otherwise returns False.
    :param line: Line from the .csv file containing the HarvardX data
    :return: True if the person explored (i.e., viewed more than half the content) of the course, otherwise false
    '''
    if line[5] == 'True':
        return True
    else:
        return False


def certified_filter(line):
    '''
    Filter that returns True if the 'certified' flag is set, otherwise returns False.
    :param line: Line from the .csv file containing the HarvardX data
    :return: True if the person was certified as completing the course, otherwise false
    '''
    if line[6] == 'True':
        return True
    else:
        return False


def completed_filter(line):
    '''
    Filter that returns True if the 'completed' flag is set, otherwise returns False.
    :param line: Line from the .csv file containing the HarvardX data
    :return: True if the person completed the course, otherwise false
    '''
    if line[7] == 'True':
        return True
    else:
        return False


def get_filter(filter_type):
    '''
    Selects the appropriate level of engagement filter for building the quasi-identifier file, allowing to look
    at all registered students, only those who viewed part of the course, those who explored the course,
    or those who completed or were certified in the course.
    :param filter_type: a single letter indicating the type of filter wanted
    :return: A function that will filter by participation
    '''
    if filter_type == 'r':
        return register_filter
    elif filter_type == 'v':
        return viewed_filter
    elif filter_type == 'e':
        return explored_filter
    elif filter_type == 'c':
        return certified_filter
    elif filter_type == 'f':
        return completed_filter
    else:
        return None


if __name__ == '__main__':
    inf = open(sys.argv[1], 'rU')
    outf = open(sys.argv[2], 'w')
    filter_type = sys.argv[3]
    inc_filter = get_filter(filter_type)
    if inc_filter == None:
        print 'No participation filter specified, defaulting to registered'
        inc_filter = register_filter()

    collapse_long_tail = False
    if sys.argv[4] == 'c':
        collapse_long_tail = True

    cin = csv.reader(inf)
    cout = csv.writer(outf)
    header = cin.next()
    out_header = create_header_from_full(header)
    cout.writerow(out_header)

    for l in cin:
        if (l[40] == 'Student') and inc_filter(l):
            qi = create_from_full_csv(l)
            qi.clean_rec()
            if collapse_long_tail:
                qi.collapse_tails()
            qi.write_csv_line(cout)

    inf.close()
    outf.close()
