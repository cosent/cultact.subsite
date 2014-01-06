from Products.Five.browser import BrowserView


class SubsiteTestView(BrowserView):

    def __call__(self):
        return self.request.get('in_subsite', '')
