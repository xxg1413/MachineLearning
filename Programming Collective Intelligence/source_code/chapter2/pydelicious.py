"""Library to access del.icio.us data via Python.

:examples:

  Using the API class directly:

  >>> a = pydelicious.apiNew('user', 'passwd')
  >>> # or:
  >>> a = DeliciousAPI('user', 'passwd')
  >>> a.tags_get() # Same as:
  >>> a.request('tags/get', )

  Or by calling the 'convenience' methods on the module.

  - def add(user, passwd, url, description, tags = "", extended = "", dt = "", replace="no"):
  - def get(user, passwd, tag="", dt="",  count = 0):
  - def get_all(user, passwd, tag = ""):
  - def delete(user, passwd, url):
  - def rename_tag(user, passwd, oldtag, newtag):
  - def get_tags(user, passwd):

  >>> a = apiNew(user, passwd)
  >>> a.posts_add(url="http://my.com/", desciption="my.com", extended="the url is my.moc", tags="my com")
  True
  >>> len(a.posts_all())
  1
  >>> get_all(user, passwd)
  1

  This are short functions for getrss calls.

  >>> rss_

def get_userposts(user):
def get_tagposts(tag):
def get_urlposts(url):
def get_popular(tag = ""):

  >>> json_posts()
  >>> json_tags()
  >>> json_network()
  >>> json_fans()

:License: pydelicious is released under the BSD license. See 'license.txt'
 for more informations.

:berend:
 - Rewriting comments to english. More documentation, examples.
 - Added JSON-like return values for XML data (del.icio.us also serves some JSON...)
 - better error/exception classes and handling, work in progress.
 - Encoding seems to be working (using UTF-8 here).

:@todo:
 - Source code SHOULD BE ASCII!
 - More tests.
 - Parse datetimes in XML.
 - Salvage and test RSS functionality?
 - Setup not used, Still works? Should setup.py be tested?
 - API functions need required argument checks.

 * lizense einbinden und auch via setup.py verteilen
 * readme auch schreiben und via setup.py verteilen
 * auch auf anderen systemen testen (linux -> uni)
 * automatisch releases bauen lassen, richtig benennen und in das
   richtige verzeichnis verschieben.
 * was k[o]nnen die anderen librarys denn noch so? (ruby, java, perl, etc)
 * was wollen die, die es benutzen?
 * wof[u]r k[o]nnte ich es benutzen?
 * entschlacken?

:done:
 * Refactored the API class, much cleaner now and functions dlcs_api_request, dlcs_parse_xml are available for who wants them.
 * stimmt das so? muss eher noch t[a]g str2utf8 konvertieren
   >>> pydelicious.getrss(tag="t[a]g")
   url: http://del.icio.us/rss/tag/t[a]g
 * requester muss eine sekunde warten
 * __init__.py gibt die funktionen weiter
 * html parser funktioniert noch nicht, gar nicht
 * alte funktionen fehlen, get_posts_by_url, etc.
 * post funktion erstellen, die auch die fehlenden attribs addiert.
 * die api muss ich noch weiter machen
 * requester muss die 503er abfangen
 * rss parser muss auf viele m[o]glichkeiten angepasst werden
"""
import sys
import os
import time
import datetime
import md5, httplib
import urllib, urllib2, time
from StringIO import StringIO

try:
    from elementtree.ElementTree import parse as parse_xml
except ImportError:
    from  xml.etree.ElementTree import parse as parse_xml

import feedparser


### Static config

__version__ = '0.5.0'
__author__ = 'Frank Timmermann <regenkind_at_gmx_dot_de>' # GP: does not respond to emails
__contributors__ = [
    'Greg Pinero',
    'Berend van Berkum <berend+pydelicious@dotmpe.com>']
__url__ = 'http://code.google.com/p/pydelicious/'
__author_email__ = ""
# Old URL: 'http://deliciouspython.python-hosting.com/'

__description__ = '''pydelicious.py allows you to access the web service of del.icio.us via it's API through python.'''
__long_description__ = '''the goal is to design an easy to use and fully functional python interface to del.icio.us. '''

