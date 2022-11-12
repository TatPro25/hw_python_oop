from dataclasses import dataclass, asdict
from typing import ClassVar, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    training_type - имя класса тренировки
    duration - длительность тренировки в часах
    distance - дистанция, которую преодолел пользователь за время тренировки
    speed - средняя скорость пользователя
    calories - количество килокалорий израсходованных за время тренировки."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    """Возвращает строку сообщения."""
    Message_Const = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return (self.Message_Const.format(**asdict(self)))


@dataclass
class Training:
    """Базовый класс тренировки.
    action - количество совершённых действий
            (число шагов при ходьбе и беге либо гребков — при плавании)
    duration - длительность тренировки
    weight - вес спортсмена
    LEN_STEP - расстояние, которое спортсмен преодолнвает за один шаг
    M_IN_KM - перевод значения из метров в километры
    MIN_IN_H - перевод значения из часов в минуты."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег.
    CALORIES_MEAN_SPEED_MULTIPLIER - множитель веса калорий
    CALORIES_MEAN_SPEED_SHIFT - множитель калорий скорости высоты."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных во время бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    CALORIES_WEIGHT_MULTIPLIER - множитель веса калорий
    CALORIES_SPEED_HEIGHT_MULTIPLIER - множитель калорий скорости высоты
    CM_IN_M - перевод из сантиметров в метры
    KMH_IN_MSEC - перевод в метры в секунду
    height - рост спортсмена."""
    height: float
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100
    LEN_STEP: ClassVar[float] = 0.65

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных во время ходьбы."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                 * self.weight
                 + ((self.get_mean_speed()
                     * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
    LEN_STEP - расстояние одного гребка при плавании
    length_pool - длина бассейна
    count_pool - сколько раз переплыл бассейн."""
    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Расчет скорости во время заплыва."""
        return ((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration))

    def get_distance(self) -> float:
        return super().get_distance()

    def get_spent_calories(self) -> float:
        """Расчет израсходованных каллорий."""
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type.keys():
        raise KeyError(f'Неизвестный тип тренировки {workout_type}')
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
