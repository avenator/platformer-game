import pygame_menu
import pygame
pygame.init()
def pool(status, jump=0):
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame_rect = pygame.Rect(1770, 0, 150, 150)
    menu = pygame_menu.Menu(title='', width= pygame.display.get_surface().get_size()[0], height=pygame.display.get_surface().get_size()[1])
    HELP = 'Какую эмоцию(и) Вы сейчас испытываете и насколько она(и) выражена(ы)? \n'\
            ' 0 - отсутствует, 8 - очень сильно выражена. \n'\
            'Используйте клавишы ВВЕРХ/ВНИЗ и ВЛЕВО/ВПРАВО для перемещения, 0 (НОЛЬ) для окончания оценивания.'

    menu.add.label(HELP, max_char=-1, font_size=20)
    # Single value
    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Радость', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])


    # Range
    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Злость', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])

    # Discrete value
    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Отвращение', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])

    # Discrete value
    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Страх (тревога)', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])

    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Грусть', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])
    range_values_discrete = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}
    menu.add.range_slider('Удивление', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])
    arr = []
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    for widget in menu.get_widgets()[3:]:
                        arr.append(widget.get_value())
                    return {
                        'status': status,
                        'jump' : jump,
                        'happiness': arr[0],
                        'anger': arr[1],
                        'disgust': arr[2],
                        'fear': arr[3],
                        'sadness': arr[4],
                        'astonishment': arr[5]
                    }

        if menu.is_enabled():
            menu.draw(surface)
            pygame.draw.rect(surface, 'black', pygame_rect)
            menu.update(events)

        pygame.display.update()
