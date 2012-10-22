from Products.CMFCore.utils import getToolByName

def uninstall(portal, reinstall=False):
    if not reinstall:
        profile = 'profile-%s:uninstall' % "mooball.plone.spreedlycore"
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return "Ran all uninstall steps."