DLCS_OK_MESSAGES = ('done', 'ok') # Known text values of positive del.icio.us <result> answers
DLCS_WAIT_TIME = 4
DLCS_REQUEST_TIMEOUT = 444 # Seconds before socket triggers timeout
#DLCS_API_REALM = 'del.icio.us API'
DLCS_API_HOST = 'https://api.del.icio.us'
DLCS_API_PATH = 'v1'
DLCS_API = "%s/%s" % (DLCS_API_HOST, DLCS_API_PATH)
DLCS_RSS = 'http://del.icio.us/rss/'

ISO_8601_DATETIME = '%Y-%m-%dT%H:%M:%SZ'

USER_AGENT = 'pydelicious.py/%s %s' % (__version__, __url__)

DEBUG = 0
if 'DLCS_DEBUG' in os.environ:
    DEBUG = int(os.environ['DLCS_DEBUG'])


# Taken from FeedParser.py
# timeoutsocket allows feedparser to time out rather than hang forever on ultra-slow servers.
# Python 2.3 now has this functionality available in the standard socket library, so under
# 2.3 you don't need to install anything.  But you probably should anyway, because the socket
# module is buggy and timeoutsocket is better.
try:
    import timeoutsocket # http://www.timo-tasi.org/python/timeoutsocket.py
    timeoutsocket.setDefaultSocketTimeout(DLCS_REQUEST_TIMEOUT)
except ImportError:
    import socket
    if hasattr(socket, 'setdefaulttimeout'): socket.setdefaulttimeout(DLCS_REQUEST_TIMEOUT)
if DEBUG: print >>sys.stderr, "Set socket timeout to %s seconds" % DLCS_REQUEST_TIMEOUT


### Utility classes

class _Waiter:
    """Waiter makes sure a certain amount of time passes between
    successive calls of `Waiter()`.

    Some attributes:
    :last: time of last call
    :wait: the minimum time needed between calls
    :waited: the number of calls throttled

    pydelicious.Waiter is an instance created when the module is loaded.
    """
    def __init__(self, wait):
        self.wait = wait
        self.waited = 0
        self.lastcall = 0;

    def __call__(self):
        tt = time.time()

        timeago = tt - self.lastcall

        if self.lastcall and DEBUG>2:
            print >>sys.stderr, "Lastcall: %s seconds ago." % lastcall

        if timeago <= self.wait:
            if DEBUG>0: print >>sys.stderr, "Waiting %s seconds." % self.wait
            time.sleep(self.wait)
            self.waited += 1
            self.lastcall = tt + self.wait
        else:
            self.lastcall = tt

Waiter = _Waiter(DLCS_WAIT_TIME)

class PyDeliciousException(Exception):
    '''Std. pydelicious error'''
    pass

class DeliciousError(Exception):
	"""Raised when the server responds with a negative answer"""


class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    '''@xxx:bvb: Where is this used? should it be registered somewhere with urllib2?

    Handles HTTP Error, currently only 503.
    '''
    def http_error_503(self, req, fp, code, msg, headers):
        raise urllib2.HTTPError(req, code, throttled_message, headers, fp)


class post(dict):
    """Post object, contains href, description, hash, dt, tags,
    extended, user, count(, shared).

    @xxx:bvb: Is this needed? Right now this is superfluous,
    """
    def __init__(self, href = "", description = "", hash = "", time = "", tag = "", extended = "", user = "", count = "",
                 tags = "", url = "", dt = ""): # tags or tag?
        self["href"] = href
        if url != "": self["href"] = url
        self["description"] = description
        self["hash"] = hash
        self["dt"] = dt
        if time != "": self["dt"] = time
        self["tags"] = tags
        if tag != "":  self["tags"] = tag     # tag or tags? # !! tags
        self["extended"] = extended
        self["user"] = user
        self["count"] = count

    def __getattr__(self, name):
        try: return self[name]
        except: object.__getattribute__(self, name)


