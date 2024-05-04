import { FC } from 'react'
import { useEffect } from 'react'
import Map from "@arcgis/core/Map.js";
import MapView from "@arcgis/core/views/MapView";
import Graphic from "@arcgis/core/Graphic";
import Point from "@arcgis/core/geometry/Point";
import SimpleMarkerSymbol from "@arcgis/core/symbols/SimpleMarkerSymbol.js";
import SimpleLineSymbol from "@arcgis/core/symbols/SimpleLineSymbol.js";
import { collisions } from "../data/collisions-small";

const MAP_DIV_ID = "mapDiv"

interface Props {
}

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
  const drawPoints = () => {
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
    }

    const graphics = collisions.map(featureToGraphic)
    view.graphics.addMany(graphics)
  };

  useEffect(drawPoints, []);

  return <div id={MAP_DIV_ID} />;
}

export default MapComp
