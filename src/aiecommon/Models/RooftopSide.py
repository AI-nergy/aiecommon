from pydantic import BaseModel, validator
from typing import Optional, List, Any

from aiecommon.Exceptions import AieException


# model describing geometry fields
class GeometryModel(BaseModel):
    EPSG: str  # e.g., '4326'
    type: str  # "Polygon", "MultiPolygon"
    coordinates: Any  # could be more specific, e.g. List[List[float]] or Tuple[Tuple[float, ...], ...]


class RooftopSide(BaseModel):
    id: Optional[int] = None
    usefulAream2: int
    orientation: str
    orientationDegrees: int
    rooftopSideSlopeDegrees: int
    colorCode: Optional[str] = None
    # geometry is optional, but if provided, it must contain EPSG/type/coordinates
    geometry: Optional[GeometryModel] = None
    rooftopShadingHourly: Optional[List[int]] = None
    shadedFraction: Optional[float] = None

    @validator(
        "geometry", pre=True
    )  # 'pre=True' means we check the raw input before Pydantic tries to parse it
    def check_geometry(cls, value):
        """If geometry is passed, ensure it has EPSG, type, and coordinates.
        Raise AieException (instead of default Pydantic) if anything is missing.
        """
        # If geometry is missing or None, that's okay for this example
        if value is None:
            return None

        # Must be a dictionary
        if not isinstance(value, dict):
            raise AieException(
                AieException.INVALID_INPUT_DATA,
                data={"message": "geometry must be an object/dict if provided"},
            )

        # Check required keys
        required_keys = {"EPSG", "type", "coordinates"}
        missing = required_keys - set(value.keys())
        if missing:
            raise AieException(
                AieException.INVALID_INPUT_DATA,
                data={"message": f"Missing required geometry keys: {missing}"},
            )

        # Check type correctness for each field
        if not isinstance(value["EPSG"], str):
            raise AieException(
                AieException.INVALID_INPUT_DATA,
                data={"message": "geometry.EPSG must be an integer"},
            )
        if not isinstance(value["type"], str):
            raise AieException(
                AieException.INVALID_INPUT_DATA,
                data={"message": "geometry.type must be a string"},
            )
        if not (
            isinstance(value["coordinates"], list)
            or isinstance(value["coordinates"], tuple)
        ):
            raise AieException(
                AieException.INVALID_INPUT_DATA,
                data={"message": "geometry.coordinates must be a list or a tuple"},
            )

        # If everything is okay, parse it into GeometryModel
        # so that 'RooftopSide.geometry' becomes a valid GeometryModel instance.
        return GeometryModel(**value)