class posts(list):
    """@xxx:bvb: idem as class post, python structures (dict/list) might
    suffice or a more generic solution is needed.
    """
    def __init__(self, *args):
        for i in args: self.append(i)

    def __getattr__(self, attr):
        try: return [p[attr] for p in self]
        except: object.__getattribute__(self, attr)

### Utility functions

def str2uni(s):
    # type(in) str or unicode
    # type(out) unicode
    return ("".join([unichr(ord(i)) for i in s]))

def str2utf8(s):
    # type(in) str or unicode
    # type(out) str
    return ("".join([unichr(ord(i)).encode("utf-8") for i in s]))

def str2quote(s):
    return urllib.quote_plus("".join([unichr(ord(i)).encode("utf-8") for i in s]))

def dict0(d):
    # Trims empty dict entries
    # {'a':'a', 'b':'', 'c': 'c'} => {'a': 'a', 'c': 'c'}
    dd = dict()
    for i in d:
            if d[i] != "": dd[i] = d[i]
    return dd

def delicious_datetime(str):
    """Parse a ISO 8601 formatted string to a Python datetime ...
    """
    return datetime.datetime(*time.strptime(str, ISO_8601_DATETIME)[0:6])

def http_request(url, user_agent=USER_AGENT, retry=4):
    """Retrieve the contents referenced by the URL using urllib2.

    Retries up to four times (default) on exceptions.
    """
    request = urllib2.Request(url, headers={'User-Agent':user_agent})

    # Remember last error
    e = None

    # Repeat request on time-out errors
    tries = retry;
    while tries:
        try:
            return urllib2.urlopen(request)

        except urllib2.HTTPError, e: # protocol errors,
            raise PyDeliciousException, "%s" % e

        except urllib2.URLError, e:
            # @xxx: Ugly check for time-out errors
			#if len(e)>0 and 'timed out' in arg[0]:
			print >> sys.stderr, "%s, %s tries left." % (e, tries)
			Waiter()
			tries = tries - 1
			#else:
			#	tries = None

    # Give up
    raise PyDeliciousException, \
            "Unable to retrieve data at '%s', %s" % (url, e)

def http_auth_request(url, host, user, passwd, user_agent=USER_AGENT):
    """Call an HTTP server with authorization credentials using urllib2.
    """
    if DEBUG: httplib.HTTPConnection.debuglevel = 1

    # Hook up handler/opener to urllib2
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, host, user, passwd)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    return http_request(url, user_agent)

def dlcs_api_request(path, params='', user='', passwd='', throttle=True):
    """Retrieve/query a path within the del.icio.us API.

    This implements a minimum interval between calls to avoid
    throttling. [#]_ Use param 'throttle' to turn this behaviour off.

    @todo: back off on 503's (HTTPError, URLError? @todo: testing).

    Returned XML does not always correspond with given del.icio.us examples
    @todo: (cf. help/api/... and post's attributes)

    .. [#] http://del.icio.us/help/api/
    """
    if throttle:
        Waiter()

    if params:
        # params come as a dict, strip empty entries and urlencode
        url = "%s/%s?%s" % (DLCS_API, path, urllib.urlencode(dict0(params)))
    else:
        url = "%s/%s" % (DLCS_API, path)

    if DEBUG: print >>sys.stderr, "dlcs_api_request: %s" % url

    try:
        return http_auth_request(url, DLCS_API_HOST, user, passwd, USER_AGENT)

    # @bvb: Is this ever raised? When?
    except DefaultErrorHandler, e:
        print >>sys.stderr, "%s" % e

