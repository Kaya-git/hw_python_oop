from dataclasses import dataclass, asdict
from typing import List, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_GET_MESSAGE = ('Тип тренировки: {training_type};'
                        ' Длительность: {duration:.3f} ч.;'
                        ' Дистанция: {distance:.3f} км;'
                        ' Ср. скорость: {speed:.3f} км/ч;'
                        ' Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.INFO_GET_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_km_h = self.get_distance() / self.duration_h
        return speed_km_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не содержит'
                                  'реализации в данном классе')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPULE: float = 18
    CALORIES_MEAN_SPEED_SUBTRACTION: float = 20

    def get_spent_calories(self) -> float:
        calories_ccal = (
            (self.CALORIES_MEAN_SPEED_MULTIPULE
                * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEED_SUBTRACTION)
            * self.weight_kg
            / self.M_IN_KM * self.duration_h * self.MIN_IN_HOUR)
        return calories_ccal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLE: float = 0.035
    CALORIES_WEIGHT_MULTIPLE_SECOND: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        calories_ccal = (
            (
                self.CALORIES_WEIGHT_MULTIPLE * self.weight_kg + (
                    self.get_mean_speed() ** 2
                    // self.height_cm
                )
                * self.CALORIES_WEIGHT_MULTIPLE_SECOND
                * self.weight_kg
            )
            * self.duration_h * self.MIN_IN_HOUR
        )
        return calories_ccal


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_ADDITION: float = 1.1
    CALORIES_WEIGHT_MULTIPLE: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_km_h = (self.length_pool_m * self.count_pool
                      / self.M_IN_KM / self.duration_h)
        return speed_km_h

    def get_spent_calories(self) -> float:
        calories_ccal = ((self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_ADDITION)
                         * self.CALORIES_WEIGHT_MULTIPLE * self.weight_kg)
        return calories_ccal


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type: dict = {'RUN': Running,
                           'WLK': SportsWalking,
                           'SWM': Swimming}

    if workout_type not in training_type:
        raise ValueError('Данной тренировки нет в словаре')

    workout = training_type[workout_type](*data)
    return workout


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
