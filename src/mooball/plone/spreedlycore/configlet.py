from plone.memoize.instance import memoize

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _p
import spreedlycore

class SpreedlyConfiglet(BrowserView):
    """Spreedly Configlet
    """

    template = ViewPageTemplateFile('configlet.pt')

    def __call__(self):
        self.request.set('disable_border', True)
        
        return self.template()