def dlcs_parse_xml(data, split_tags=False):
    """Parse any del.icio.us XML document and return Python data structure.

    Recognizes all XML document formats as returned by the version 1 API and
    translates to a JSON-like data structure (dicts 'n lists).

    Returned instance is always a dictionary. Examples::

     {'posts': [{'url':'...','hash':'...',},],}
     {'tags':['tag1', 'tag2',]}
     {'dates': [{'count':'...','date':'...'},], 'tag':'', 'user':'...'}
	 {'result':(True, "done")}
     # etcetera.
    """

    if DEBUG>3: print >>sys.stderr, "dlcs_parse_xml: parsing from ", data

    if not hasattr(data, 'read'):
        data = StringIO(data)

    doc = parse_xml(data)
    root = doc.getroot()
    fmt = root.tag

	# Split up into three cases: Data, Result or Update
    if fmt in ('tags', 'posts', 'dates', 'bundles'):

        # Data: expect a list of data elements, 'resources'.
        # Use `fmt` (without last 's') to find data elements, elements
        # don't have contents, attributes contain all the data we need:
        # append to list
        elist = [el.attrib for el in doc.findall(fmt[:-1])]

        # Return list in dict, use tagname of rootnode as keyname.
        data = {fmt: elist}

        # Root element might have attributes too, append dict.
        data.update(root.attrib)

        return data

    elif fmt == 'result':

        # Result: answer to operations
        if root.attrib.has_key('code'):
            msg = root.attrib['code']
        else:
            msg = root.text

		# Return {'result':(True, msg)} for /known/ O.K. messages,
        # use (False, msg) otherwise
        v = msg in DLCS_OK_MESSAGES
        return {fmt: (v, msg)}

    elif fmt == 'update':

        # Update: "time"
        #return {fmt: root.attrib}
		return {fmt: {'time':time.strptime(root.attrib['time'], ISO_8601_DATETIME)}}

    else:
        raise PyDeliciousException, "Unknown XML document format '%s'" % fmt

def dlcs_rss_request(tag = "", popular = 0, user = "", url = ''):
    """Handle a request for RSS

    @todo: translate from German

    rss sollte nun wieder funktionieren, aber diese try, except scheisse ist so nicht schoen

    rss wird unterschiedlich zusammengesetzt. ich kann noch keinen einheitlichen zusammenhang
    zwischen daten (url, desc, ext, usw) und dem feed erkennen. warum k[o]nnen die das nicht einheitlich machen?
    """
    tag = str2quote(tag)
    user = str2quote(user)
    if url != '':
        # http://del.icio.us/rss/url/efbfb246d886393d48065551434dab54
        url = DLCS_RSS + '''url/%s'''%md5.new(url).hexdigest()
    elif user != '' and tag != '':
        url = DLCS_RSS + '''%(user)s/%(tag)s'''%dict(user=user, tag=tag)
    elif user != '' and tag == '':
        # http://del.icio.us/rss/delpy
        url = DLCS_RSS + '''%s'''%user
    elif popular == 0 and tag == '':
        url = DLCS_RSS
    elif popular == 0 and tag != '':
        # http://del.icio.us/rss/tag/apple
        # http://del.icio.us/rss/tag/web2.0
        url = DLCS_RSS + "tag/%s"%tag
    elif popular == 1 and tag == '':
        url = DLCS_RSS + '''popular/'''
    elif popular == 1 and tag != '':
        url = DLCS_RSS + '''popular/%s'''%tag
    rss = http_request(url).read()
    rss = feedparser.parse(rss)
    # print rss
#     for e in rss.entries: print e;print
    l = posts()
    for e in rss.entries:
        if e.has_key("links") and e["links"]!=[] and e["links"][0].has_key("href"):
            url = e["links"][0]["href"]
        elif e.has_key("link"):
            url = e["link"]
        elif e.has_key("id"):
            url = e["id"]
        else:
            url = ""
        if e.has_key("title"):
            description = e['title']
        elif e.has_key("title_detail") and e["title_detail"].has_key("title"):
            description = e["title_detail"]['value']
        else:
            description = ''
        try: tags = e['categories'][0][1]
        except:
            try: tags = e["category"]
            except: tags = ""
        if e.has_key("modified"):
            dt = e['modified']
        else:
            dt = ""
        if e.has_key("summary"):
            extended = e['summary']
        elif e.has_key("summary_detail"):
            e['summary_detail']["value"]
        else:
            extended = ""
        if e.has_key("author"):
            user = e['author']
        else:
            user = ""
