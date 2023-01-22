from dataclasses import dataclass

KMCH_IN_MS: float = 0.278
SM_IN_M: int = 100
M_IN_KM: int = 1000
MINUTES_IN_HOUR: int = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> NotADirectoryError:
        raise NotImplementedError('Определите get_spent_calories '
                                  f'в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_message


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed: float = super().get_mean_speed()
        time: float = MINUTES_IN_HOUR * self.duration

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER*mean_speed +
                self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM
                * time)


class SportsWalking(Training):

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029

    def __init__(self, action: int, duration: float, weight: float, height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        mean_speed: float = super().get_mean_speed() * KMCH_IN_MS
        time: float = MINUTES_IN_HOUR * self.duration
        height: float = self.height / SM_IN_M

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                + (mean_speed**2 / height) * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight) * time)


class Swimming(Training):

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        mean_speed: float = self.get_mean_speed()
        return ((mean_speed + self.CALORIES_MEAN_SPEED_MULTIPLIER) *
                self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in types:
        training = types[workout_type](*data)
    return training


def main(training: Training) -> str:
    info: InfoMessage = training.show_training_info()
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
