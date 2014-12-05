import ckanext.ogcpreview.plugin as plugin

class TestOGCPreviewPlugin(object):

    #setup_class executes (auto once) before anything in this class
    @classmethod
    def setup_class(self):
        print ("")
        # get config options

        self.oOGCPreview = plugin.OGCPreview()
        self.OGCFormat = ['wfs', 'wms', 'ogc:wfs', 'ogc:wms']
        self.OGCBadFormat = ['wfs_b', 'wms_b', 'ogc:wfs_b', 'ogc:wms_b']

    #teardown_class executes (auto once) after anything in this class
    @classmethod
    def teardown_class(self):
        print ("")
        self.oOGCPreview = None
        self.OGCBadFormat = None
        del self.oOGCPreview
        del self.OGCBadFormat

    #setup executes before each method in this class
    def setup(self):
        print ("")
        print ("TestUM:setup() before each test method")

    #setup executes after each method in this class
    def teardown(self):
        print ("")
        print ("TestUM:teardown() after each test method")

    #Test method can_preview of OGCPreview Class
    def test_canPreview(self):
        print 'test_canPreview(): Running actual test code ..........................'

        for format in self.OGCFormat:
            params = {u"resource" : {u"format" : format}}
            result = self.oOGCPreview.can_preview(params)

            assert result is True

    #Bad Test method can_preview of OGCPreview Class
    def testBad_canPreview(self):
        print 'testBad_canPreview(): Running actual test code ..........................'

        for format in self.OGCBadFormat:
            params = {u"resource" : {u"format" : format}}
            result = self.oOGCPreview.can_preview(params)

            assert result is False

    #Test method preview_template of OGCPreview Class
    def test_previewTemplate(self):
        print 'test_previewTemplate(): Running actual test code ..........................'

        for format in self.OGCFormat:
            params = {u"resource" : {u"format" : format, u"error": False}}
            result = self.oOGCPreview.preview_template({}, params)
            assert result in ['wfs_preview_template.html', 'wms_preview_template.html']

    #Bad Test method preview_template of OGCPreview Class
    def testBad_previewTemplate(self):
        print 'testBad_previewTemplate(): Running actual test code ..........................'

        for format in self.OGCBadFormat:
            params = {u"resource" : {u"format" : format, u"error": False}}
            result = self.oOGCPreview.preview_template({}, params)
            assert result == 'preview_error.html'
