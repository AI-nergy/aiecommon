from pydantic import BaseModel, validator
from typing import Optional, List, Any, Union

from aiecommon.Exceptions import AieException


# model describing geometry fields
class OLD_GeometryModel(BaseModel):
    type: str  # e.g., "Polygon", "MultiPolygon"
    coordinates: Any  # could be more specific, e.g. List[List[float]] or Tuple[Tuple[float, ...], ...]

class RooftopSide(BaseModel):
    id: Optional[int] = None
    usefulAream2: int
    orientation: str
    orientationDegrees: float
    rooftopSideSlopeDegrees: int
    colorCode: Optional[str] = None
    # geometry is optional, but if provided, it must contain EPSG/type/coordinates
    geometry: Optional[OLD_GeometryModel] = None
    rooftopShadingHourly: Optional[List[int]] = None
    shadedFraction: Optional[float] = None

    @validator("geometry", pre=True)
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
        # Note: We allow EPSG to be a string or int; conversion is handled in GeometryModel
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
        return OLD_GeometryModel(**value)