#  time = dt ist weist auf ein problem hin
# die benennung der variablen ist nicht einheitlich
#  api senden und
#  xml bekommen sind zwei verschiedene schuhe :(
        l.append(post(url = url, description = description, tags = tags, dt = dt, extended = extended, user = user))
    return l


### Main module class

class DeliciousAPI:
    """Class providing main interace to del.icio.us API.

    Methods ``request`` and ``request_raw`` represent the core. For all API
    paths there are furthermore methods (e.g. posts_add for 'posts/all') with
    an explicit declaration of the parameters and documentation. These all call
    ``request`` and pass on extra keywords like ``_raw``.
    """

    def __init__(self, user, passwd, codec='iso-8859-1', api_request=dlcs_api_request, xml_parser=dlcs_parse_xml):
        """Initialize access to the API with ``user`` and ``passwd``.

        ``codec`` sets the encoding of the arguments.

        The ``api_request`` and ``xml_parser`` parameters by default point to
        functions within this package with standard implementations to
        request and parse a resource. See ``dlcs_api_request()`` and
        ``dlcs_parse_xml()``. Note that ``api_request`` should return a
        file-like instance with an HTTPMessage instance under ``info()``,
        see ``urllib2.openurl`` for more info.
        """
        assert user != ""
        self.user = user
        self.passwd = passwd
        self.codec = codec

        # Implement communication to server and parsing of respons messages:
        assert callable(api_request)
        self._api_request = api_request
        assert callable(xml_parser)
        self._parse_response = xml_parser

    def _call_server(self, path, **params):
        params = dict0(params)
        for key in params:
            params[key] = params[key].encode(self.codec)

        # see __init__ for _api_request()
        return self._api_request(path, params, self.user, self.passwd)


    ### Core functionality

    def request(self, path, _raw=False, **params):
        """Calls a path in the API, parses the answer to a JSON-like structure by
        default. Use with ``_raw=True`` or ``call request_raw()`` directly to
        get the filehandler and process the response message manually.

        Calls to some paths will return a `result` message, i.e.::

            <result code="..." />

        or::

            <result>...</result>

        These are all parsed to ``{'result':(Boolean, MessageString)}`` and this
        method will raise ``DeliciousError`` on negative `result` answers. Using
        ``_raw=True`` bypasses all parsing and will never raise ``DeliciousError``.

        See ``dlcs_parse_xml()`` and ``self.request_raw()``."""

        # method _parse_response is bound in `__init__()`, `_call_server`
        # uses `_api_request` also set in `__init__()`
        if _raw:
            # return answer
            return self.request_raw(path, **params)

        else:
            # get answer and parse
            fl = self._call_server(path, **params)
            rs = self._parse_response(fl)

			# Raise an error for negative 'result' answers
            if type(rs) == dict and rs == 'result' and not rs['result'][0]:
                errmsg = ""
                if len(rs['result'])>0:
                    errmsg = rs['result'][1:]
                raise DeliciousError, errmsg

            return rs

    def request_raw(self, path, **params):
        """Calls the path in the API, returns the filehandle. Returned
        file-like instances have an ``HTTPMessage`` instance with HTTP header
        information available. Use ``filehandle.info()`` or refer to the
        ``urllib2.openurl`` documentation.
        """
        # see `request()` on how the response can be handled
        return self._call_server(path, **params)

    ### Explicit declarations of API paths, their parameters and docs

    # Tags
    def tags_get(self, **kwds):
        """Returns a list of tags and the number of times it is used by the user.
        ::

            <tags>
                <tag tag="TagName" count="888">
        """
        return self.request("tags/get", **kwds)

    def tags_rename(self, old, new, **kwds):
        """Rename an existing tag with a new tag name. Returns a `result`
        message or raises an ``DeliciousError``. See ``self.request()``.

        &old (required)
            Tag to rename.
        &new (required)
            New name.
        """
        return self.request("tags/rename", old=old, new=new, **kwds)

    # Posts
    def posts_update(self, **kwds):
        """Returns the last update time for the user. Use this before calling
        `posts_all` to see if the data has changed since the last fetch.
        ::

            <update time="CCYY-MM-DDThh:mm:ssZ">
		"""
        return self.request("posts/update", **kwds)

    def posts_dates(self, tag="", **kwds):
        """Returns a list of dates with the number of posts at each date.
        ::

            <dates>
                <date date="CCYY-MM-DD" count="888">

        &tag (optional).
            Filter by this tag.
        """
        return self.request("posts/dates", tag=tag, **kwds)

    def posts_get(self, tag="", dt="", url="", **kwds):
        """Returns posts matching the arguments. If no date or url is given,
        most recent date will be used.
        ::

            <posts dt="CCYY-MM-DD" tag="..." user="...">
                <post ...>

        &tag (optional).
            Filter by this tag.
        &dt (optional).
            Filter by this date (CCYY-MM-DDThh:mm:ssZ).
        &url (optional).
            Filter by this url.
        """
        return self.request("posts/get", tag=tag, dt=dt, url=url, **kwds)

    def posts_recent(self, tag="", count="", **kwds):
        """Returns a list of the most recent posts, filtered by argument.
        ::

            <posts tag="..." user="...">
                <post ...>

        &tag (optional).
            Filter by this tag.
        &count (optional).
            Number of items to retrieve (Default:15, Maximum:100).
        """
        return self.request("posts/recent", tag=tag, count=count, **kwds)

    def posts_all(self, tag="", **kwds):
        """Returns all posts. Please use sparingly. Call the `posts_update`
        method to see if you need to fetch this at all.
        ::

            <posts tag="..." user="..." update="CCYY-MM-DDThh:mm:ssZ">
                <post ...>

        &tag (optional).
            Filter by this tag.
        """
        return self.request("posts/all", tag=tag, **kwds)

    def posts_add(self, url, description, extended="", tags="", dt="",
            replace="no", shared="yes", **kwds):
        """Add a post to del.icio.us. Returns a `result` message or raises an
        ``DeliciousError``. See ``self.request()``.

        &url (required)
            the url of the item.
        &description (required)
            the description of the item.
        &extended (optional)
            notes for the item.
        &tags (optional)
            tags for the item (space delimited).
        &dt (optional)
            datestamp of the item (format "CCYY-MM-DDThh:mm:ssZ").

        Requires a LITERAL "T" and "Z" like in ISO8601 at http://www.cl.cam.ac.uk/~mgk25/iso-time.html for example: "1984-09-01T14:21:31Z"
        &replace=no (optional) - don't replace post if given url has already been posted.
        &shared=no (optional) - make the item private
        """
        return self.request("posts/add", url=url, description=description,
                extended=extended, tags=tags, dt=dt,
                replace=replace, shared=shared, **kwds)

    def posts_delete(self, url, **kwds):
        """Delete a post from del.icio.us. Returns a `result` message or
        raises an ``DeliciousError``. See ``self.request()``.

        &url (required)
            the url of the item.
        """
        return self.request("posts/delete", url=url, **kwds)

    # Bundles
    def bundles_all(self, **kwds):
        """Retrieve user bundles from del.icio.us.
        ::

            <bundles>
                <bundel name="..." tags=...">
        """
        return self.request("tags/bundles/all", **kwds)

    def bundles_set(self, bundle, tags, **kwds):
        """Assign a set of tags to a single bundle, wipes away previous
        settings for bundle. Returns a `result` messages or raises an
        ``DeliciousError``. See ``self.request()``.

        &bundle (required)
            the bundle name.
        &tags (required)
            list of tags (space seperated).
        """
        if type(tags)==list:
            tags = " ".join(tags)
        return self.request("tags/bundles/set", bundle=bundle, tags=tags,
                **kwds)

    def bundles_delete(self, bundle, **kwds):
        """Delete a bundle from del.icio.us. Returns a `result` message or
        raises an ``DeliciousError``. See ``self.request()``.

        &bundle (required)
            the bundle name.
        """
        return self.request("tags/bundles/delete", bundle=bundle, **kwds)

    ### Utils

    # Lookup table for del.icio.us url-path to DeliciousAPI method.
    paths = {
        'tags/get': tags_get,
        'tags/rename': tags_rename,
        'posts/update': posts_update,
        'posts/dates': posts_dates,
        'posts/get': posts_get,
        'posts/recent': posts_recent,
        'posts/all': posts_all,
        'posts/add': posts_add,
        'posts/delete': posts_delete,
        'tags/bundles/all': bundles_all,
        'tags/bundles/set': bundles_set,
        'tags/bundles/delete': bundles_delete,
    }

    def get_url(self, url):
        """Return the del.icio.us url at which the HTML page with posts for
        ``url`` can be found.
        """
        return "http://del.icio.us/url/?url=%s" % (url,)


