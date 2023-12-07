import unittest
from main import find_best_match, check_words_in_sentence
import os
import json
import index_data
import lucene

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        #lucene.initVM()
        file_p =  open(os.path.join("results", "data", "all_cleaned.json"), "r", encoding="utf8")
        self.dictionary = json.load(file_p)
        file_p.close()
        f_p = open(os.path.join("results", "data", "keywords.json"), "r", encoding="utf8")
        self.keyword_info = json.load(f_p)
        f_p.close()

        

    def test_search_article_about_james_webb(self):
        
        result, article = index_data.search_in_index("james webb", 1)
        #print(result, article)
        self.assertEqual(result, "james-webb-space-telescope-updates")

    def test_search_about_europa_moon(self):
        result, article = index_data.search_in_index("Europa moon", 1)
        #print(result, article)
        self.assertEqual(result, "13624-photos-europa-mysterious-moon-jupiter")

    def test_find_suns_mass(self):
        result, article = find_best_match("info:sun|mass", self.dictionary, self.keyword_info)
        result = result.split("[5]")[0]
        self.assertEqual(result, "Mass: 1.9885×1030kg")

    def test_find_suns_radius(self):
        result, article = find_best_match("info:sun|equatorialradius", self.dictionary, self.keyword_info)
        result = result.split(",[10]")[0]
        self.assertEqual(result, "Equatorialradius: 695,700km")

    def test_find_jupiter_escape_velocity(self):
        result, article = find_best_match("info:jupiter|escape velocity", self.dictionary, self.keyword_info)
        result = result.replace("\xa0", " ")    #replace strane characters
        self.assertEqual(result, "Escape velocity: 59.5 km/s (37.0 mi/s)[a]")

    def test_find_jupiter_orbital_period(self):
        result, article = find_best_match("info:jupiter|Orbital period (synodic)", self.dictionary, self.keyword_info)
        result = result.replace("\xa0", " ")    #replace strane characters
        self.assertEqual(result, "Orbital period (synodic): 398.88 d")

    def test_find_wrong_jupiter_orbital_period(self):
        result, article = find_best_match("info:jupiter|Orbital period (synodic)", self.dictionary, self.keyword_info)
        result = result.replace("\xa0", " ")    #replace strane characters
        self.assertFalse(result == "Orbital period (synodic): 500.88 d")


if __name__ == '__main__':
    # lucene.initVM()
    # unittest.main()

    all_keywords = open(os.path.join("results", "data", "all_keywords.txt"), "r", encoding="utf8")
    total_count = len(set(all_keywords.readlines()))
    extracted =  open(os.path.join("results", "data", "keywords.json"), "r", encoding="utf8")
    keyword_info = json.load(extracted)
    count = len(keyword_info.keys())
    print(f"Coverage: {count}, {total_count}, {count/total_count}")