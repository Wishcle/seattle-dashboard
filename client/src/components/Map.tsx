import { FC } from 'react'
import { useState, useEffect } from 'react'
import Map from "@arcgis/core/Map.js";
import MapView from "@arcgis/core/views/MapView";
import Graphic from "@arcgis/core/Graphic";
import Point from "@arcgis/core/geometry/Point";
import SimpleMarkerSymbol from "@arcgis/core/symbols/SimpleMarkerSymbol.js";
import SimpleLineSymbol from "@arcgis/core/symbols/SimpleLineSymbol.js";
import FeatureLayer from "@arcgis/core/layers/FeatureLayer.js";
import HeatmapRenderer from "@arcgis/core/renderers/HeatmapRenderer.js";
import HeatmapColorStop from "@arcgis/core/renderers/support/HeatmapColorStop.js";
import SimpleRenderer from "@arcgis/core/renderers/SimpleRenderer.js";
import Gradient from "javascript-color-gradient";

const MAP_DIV_ID = "mapDiv"
const URL_COLLISIONS_MANY = "http://127.0.0.1:5000/collisions/many"


// ============= //
//   INTERFACES  //
// ============= //

interface Props {
}

// The fields of a collisions datum that we use and rely on.
// More fields may be (and probably are) present, but they are unused.
interface Collision {
  OBJECTID: number;
  x: number;
  y: number;
}


// ============ //
//   RENDERERS  //
// ============ //

// Render data as a heatmap.
const RENDERER_HEATMAP = (() => {
  // https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html
  const veridisColors = ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"];
  const gradientColors = new Gradient()
    .setColorGradient(...veridisColors)
    .setMidpoint(12)
    .getColors();

  // Base color is transparent.
  const heatmapColors = ["rgba(0, 0, 0, 0)"].concat(gradientColors)
  const heatmapColorStops = heatmapColors.map(
    (c, i) => new HeatmapColorStop({
      color: c, ratio: i / (heatmapColors.length - 1)
    }
  ));

  return new HeatmapRenderer({
    colorStops: heatmapColorStops,
    radius: 10,
    maxDensity: 0.04625,
    minDensity: 0,
  });
})();


// Render points as orange dots.
const RENDERER_POINTS = (() => {
  const markerSymbol = new SimpleMarkerSymbol({
    color: [226, 119, 40],
    outline: new SimpleLineSymbol({
      color: [255, 255, 255],
      width: 2,
    }),
  });

  return new SimpleRenderer({
    symbol: markerSymbol,
  });
})();


// ============= //
//   COMPONENT   //
// ============= //

const MapComp:FC<Props> = (_props) => {
  const [mapView, setMapView] = useState<MapView | null>(null)
  const [graphics, setGraphics] = useState<Graphic[]>([])

  const createMapView = () => {
    const map = new Map({
      basemap: "dark-gray",
    });

    const extent = {
      xmin: 1248138.8562188894,
      ymin: 184059.089008525,
      xmax: 1293052.1542488784,
      ymax: 271525.4147941023,
      spatialReference: {
        wkid: 2926,
      },
    }

    const view = new MapView({
      container: MAP_DIV_ID,
      map: map,
      extent: extent,
    });

    setMapView(view);
  }

  const plotGraphics = () => {
    if (mapView == null || graphics.length == 0) {
      return;
    }

    const layer = new FeatureLayer({
      source: graphics,
      objectIdField: "bogus",  // Required, but what I put here does not change how points are drawn.
      geometryType: "point",
      renderer: RENDERER_POINTS,
    });

    mapView.map.removeAll();
    mapView.map.add(layer);

    // For now, just to showcase both renderers, switch to the heatmap after three seconds.
    (async () => {
      const timeout = (delay: number) =>
        new Promise(resolve => setTimeout(resolve, delay));
      await timeout(3000);
      console.log("point renderer");
      layer.renderer = RENDERER_HEATMAP;
    })();
  };

  const fetchCollisions = () => {
    const collisionToGraphic = (collision: Collision) => {
      return new Graphic({
        geometry: new Point({
          x: collision.x,
          y: collision.y,
          spatialReference: { wkid: 2926 },
        }),
      });
    };

    (async () => {
      const response = await fetch(URL_COLLISIONS_MANY);
      const collisions = await response.json();
      const newGraphics = collisions.map(collisionToGraphic);
      setGraphics(newGraphics);
    })();
  };

  useEffect(createMapView, []);
  useEffect(fetchCollisions, []);
  useEffect(plotGraphics, [mapView, graphics])

  return <div id={MAP_DIV_ID} />;
}

export default MapComp
