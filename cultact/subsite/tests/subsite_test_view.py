from Products.Five.browser import BrowserView


class SubsiteTestView(BrowserView):

    def __call__(self):
        try:
            return self.request.in_subsite
        except AttributeError:
            return ''
