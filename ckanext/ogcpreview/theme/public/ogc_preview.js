this.ckan.module('ogc_view', function ($, _) {
  return {
    options: {
      i18n: {
        errorLoadingPreview: "Could not load preview",
        errorDataProxy: "DataProxy returned an error",
        errorDataStore: "DataStore returned an error",
        previewNotAvailableForDataType: "Preview not available for data type: "
      },
      site_url: ""
    },

    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.ready(this._onReady);
      // hack to make leaflet use a particular location to look for images
      L.Icon.Default.imagePath = this.options.site_url + 'vendor/leaflet/0.4.4/images';
    },

    _onReady: function() {
      this.loadPreviewDialog(preload_resource);
    },

    loadPreviewDialog: function (resourceData) {
      var self = this;

      function showError(msg){
        msg = msg || _('error loading preview');
        window.parent.ckan.pubsub.publish('data-viewer-error', msg);
      }

      recline.Backend.DataProxy.timeout = 10000;

      resourceData.formatNormalized = this.normalizeFormat(resourceData.format);

      resourceData.url  = this.normalizeUrl(resourceData.url);

      if (resourceData.formatNormalized === '') {
        var tmp = resourceData.url.split('/');
        tmp = tmp[tmp.length - 1];
        tmp = tmp.split('?'); // query strings
        tmp = tmp[0];
        var ext = tmp.split('.');
        if (ext.length > 1) {
          resourceData.formatNormalized = ext[ext.length-1];
        }
      }

      var dataset
        , format;

      format = resourceData.format.toLowerCase();
      if (['wfs', 'ogc:wfs'].indexOf(format) > -1) {
          resourceData.backend = 'memory';
          dataset = new recline.Model.Dataset({records:resourceData.reclineJSON});
          dataset.fetch().done(function(dataset){self.initializeDataExplorer(dataset)});
      } else if (['wms', 'ogc:wms'].indexOf(format) > -1) {

        (function () {
          var map
            , opts
            , baseMap
            , serviceUrl
            , wms
            , bbox
            , bounds
            ;

          opts = {attributionControl: true};
          bbox = resourceData.bbox;
          bounds = L.latLngBounds([
            [bbox[1], bbox[0]],
            [bbox[3], bbox[2]]
          ]);

          map = new L.Map('map', opts).fitBounds(bounds);

          baseMap = new L.TileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
            subdomains: 1234,
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">'
              + 'MapQuest</a> &mdash; Map data &copy; <a href="http://openstreetm'
              + 'ap.org">OpenStreetMap</a> contributors, <a href="http://creative'
              + 'commons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            minZoom: 1,
            maxZoom: 12
          });

          serviceUrl = resourceData.service_url.split('?')[0];
          wms = new L.TileLayer.WMS(serviceUrl, {
            layers: resourceData.layer,
            format: resourceData.tile_format,
            transparent: true
          });

          map.addLayer(baseMap);
          map.addLayer(wms);
        })();
      }
    },

    initializeDataExplorer: function (dataset) {
      var views = [
        {
          id: 'grid',
          label: 'Grid',
          view: new recline.View.SlickGrid({
            model: dataset
          })
        },
        {
          id: 'graph',
          label: 'Graph',
          view: new recline.View.Graph({
            model: dataset
          })
        },
        {
          id: 'map',
          label: 'Map',
          view: new recline.View.Map({
            model: dataset
          })
        },
        // @NGDS: added a tab for histograms
        {
            id: 'histogram',
            label: 'Histogram',
            view: new recline.View.FlotHisto({
              model: dataset
            })
          }
      ];

      var sidebarViews = [
        {
          id: 'valueFilter',
          label: 'Filters',
          view: new recline.View.ValueFilter({
            model: dataset
          })
        }
      ];

      var dataExplorer = new recline.View.MultiView({
        el: this.el,
        model: dataset,
        views: views,
        sidebarViews: sidebarViews,
        config: {
          readOnly: true
        }
      });

    },
    normalizeFormat: function (format) {
      var out = format.toLowerCase();
      out = out.split('/');
      out = out[out.length-1];
      return out;
    },
    normalizeUrl: function (url) {
      if (url.indexOf('https') === 0) {
        return 'http' + url.slice(5);
      } else {
        return url;
      }
    }
  };
});