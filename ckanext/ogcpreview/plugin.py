import ckan.plugins as p
import ckanext.ogcpreview.model.process as process
from pylons import config
from urlparse import urlparse

class OGCPreview(p.SingletonPlugin):
    '''
    Custom class to add support to the Recline.js CKAN preview feature.
    '''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)

    OGC = ['wfs', 'wms', 'ogc:wfs', 'ogc:wms']

    # Add new resource containing libraries, scripts, etc. to the global config
    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-ogcpreview')

    # If the resource protocol is a WFS or WMS, then we can preview it
    def can_preview(self, data_dict):
        format = data_dict['resource']['format'].lower()
        return format in self.OGC

    # Get the GML service for our resource and parse it into a JSON object
    # that is compatible with recline.  Bind that JSON object to the
    # CKAN resource in order to pass it client-side.
    def setup_template_variables(self, context, data_dict):
        try:
            resource = data_dict["resource"]
            format = resource["format"].lower()
            if format in ['wms', 'ogc:wms']:

                # for ogc:wms use url_ogc else use url
                resourceURL = resource.get("url_ogc", {})
                if not resourceURL:
                    resourceURL = resource.get("url", {})

                armchair = process.HandleWMS(resourceURL)
                ottoman = armchair.get_layer_info(resource)
                p.toolkit.c.resource["layer"] = ottoman["layer"]
                p.toolkit.c.resource["bbox"] = ottoman["bbox"]
                p.toolkit.c.resource["srs"] = ottoman["srs"]
                p.toolkit.c.resource["tile_format"] = ottoman["tile_format"]
                p.toolkit.c.resource["service_url"] = ottoman["service_url"]
                p.toolkit.c.resource["error"] = False
            elif format in ['wfs', 'ogc:wfs']:

                # for ogc:wfs use url_ogc else use url
                resourceURL = resource.get("url_ogc", {})
                if not resourceURL: 
                    resourceURL = resource.get("url", {})

                armchair = process.HandleWFS(resourceURL)
                reclineJSON = armchair.make_recline_json(data_dict)
                p.toolkit.c.resource["reclineJSON"] = reclineJSON
                p.toolkit.c.resource["error"] = False
        except:
            p.toolkit.c.resource["error"] = True

    # Render the jinja2 template which builds the recline preview
    def preview_template(self, context, data_dict):
        error_log = data_dict['resource']["error"]
        format = data_dict['resource']["format"].lower()

        if error_log:
            return "preview_error.html"
        elif format in ['wfs', 'ogc:wfs']:
            return 'wfs_preview_template.html'
        elif format in ['wms', 'ogc:wms']:
            return 'wms_preview_template.html'
        else:
            return "preview_error.html"
