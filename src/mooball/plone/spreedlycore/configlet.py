from five import grok
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool
from zope.component import adapts

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IRegistry
from zope.component import queryUtility, getUtility

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.events import ConfigurationChangedEvent

from Products.statusmessages.interfaces import IStatusMessage
from zope.i18nmessageid import MessageFactory

import zope.formlib.form
import zope.interface
import plone.app.controlpanel
import zope.schema
import spreedlycore
import urllib2

_ = MessageFactory('mooball.plone.spreedlycore')

class SiteSpreedlyCredentials:
    spreedly_login = None
    spreedly_secret = None
    default_spreedly_gateway = None

    def __init__(self):
        registry = queryUtility(IRegistry)
        if registry is not None:
            settings = registry.forInterface(ISpreedlyLoginSettings)
            self.spreedly_login = settings.spreedly_login
            self.spreedly_secret = settings.spreedly_secret
            self.default_spreedly_gateway = settings.default_spreedly_gateway
        else:
            return None

    def getLogin(self):
        return self.spreedly_login

    def getSecret(self):
        return self.spreedly_secret

    def getGateway(self):
        return self.default_spreedly_gateway

class GatewayVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        """ Named Vocabulary for the default_spreedly_gateway field, update
            contents according to the existing gateways.
        """
        registry = queryUtility(IRegistry)
        terms = []

        if registry is not None:
            settings = registry.forInterface(ISpreedlyLoginSettings)
            if settings.spreedly_login and settings.spreedly_secret:
                connect = spreedlycore.APIConnection(
                    settings.spreedly_login, settings.spreedly_secret)
                gateways = connect.gateways()
                for gateway in gateways:
                    terms.append(SimpleVocabulary.createTerm(
                            unicode(gateway.token),
                            unicode(gateway.token),
                            unicode(gateway.data['gateway_type'])))

        return SimpleVocabulary(terms)
grok.global_utility(GatewayVocabulary,
        name=u"mooball.plone.spreedlycore.Gateway")

class ISpreedlyLoginSettings(zope.interface.Interface):
    """ Global Spreedly Login settings. This describes records stored in the
        configuration registry and obtainable via plone.registry.
    """

    spreedly_login = zope.schema.TextLine(
                            title=_(u"Spreedly Login"),
                            description=_(u"spreedly_login",
                            default=u"Login to Spreedly."),
                            required=True,
                            default=None,)

    spreedly_secret = zope.schema.TextLine(
                            title=_(u"Spreedly Secret"),
                            description=_(u"spreedly_secret",
                            default=u"Enter in Spreedly Secret here."),
                            required=True,
                            default=None,)

    default_spreedly_gateway = zope.schema.Choice(
                            title=_(u"Default Spreedly Gateway"),
                            description=_(u"default_spreedly_gateway",
                            default=(u"Choose the Default Spreedly Gateway. "
                            "Gateway objects must be instantiated via API "
                            "outside this Application")),
                            vocabulary=u"mooball.plone.spreedlycore.Gateway",
                            required=False,
                            default=None,)

class SpreedlySettingsControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    zope.interface.implements(ISpreedlyLoginSettings)

    def __init__(self, context):
        super(SpreedlySettingsControlPanelAdapter, self).__init__(context)
        registry = queryUtility(IRegistry)
        if registry is not None:
            self.settings = registry.forInterface(ISpreedlyLoginSettings)
        else:
            self.settings = None

    def get_spreedly_login(self):
        return self.settings.spreedly_login

    def set_spreedly_login(self, login):
        self.settings.spreedly_login = login

    def get_spreedly_secret(self):
        return self.settings.spreedly_secret

    def set_spreedly_secret(self, secret):
        self.settings.spreedly_secret = secret

    def get_default_spreedly_gateway(self):
        return self.settings.default_spreedly_gateway

    def set_default_spreedly_gateway(self, gateway):
        self.settings.default_spreedly_gateway = gateway

    spreedly_login = property(get_spreedly_login, set_spreedly_login)
    spreedly_secret = property(get_spreedly_secret, set_spreedly_secret)
    default_spreedly_gateway = property(
        get_default_spreedly_gateway, set_default_spreedly_gateway)

class SpreedlySettings(ControlPanelForm):
    zope.interface.implements(ISpreedlyLoginSettings)

    id = u"SpreedlyLoginSettingsForm"
    form_name = u"Spreedly Credentials Configuration"
    description = u""""""
    form_fields = zope.formlib.form.FormFields(ISpreedlyLoginSettings)

    @zope.formlib.form.action(u'Save', name=u'save')
    def handle_edit_action(self, action, data):
        """ When save button pressed, check for errors, attempt to connect to
            API, and throw error if key wrong, otherwise, continue.
        """
        plone.protect.CheckAuthenticator(self.request)
        self.context.manage_changeProperties(**data)

        try:
            connect = spreedlycore.APIConnection(
                    data['spreedly_login'],
                    data['spreedly_secret'])
            gateway = connect.gateways()
        except urllib2.HTTPError, e:
            IStatusMessage(self.request).addStatusMessage(
                    _(u"The credentials that were provided are incorrect. "
                    "SpreedlyCore.com returned " + unicode(e)), "error")
            self.context.REQUEST.RESPONSE.redirect("@@spreedly_settings")
            return

        zope.formlib.form.applyChanges(
                self.context, self.form_fields, data,self.adapters)

        zope.event.notify(ConfigurationChangedEvent(self, data))
        self.status = "Changes saved."
        self.context.REQUEST.RESPONSE.redirect("@@spreedly_settings")

    @zope.formlib.form.action(u'Cancel', name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(
                _("Changes canceled."), type="info")
        return self.request.response.redirect(
                self.context.absolute_url() + '/plone_control_panel')
