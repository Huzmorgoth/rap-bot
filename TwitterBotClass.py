# -*- coding: utf-8 -*-
"""
Bot-hard-app
"""
from spellchecker import SpellChecker
from better_profanity import profanity

from datamuse import datamuse
import wikipediaapi as wpa
import whapi as wh
import random as ran
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageDraw, ImageFont


class TwitterBotClass:
    def __init__(self):
        pass

    def check_if_english(self, word):
        spell = SpellChecker()
        if len(spell.known([word])) < 1:
            return False
        return True

    def check_if_contain_profanity(self, word):
        res = profanity.contains_profanity(word)
        return res

    def return_muse_rhymes(self, word):
        api = datamuse.Datamuse()
        datamuse_rhymes = api.words(rel_rhy=word, max=30)
        rhymes = [x['word'] for x in datamuse_rhymes]
        print(rhymes)
        if len(rhymes) - 1 >= 3:
            idxs = ran.sample(range(0, len(rhymes) - 1), 3)
            rhymes = [rhymes[i] for i in idxs]

        rhymes.insert(0, word)

        return rhymes

    def get_wiki_text(self, seed):
        wiki = wpa.Wikipedia('en')
        wiki_page = wiki.page(seed)
        wiki_text = wiki_page.text

        return wiki_text

    def get_wikihow_text(self, seed):
        search_results = wh.search(seed, 10)
        max = len(search_results)
        if max < 1:
            return ''
        rand_index = ran.randint(0, max - 1)
        article_id = search_results[rand_index]['article_id']
        html = wh.get_html(article_id)
        soup = bs(html, 'html.parser')
        wh_text = soup.text

        return wh_text

    def preprocess_text(self, text, seed):
        text = text.replace('\n', ' ').replace('(', '').replace(')', '').replace('\"', '')
        text_list = [x + ' ' + seed for x in text.split(seed)]
        text_token = [i.split() for i in text_list]

        return text_token

    def collect_text(self, seed):
        wiki_text = self.preprocess_text(self.get_wiki_text(seed), seed)
        wh_text = self.preprocess_text(self.get_wikihow_text(seed), seed)
        consol_text = wh_text + wiki_text
        text_token = consol_text #self.preprocess_text(consol_text, seed)

        return text_token

    def generate_rap(self, rhymes, restrict_f_terms):
        result = []
        for seed in rhymes:
            text_token = self.collect_text(seed)
            for x in text_token:
                char_bool = False
                if len(x) >= 8:
                    cont_bool = True
                    itr = 0
                    for wrd in x[-8:]:
                        if '.' in wrd:
                            cont_bool = False
                            break
                        if itr != 0 and wrd == wrd.capitalize():
                            cont_bool = False
                            break
                        itr += 1
                    if cont_bool:
                        rap_line = x[-8:]
                        if rap_line[0] in restrict_f_terms:
                            rap_line.pop(0)
                        # rap_line[0] = rap_line[0].capitalize()
                        rap_line.insert(5, '\n')
                        text = ' '.join(rap_line)
                        result.append(text)
                        char_bool = True
                if char_bool:
                    break
        if len(result) < 4 and len(result) > 0:
            if rhymes[0] not in result[0]:
                result.append(
                    '\n (I could not rap on '+rhymes[0].capitalize()+' but\nI spat some lines on its rhymes!)')
            else:
                result.append(
                    '\n (I could not rap more than ' + str(len(result)) + ' lines,\nI am still new to music, sorry!)')
            result_out = '\n\n'.join(result)
            return result_out
        elif len(result) < 1:
            result.append(
                '\n (I could not rap on ' + rhymes[0].capitalize() + ',\nI am still new to music, sorry!)')
            result_out = '\n\n'.join(result)
            return result_out

        result_out = '\n\n'.join(result)
        return result_out

    def generate_rap_image(self, content, img_loc, font_loc):
        """image = Image.open(img_loc)
        W, H = image.size
        d = ImageDraw.Draw(image)
        font_type = ImageFont.truetype(font_loc, 30)
        w, h = d.textsize(content, font_type)
        d.text(((W - w) / 2, (H - h) / 2), content, font=font_type,
               size=40, align='center', spacing=13)"""
        img_loc = 'bot_hard_rap.png'
        #image.save(img_loc)

        return img_loc, content

    def execute_code(self, input, img, font, restrict_f_terms):
        if self.check_if_english(input):
            if self.check_if_contain_profanity(input):
                rap_content = 'I will be shut down if I start\nrapping on such words'
                result = self.generate_rap_image(rap_content, img, font)
                return result
            else:
                muse_rhymes_list = self.return_muse_rhymes(input)
                if len(muse_rhymes_list) > 2:
                    rap_content = self.generate_rap(muse_rhymes_list, restrict_f_terms)
                    result = self.generate_rap_image(rap_content, img, font)
                    return result
                else:
                    rap_content = 'I couldn\'t find enough rhymes\nfor ' + input.capitalize() + ', please bare my idiocy'
                    result = self.generate_rap_image(rap_content, img, font)
                    return result
        else:
            rap_content = 'The word ' + input.capitalize() + ' doesn\'t seem\nlike english, but what do I know'
            result = self.generate_rap_image(rap_content, img, font)
            return result
