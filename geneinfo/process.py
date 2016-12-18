# Helper function to handle case where author is lacking a name
def _getAttr(el, attr):
    ret = el.find(attr)
    return '' if ret is None else str(ret.string)


# Given an xml element representing an author, extract information
def _extract_author(title, journal, author):
    affiliations = [
        str(affiliation.string)
        for affiliation in author.find_all('affiliation')
    ]
    email = ''
    for affiliation in affiliations:
        emails = _email_re.findall(affiliation)
        if len(emails) > 0:
            email = emails[0]
    return dict(
        lastName=_getAttr(author, 'lastname'),
        foreName=_getAttr(author, 'forename'),
        affiliation1=_get_affiliation(affiliations, 0),
        affiliation2=_get_affiliation(affiliations, 1),
        affiliation3=_get_affiliation(affiliations, 2),
        affiliation4=_get_affiliation(affiliations, 3),
        email=email,
        title=title,
        journal=journal,
    )


def extract_paper_info(paper):
    return paper.articletitle.string
    # title = paper.articletitle.string
    # journal = paper.journal.title.string