### Convenience functions on this package

def apiNew(user, passwd):
    """creates a new DeliciousAPI object.
    requires user(name) and passwd
	"""
    return DeliciousAPI(user=user, passwd=passwd)

def add(user, passwd, url, description, tags="", extended="", dt="", replace="no"):
    return apiNew(user, passwd).posts_add(url=url, description=description, extended=extended, tags=tags, dt=dt, replace=replace)

def get(user, passwd, tag="", dt="",  count = 0):
    posts = apiNew(user, passwd).posts_get(tag=tag,dt=dt)
    if count != 0: posts = posts[0:count]
    return posts

def get_all(user, passwd, tag=""):
    return apiNew(user, passwd).posts_all(tag=tag)

def delete(user, passwd, url):
    return apiNew(user, passwd).posts_delete(url=url)

def rename_tag(user, passwd, oldtag, newtag):
    return apiNew(user=user, passwd=passwd).tags_rename(old=oldtag, new=newtag)

def get_tags(user, passwd):
    return apiNew(user=user, passwd=passwd).tags_get()


### RSS functions @bvb: still working...?
def getrss(tag="", popular=0, url='', user=""):
    """get posts from del.icio.us via parsing RSS @bvb[or HTML]

	@bvb[not tested]

    tag (opt) sort by tag
    popular (opt) look for the popular stuff
    user (opt) get the posts by a user, this striks popular
    url (opt) get the posts by url
	"""
    return dlcs_rss_request(tag=tag, popular=popular, user=user, url=url)

