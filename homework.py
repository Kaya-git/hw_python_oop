class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    training_type = 'RUN'
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    min_in_hour = 60

    def get_spent_calories(self) -> float:
        calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                     - self.coeff_calorie_2) * self.weight
                    / self.M_IN_KM * self.duration * self.min_in_hour)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    training_type = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029
    min_in_hour = 60

    def get_spent_calories(self) -> float:
        calories = ((self.coeff_calorie_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.height)
                    * self.coeff_calorie_2 * self.weight)
                    * self.duration * self.min_in_hour)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    training_type = 'SWM'
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    coeff_calorie_1 = 1.1

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed()
                     + self.coeff_calorie_1) * 2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dictionary: dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}

    if workout_type in dictionary:
        workout = dictionary[workout_type](*data)
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
