class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция, которую преодолел
                                   # пользователь за время тренировки
                 speed: float,  # средняя скорость пользователя
                 calories: float  # количество килокалорий
                                  # израсходованных за время тренировки
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """возвращает строку сообщения"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                # :.3f- округление до 3-его знака после запятой
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,  # количество совершённых действий
                               # число шагов при ходьбе и
                               # беге либо гребков — при плавании
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
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
        training_type = self.__class__.__name__  # вопрос вот
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    M_IN_H: int = 60

    def get_spent_calories(self) -> float:
        """расчёт количества калорий, израсходованных во время бега"""
        SUM_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                * self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SHIFT)
                               * self.weight / self.M_IN_KM
                               * self.duration * self.M_IN_H
                               )
        return SUM_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    M_IN_H: int = 60
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,  # число шагов при ходьбе
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 height: float  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """расчёт количества калорий, израсходованных во время ходьбы"""
        SUM_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                * self.weight
                                + ((self.get_mean_speed()
                                    * self.KMH_IN_MSEC) ** 2
                                   / (self.height / self.CM_IN_M))
                                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                * self.weight) * self.duration * self.M_IN_H)
        return SUM_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # расстояние одного гребка при плавании
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна
        self.count_pool = count_pool  # сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Расчет скорости во время заплыва"""
        speed_mean_swim: float = (self.length_pool * self.count_pool
                                  / self.M_IN_KM / self.duration)
        return speed_mean_swim

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_spent_calories(self) -> float:
        """Расчет израсходованных каллорий"""
        SUM_calories: float = ((self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SHIFT)
                               * self.CALORIES_WEIGHT_MULTIPLIER
                               * self.weight * self.duration)
        return SUM_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return code[workout_type](*data)


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