def get_userposts(user):
    return getrss(user = user)

def get_tagposts(tag):
    return getrss(tag = tag)

def get_urlposts(url):
    return getrss(url = url)

def get_popular(tag = ""):
    return getrss(tag = tag, popular = 1)


### @TODO: implement JSON fetching
def json_posts(user, count=15):
    """http://del.icio.us/feeds/json/mpe
    http://del.icio.us/feeds/json/mpe/art+history
    count=###   the number of posts you want to get (default is 15, maximum is 100)
    raw         a raw JSON object is returned, instead of an object named Delicious.posts
    """

def json_tags(user, atleast, count, sort='alpha'):
    """http://del.icio.us/feeds/json/tags/mpe
    atleast=###         include only tags for which there are at least ### number of posts
    count=###           include ### tags, counting down from the top
    sort={alpha|count}  construct the object with tags in alphabetic order (alpha), or by count of posts (count)
    callback=NAME       wrap the object definition in a function call NAME(...), thus invoking that function when the feed is executed
    raw                 a pure JSON object is returned, instead of code that will construct an object named Delicious.tags
    """

def json_network(user):
    """http://del.icio.us/feeds/json/network/mpe
    callback=NAME       wrap the object definition in a function call NAME(...)
    ?raw         a raw JSON object is returned, instead of an object named Delicious.posts
    """

def json_fans(user):
    """http://del.icio.us/feeds/json/fans/mpe
    callback=NAME       wrap the object definition in a function call NAME(...)
    ?raw         a pure JSON object is returned, instead of an object named Delicious.
    """

