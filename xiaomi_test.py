from xiaomi import *


if __name__ == "__main__":
    rdir = os.path.join('result', '')
    os.makedirs(rdir, exist_ok=True)
    args = arg_pars('data.yml')
    work = RobotPosition(args)
    while True:
        print(f'Доступные операции:\n'
              f'    1 - Вращаем против часовой (угол в градусах).\n'
              f'    2 - Меняем расположение (координаты центра робота).\n'
              f'    3 - Перезаписываем файл с координатами.\n'
              f'    4 - Рисуем 2D.\n'
              f'    5 - Делаем АНИМУ.\n'
              f'    Другой символ - выход.\n')
        numb = input('Введите номер операции: ')
        if numb == '1':
            work.turn(float(input('Число градусов: ')))
        elif numb == '2':
            work.position(int(input('Коорд. X: ')), int(input('Коорд. Y: ')))
        elif numb == '3':
            work.writing_coords()
        elif numb == '4':
            fig = work.pos_rob(make_graph())
            fig.savefig(f'{rdir}position.png')
            plt.close(fig)
        elif numb == '5':
            work.movement(int(input('Коорд. X: ')), int(input('Коорд. Y: ')), rdir)
        else:
            break
