from challenge import *
import unittest

class TestCases(unittest.TestCase):

    # edge cases
    def test_batman_to_batman(self):
        result = run_program('superheroes.txt', 'Batman', 'Batman')
        self.assertEqual(result, '"Batman" is not an employee or there is only one with this name')

    def test_batman_to_batman_two_batmans(self):
        result = run_program('superheroes_two_batmans.txt', 'Batman', 'Batman')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the great (2) -> Dangermouse (1) -> Batman (3)')

    def test_different_case_in_chart(self):
        result = run_program('superheroes_two_batmans.txt', 'Batman', 'Gonzo the Great')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the great (2)')

    def test_first_employee_not_in_chart(self):
        result = run_program('superheroes.txt', 'Spiderman', 'Batman')
        self.assertEqual(result, '"Spiderman" is not an employee')

    def test_second_employee_not_in_chart(self):
        result = run_program('superheroes.txt', 'Batman', 'The Flash')
        self.assertEqual(result, '"The Flash" is not an employee or there is only one with this name')

    def test_gonzo_the_great_invalid_variation(self):
        result = run_program('superheroes.txt', 'Gon Zot Heg Reat', 'Batman')
        self.assertEqual(result, '"Gon Zot Heg Reat" is not an employee')

    def test_batman_to_inivisble_woman_case_change(self):
        result = run_program('superheroes.txt', 'batman', 'invisible Woman')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) -> Invisible Woman (3)')

    # main cases
    def test_batman_to_catwoman(self):
        result = run_program('superheroes.txt', 'Batman', 'Catwoman')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Catwoman (17)')

    def test_batman_to_black_widow(self):
        result = run_program('superheroes.txt', 'Batman', 'Black Widow')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6)')

    def test_batman_to_gonzo_the_great(self):
        result = run_program('superheroes.txt', 'Batman', 'Gonzo the Great')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the Great (2)')

    def test_batman_to_gonzo_the_great_variation(self):
        result = run_program('superheroes.txt', 'Batman', ' Gonzo  the Great ')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the Great (2)')

    def test_dangermouse_to_batman(self):
        result = run_program('superheroes.txt', 'Dangermouse', 'Batman')
        self.assertEqual(result, 'Dangermouse (1) -> Gonzo the Great (2) -> Black Widow (6) -> Batman (16)')

    def test_dangermouse_to_hit_girl(self):
        result = run_program('superheroes.txt', 'Dangermouse', 'hit Girl')
        self.assertEqual(result, 'Dangermouse (1) -> Invisible Woman (3) -> Hit Girl (12)')

    def test_batman_to_inivisble_woman(self):
        result = run_program('superheroes.txt', 'Batman', 'Invisible Woman')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) -> Invisible Woman (3)')

    def test_batman_to_super_ted(self):
        result = run_program('superheroes.txt', 'Batman', 'Super Ted')
        self.assertEqual(result, 'Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) -> Invisible Woman (3) -> Super Ted (15)')

    def test_invisible_woman_to_dangermouse(self):
        result = run_program('superheroes.txt', 'Invisible Woman', 'Dangermouse')
        self.assertEqual(result, 'Invisible Woman (3) -> Dangermouse (1)')

    def test_invisible_woman_to_black_widow(self):
        result = run_program('superheroes.txt', 'Invisible Woman', 'Black Widow')
        self.assertEqual(result, 'Invisible Woman (3) -> Dangermouse (1) -> Gonzo the Great (2) -> Black Widow (6)')


if __name__ == '__main__':
    unittest.main()