import logging

import simplejson

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sqlalchemy import and_, desc, func, or_, select

from silcc.lib.base import BaseController, render
from silcc.lib.tweettagger import TweetTagger
from silcc.model import Place
from silcc.model.meta import Session


log = logging.getLogger(__name__)

class ApiController(BaseController):

    def index(self):
        return render('/silcc_api_demo.mako')

    def extract_tags(self):

        text = request.params.get('text')
        if text:
            log.info('Text to be tagged: %s', text)
            tags = TweetTagger.tag(text)
            log.info('Tags extracted: %s', str(tags))
            return simplejson.dumps(tags)
        else:
            return render('/silcc_api_demo.mako')


