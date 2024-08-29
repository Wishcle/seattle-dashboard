import { FC } from 'react'
import { useState, useEffect } from 'react'
import Map from "@arcgis/core/Map.js";
import MapView from "@arcgis/core/views/MapView";
import Graphic from "@arcgis/core/Graphic";
import Point from "@arcgis/core/geometry/Point";
import SimpleMarkerSymbol from "@arcgis/core/symbols/SimpleMarkerSymbol.js";
import SimpleLineSymbol from "@arcgis/core/symbols/SimpleLineSymbol.js";

const MAP_DIV_ID = "mapDiv"
const URL_COLLISIONS_MANY = "http://127.0.0.1:5000/collisions/many"

interface Props {
}

// The fields of a collisions datum that we use and rely on.
// More fields may be (and probably are) present, but they are unused.
interface Collision {
  OBJECTID: number;
  x: number;
  y: number;
}

// The format of a GeoJSON "feature".
interface Feature {
  type: string;
  id: number;
  geometry: {
    type: string;
    coordinates: number[];
  };
}


// ============= //
//   COMPONENT   //
// ============= //

const MapComp:FC<Props> = (_props) => {
  const [features, setFeatures] = useState<Feature[]>([])
  const [mapView, setMapView] = useState<MapView | null>(null)

  const createMapView = () => {
    const map = new Map({
      basemap: "streets",
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

  const plotFeatures = () => {
    if (mapView == null) {
      return;  // Do nothing if the map view does not exist yet.
    }

    const markerSymbol = new SimpleMarkerSymbol({
      color: [226, 119, 40],
      outline: new SimpleLineSymbol({
        color: [255, 255, 255],
        width: 2,
      }),
    });

    const featureToGraphic = (feature: Feature) => {
      const [x, y] = feature.geometry.coordinates;
      const spatialReference = { wkid: 2926 };
      const point = new Point({ x, y, spatialReference });
      return new Graphic({
        geometry: point,
        symbol: markerSymbol,
      });
    };

    const graphics = features.map(featureToGraphic)
    mapView.graphics.removeAll()
    mapView.graphics.addMany(graphics)
  };

  const fetchCollisions = () => {
    const collisionToFeature = (collision: Collision) => {
      return {
        type: "Feature",
        id: collision.OBJECTID,
        geometry: {
          type: "Point",
          coordinates: [
            collision.x,
            collision.y
          ]
        }
      }
    }

    (async () => {
      const response = await fetch(URL_COLLISIONS_MANY);
      const collisions = await response.json();
      const newFeatures = collisions.map(collisionToFeature);
      setFeatures(newFeatures);
    })();
  };

  useEffect(createMapView, []);
  useEffect(fetchCollisions, []);
  useEffect(plotFeatures, [mapView, features])

  return <div id={MAP_DIV_ID} />;
}

export default MapComp
