from plone.memoize.instance import memoize
from five import grok

from z3c.form import interfaces
from z3c.form import button
from zope import schema
from zope.interface import Interface
from plone.app.registry.browser import controlpanel
from zope.i18nmessageid import MessageFactory

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IRegistry
from plone.registry import field
from zope.component import queryUtility

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import spreedlycore
import urllib2

_ = MessageFactory('mooball.plone.spreedlycore')

class GatewayVocabulary(object):
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        
        if registry is not None:
            settings = registry.forInterface(ISpreedlyLoginSettings)
            if settings.spreedly_login and settings.spreedly_secret:
                connect = spreedlycore.APIConnection(settings.spreedly_login, settings.spreedly_secret)
                gateways = connect.gateways()
                for gateway in gateways:
                    terms.append(SimpleVocabulary.createTerm(unicode(gateway.token), unicode(gateway.data['gateway_type']), unicode(gateway.data['gateway_type'])))
        
        return SimpleVocabulary(terms)
grok.global_utility(GatewayVocabulary, name=u"mooball.plone.spreedlycore.Gateway")

class ISpreedlyLoginSettings(Interface):
    """Global Spreedly Login settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    
    spreedly_login = field.TextLine(title=_(u"Spreedly Login"),
                                  description=_(u"spreedly_login",
                                                default=u"Login to Spreedly."),
                                  required=True,
                                  default=None,)

    spreedly_secret = field.TextLine(title=_(u"Spreedly Secret"),
                                  description=_(u"spreedly_secret",
                                                default=u"Enter in Spreedly Secret here."),
                                  required=True,
                                  default=None,)
    
    default_spreedly_gateway = field.Choice(title=_(u"Default Spreedly Gateway"),
                                  description=_(u"default_spreedly_gateway",
                                                default=u"Choose the Default Spreedly Gateway"),
                                  vocabulary=u"mooball.plone.spreedlycore.Gateway",
                                  required=False,
                                  default=None,)

class SpreedlyLoginSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISpreedlyLoginSettings
    id = u"SpreedlyLoginSettingsEditForm"
    label = _(u"Spreedly Credentials Configuration")
    description = _(u"""""")

    def updateFields(self):
        super(SpreedlyLoginSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SpreedlyLoginSettingsEditForm, self).updateWidgets()
    
    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        
        if errors:
            self.status = self.formErrorsMessage
            return
        
        try:
            connect = spreedlycore.APIConnection(data['spreedly_login'], data['spreedly_secret'])
            gateway = connect.gateways()
        except urllib2.HTTPError, e:
            IStatusMessage(self.request).addStatusMessage(_(u"The credentials that were provided are incorrect. " + unicode(e)), "error")
            self.context.REQUEST.RESPONSE.redirect("@@spreedly_loginconfig")
            return
        
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@spreedly_loginconfig")
    
    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))

class SpreedlyLoginConfiglet(controlpanel.ControlPanelFormWrapper):
    """Spreedly Login Configlet
    """
    form = SpreedlyLoginSettingsEditForm
    index = ViewPageTemplateFile('configlet.pt')

    def settings(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ISpreedlyLoginSettings, check=False)
        output = []
        
        if settings.spreedly_login:
            output.append("spreedly_login")
        
        if settings.spreedly_secret:
            output.append("spreedly_secret")
        
        if settings.default_spreedly_gateway:
            output.append("default_spreedly_gateway")
        
        return ' '.join(output)
    
    def gateway_info(self):
        classes = self.settings()
        
        if "spreedly_login" in classes and "spreedly_secret" in classes:
            return False
        else:
            return True
