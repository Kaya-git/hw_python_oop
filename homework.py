from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )


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

    CALORIES_MEAN_SPEED_MULTIPULE = 18
    CALORIES_MEAN_SPEED_SUBTRACTION = 20

    def get_spent_calories(self) -> float:
        calories_ccal = ((self.CALORIES_MEAN_SPEED_MULTIPULE
                         * self.get_mean_speed()
                         - self.CALORIES_MEAN_SPEED_SUBTRACTION)
                         * self.weight_kg
                         / self.M_IN_KM * self.duration_h * self.MIN_IN_HOUR)
        return calories_ccal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLE = 0.035
    CALORIES_WEIGHT_MULTIPLE_SECOND = 0.029
    NUMERATOR_OF_MEAN_SPEED_DERIVATIVE = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        calories_ccal = ((self.CALORIES_WEIGHT_MULTIPLE * self.weight_kg
                          + (self.get_mean_speed()
                             ** self.NUMERATOR_OF_MEAN_SPEED_DERIVATIVE
                             // self.height_cm)
                         * self.CALORIES_WEIGHT_MULTIPLE_SECOND
                         * self.weight_kg)
                         * self.duration_h * self.MIN_IN_HOUR)
        return calories_ccal


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_ADDITION = 1.1
    CALORIES_WEIGHT_MULTIPLE = 2

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


def read_package(workout_type: str, data: float) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict: dict = {'RUN': Running,
                           'WLK': SportsWalking,
                           'SWM': Swimming}

    if workout_type in training_dict:
        workout = training_dict[workout_type](*data)
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
