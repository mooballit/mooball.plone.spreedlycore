from plone.memoize.instance import memoize
from five import grok

from z3c.form import interfaces
from zope import schema
from zope.interface import Interface
from plone.app.registry.browser import controlpanel
from zope.i18nmessageid import MessageFactory

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

from Products.statusmessages.interfaces import IStatusMessage

import spreedlycore

_ = MessageFactory('mooball.plone.spreedlycore')

class ISpreedlyLoginSettings(Interface):
    """Global Spreedly Login settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    
    spreedly_login = schema.TextLine(title=_(u"Spreedly Login"),
                                  description=_(u"spreedly_login",
                                                default=u"Login to Spreedly."),
                                  required=True,
                                  default=u'',)

    spreedly_secret = schema.TextLine(title=_(u"Spreedly Secret"),
                                  description=_(u"spreedly_secret",
                                                default=u"Enter in Spreedly Secret here."),
                                  required=True,
                                  default=u'',)

class SpreedlyLoginSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISpreedlyLoginSettings
    label = _(u"Spreedly Credentials Configuration")
    description = _(u"""""")

    def updateFields(self):
        super(SpreedlyLoginSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SpreedlyLoginSettingsEditForm, self).updateWidgets()

class SpreedlyLoginConfiglet(controlpanel.ControlPanelFormWrapper):
    """Spreedly Login Configlet
    """
    form = SpreedlyLoginSettingsEditForm

class GatewayVocabulary(object):
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ISpreedlyLoginSettings)

        terms = []
        
        if registry is not None:
            connect = spreedlycore.APIConnection(settings.spreedly_login, settings.spreedly_secret)
            gateways = connect.gateways()
            for gateway in gateways:
                terms.append(SimpleVocabulary.createTerm(gateway.data['gateway_type'], str(gateway.token), gateway.data['gateway_type']))
        
        return SimpleVocabulary(terms)

grok.global_utility(GatewayVocabulary, name=u"mooball.plone.spreedlycore.Gateway")

class ISpreedlyGatewaySettings(Interface):
    """Global Spreedly Gateway settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    
    spreedly_gateway = schema.Choice(title=_(u"Spreedly Gateway"),
                                  description=_(u"spreedly_gateway",
                                                default=u"Choose Spreedly Gateway"),
                                  vocabulary=u"mooball.plone.spreedlycore.Gateway",
                                  required=True,)

class SpreedlyGatewaySettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISpreedlyGatewaySettings
    label = _(u"Spreedly Gateway Configuration")
    description = _(u"""""")

    def updateFields(self):
        super(SpreedlyGatewaySettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SpreedlyGatewaySettingsEditForm, self).updateWidgets()

class SpreedlyGatewayConfiglet(controlpanel.ControlPanelFormWrapper):
    """Spreedly Gateway Configlet
    """
    
    form = SpreedlyGatewaySettingsEditForm
