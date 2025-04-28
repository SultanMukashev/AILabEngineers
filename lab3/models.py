from pydantic import BaseModel, Field, field_validator

class CarFeatures(BaseModel):
    brand: str = Field(..., description="Марка автомобиля (например: Toyota)")
    model: str = Field(..., alias="car_model", description="Модель автомобиля (например: Camry)")
    year: int = Field(..., description="Год выпуска автомобиля (например: 2018)")
    mileage: float = Field(..., description="Пробег в километрах (например: 45000)")
    city: str = Field(..., description="Город продажи автомобиля (например: Алматы)")
    engine_volume_liters: float = Field(..., description="Объём двигателя в литрах (например: 2.0)")
    body_style: str = Field(..., description="Тип кузова (например: седан, хэтчбек)")
    color: str = Field(..., description="Цвет автомобиля (например: белый)")
    transmission: str = Field(..., description="Тип коробки передач (например: автомат)")
    drive_type: str = Field(..., description="Тип привода (например: передний, полный)")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore"
    }

    @field_validator(
        'brand', 'model', 'city', 'body_style', 'color', 'transmission', 'drive_type',
        mode="before"
    )
    @classmethod
    def lowercase_str(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

class PredictResponse(BaseModel):
    price: float

class RetrainItem(CarFeatures):
    price: float

class RetrainResponse(BaseModel):
    message: str
    new_train_size: int
