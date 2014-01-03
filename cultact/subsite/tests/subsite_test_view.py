from Products.Five.browser import BrowserView


class SubsiteTestView(BrowserView):

    def __call__(self):
        try:
            return self.request.subsite
        except AttributeError:
            return ''
