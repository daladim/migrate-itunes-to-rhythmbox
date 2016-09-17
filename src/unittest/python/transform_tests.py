import unittest
from migrate_itunes_to_rhythmbox import rhythmbox_playlists_writer


class LocationTransformTests(unittest.TestCase):
    @staticmethod
    def transform_fixed_replacement(location: str):
        return rhythmbox_playlists_writer.transform(
            location=location, source_library_root="D:/Music/", target_library_root="/home/pha/Music/")

    def test_transform(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Sum 41/Screaming Bloody Murder (2011)/13-Sum 41 - Back Where I Belong.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Sum%2041/Screaming%20Bloody%20Murder%20(2011)/13-Sum%2041%20-%20Back%20Where%20I%20Belong.mp3")

    def test_transform_umlauts(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Casper/Hinterland (2013)/08 - Ganz Schön Okay - Casper  Kraftklub.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Casper/Hinterland%20(2013)/08%20-%20Ganz%20Sch%C3%B6n%20Okay%20-%20Casper%20%20Kraftklub.mp3")

    def test_transform_exclamation_mark(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Seeed/Next!/09.Goosebumps.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Seeed/Next!/09.Goosebumps.mp3")

    # preserve ampersand. it will escaped with "&amp;" during xml serialization. this way we avoid double escaping ("&amp;amp;").
    def test_transform_ampersand(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Macklemore & Ryan Lewis/The Heist (2012)/01. Macklemore & Ryan Lewis - Ten Thousand Hours.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Macklemore%20&%20Ryan%20Lewis/The%20Heist%20(2012)/01.%20Macklemore%20&%20Ryan%20Lewis%20-%20Ten%20Thousand%20Hours.mp3")

    def test_transform_apostrophe(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Die Orsons/What's goes (2015)/06. Schwung In Die Kiste.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Die%20Orsons/What's%20goes%20(2015)/06.%20Schwung%20In%20Die%20Kiste.mp3")

    def test_transform_special_characters(self):
        transformed_location = self.transform_fixed_replacement("D:/Music/Bla/*?:[]\"<>|(){}'!\;.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Bla/*%3F:%5B%5D%22%3C%3E%7C()%7B%7D'!%5C%3B.mp3")

        transformed_location = self.transform_fixed_replacement("D:/Music/Bla/§$%=~°^.mp3")
        self.assertEqual(transformed_location, "file:///home/pha/Music/Bla/%C2%A7$%25=~%C2%B0%5E.mp3")


if __name__ == '__main__':
    unittest.main()

